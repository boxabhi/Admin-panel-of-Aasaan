<template>
  <dashboard-layout>
    <div slot="main-content">
      <h2 class="dash-title">Add Question</h2>
      <section class="recent">

        <form v-on:submit.prevent="addQuestion">


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
                    <select class="form-control" required>
                      <option :value="question.id" v-for="(question,i) in allQuestions" :data-id="i"
                        :selected="i == 0 ? '' :'selected' " :key="question.id">{{question.text.english}}</option>
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <v-btn @click="removeAnswer(i)" color="red" class="btn btn-main">
                    <i class="fa fa-trash"></i>
                  </v-btn>
                </div>
              </div>
              <div class="form-group mt-5 pt-5">
                <button @click="addQuestion()" class="btn btn-main">Submit</button>
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
  import axios from 'axios'
  import {
    mapGetters
  } from 'vuex';
  export default {
    name: 'AddCategory',
    components: {
      DashboardLayout,
    },
    data() {
      return {
        question_type: null,
        text: {
          english: '',
          hindi: ''
        },
        isMandatory: false,
        question: {
          question_type: '',
          text: {
            english: '',
            hindi: ''
          },
          isMandatory: false
        },
        questions: [],
        answers: []
      }
    },
    methods: {
      setQuestion(e) {
        //    var index = e.target.getAttribute('data-id')
        console.log(e.target.value)
        //      this.answers[index].questions.push(e.target.value)

      },
      addAnswers() {
        this.answers.push({
          text: {
            english: '',
            hindi: ''
          },
          questions: []
        })
      },
      removeAnswer(index) {
        this.answers.splice(index, 1)
      },
      addQuestion() {
        var payload = this.question
        payload.answers = this.answers

        var result = []
        result.push(payload)
        console.log(result)
        axios.post(`${window.url}/questions`, result)
          .then(res => {
            this.$swal.fire({
              icon: 'success',
              title: 'Success...',
              text: res.data.message,
            })

             this.answers = []
        this.question = {
          question_type: '',
          text: {
            english: '',
            hindi: ''
          }
      }
          })
       
      }

    },
    computed: mapGetters(['allQuestions']),
    mounted() {
      this.$store.dispatch('fetchQuestions')
    },
  }
</script>

<style lang="css">
  .pad-1 {
    padding: 1rem
  }
</style>