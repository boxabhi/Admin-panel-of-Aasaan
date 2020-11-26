import Vue from 'vue';
import Vuex from 'vuex';

import Questions from './modules/Questions.js'
import Super from './modules/Super.js'
import Categories from './modules/Categories.js'




Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        Questions,
        Super,
        Categories
    }
})