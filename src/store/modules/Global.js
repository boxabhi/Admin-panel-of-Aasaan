import axios from 'axios';

const state = {
    mobiles : [],
    images : [],
    requests : [],
}



const getters  ={
     getMobileNumbers : function() {
        return state.mobiles;
    },
    getImages : function() {
        return state.images;
    },
    getRequests : function() {
        return state.requests;
    }
}

const actions = {
    async fetchMobiles({commit}){
        var url= window.url
        var token = JSON.parse(localStorage.getItem('admin'))
        const response =  await axios.get(`${url}/api/admin/mobiles`,{
            headers: {
              'Authorization': `Bearer ${token.access} `
            }
        })
        commit('setMobiles',response.data)
    },

    async fetchImages({commit}){
        var url = window.url
        const response = await axios.get(`${url}/api/image`)
        commit('setImages' , response.data)
    },

    async fetchRequests({commit}){
        var url = window.url
        const response = await axios.get(`${url}/api/admin/requests`)
        commit('setRequests' , response.data)
    }

}


const mutations ={
    setMobiles :(state,mobiles) => (state.mobiles = mobiles),    
    setImages :(state,images) => (state.images = images) ,
    setRequests : (state , requests) => (state.requests = requests)
}

export default{
    state,
    getters,
    actions,
    mutations,

}
