<template>
<el-container>
    <el-header>
        <span>点表配置工具</span>
    </el-header>
    
    <el-container>
        <el-aside>
            <el-tree :data="treeData" 
                     @node-click="handleNodeClick"
                     :props="defaultProps"
                     style="background-color: #F5F7FA;max-width: 300px;"
                     highlight-current>
            </el-tree>
        </el-aside>
        
        <el-main>
                <vue-xlsx-table @on-select-file="handleSelectedFile"><i class="el-icon-download"></i>导入</vue-xlsx-table>
            <el-button-group>
                <el-button type="primary" @click="handleAdd" icon="el-icon-plus">添加</el-button>
                <el-button type="primary" @click="refresh" icon="el-icon-refresh">重置</el-button>
                <el-button type="danger" @click="handleDelete" icon="el-icon-delete">批量删除</el-button>
                <el-button type="primary" @click="importData" icon="el-icon-download">导出</el-button>
            </el-button-group>
            <el-table :data="viewtableData"
                      highlight-current-row
                      :header-cell-style="headercellstyle"
                      :cell-style="cesty"
                      v-loading="loading"
                      ref="xTable"
                      border>
                <el-table-column
                    type="selection"
                    width="55">
                </el-table-column>
                <!-- <el-table-column :label="item.label" 
                                :prop="item.value" v-for="(item, key) in viewcolumns"
                                :min-width="item.minwidth"
                                :show-overflow-tooltip=true
                                :resizable=true
                                :key="key">
                </el-table-column> -->

                <template v-for="item in viewcolumns">
                    <!-- 正常表格列 -->
                    <el-table-column
                        v-bind:key="item.label"
                        v-if="!item.noRepeat"
                        :prop="item.value"
                        :label="item.label"
                        :show-overflow-tooltip="true"
                        :fixed="item.fixed ? item.fixed : false"
                        :width="item.width ? item.width : ''"
                    ></el-table-column>
                    <!-- 排序 ID -->
                    <el-table-column
                        label="ID"
                        :prop="item.value"
                        sortable
                        v-bind:key="item.label"
                        :fixed="item.fixed ? item.fixed : false"
                        :width="item.width ? item.width : ''"
                        v-if="item.label === '点号'"
                    ></el-table-column>
                    <!-- 编辑 name -->
                    <el-table-column
                        v-bind:key="item.label" 
                        :label="item.label"
                        :prop="item.value"
                        :width="item.width"
                        show-overflow-tooltip
                        v-if="item.label === '名称'"
                    >
                    <template slot-scope="scope">
                        <el-input placeholder="请输入内容" v-show="scope.row.show" v-model="scope.row.name"></el-input>
                        <span v-show="!scope.row.show">{{scope.row.name}}</span>
                    </template>
                    </el-table-column>
                    <!-- 编辑 address -->
                    <el-table-column
                        v-bind:key="item.label" 
                        :label="item.label"
                        :prop="item.value"
                        :width="item.width"
                        show-overflow-tooltip
                        v-if="item.label === '地址'"
                    >
                    <template slot-scope="scope">
                        <el-input placeholder="请输入内容" v-show="scope.row.show" v-model="scope.row.address"/>
                        <span v-show="!scope.row.show">{{scope.row.address}}</span>
                    </template>
                    </el-table-column>
                </template>

                <!-- 操作列 -->
                <el-table-column label="操作" fixed="right" width="300" align="center">
                <template slot-scope="scope">
                <el-button-group>
                    <el-button @click="scope.row.show =true;" icon="el-icon-edit" type="primary">修改</el-button>
                    <el-button @click="scope.row.show =false; save(scope.row);" icon="el-icon-check" type="success">保存</el-button>
                    <el-button @click="singleDelete(scope.$index, scope.row);" icon="el-icon-delete" type="danger">删除</el-button>
                </el-button-group>
                </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <div class="block" style="float: right;margin-top: 1px;margin-bottom: 1px;padding-right: 15px">
                <span class="demonstration"></span>
                <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentpage"
                    :page-sizes="[10, 30, 50, 100]"
                    :page-size="pagesize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="totalcount">
                </el-pagination>
            </div>
        </el-main>
    </el-container>

    <el-footer>
        <span>@2022 西安端怡科技有限公司</span>
    </el-footer>
