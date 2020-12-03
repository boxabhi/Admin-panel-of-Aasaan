import Vue from 'vue'
import axios from 'axios'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import QuestionIndex from '../views/question/QuestionIndex.vue'
import QuestionCreate from '../views/question/QuestionCreate.vue'
import QuestionShow from '../views/question/QuestionShow.vue'

import SuperIndex from '../views/super/SuperIndex.vue'
import SuperCreate from '../views/super/SuperCreate.vue'
import SuperShow from '../views/super/SuperShow.vue'
import CategoryIndex from '../views/category/CategoryIndex.vue'
import CategoryCreate from '../views/category/CategoryCreate.vue'
import CategoryShow from '../views/category/CategoryShow.vue'
import Password from '../views/admin/Password.vue'
import CreateAdmin from '../views/admin/CreateAdmin.vue'
import UsersIndex from '../views/users/UsersIndex.vue'

import ImageUpload from '../views/admin/ImageUpload.vue'
import RequestIndex from '../views/requests/RequestIndex.vue'


import NotificationsIndex from '../views/notifications/NotificationsIndex.vue'



Vue.use(VueRouter)

const routes = [{
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    beforeEnter: (to, from, next) => {
      let currentAdmin = (localStorage.getItem('admin')) || null;
      console.log(currentAdmin)
      if(currentAdmin == null){
        next('/')
        return;
      }

      currentAdmin = JSON.parse(localStorage.getItem('admin'));
      axios.post(`${window.url}/api/token/verify/`, {token: currentAdmin.access})
      .then(res => {
        console.log(res)
        next();
      }).catch(err => {
        console.log(err)
        next('/');
      })


    }
  },

  {
    path: '/question',
    name: 'QuestionIndex',
    component: QuestionIndex
  },
  {
    path: '/question/add',
    name: 'QuestionCreate',
    component: QuestionCreate
  },
  {
    path: '/question/show/:id',
    name: 'QuestionShow',
    component: QuestionShow
  },
  {
    path: '/super',
    name: 'SuperIndex',
    component: SuperIndex
  },
  {
    path: '/super/add',
    name: 'SuperCreate',
    component: SuperCreate
  },
  {
    path: '/super/show/:id',
    name: 'SuperShow',
    component: SuperShow
  },
  {
    path: '/category',
    name: 'CategoryIndex',
    component: CategoryIndex
  },
  {
    path: '/category/add',
    name: 'CategoryCreate',
    component: CategoryCreate
  },
  {
    path: '/category/show/:id',
    name: 'CategoryShow',
    component: CategoryShow
  },
  {
    path: '/password',
    name: 'Password',
    component: Password
  },
  {
    path: '/notifications',
    name: 'NotificationsIndex',
    component: NotificationsIndex
  },
  {
    path : '/admin/create',
    name: 'AdminCreate',
    component: CreateAdmin
  },
  {
    path : '/users',
    name: 'UserIndex',
    component: UsersIndex
  },
  {
    path : '/upload-image',
    name: 'UploadImage',
    component: ImageUpload
  },
  {
    path : '/requests',
    name: 'Requests',
    component: RequestIndex
  },
  {
    path: '/about',
    name: 'About',
    component: () => import( /* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/*',
    component: Home
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router