import axios from 'axios';

const state = {
   questions : []
}



const getters  ={
     allQuestions : function() {
        return state.questions;
    },
    allQuestionsIds : function() {
        var ids = state.questions.map(question => question.id)
        return ids
    }
}

const actions = {
    async fetchQuestions({commit}){
        var url= window.url
        const response =  await axios.get(`${url}/questions`)
        commit('setQuestions',response.data.data)
    },



}


const mutations ={
    setQuestions :(state,questions) =>(state.questions = questions),     
}

export default{
    state,
    getters,
    actions,
    mutations,

}
