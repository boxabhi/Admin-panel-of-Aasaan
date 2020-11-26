<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Categories</h2>
                    
            <div class="page-action">
                <button class="btn btn-main" @click="$router.push('/category/add')"><span class="ti-plus"></span> Add category</button>
            </div>
            
            
            <section class="recent">
                <div class="">
                    <div class="activity-card">
                        <h3>Added  Categories</h3>
                        
                        <div class="table-responsive">
                            <table class="p-5">
                                <thead >
                                    <tr>
                                        <th>S.no</th>
                                        <th class="text-center">Icons</th>
                                        <th>name</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                               
                                    <tr v-for="(category, index) in allCategories" :key="index" >
                                        <td >#{{index + 1}}</td>
                                        <th><img :src="category.icon_url" class="img-fluid img-responsive" style="height:100px"></th>
                                        <td><p>{{category.name.english}} | {{category.name.hindi}}</p>
                                        </td>
                                        <td>
                                            <v-btn color="primary"  class="mr-2">
                                                View
                                            </v-btn>
                                            <button class="btn btn-main-gradient" ><i class="fa fa-trash-o" aria-hidden="true"></i></button>
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
    name: 'SuperIndex',
    components: {
        DashboardLayout,
    },
    data() {
        return {
            categories: [],
        }
    },
    mounted() {
       this.$store.dispatch('fetchCategories')
    },
    methods: {
       
    },
     computed: mapGetters(['allCategories' ]),
}
</script>