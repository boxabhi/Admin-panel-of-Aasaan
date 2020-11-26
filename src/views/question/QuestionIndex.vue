<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Questions</h2>
                    
            <div class="page-action">
                <button class="btn btn-main" @click="$router.push('/question/add')"><span class="ti-plus"></span> Add question</button>
            </div>
            
            
            <section class="recent">
                <div class="">
                    <div class="activity-card">
                        <h3>Added questions</h3>
                        
                        <div class="table-responsive">
                            <table>
                                <thead>
                                    <tr>
                                        <th>S.no</th>
                                        <th class="">Question</th>
                                        <th class="">Question type</th>
                                        <th>IsMandatory</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(question, index) in allQuestions" :key="index" >
                                        <td class="text-left">#{{index + 1}}</td>
                                        <td><p>{{question.text.english}} | {{question.text.hindi}}</p>
                                        <p>{{question.text.hindi}}</p></td>
                                        <td><p>{{question.question_type}}</p></td>
                                        <td>
                                            <v-btn color="green" dark small v-if="question.isMandatory">
                                                {{question.isMandatory}}
                                            </v-btn>
                                             <v-btn color="red" dark small v-else>
                                                {{question.isMandatory}}
                                            </v-btn>
                                        </td>
                                        <td>
                                            <v-btn color="primary"  class="mr-2">
                                                View
                                            </v-btn>
                                            <button class="btn btn-main-gradient" >
                                                <i class="fa fa-trash-o" aria-hidden="true"></i>
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </dashboard-layout>
</template>

<script>
import DashboardLayout from '@/components/Layouts/DashboardLayout'
 import {
    mapGetters
  } from 'vuex';

export default {
    name: 'Categories',
    components: {
        DashboardLayout,
    },
    data() {
        return {
            categories: [],
        }
    },
    mounted() {
       this.$store.dispatch('fetchQuestions')
    },
    methods: {
       
    },
     computed: mapGetters(['allQuestions' ]),
}
</script>