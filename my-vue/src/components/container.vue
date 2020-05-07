<template>
<el-container>
    <el-header>
        <span>点表配置工具</span>
    </el-header>

    <el-container>
        <el-aside>
            <el-tree :data="treeData" :props="defaultProps">
            </el-tree>
        </el-aside>
    
        <el-main>
            <el-table :data="tableData">
                <el-table-column prop="date" label="日期" width="140">
                </el-table-column>
                <el-table-column prop="name" label="姓名" width="120">
                </el-table-column>
                <el-table-column prop="address" label="地址">
                </el-table-column>
            </el-table>
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
</style>

<script>
    import axios from 'axios';

    export default {
        data() {
            const table_item = {
                date: '2016-05-02',
                name: '王小虎',
                address: '上海市普陀区金沙江路 1518 弄'
            };
            return {
                treeData: [],
                defaultProps: {
                    children: 'children',
                    label: 'label'
                },
                tableData: Array(10).fill(table_item),
            };
        },
        mounted() {
		    this.getTreeData();
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
                            }, {
                                label: '遥测',  
                            }, {
                                label: '遥控',
                            }, {
                                label: '遥调',
                            }, {
                                label: 'SOE',
                            }]
                        };
                        treeitem.children.push(tree_item);
                    }
                    that.treeData.push(treeitem);
		        });
            },
        },
    };
</script>