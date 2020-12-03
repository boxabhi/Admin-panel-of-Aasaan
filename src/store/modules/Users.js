import axios from 'axios';

const state = {
   users : []
}



const getters  ={
     allUsers : function() {
        return state.users;
    }
}

const actions = {
    async fetchUsers({commit}){
        var url= window.url
        var token = JSON.parse(localStorage.getItem('admin'))
        const response =  await axios.get(`${url}/api/admin/users`, {
            headers: {
            'Authorization': `Bearer ${token.access} `
          }
        })
        commit('setUsers',response.data)
    },

}


const mutations ={
    setUsers :(state,users) =>(state.users = users),     
}

export default{
    state,
    getters,
    actions,
    mutations,

}
