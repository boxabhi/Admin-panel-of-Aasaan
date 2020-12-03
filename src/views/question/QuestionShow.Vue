<template>
  <dashboard-layout>
    <div slot="main-content">
      {{question}}
      <h2 class="dash-title"> Question <span class="green--text">{{question.text.english}}</span> </h2>
      <section class="recent">
        <form v-on:submit.prevent="UpdateQuestion">
          <div class="">
            <div class="activity-card pad-1">
              <div class="form-group">
                <label for="exampleFormControlSelect1">Question type</label>
                <select required class="form-control" v-model="question.question_type" id="exampleFormControlSelect1">
                  <option value="select-one">Select one</option>
                  <option value="select-many">Select many</option>

                </select>
              </div>
              <div class="row">

                <div class="form-group col-md-6">
                  <label for="">Question in english</label>
                  <input required type="text" v-model="question.text.english" class="form-control"
                    placeholder="Write question in english ">
                </div>
                <div class="form-group col-md-6">
                  <label for="">Question in hindi</label>
                  <input required type="text" v-model="question.text.hindi" class="form-control"
                    placeholder="Write question in hindi ">
                </div>
              </div>
              <div class="row">
                <div class="form-group col-md-6">
                  <v-switch label="Is manadatory" v-model="question.isMandatory"></v-switch>
                </div>
                <div class="form-group col-md-6">
                  <v-btn depressed color="primary" v-on:click="addAnswers()">
                    Add Answers <v-icon class="ml-3" dark>
                      mdi-plus
                    </v-icon>
                  </v-btn>
                </div>
              </div>
              <div v-for="(answer,index) in answers" :key="index">
                <hr>
                <div class="mt-2 pt-4">
                  <b>Answer {{index + 1}}</b>
                </div>
                <div class="row mt-2 ">

                  <div class="form-group col-md-4">
                    <label for="">Answer in english</label>
                    <input type="text" required v-model="answers[index].text.english" class="form-control"
                      placeholder="Write Answer in english ">
                  </div>
                  <div class="form-group col-md-4">
                    <label for="">Answer in hindi</label>
                    <input type="text" required v-model="answers[index].text.hindi" class="form-control"
                      placeholder="Write Answer in hindi ">
                  </div>
                
          
                  <div class="form-group col-md-4">
                    <label for="">Select question</label>
                    <input type="text"  v-model="question.answers[index].questions" class="form-control"
                      placeholder="Write Answer in hindi ">
      
                  </div>
                </div>
                <div class="form-group">
                  <v-btn @click="removeAnswer(i)" color="red" class="btn btn-main">
                    <i class="fa fa-trash"></i>
                  </v-btn>
                </div>
              </div>
              <div class="form-group mt-5 pt-5">
                <button @click="updateQuestion()" class="btn btn-main">Submit</button>
              </div>
            </div>
          </div>
        </form>
      </section>

    </div>
  </dashboard-layout>
</template>

<script>
  import DashboardLayout from '@/components/Layouts/DashboardLayout'
  import { mapGetters } from 'vuex';
  import axios from 'axios'
  export default { 
    name: 'ShowQuestion', components: { DashboardLayout},
    data() {
      return {
        question_type: null,
        text: { english: '', hindi: ''},
        isMandatory: false,
        question: [],
        questions: [],
        answers: []
      }
    },
    methods: {
        getQuestion(){
            var id = this.$route.params
            axios.get(`${window.url}/questions?id=${id.id}`)
            .then(response =>{
                this.question = response.data
                this.answers = response.data.answers
            })
        },
      updateQuestion() {
        var payload = this.question
        for(var i = 0; i < payload.answers.length;i++){
          var ques = payload.answers[i].questions
          console.log(ques)
          if(Array.isArray(ques)){
            console.log("array")
          }
          if(ques.length > 0 )
          payload.answers[i].questions = ques.split(',')
        
        }
         axios.put(`${window.url}/questions`, payload)
          .then(res => {
            this.$swal.fire({
                            icon: 'success',
                            title: 'Success...',
                            text: res.data.message,
                        })
          })
      },
    
    },
    computed: mapGetters(['allQuestions']),
    mounted() {
        this.getQuestion()
    }
  }
</script>

<style lang="css">
  .pad-1 {
    padding: 1rem
  }
</style>