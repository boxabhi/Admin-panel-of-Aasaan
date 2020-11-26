import axios from 'axios';

const state = {
    categories : []
}



const getters  ={
     allCategories : function() {
        return state.categories;
     },
     allCategoriesName : function() {
         var category_names = [];
         for(var i = 0; i < state.categories.length;i++){
             category_names.push(JSON.stringify({'id':state.categories[i].id ,'name':state.categories[i].name.english}))
         }
         return category_names
     }
}

const actions = {
    async fetchCategories({commit}){
        var url= window.url
        const response =  await axios.get(`${url}/categories`)
        console.log(response)
        commit('setCategories',response.data)
    },

}


const mutations ={
    setCategories :(state,categories) => (state.categories = categories),     
}

export default{
    state,
    getters,
    actions,
    mutations,

}
