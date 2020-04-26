import axios from 'axios';

const state = {
    courses : [],

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
    async fetchCourses({commit}){
        const response = await axios.get('https://cors-anywhere.herokuapp.com/https://boiling-garden-13643.herokuapp.com/course/courseDetails');
       
        commit('setCourses',response.data)
    },
    
}


const mutations ={
        setCourses :(state,courses) =>(state.courses = courses),

}

export default{
    state,
    getters,
    actions,
    mutations,
}