</el-container>
</template>

<style>
    html,body,#app,.el-container{
        /* 设置内部填充为0，几个布局元素之间没有间距 */
        padding: 0px;
         /*外部间距也是如此设置*/
        margin: 0px;
        /*统一设置高度为100%*/
        height: 100%;
    }

    .el-header {
        background-color: #003366;
        color: white;
        line-height: 60px;
        text-align: center; 
        font-size: 35px;
    }

    .el-aside {
        background-color: rgb(238, 241, 246);
        color: black;
    }

    .el-footer {
        background-color: #003366;
        color: white;
        text-align: center; 
        line-height: 60px;
    }

    .current-row > td {
        /* background: #218af3 !important; */
    }

    .el-tree-node:focus > .el-tree-node__content {
        background-color: #218af3 !important;
    }

    .table-edit {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }

    .content {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .cell-icon {
        cursor: pointer;
        color: #3963bc;
        font-size: 16px;
    }

    .cell-icon-edit {
        display: flex;
        margin-left: 20px;
        width: 50px;
        justify-content: space-between;
    }

    .cell-cancel {
        cursor: pointer;
        color: #3963bc;
        font-size: 16px;
    }

    .cell-save {
        cursor: pointer;
        color: #3963bc;
        font-size: 16px;
        margin-right: -20px;
    }
</style>

<script>
    import axios from 'axios';
    import XLSX from 'xlsx';
    import { Linkheader } from './js/staProperty';
    import { YXheader } from './js/yxProperty';
    import { YCheader } from './js/ycProperty';
    import { YKheader } from './js/ykProperty';
    import { YTheader } from './js/ytProperty';
    import { SOEheader } from './js/soeProperty';

    export default {
        data() {
            return {
                loading: false,
                treeData: [],
                defaultProps: {
                    children: 'children',
                    label: 'label'
                },
                viewcolumns: [],  //显示的列
                viewtableData: [], //根据列显示的数据
                tabledata: [],
                lianludata: [],
                ycdata: [],
                yxdata: [],
                ykdata: [],
                ytdata: [],
                soedata: [],
                station_ID: '', 
                pagesize: 10,  //一页显示多少个
                totalcount: 0, //总共有多少条数据
                currentpage: 1,
            }
        },
        created() {
            // 获取数据
            this.getTreeData();
            this.Linkheader = Linkheader
            this.YXheader = YXheader
            this.YCheader = YCheader
            this.YKheader = YKheader
            this.YTheader = YTheader
            this.SOEheader = SOEheader
        },
		methods: {
		    async getTreeData() {
                // 对应Python提供的接口
                /* const path = 'http://127.0.0.1:5000/getStaTree'; */
                const path = BASE_INFO.BING_URL + '/getStaTree';
                let that = this;
                that.treeData = [];
                
		        await axios.get(path).then(function (response) {
		            var staLen = response.data.staLen;
                    var staNames = response.data.staNames;
                    var treeitem = {};
                    treeitem.label = "厂站列表";
                    treeitem.children = [];
                    for(var i=0; i<staNames.length; i++) {
                        var tree_item = {
                            label: staNames[i],
                            children: [{
                                label: '遥信',
                                id: i+1,
                            }, {
                                label: '遥测', 
                                id: i+1,
                            }, {
                                label: '遥控',
                                id: i+1,
                            }, {
                                label: '遥调',
                                id: i+1,
                            }, {
                                label: 'SOE',
                                id: i+1,
                            }]
                        };
                        treeitem.children.push(tree_item);
                    }
                    that.treeData.push(treeitem);
                });
            },

            //点击树触发事件
            handleNodeClick: function (data) {
                let that = this;
                if(data.label=="厂站列表") {
                    that.viewcolumns=that.Linkheader;
                    that.getLianludata();
                }
                if(data.label=="遥测") {
                    var station_ID = data.id;
                    that.station_ID = station_ID;
                    that.viewcolumns=that.YCheader;
                    that.getYCdata();
                }
                if(data.label=="遥信") {
                    var station_ID = data.id;
                    that.station_ID = station_ID;
                    that.viewcolumns=that.YXheader;
                    that.getYXdata();
                }
                if(data.label=="遥控") {
                    var station_ID = data.id;
                    that.station_ID = station_ID;
                    that.viewcolumns=that.YKheader;
                    that.getYKdata();
                }
                if(data.label=="遥调") {
                    var station_ID = data.id;
                    that.station_ID = station_ID;
                    that.viewcolumns=that.YTheader;
                    that.getYTdata();
                }
                if(data.label=="SOE") {
                    var station_ID = data.id;
                    that.station_ID = station_ID;
                    that.viewcolumns=that.SOEheader;
                    that.getSOEdata();
                }
            },

            async getSOEdata() {
                let that = this;
                const path = BASE_INFO.BING_URL + '/getSOEdata';
                var station_ID = that.station_ID;
                var params = {
                    stationId: station_ID,
                };

                await axios.get(path, {params: params}).then(function (response) {
                    var soedata = response.data.soeproperty;
                    var count = response.data.lensoep;
                    that.totalcount = count;
                    that.soedata = soedata;
                    that.tabledata = that.soedata;
                    that.viewTableData(soedata);
                });
            },

            async getYTdata() {
                let that = this;
                const path = BASE_INFO.BING_URL + '/getYTdata';
                var station_ID = that.station_ID;
                var params = {
                    stationId: station_ID,
                };

                await axios.get(path, {params: params}).then(function (response) {
                    var ytdata = response.data.ytproperty;
                    var count = response.data.lenytp;
                    that.totalcount = count;
                    that.ytdata = ytdata;
                    that.tabledata = that.ytdata;
                    that.viewTableData(ytdata);
                });
            },

            async getYKdata() {
                let that = this;
                const path = BASE_INFO.BING_URL + '/getYKdata';
                var station_ID = that.station_ID;
                var params = {
                    stationId: station_ID,
                };

                await axios.get(path, {params: params}).then(function (response) {
                    var ykdata = response.data.ykproperty;
                    var count = response.data.lenykp;
                    that.totalcount = count;
                    that.ykdata = ykdata;
                    that.tabledata = that.ykdata;
                    that.viewTableData(ykdata);
                });
            },

            async getYXdata() {
                let that = this;
                const path = BASE_INFO.BING_URL + '/getYXdata';
                var station_ID = that.station_ID;
                var params = {
                    stationId: station_ID,
                };

                await axios.get(path, {params: params}).then(function (response) {
                    var yxdata = response.data.yxproperty;
                    var count = response.data.lenyxp;
                    that.totalcount = count;
                    that.yxdata = yxdata;
                    that.tabledata = that.yxdata;
                    that.viewTableData(yxdata);
                });
            },

            async getYCdata() {
                let that = this;
                const path = BASE_INFO.BING_URL + '/getYCdata';
                var station_ID = that.station_ID;
                var params = {
                    stationId: station_ID,
                };

                await axios.get(path, {params: params}).then(function (response) {
                    var ycdata = response.data.ycproperty;
                    var count = response.data.lenycp;
                    that.totalcount = count;
                    that.ycdata = ycdata;
                    that.tabledata = that.ycdata;
                    that.viewTableData(ycdata);
                });
            },

            async getLianludata() {
                let that = this;
                const path = BASE_INFO.BING_URL + '/getLianludata';

                await axios.get(path).then(function (response) {
                    var lianludata = response.data.staproperty;
                    var count = response.data.lenstap;
                    that.lianludata = lianludata;
                    that.totalcount = count;
                    that.tabledata = that.lianludata;
                    //console.log(lianludata);
                    that.viewTableData(lianludata);
                });
            },

            //分页显示table数据
            viewTableData(data) {
                let that = this;
                //显示分页数据
                var currentpage= that.currentpage;
                var begin = (currentpage-1) * that.pagesize;
                var end = (currentpage-1) * that.pagesize + that.pagesize;
                let tableData = data;
                let viewtableData = [];
                if (tableData.length < end) {
                    end = tableData.length;
                }
                for (var index=begin; index<end; index++) {
                    var newitem = tableData[index];
                    viewtableData.push(newitem);
                }
                that.viewtableData = viewtableData;
            },

            headercellstyle({row, column, rowIndex, columnIndex}) {
                return "background:#E4E7EB;font-weight: bold;color: #101010;pading:0;height:15px;";
            },

            cesty({row, column, rowIndex, columnIndex}) {
                return "padding:0;";
            },

            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
                this.pagesize = val;
                var data = this.tabledata;
                this.viewTableData(data);
            },

            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
                this.currentpage = val;
                var data = this.tabledata;
                this.viewTableData(data);
            },

            async save(row) {
                let that = this;
                const path = BASE_INFO.BING_URL + '/setStation';
                console.log(row)
                await axios.post(path, row).then(function (response) {
                    var status = response.data.status;
                    // console.log(status)
                    if(status == 1) {
                        alert("保存成功！")
                        that.getTreeData();
                    } else {
                        alert("保存失败！")
                    }
                });
            },

            handleAdd() {
                var num = this.totalcount
                this.viewtableData.push({
                    ID: num+1,
                    PORT: 60000,
                    address: "",
                    describe: "1",
                    name: "",
                    role: 1,
                    ruleID: 1,
                    show: true,
                });
            },

            async handleDelete() {
                let that = this;
                var checkrows = this.$refs.multipleTable.selection;
                var ids = [];
                var num = checkrows.length
                if(num == 0) {
                    alert("请先选择要删除的行！")
                } else {
                    for(var i=0; i<num; i++) {
                        var id = checkrows[i]["ID"];
                        ids.push(id);
                    }
                    const path = BASE_INFO.BING_URL + '/deleteStation';
                    await axios.post(path, ids).then(function (response) {
                        var status = response.data.status;
                        if(status == 1) {
                            alert("删除成功！");
                            that.getLianludata();
                            that.getTreeData();
                        } else {
                            alert("删除失败！")
                        }
                    });
                }
            },

            async singleDelete(index) {
                let that = this;
                var ids = [index + 1];
                console.log(ids)
                const path = BASE_INFO.BING_URL + '/deleteStation';
                await axios.post(path, ids).then(function (response) {
                    var status = response.data.status;
                    if(status == 1) {
                        alert("删除成功！");
                        that.getLianludata();
                        that.getTreeData();
                    } else {
                        alert("删除失败！")
                    }
                });
            },

            refresh() {
                this.getLianludata();
            },

            // Excel导入
            handleSelectedFile() {
                const path = BASE_INFO.BING_URL + '/getTableHeader';

                axios.get(path).then(function (response) {
                    let tableHeader = response.data.tableHeader;
                    let staHeader = tableHeader[0];
                    console.log(staHeader);
                });
            },

            //导出Excel
            importData () {
                const workBook = XLSX.utils.table_to_book(this.$refs.xTable.$el.querySelector('.body--wrapper>.vxe-table--body'))
                XLSX.writeFile(workBook, '数据导出.xlsx')
            },
        },

        watch: {
            // 默认点击Tree第一个节点
            treeData(val) {
                if (val) {
                    this.$nextTick(() => {
                        document.querySelector('.el-tree-node__content').click();
                    });
                }
            },
        },
    }
</script>