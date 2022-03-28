// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App'
import router from './router'

import 'xe-utils'
import vueXlsxTable from 'vue-xlsx-table'
import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'
import "font-awesome/css/font-awesome.css"
// vxe-table-plugin-export-xlsx 插件
import VXETablePluginExportXLSX from 'vxe-table-plugin-export-xlsx'

Vue.use(VXETable)
VXETable.use(VXETablePluginExportXLSX)
Vue.prototype.$XModal = VXETable.modal
Vue.use(vueXlsxTable, {rABS: false})
Vue.use(ElementUI, { size: 'small', zIndex: 3000 });
Vue.config.productionTip = false

// eslint-disable no-new 
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})