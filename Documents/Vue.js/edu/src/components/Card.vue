<template>
    <div>
          <!-- Session Card Section -->
        <div class="Session-section section bg-dark">
            <div class="session-section-head">
                Live Sessions.. 
              
            </div>
            <div class="container-fluid">
                <div class="">
<div class="row">
    <div class="col-lg-3" v-for="(course,index) in courses" v-bind:key="course.id"  >

                    <div class="session-card  p-3" >               
                        <div class="" style="margin:10px" >
                            <div class="card-front">
                                <div class="" style="color:#fff !impotant">
                                    <h2 class="" :style="`background:${background[index % background.length]}`"> {{course.courseName}}</h2>
                                    <div class="line"></div>
                                </div>
                                <div class="training">{{index}}By Sumit Training Services </div>
                                <p><strike>$19.99</strike> <span class="price">$10</span></p>


                                <p class="timings-title"> Start Date:<span class="timings">20/04/2020 </span> </p>

                                <p class="timings-title"> Timings:<span class="timings">3 PM(1 hour) </span> </p>
                                <p class="session-summary">
                                  {{course.summary}}
                                    </p>
                                  <h3>  {{course.rating}}</h3>
                                <div class="session-ratings">

                                    <span v-for="(i,index) in course.rating" :key="index"  class="fa fa-star checked"></span>
                                   
                                   </div>
                                <p>
                                <button class="btn btn-primary btn-sm"
                                 @click="addcart(course._id)">
                                    Add to Cart
                                    
                                    </button></p>
                            </div>

                            <div class="card_back">
                                view details
                            </div>

                        </div>
                    </div>
    </div>
</div>

                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from "axios"
 import {
    mapGetters,
    mapActions
  } from 'vuex';
export default {
    name: 'Card',
    computed: mapGetters([
      'courses'

    ]),
    data(){
        return{
            background : ['#c3a9ff', '#54bcc9', '#de8ad8', '#99ddb6', '#FF5733', '#2B9A4F'],

        }
    },

    created() {
      this.fetchCourses()
    
    },

    methods: {
      ...mapActions(['fetchCourses']),
      index() {
       
      },
      addcart(id){
          console.log(id)
          axios.post('https://cors-anywhere.herokuapp.com/https://boiling-garden-13643.herokuapp.com/cart/Addcart/', {courseId : id},{
                headers: {
               authorization:  localStorage.getItem('token')
               }
             }).then( response => {
                 console.log(response.data)
             }).catch( err => {
                 console.log(err)
             })
      }
    },
}
</script>