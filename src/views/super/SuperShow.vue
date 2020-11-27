<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Super Category <span class="green--text">{{category.name.english}}</span></h2>
            <form v-on:submit.prevent="addCategory">
                <section class="recent">
                    <div class="">
                        <div class="activity-card pad-1">
                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">Super Category name in English</label>
                                    <div>
                                        <input type="text" required v-model="category.name.english" class="form-control"
                                            placeholder="Write category in english ">
                                    </div>
                                </div>
                                <div class="form-group col-md-6">
                                    <label for="">Super Category name in Hindi</label>

                                    <input type="text" required v-model="category.name.hindi" class="form-control"
                                        placeholder="Write category in hindi ">
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="formGroupExampleInput">Default View Count</label>
                                <input type="text" class="form-control" required v-model="category.default_view_count"
                                    id="formGroupExampleInput" placeholder="Default view count">
                            </div>

                            <v-select v-model="categories" :items="category.categories" selected attach chips 
                                label="Select Category" multiple></v-select>
                            <div class="form-group">
                                <button type="submit" class="btn btn-main">Submit</button>
                            </div>
                        </div>
                    </div>
                </section>
            </form>
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
                name: '',
                categories: [],
                category : [],
                items: ['foo', 'bar', 'fizz', 'buzz'],
                data: {
                    name: {
                        english: '',
                        hindi: ''
                    },
                    default_view_count: 5
                }
            }
        },
        methods: {
            addCategory() {
                var payload = this.data
                var categories = this.categories.map((category) =>{
                    var cat = JSON.parse(category) 
                    return cat.id
                })
                payload.categories = categories
                console.log(payload)
                var result = []
                result.push(payload)
                axios.post(`${window.url}/super`, result)
                    .then(res => {
                        console.log(res)
                         this.$swal.fire({
                            icon: 'success',
                            title: 'Success',
                            text: 'Super Category Added',
                })})
            this.data = {name: {english: '',hindi: ''},default_view_count: 5}
            this.categories = []
            },
           async getSuperCategory(){
               await axios.get(`${window.url}/super?id=${this.$route.params.id}`)
                .then(res =>{ 
                    this.category = res.data
                })
            }
        },
        mounted() {
             this.getSuperCategory()
        },
        computed: mapGetters(['allCategories', 'allCategoriesName']),

    }
</script>

<style lang="css">
    .pad-1 {
        padding: 1rem
    }
</style>