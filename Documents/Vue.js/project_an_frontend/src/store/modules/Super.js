import axios from 'axios';

const state = {
    super_category : []
}



const getters  ={
     allSuper : function() {
        return state.super_category;
    }
}

const actions = {
    async fetchSuper({commit}){
        var url= window.url
        const response =  await axios.get(`${url}/super`)
        commit('setSuper',response.data.data)
    },

}


const mutations ={
    setSuper :(state,super_category) => (state.super_category = super_category),     
}

export default{
    state,
    getters,
    actions,
    mutations,

}
