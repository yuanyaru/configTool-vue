<template>
<el-container>
    <el-header>
        <span>配置工具</span>
        <span id="sta_name" style="font-size: 15px;"></span>
        
        <div class="screenfull" @click="screenfullclick">
          <i class="el-icon-full-screen"></i>
          <span>{{ isscreenfull ? '退出全屏' : '全屏' }}</span>
        </div>
        <div class="refresh" @click="refresh">
          <i class="vxe-icon--refresh roll"></i>
          <span @click="refresh">刷新</span>
        </div>
        <div style="float: left;">
            <el-link @click="monitoringPage" id="monitoring_id" icon="el-icon-data-analysis" type="danger">监控界面</el-link>
        </div>
    </el-header>

    <el-container>
        <el-aside>
            <el-scrollbar style="height:90%">
            <el-tree :data="treeData" 
                     @node-click="handleNodeClick"
                     :props="defaultProps"
                     style="background-color: #F5F7FA;max-width: 300px;"
                     :highlight-current="true">
            </el-tree>
            </el-scrollbar>
        </el-aside>

        <el-main>
            <vxe-toolbar custom>
                <template #buttons>
                <!-- <vxe-input v-model="filterName1" type="search" placeholder="试试全表搜索" @keyup="searchEvent1"></vxe-input> -->
                <vxe-button status="primary" icon="vxe-icon--upload" @click="impotEvent" title="导入"></vxe-button>
                <vxe-button status="primary" icon="vxe-icon--download" @click="exportEvent" title="导出"></vxe-button>
                <vxe-button status="danger" icon="fa fa-trash-o" @click="removeEvent" title="删除"></vxe-button>
                <vxe-button status="primary" icon="fa fa-save" @click="saveEvent" title="保存"></vxe-button>
                <vxe-button status="primary" icon="fa fa-plus" @click="insertEvent()" title="插入"></vxe-button>
                <vxe-button status="primary" icon="fa fa-refresh" @click="chongzhi" title="重置"></vxe-button>
                <vxe-button style="float: right;">
                <template #default>滚动操作</template>
                <template #dropdowns>
                    <vxe-button type="text" @click="$refs.xTable.scrollToRow($refs.xTable.getData(30))">滚动到第 30 行</vxe-button>
                    <vxe-button type="text" @click="$refs.xTable.scrollToRow($refs.xTable.getData(100))">滚动到第 100 行</vxe-button>
                    <vxe-button type="text" @click="$refs.xTable.scrollToRow($refs.xTable.getData(300))">滚动到第 300 行</vxe-button>
                    <vxe-button type="text" @click="$refs.xTable.scrollToRow($refs.xTable.getData(1000))">滚动第 1000 行</vxe-button>
                </template>
                </vxe-button>
                <!-- <vxe-button @click="handleCheckbox">所有行选中</vxe-button> -->
                </template>
            </vxe-toolbar>

            <vxe-table
                border
                :loading="loading"
                stripe
                resizable
                :height="Height"
                auto-resize
                keep-source
                show-overflow
                ref="xTable"
                row-id="ID"
                :columns="viewcolumns"
                :data="tabledata"
                :mouse-config="{selected: true}"
                :checkbox-config="{reserve: true, range: true, highlight: true}" 
                :edit-rules="validRules"
                :edit-config="{trigger: 'dblclick', mode: 'cell', activeMethod: activeCellMethod}"
                @edit-disabled="editDisabledEvent"
                @edit-closed="editClosedEvent">
                <vxe-column type="checkbox" width="50"></vxe-column>

                <vxe-column :field = item.field
                            :title = item.title 
                             v-for="(item, key) in viewcolumns"
                            :key="key"
                            :edit-render="{placeholder: '请点击输入...', autofocus: '.vxe-input--inner', autoselect: true}">
                <template #edit="{ row }" >
                    <!-- <div>{{item.title}}</div> -->
                    <vxe-input v-model="row[item.title]" type="text"></vxe-input>
                </template>
                </vxe-column>
                <template #empty>
                    <span style="color: red;">
                    <img src="https://n.sinaimg.cn/sinacn17/w120h120/20180314/89fc-fyscsmv5911424.gif">
                <p>没有更多数据了！</p>
            </span>
          </template>
            </vxe-table>

            <!-- 分页 -->
            <!-- <div class="block" style="float: right;margin-top: 1px;margin-bottom: 1px;padding-right: 15px">
                <span class="demonstration"></span>
                <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentpage"
                    :page-sizes="[10, 30, 50, 100, totalcount]"
                    :page-size="pagesize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="totalcount">
                </el-pagination>
            </div> -->
        </el-main>
    </el-container>

    <el-footer>
        <span>@2022 西安端怡科技有限公司</span>
    </el-footer>
