import Vue from 'vue';
import Vuex from 'vuex';

import Questions from './modules/Questions.js'
import Super from './modules/Super.js'
import Categories from './modules/Categories.js'
import Admin from './modules/Admin.js'
import Global from './modules/Global.js'
import Users from './modules/Users.js'







Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        Questions,
        Super,
        Categories,
        Admin,
        Global,
        Users
    }
})