<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Add Category</h2>
            <section class="recent">
                <div class="">
                    <div class="activity-card pad-1">
                        <div class="row">
                            <div class="form-group col-md-6">

                                <label for="">Category name in english</label>
                                <div>
                                    <input type="text" v-model="category.name.english" class="form-control"
                                        placeholder="Write category in english ">
                                </div>

                            </div>
                            <div class="form-group col-md-6">
                                <label for="">Category name in hindi</label>

                                <input type="text" v-model="category.name.hindi" class="form-control "
                                    placeholder="Write category in hindi ">

                            </div>
                        </div>


                        <div class="form-group">
                            <label for="formGroupExampleInput">Image url</label>
                            <input type="text" class="form-control" v-model="category.icon_url"
                                id="formGroupExampleInput" placeholder="Image URL">
                        </div>

                       
                        <v-autocomplete :items="allQuestionsIds"   chips label="Select Category"
                            multiple v-model="category.questions" deletable-chips  >
                        </v-autocomplete>

                        <div class="form-group">
                            <button @click="addCategory" class="btn btn-main">Submit</button>
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
        name: 'AddCategory',
        components: {
            DashboardLayout,
        },
        data() {
            return {
                name: '',
                questions: [],
                category: {
                    name: {
                        english: '',
                        hindi: ''
                    },
                    icon_url: '',
                    questions: []
                }
            }
        },
        methods: {
            addCategory() {
                var payload = []
                payload.push(this.category)
                console.log(payload)
                axios.post(`${window.url}/categories`, payload)
                    .then(res => {
                        this.$swal.fire({
                            icon: 'success',
                            title: 'Success...',
                            text: res.data.message,
                        })

                        this.category = {
                            name: {
                                english: '',
                                hindi: ''
                            },
                            icon_url: '',
                            questions: []
                        }
                    })

            }
        },
        mounted() {
            this.$store.dispatch('fetchQuestions')
        },
        computed: mapGetters(['allQuestions', 'allQuestionsIds']),

    }
</script>

<style lang="css">
    .pad-1 {
        padding: 1rem
    }
</style>