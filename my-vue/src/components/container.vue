<template>
<el-container>
    <el-header>
        <span>点表配置工具</span>
    </el-header>

    <el-container>
        <el-aside>
            <el-tree :data="treeData" @node-click="handleNodeClick" 
                     :props="defaultProps"
                     style="background-color: #F5F7FA;max-width: 300px;"
                     highlight-current>
            </el-tree>
        </el-aside>
    
        <el-main>
            <el-table :data="viewtableData" ref="singleTable" 
                      highlight-current-row
                      :header-cell-style="headercellstyle"
                      :cell-style="cesty"
                      border>
                <el-table-column :label="item.label" 
                                 :prop="item.value" v-for="(item, key) in viewcolumns"
                                 :min-width="item.minwidth"
                                 :show-overflow-tooltip=true
                                 :resizable=true
                                 :key="key">
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
        <span>@2020  西安端怡科技有限公司</span>
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
        background: #218af3 !important;
    }

    .el-tree-node:focus > .el-tree-node__content {
        background-color: #218af3 !important;
    }
</style>

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
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
                Linkheader: [
                    {
                        label: "点号",
                        value:'ID',
                        minwidth: '30'
                    }, {
                        label: "名称",
                        value:'name',
                        minwidth: '140'
                    },
                    {
                        label: "描述",
                        value:'describe',
                        minwidth: '80'
                    },
                    {
                        label: "ruleID",
                        value:'ruleID',
                        minwidth: '40'
                    },
                    {
                        label: "地址",
                        value:'address',
                        minwidth: '80'
                    },
                    {
                        label: "端口",
                        value:'PORT',
                        minwidth: '40'
                    },
                    {
                        label: "ROLE",
                        value:'role',
                        minwidth: '40'
                    },
                ],
                YCheader: [
                    {
                        label: "点号",
                        value:'ID',
                        minwidth: '30'
                    }, {
                        label: "名称",
                        value:'name',
                        minwidth: '120',
                    },
                    {
                        label: "描述",
                        value:'describe',
                        minwidth: '80'
                    },
                    {
                        label: "单位",
                        value:'unit',
                        minwidth: '40'
                    },
                    {
                        label: "K值",
                        value:'kval',
                        minwidth: '40'
                    },
                    {
                        label: "B值",
                        value:'bval',
                        minwidth: '40'
                    },
                    {
                        label: "地址",
                        value:'address',
                        minwidth: '70'
                    },
                    {
                        label: "上限",
                        value:'uplimt',
                        minwidth: '40'
                    },
                    {
                        label: "下限",
                        value:'downlimt',
                        minwidth: '40'
                    },
                ],
                YXheader: [
                    {
                        label: "点号",
                        value: 'ID',
                        minwidth: '30'
                    }, {
                        label: "名称",
                        value: 'name',
                        minwidth: '140'
                    },
                    {
                        label: "描述",
                        value: 'describe',
                        minwidth: '80'
                    },
                    {
                        label: "ASDU",
                        value: 'ASDU',
                        minwidth: '80'
                    },
                    {
                        label: "字节位",
                        value:'wordPos',
                        minwidth: '40'
                    },
                    {
                        label: "bit位",
                        value: 'bitPos',
                        minwidth: '40'
                    },
                    {
                        label: "所占位",
                        value: 'bitLength',
                        minwidth: '50'
                    },
                    {
                        label: "LinkPoint1",
                        value:'LinkPoint1',
                        minwidth: '80'
                    },
                    {
                        label: "LinkPoint2",
                        value: 'LinkPoint2',
                        minwidth: '80'
                    },
                    {
                        label: "OneToZero",
                        value: 'OneToZero',
                        minwidth: '80'
                    },
                    {
                        label: "ZeroToOne",
                        value:'ZeroToOne',
                        minwidth: '80'
                    },
                    {
                        label: "address",
                        value:'address',
                        minwidth: '80'
                    },
                ],
                YKheader: [
                    {
                        label: "点号",
                        value: 'ID',
                        minwidth: '30'
                    }, {
                        label: "名称",
                        value: 'name',
                        minwidth: '120'
                    },
                    {
                        label: "描述",
                        value: 'describe',
                        minwidth: '80'
                    },
                    {
                        label: "ASDU",
                        value: 'ASDU',
                        minwidth: '80'
                    },
                    {
                        label: "字节位",
                        value: 'wordPos',
                        minwidth: '40'
                    },
                    {
                        label: "bit位",
                        value: 'bitPos',
                        minwidth: '40'
                    },
                    {
                        label: "所占位数",
                        value: 'bitLength',
                        minwidth: '40'
                    },
                    {
                        label: "EnablePoint",
                        value: 'EnablePoint',
                        minwidth: '40'
                    },
                    {
                        label: "EnableValue",
                        value: 'EnableValue',
                        minwidth: '80'
                    },
                    {
                        label: "地址",
                        value: 'address',
                        minwidth: '80'
                    },
                ],
                YTheader: [
                    {
                        label: "点号",
                        value: 'ID',
                        minwidth: '30'
                    }, {
                        label: "名称",
                        value: 'name',
                        minwidth: '140'
                    },
                    {
                        label: "描述",
                        value: 'describe',
                        minwidth: '80'
                    },
                    {
                        label: "单位",
                        value: 'unit',
                        minwidth: '40'
                    },
                    {
                        label: "K值",
                        value: 'kval',
                        minwidth: '40'
                    },
                    {
                        label: "B值",
                        value: 'bval',
                        minwidth: '40'
                    },
                    {
                        label: "地址",
                        value: 'address',
                        minwidth: '80'
                    },
                    {
                        label: "上限",
                        value: 'uplimt',
                        minwidth: '40'
                    },
                    {
                        label: "下限",
                        value: 'downlimt',
                        minwidth: '40'
                    },

                ],
                SOEheader: [
                   {
                        label: "点号",
                        value: 'ID',
                        minwidth: '30'
                    }, {
                        label: "名称",
                        value: 'name',
                        minwidth: '140'
                    },
                    {
                        label: "描述",
                        value: 'describe',
                        minwidth: '80'
                    }, 
                    {
                        label: "level",
                        value: 'level',
                        minwidth: '80'
                    },
                ],
            };
        },
        mounted() {
            // document.oncontextmenu = function (e) { return false; }
            this.getTreeData();
            // this.getTableHeader();
        },
        watch: {
            // 默认点击Tree第一个节点
            treeData(val) {
                if (val) {
                    this.$nextTick(() => {
                        document.querySelector('.el-tree-node__content').click();
                    })
                }
            },
        },
		methods: {
		    async getTreeData() {
                // 对应Python提供的接口
                const path = 'http://127.0.0.1:5000/getStaTree';
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

            async getTableHeader() {
                const path = 'http://127.0.0.1:5000/getTableHeader';

                await axios.get(path).then(function (response) {
                    var tableHeader = response.data.tableHeader;
                    // console.log(tableHeader);
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
                const path = 'http://127.0.0.1:5000/getSOEdata';
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
                const path = 'http://127.0.0.1:5000/getYTdata';
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
                const path = 'http://127.0.0.1:5000/getYKdata';
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
                const path = 'http://127.0.0.1:5000/getYXdata';
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
                const path = 'http://127.0.0.1:5000/getYCdata';
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
                const path = 'http://127.0.0.1:5000/getLianludata';

                await axios.get(path).then(function (response) {
                    var lianludata = response.data.staproperty;
                    var count = response.data.lenstap;
                    that.lianludata = lianludata;
                    that.totalcount = count;
                    that.tabledata = that.lianludata;
                    that.viewTableData(lianludata);
                });
            },

            //显示的table数据
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
        },
    };
</script>