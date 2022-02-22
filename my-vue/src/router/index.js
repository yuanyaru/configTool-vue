import Vue from 'vue'
import Router from 'vue-router'
import configTool from '@/components/configTool'
import report from '@/components/report'
import editTable from '@/components/editTable'
import configToolb from '@/components/configToolb'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'configTool',
      component: configTool
    },
    {
      path: '/b',
      name: 'configToolb',
      component: configToolb
    },
    {
      path: '/report',
      name: 'report',
      component: report
    },
    {
      path: '/editTable',
      name: 'editTable',
      component: editTable
    },
  ],
  // 让 URL 变成http://localhost:8080/ping的形式。如果，不加该设置，默认的 URL 为http://localhost:8080/#/ping的形式。
  mode: 'history',
})