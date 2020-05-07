import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import container from '@/components/container'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/container',
      name: 'container',
      component: container
    },
  ],
  // 让 URL 变成http://localhost:8080/ping的形式。如果，不加该设置，默认的 URL 为http://localhost:8080/#/ping的形式。
  mode: 'history',
})