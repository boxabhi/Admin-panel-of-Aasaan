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
                                    <input type="text" v-model="name" class="form-control"
                                        placeholder="Write category in english ">
                                </div>

                            </div>
                            <div class="form-group col-md-6">
                                <label for="">Category name in hindi</label>

                                <input type="text" v-model="name" class="form-control "
                                    placeholder="Write category in hindi ">

                            </div>
                        </div>

                        <div class="form-group">
                            <label for="formGroupExampleInput">Default View Count</label>
                            <input type="text" class="form-control" value="5" id="formGroupExampleInput"
                                placeholder="Default view count">
                        </div>

                        <v-file-input accept="image/*" label="Upload Catgeory image"></v-file-input>

                        <v-select v-model="value" :items="allCategoriesName" attach chips label="Select Category"
                            multiple></v-select>

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

    export default {
        name: 'AddCategory',
        components: {
            DashboardLayout,
        },
        data() {
            return {
                name: '',
                categories: [],
                items: ['foo', 'bar', 'fizz', 'buzz'],
            }
        },
        methods: {
            addCategory() {
                if (!this.name) {
                    return this.$alertify.error('Incomplete form data')
                }

                this.$axios.post(`${this.$apiUrl}/categories/add`, {
                        name: this.name
                    }, {
                        headers: {
                            Authorization: `Bearer ${localStorage.authtoken}`
                        }
                    })
                    .then(() => {
                        this.$router.push('/admin/categories')
                    })
                    .catch(error => {
                        if (error.response.data.message) {
                            return this.$alertify.error(error.response.data.message)
                        }
                        this.$alertify.error(Object.values(error.response.data)[0][0])
                    })
            }
        },
        mounted() {
            this.$store.dispatch('fetchCategories')
        },
        computed: mapGetters(['allCategories', 'allCategoriesName']),

    }
</script>

<style lang="css">
    .pad-1 {
        padding: 1rem
    }
</style>