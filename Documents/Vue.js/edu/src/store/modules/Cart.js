import axios from 'axios';

const state = {
    cart : [],
    

}

const getters  ={
    courses : function() {
        state.blogs = JSON.parse(JSON.stringify(state.courses))
        if(state.courses.length == 0){
            //
        }else{
            return state.courses
        }
        return []
    },
    
}

const actions = {
    async fetchCart({commit}){
        const response = await axios.get('https://cors-anywhere.herokuapp.com/https://boiling-garden-13643.herokuapp.com/cart/getCartDetails',
        {
            headers: {
                authorization:  localStorage.getItem('token')
                }
        });
       
        commit('setCart',response.data)
    },
    
}


const mutations ={
        setCart :(state,cart) =>(state.cart = cart),

}

export default{
    state,
    getters,
    actions,
    mutations,
}
