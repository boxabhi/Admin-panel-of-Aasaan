import Vue from 'vue'
import axios from 'axios'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import QuestionIndex from '../views/question/QuestionIndex.vue'
import QuestionCreate from '../views/question/QuestionCreate.vue'
import SuperIndex from '../views/super/SuperIndex.vue'
import SuperCreate from '../views/super/SuperCreate.vue'
import SuperShow from '../views/super/SuperShow.vue'
import CategoryIndex from '../views/category/CategoryIndex.vue'
import CategoryCreate from '../views/category/CategoryCreate.vue'
import Password from '../views/admin/Password.vue'
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