</el-container>
</template>
 
<script>
import axios from 'axios';
import XLSX from 'xlsx';
import screenfull from "screenfull"
import XEUtils from 'xe-utils'

export default {
    data () {
        return {
            Height: "530px",
            loading: false,
            custom: true,
            filterName1: '',
            loading: false,
            isscreenfull: false,
            treeData: [],
            defaultProps: {
                children: 'children',
                label: 'label'
            },
            viewcolumns: [],  //显示的列
            viewtableData: [], //根据列显示的数据
            tabledata: [],
            station_ID: '', 
            station_name: '',
            pagesize: 10,  //一页显示多少个
            totalcount: 0, //总共有多少条数据
            currentpage: 1,
            exportFileName: '',
            setData: '',
            deleteData: '',

            staColumn: [
                { field: "ID", title: 'ID' },
                { field: 'name', title: 'name' },
                { field: 'describe', title: 'describe' },
                { field: 'ruleID', title: 'ruleID' },
                { field: 'address', title: 'address' },
                { field: 'PORT', title: 'PORT' },
                { field: 'role', title: 'role' },
            ],
            yxColumn: [
                { field: "ID", title: 'ID'},
                { field: 'name', title: 'name' },
                { field: 'describe', title: 'describe' },
                { field: 'ASDU', title: 'ASDU' },
                { field: 'wordPos', title: 'wordPos' },
                { field: 'bitPos', title: 'bitPos' },
                { field: 'bitLength', title: 'bitLength' },
                { field: 'LinkPoint1', title: 'LinkPoint1' },
                { field: 'LinkPoint2', title: 'LinkPoint2' },
                { field: 'OneToZero', title: 'OneToZero' },
                { field: 'ZeroToOne', title: 'ZeroToOne' },
                { field: 'address', title: 'address' },
            ],
            ykColumn: [
                { field: "ID", title: 'ID' },
                { field: 'name', title: 'name' },
                { field: 'describe', title: 'describe' },
                { field: 'ASDU', title: 'ASDU' },
                { field: 'wordPos', title: 'wordPos' },
                { field: 'bitPos', title: 'bitPos' },
                { field: 'bitLength', title: 'bitLength' },
                { field: 'EnablePoint', title: 'EnablePoint' },
                { field: 'EnableValue', title: 'EnableValue' },
                { field: 'address', title: 'address' },
            ],
            ycColumn: [
                { field: "ID", title: 'ID' },
                { field: 'name', title: 'name' },
                { field: 'describe', title: 'describe' },
                { field: 'unit', title: 'unit' },
                { field: 'kval', title: 'kval' },
                { field: 'bval', title: 'bval' },
                { field: 'address', title: 'address' },
                { field: 'uplimt', title: 'uplimt' },
                { field: 'downlimt', title: 'downlimt' },
            ],
            ytColumn: [
                { field: "ID", title: 'ID' },
                { field: 'name', title: 'name' },
                { field: 'describe', title: 'describe' },
                { field: 'unit', title: 'unit' },
                { field: 'kval', title: 'kval' },
                { field: 'bval', title: 'bval' },
                { field: 'address', title: 'address' },
                { field: 'uplimt', title: 'uplimt' },
                { field: 'downlimt', title: 'downlimt' },
            ],
            soeColumn: [
                { field: "ID", title: 'ID' },
                { field: 'name', title: 'name' },
                { field: 'describe', title: 'describe' },
                { field: 'level', title: 'level' },
            ],
            
            validRules: {
                name: [
                    { required: true, message: '名称必须填写' }
                ]
            },
        }
    },
    created() {
        // 获取数据
        this.getTreeData();
        this.searchEvent1();
    },
    mounted() {
        // 表格高度自适应屏幕大小
        this.Height = window.innerHeight - this.$refs.xTable.$el.offsetTop - 110;
    },
    methods: {
        monitoringPage() {
            var monitoring_URL = BASE_INFO.monitoring_URL + "/THPBuilder/viewer.html";
            var v = document.getElementById("monitoring_id");
            v.href = monitoring_URL ;
        },

        activeCellMethod ({ column, columnIndex }) {
            if (columnIndex === 1) {
            return false
            }
            return true
        },

        editDisabledEvent ({ row, column }) {
            this.$XModal.message({ content: '禁止编辑', status: 'error' })
        },

        searchEvent1 () {
            const filterName = XEUtils.toValueString(this.filterName1).trim().toLowerCase()
            if (filterName) {
                const filterRE = new RegExp(filterName, 'gi')
                const searchProps = ['name']
                const rest = this.tabledata.filter(item => searchProps.some(key => XEUtils.toValueString(item[key]).toLowerCase().indexOf(filterName) > -1))
                this.tabledata = rest.map(row => {
                    const item = Object.assign({}, row)
                    searchProps.forEach(key => {
                        item[key] = XEUtils.toValueString(item[key]).replace(filterRE, match => `<span class="keyword-lighten">${match}</span>`)
                    })
                    return item
                })
            } else {
                //this.tabledata = this.tabledata
                this.chongzhi()
            }
        },

        async getTreeData() {
            let that = this;
            that.viewcolumns=that.staColumn
            this.getLianludata()
            // 对应Python提供的接口
            /* const path = 'http://127.0.0.1:5000/getStaTree'; */
            const path = BASE_INFO.back_URL + '/getStaTree';
            that.treeData = [];
            
            await axios.get(path).then(function (response) {
                //var staLen = response.data.staLen;
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
                            name:staNames[i],
                        }, {
                            label: '遥测', 
                            id: i+1,
                            name:staNames[i],
                        }, {
                            label: '遥控',
                            id: i+1,
                            name:staNames[i],
                        }, {
                            label: '遥调',
                            id: i+1,
                            name:staNames[i],
                        }, {
                            label: 'SOE',
                            id: i+1,
                            name:staNames[i],
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
                that.viewcolumns = [];
                that.viewcolumns=that.staColumn
                that.exportFileName = "station"
                that.setData = "/setStation"
                that.deleteData = "/deleteStation"
                that.getLianludata();
            }
            if(data.label=="遥测") {
                that.station_ID = data.id
                that.station_name = data.name
                console.log(that.station_name)
                that.viewcolumns = [];
                that.viewcolumns = that.ycColumn
                that.exportFileName = "yc"
                that.setData = "/setYc"
                that.deleteData = "/deleteYc"
                that.getYCdata();
            }
            if(data.label=="遥信") {
                that.station_ID = data.id;
                that.station_name = data.name
                that.viewcolumns = [];
                that.viewcolumns = that.yxColumn
                that.exportFileName = "yx"
                that.setData = "/setYx"
                that.deleteData = "/deleteYx"
                that.getYXdata();
            }
            if(data.label=="遥控") {
                that.station_ID = data.id;
                that.station_name = data.name
                that.viewcolumns = [];
                that.viewcolumns = that.ykColumn
                that.exportFileName = "yk"
                that.setData = "/setYk"
                that.deleteData = "/deleteYk"
                that.getYKdata();
            }
            if(data.label=="遥调") {
                that.station_ID = data.id;
                that.station_name = data.name
                that.viewcolumns = [];
                that.viewcolumns = that.ytColumn
                that.exportFileName = "yt"
                that.setData = "/setYt"
                that.deleteData = "/deleteYt"
                that.getYTdata();
            }
            if(data.label=="SOE") {
                that.station_ID = data.id;
                that.station_name = data.name
                that.viewcolumns = [];
                that.viewcolumns = that.soeColumn
                that.exportFileName = "soe"
                that.setData = "/setSoe"
                that.deleteData = "/deleteSoe"
                that.getSOEdata();
            }
        },

        async getLianludata() {
            this.loading = true
            let that = this;
            //document.getElementById("sta_name").innerText="";
            that.tabledata = [];
            const path = BASE_INFO.back_URL + '/getLianludata';

            await axios.get(path).then(function (response) {
                var lianludata = response.data.staproperty;
                var count = response.data.lenstap;
                that.totalcount = count;
                that.tabledata = lianludata;
                that.viewTableData(lianludata);
            });
            this.loading = false
        },

        async getYXdata() {
            this.loading = true
            let that = this;
            document.getElementById("sta_name").innerText="---"+ that.station_name;
            that.tabledata = [];
            const path = BASE_INFO.back_URL + '/getYXdata';
            var station_ID = that.station_ID;
            var params = {
                stationId: station_ID,
            };

            await axios.get(path, {params: params}).then(function (response) {
                var yxdata = response.data.yxproperty
                var count = response.data.lenyxp
                that.totalcount = count
                that.yxdata = yxdata
                that.tabledata = yxdata
                that.viewTableData(yxdata);
            });
            this.loading = false
        },

        async getYCdata() {
            this.loading = true
            let that = this;
            that.tabledata = [];
            const path = BASE_INFO.back_URL + '/getYCdata';
            var station_ID = that.station_ID;
            var params = {
                stationId: station_ID,
            };

            await axios.get(path, {params: params}).then(function (response) {
                var ycdata = response.data.ycproperty;
                var count = response.data.lenycp;
                that.totalcount = count;
                that.tabledata = ycdata;
                that.viewTableData(ycdata);
            });
            this.loading = false
        },

        async getYKdata() {
            this.loading = true
            let that = this;
            that.tabledata = [];
            const path = BASE_INFO.back_URL + '/getYKdata';
            var station_ID = that.station_ID;
            var params = {
                stationId: station_ID,
            };

            await axios.get(path, {params: params}).then(function (response) {
                var ykdata = response.data.ykproperty;
                var count = response.data.lenykp;
                that.totalcount = count;
                that.tabledata = ykdata;
                that.viewTableData(ykdata);
            });
            this.loading = false
        },

        async getYTdata() {
            this.loading = true
            let that = this;
            that.tabledata = [];
            const path = BASE_INFO.back_URL + '/getYTdata';
            var station_ID = that.station_ID;
            var params = {
                stationId: station_ID,
            };

            await axios.get(path, {params: params}).then(function (response) {
                var ytdata = response.data.ytproperty;
                var count = response.data.lenytp;
                that.totalcount = count;
                that.tabledata = ytdata;
                that.viewTableData(ytdata);
            });
            this.loading = false
        },

        async getSOEdata() {
            this.loading = true
            let that = this;
            that.tabledata = [];
            const path = BASE_INFO.back_URL + '/getSOEdata';
            var station_ID = that.station_ID;
            var params = {
                stationId: station_ID,
            };

            await axios.get(path, {params: params}).then(function (response) {
                var soedata = response.data.soeproperty;
                var count = response.data.lensoep;
                that.totalcount = count;
                that.tabledata = soedata;
                that.viewTableData(soedata);
            });
            this.loading = false
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
            //console.log(`每页 ${val} 条`);
            this.pagesize = val;
            var data = this.tabledata;
            this.viewTableData(data);
        },

        handleCurrentChange(val) {
            //console.log(`当前页: ${val}`);
            this.currentpage = val;
            var data = this.tabledata;
            this.viewTableData(data);
        },

        async insertEvent (row) {
            const $table = this.$refs.xTable
            if(this.setData == "/setStation") {
                var record = {
                    ID: this.totalcount + 1,
                    name: '',
                    describe: '1',
                    ruleID: '1',
                    address: '0',
                    PORT: '60000',
                    role: '1'
                }
            } else if(this.setData == "/setYc") {
                var id = this.totalcount + 1
                var record = {
                    ID: id,
                    name: '',
                    describe: 'station1_YC_' + id,
                    unit: '',
                    kval: '1',
                    bval: '0',
                    address: '0',
                    uplimt: '200',
                    downlimt: '0'
                }
            } else if(this.setData == "/setYx") {
                var id = this.totalcount + 1
                var record = {
                    ID: id,
                    name: '',
                    describe: 'station1_YX_' + id,
                    ASDU: '1',
                    wordPos: '0',
                    bitPos: '0',
                    bitLength: '1',
                    LinkPoint1: '0',
                    LinkPoint2: '0',
                    OneToZero: '由分到合',
                    ZeroToOne: '由合到分',
                    address: '0',
                }
            } else if(this.setData == "/setYk") {
                var id = this.totalcount + 1
                var record = {
                    ID: id,
                    name: '',
                    describe: 'station1_YK_' + id,
                    ASDU: '1',
                    wordPos: '0',
                    bitPos: '0',
                    bitLength: '1',
                    EnablePoint: '0',
                    EnableValue: '0',
                    address: '0',
                }
            } else if(this.setData == "/setYt") {
                var id = this.totalcount + 1
                var record = {
                    ID: id,
                    name: '',
                    describe: 'station1_YT_' + id,
                    unit: '',
                    kval: '1',
                    bval: '0',
                    address: '0',
                    uplimt: '200',
                    downlimt: '0'
                }
            } else if(this.setData == "/setSoe") {
                var id = this.totalcount + 1
                var record = {
                    ID: id,
                    name: '',
                    describe: 'station1_SOE_' + id,
                    level: '1'
                }
            }
            const { row: newRow } = await $table.insertAt(record, row)
            // await $table.setActiveCell(newRow, 'name')
        },

        // 实时保存
        async editClosedEvent ({ row }) {
            let that = this;
            const $table = that.$refs.xTable
            const errMap = await $table.validate().catch(errMap => errMap)
            if (errMap) {
                return
            }
            let station = [row]
            const path = BASE_INFO.back_URL + this.setData;
            var station_ID = this.station_ID

            axios.post(path, {"selectRecords": station, "station": station_ID}).then(function (response) {
                var status = response.data.status;
                if(status == 1) {
                    that.$XModal.message({
                        content: `保存成功！`,
                        status: 'success'});
                        if(that.setData == "/setStation") {
                            that.getTreeData();
                        } else if(that.setData == "/setYc") {
                            that.getYCdata();
                        } else if(that.setData == "/setYx") {
                            that.getYXdata();
                        } else if(that.setData == "/setYk") {
                            that.getYKdata();
                        } else if(that.setData == "/setYt") {
                            that.getYTdata();
                        } else if(that.setData == "/setSoe") {
                            that.getSOEdata();
                        }
                } else {
                    that.$XModal.message({
                        content: `保存失败！`,
                        status: 'error'});
                  }
            });
        },

        async saveRowEvent (row) {
            let that = this;
            const $table = that.$refs.xTable
            let station = [row]
            var station_ID = this.station_ID
            //console.log(typeof station_ID)

            $table.clearActived().then(() => {
                that.$axios.post(that.$ipconfig.updateTable, {params: params}).then(function (response) {
                    var status = response.data.status;
                    console.log(status)
                    if(status == 1) {
                        that.$XModal.message({
                            content: `保存成功！`,
                            status: 'success'});
                            if(that.setData == "/setStation") {
                                that.getTreeData();
                            } else if(that.setData == "/setYc") {
                                that.getYCdata();
                            } else if(that.setData == "/setYx") {
                                that.getYXdata();
                            } else if(that.setData == "/setYk") {
                                that.getYKdata();
                            } else if(that.setData == "/setYt") {
                                that.getYTdata();
                            } else if(that.setData == "/setSoe") {
                                that.getSOEdata();
                            }
                    } else {
                        that.$XModal.message({
                            content: `保存失败！`,
                            status: 'error'});
                    }
                })
            })
        },

        // 批量保存
        saveEvent () {
            let that = this;
            const $table = this.$refs.xTable
            const selectRecords = $table.getCheckboxRecords();
            const checkedRows = selectRecords.length;
            var station_ID = this.station_ID
            console.log(selectRecords)
            console.log(station_ID)

            if(checkedRows > 0) {
                const path = BASE_INFO.back_URL + that.setData;
                axios.post(path, {"selectRecords": selectRecords, "station": station_ID}).then(function (response) {
                    var status = response.data.status;
                    if(status == 1) {
                        that.$XModal.message({
                            content: `保存成功！`,
                            status: 'success'});
                            if(that.setData == "/setStation") {
                                that.getTreeData();
                            } 
                            $table.clearCheckboxRow()
                    } else {
                        that.$XModal.message({
                            content: `保存失败！`,
                            status: 'error'});
                    }
                });
            } else {
                that.$XModal.message({
                    content: `请至少选择一条记录！`,
                    status: 'warning'});
            }
        },

        // 表格全选
        handleCheckbox() {
            const $table = this.$refs.xTable
            var dataLen = (this.tabledata).length
            for(var i=0; i<dataLen; i++) {
                $table.setCheckboxRow(this.tabledata[i], true)
            }
        },

        // 删除
        async removeEvent () {
            let that = this
            const $table = this.$refs.xTable
            const selectRecords = $table.getCheckboxRecords()
            var ids = []
            const checkedRows = selectRecords.length
            console.log(checkedRows)
            var station_ID = that.station_ID

            if(checkedRows > 0) {
                const type = await this.$XModal.confirm('您确定要删除该数据?')
                if (type === 'confirm') {
                    for(var i=0; i<checkedRows; i++) {
                        var id = selectRecords[i]["ID"];
                        ids.push(id);
                    }
                    const path = BASE_INFO.back_URL + that.deleteData;
                    await axios.post(path, {"ids": ids, "station": station_ID}).then(function (response) {
                        var status = response.data.status;
                        if(status == 1) {
                            that.$XModal.message({
                                content: `删除成功！`,
                                status: 'success'});
                                if(that.deleteData == "/deleteStation") {
                                    that.getTreeData();
                                } else if(that.deleteData == "/deleteYc") {
                                    that.getYCdata();
                                } else if(that.deleteData == "/deleteYx") {
                                    that.getYXdata();
                                } else if(that.deleteData == "/deleteYk") {
                                    that.getYKdata();
                                } else if(that.deleteData == "/deleteYt") {
                                    that.getYTdata();
                                } else if(that.deleteData == "/deleteSoe") {
                                    that.getSOEdata();
                                }
                                $table.clearCheckboxRow()
                        } else {
                            that.$XModal.message({
                                content: `删除失败！`,
                                status: 'error'});
                        }
                    });
                } else {
                    // 清除所有行选中
                    $table.clearCheckboxRow()
                } 
            } else {
                that.$XModal.message({
                    content: `请至少选择一条记录！`,
                    status: 'warning'});
            }
        },

        // 导入
        async impotEvent () {
            this.loading = true
            const { files } = await this.$refs.xTable.readFile({
                types: ['xls', 'xlsx']
            })
            const fileReader = new FileReader()
            fileReader.onload = (ev) => {
                const data = ev.target.result
                const workbook = XLSX.read(data, { type: 'binary' })
                var sheetname = workbook.SheetNames[0]
                //console.log(sheetname)
                const csvData = XLSX.utils.sheet_to_csv(workbook.Sheets.Sheet1)
                const tableData = []
                var rows = csvData.split('\n');
                // 删除表头
                delete rows[0];
                // 解析数据
                rows.forEach((vRow) => {
                    if (vRow) {
                        //console.log(vRow)
                        const vCols = vRow.split(',')
                        const item = {}
                        // 删除数组的第一个元素
                        vCols.shift()
                        // console.log(vCols)
                        vCols.forEach((val, cIndex) => {
                            const column = this.viewcolumns[cIndex]
                            if (column.field) {
                                item[column.field] = val
                            }
                        })
                        tableData.push(item)
                    }
                })
                this.tabledata = tableData
                this.loading = false
            }
            fileReader.readAsBinaryString(files[0])
        },

        // 导出
        exportEvent () {
            // 有问题：tbody显示不全
            /* console.log(this.$refs.xTable.$el.querySelector('.body--wrapper>.vxe-table--body tbody'))
            var workBook = XLSX.utils.table_to_book(this.$refs.xTable.$el.querySelector('.body--wrapper>.vxe-table--body'))
            XLSX.writeFile(workBook, this.exportFileName) */

            this.$refs.xTable.exportData({
                filename: this.exportFileName,
                sheetName: 'Sheet1',
                type: 'xlsx',
                isHeader: true
            })
        }, 

        chongzhi() {
            if(this.deleteData == "/deleteStation") {
                this.getLianludata();
            } else if(this.deleteData == "/deleteYc") {
                this.getYCdata();
            } else if(this.deleteData == "/deleteYx") {
                this.getYXdata();
            } else if(this.deleteData == "/deleteYk") {
                this.getYKdata();
            } else if(this.deleteData == "/deleteYt") {
                this.getYTdata();
            } else if(this.deleteData == "/deleteSoe") {
                this.getSOEdata();
            }
        },

        screenfullclick() {
            // 判断是否支持
            if (!screenfull.enabled) {
                console.dir('不支持全屏')
            }
            this.isscreenfull = !this.isscreenfull
            screenfull.toggle();
        },

        refresh() {
            location.reload();
        },
    }
}
</script>

<style>
    .el-scrollbar .el-scrollbar__wrap {overflow-x: hidden;}

    .el-header {
        position: fixed;
        top: 0px;
        width: 100%;
        height: 50px;
        left: 0px;
        line-height: 50px;
        padding: 5px;
        background-color: #003366;
        color: white;
        text-align: center; 
        font-size: 35px;
    }

    .el-main {
        position: fixed;
        left: 285px;
        right: 10px;
        top: 60px;
        bottom: 35px;
        float: left;
        padding: 5px;
    }

    .el-aside {
        position: fixed;
        line-height: 30px;
        left: 0px;
        top: 60px;
        bottom: 35px;
        width:280px;
        float:left;
        padding:5px;
        background-color: rgb(238, 241, 246);
        color: black;
    }

    .el-footer {
        position: fixed;
        background-color: #003366;
        color: white;
        text-align: center; 
        line-height: 60px;
        width: 100%;
        bottom: 0px;
        left: 0px;
        height: 25px;
        padding: 5px;
    }

    .keyword-lighten {
        color: #000;
        background-color: #FFFF00;
    }
</style>