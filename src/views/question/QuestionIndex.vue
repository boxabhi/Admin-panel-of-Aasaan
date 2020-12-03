<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Questions</h2>

            <div class="page-action">
                <button class="btn btn-main" @click="$router.push('/question/add')"><span class="ti-plus"></span> Add
                    question</button>
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
                                        <th>Question id</th>

                                        <th class="">Question</th>
                                        <th class="">Question type</th>
                                        <th>IsMandatory</th>
                                        <th>Answers</th>

                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(question, index) in allQuestions" :key="index">
                                        <td class="text-left">#{{index + 1}}</td>
                                        <td>
                                            <p>{{question.id}} </p>

                                        <td>
                                            <p>{{question.text.english}} </p>
                                            <p>{{question.text.hindi}}</p>
                                        </td>
                                        <td>
                                            <p>{{question.question_type}}</p>
                                        </td>
                                        <td>
                                            <v-btn color="green" dark small v-if="question.isMandatory">
                                                {{question.isMandatory}}
                                            </v-btn>
                                            <v-btn color="red" dark small v-else>
                                                {{question.isMandatory}}
                                            </v-btn>
                                        </td>
                                        <td>
                                            <span v-for="(answer,i) in question.answers " :key="i">
                                                {{answer.text.english}}<b>, </b>
                                            </span>
                                        </td>
                                        <td>
                                            <router-link :to="`question/show/${question.id}`">
                                            <v-btn color="primary" small class="mr-2">
                                                View
                                            </v-btn>
                                            </router-link>
                                            <button class="btn btn-main-gradient btn-sm"
                                                v-on:click="deleteQuestion(question.id)">
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
    import axios from 'axios'
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
            deleteQuestion(id) {
                this.$swal.fire({
                    title: '<p>Do you really want to delete?</p>',
                    showDenyButton: true,
                    confirmButtonText: `Yes`,
                    denyButtonText: `No`,
                }).then((result) => {
                    if (result.isConfirmed) {
                        var data = {
                            'id': id
                        }
                        console.log(data)
                        axios.delete(`${window.url}/questions`, {
                                data: {
                                    question_id: id
                                }
                            })
                            .then(res => {
                                this.$swal.fire({
                                    icon: 'error',
                                    title: 'Deleted',
                                    text: res.data.message,
                                })
                                this.$store.dispatch('fetchQuestions')

                            })

                    }
                })
            }
        },
        computed: mapGetters(['allQuestions']),
    }
</script>