<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Categories</h2>

            <div class="page-action">
                <button class="btn btn-main" @click="$router.push('/category/add')"><span class="ti-plus"></span> Add
                    category</button>
            </div>


            <section class="recent">
                <div class="">
                    <div class="activity-card">
                        <h3>Added Categories</h3>

                        <div class="table-responsive">
                            <table class="p-5">
                                <thead>
                                    <tr>
                                        <th>S.no</th>
                                        <th>Category Id</th>

                                        <th class="text-center">Icons</th>
                                        <th>Name</th>
                                        <th>Question</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>

                                    <tr v-for="(category, index) in allCategories" :key="index">
                                        <td>#{{index + 1}}</td>
                                        <td>
                                            <p>{{category.id}} </p>
                                        </td>
                                        <th><img :src="category.icon_url" class="img-fluid img-responsive"
                                                style="height:100px"></th>
                                        <td>
                                            <p>{{category.name.english}} | {{category.name.hindi}}</p>
                                        </td>

                                        <td>
                                            <v-row justify="center">
                                                <v-dialog v-model="dialog[index]" v-if="category.questions.length >0"
                                                    persistent max-width="1200px">
                                                    <template v-slot:activator="{ on, attrs }">
                                                        <v-btn color="primary" dark v-bind="attrs" v-on="on"
                                                            @click="getQuestion(category.questions)">
                                                            Show Question
                                                        </v-btn>
                                                    </template>
                                                    <v-card>
                                                        <v-card-title>
                                                            <span class="headline">Question List</span>
                                                        </v-card-title>

                                                        <v-simple-table>
                                                            <template v-slot:default>
                                                                <thead>
                                                                    <tr>
                                                                        <th class="text-left">
                                                                            id
                                                                        </th>
                                                                        <th class="text-left">
                                                                            Question text
                                                                        </th>
                                                                        <th class="text-left">
                                                                            IsMandatory
                                                                        </th>
                                                                        <th class="text-left">
                                                                            Answer
                                                                        </th>

                                                                         <th class="text-left">
                                                                            View Question
                                                                        </th>

                                                                    </tr>
                                                                </thead>
                                <tbody>
                                    <tr class="text-center" v-if="modal_questions.length == 0">
                                        <td>
                                            <v-text-field color="success" loading disabled></v-text-field>
                                        </td>
                                    </tr>
                                    <tr v-for="item in modal_questions" :key="item.id" else>
                                        <td>{{ item.id }}</td>
                                        <td>{{ item.text.english }} <b>|</b>{{ item.text.hindi }}</td>
                                        <td>{{ item.isMandatory }}</td>
                                        <td>
                                            <span v-for="(answer,i) in item.answers " :key="i">
                                                {{answer.text.english}}<b>, </b>
                                            </span>
                                        </td>
                                        <td>
                                            <router-link :to="`/question/show/${item.id}`">
                                            <v-btn small dark color="red">View</v-btn>
                                            </router-link>
                                        </td>
                                    </tr>
                                </tbody>
</template>
</v-simple-table>


<v-card-actions>
    <v-spacer></v-spacer>
    <v-btn color="blue darken-1" text @click="dialogOff()">
        Close
    </v-btn>

</v-card-actions>
</v-card>
</v-dialog>
</v-row>
</td>
<td>
    <router-link :to="`/category/show/${category.id}`">
        <v-btn color="primary" class="mr-2">
            View
        </v-btn>
    </router-link>
    <button class="btn btn-main-gradient" v-on:click="deleteCategory(category.id)">
        <i class="fa fa-trash-o" aria-hidden="true"></i></button>
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
        name: 'SuperIndex',
        components: {
            DashboardLayout,
        },
        data() {
            return {
                categories: [],
                dialog: [],
                modal_questions: []
            }
        },
        mounted() {
            this.$store.dispatch('fetchCategories')

        },
        methods: {
            dialogOff() {

                this.dialog = []
                this.modal_questions = []
            },
            getQuestion(arr) {

                axios.post(`${window.url}/api/question/modal`, {
                        'questions': arr
                    })
                    .then(result => {
                        this.modal_questions = result.data
                        console.log(result)
                    })
                //console.log(arr)
            },
            deleteCategory(id) {
                this.$swal.fire({
                    title: '<p>Do you really want to delete?</p>',
                    showDenyButton: true,
                    confirmButtonText: `Yes`,
                    denyButtonText: `No`,
                }).then((result) => {
                    if (result.isConfirmed) {

                        axios.delete(`${window.url}/categories`, {
                                data: {
                                    id: id
                                }
                            })
                            .then(res => {
                                this.$swal.fire({
                                    icon: 'error',
                                    title: 'Deleted',
                                    text: res.data.message,
                                })
                                this.$store.dispatch('fetchCategories')

                            })

                    }
                })
            }
        },
        computed: mapGetters(['allCategories']),
    }
</script>