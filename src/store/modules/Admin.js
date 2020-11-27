
const state = {
    admin : {
        isLogged : false,
        refresh : null,
        access : null,
        timeLoggedIn : null,
    }
}



const getters  ={
     getAdmin : function() {
        return state.admin;
     },
    
}

const actions = {
    async loginAdmin({commit}, data){
        console.log("this is admin data")
        console.log(data)
        localStorage.setItem('admin', JSON.stringify(data))
       
        commit('setAdmin',data)
    },

}


const mutations = {
    setAdmin :(state,admin) => (state.admin = admin),     
}

export default{ state, getters, actions, mutations}
