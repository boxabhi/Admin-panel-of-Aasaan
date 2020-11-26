import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import QuestionIndex from '../views/question/QuestionIndex.vue'
import QuestionCreate from '../views/question/QuestionCreate.vue'
import SuperCreate from '../views/super/SuperCreate.vue'
import SuperIndex from '../views/super/SuperIndex.vue'
import CategoryIndex from '../views/category/CategoryIndex.vue'
import CategoryCreate from '../views/category/CategoryCreate.vue'
import Password  from '../views/admin/Password.vue'






Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path :'/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
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
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
