<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">All Users of Aasaan</h2>

            


            <section class="recent">
                <div class="">
                    <div class="activity-card">

                        <div class="table-responsive">
                            <table>
                                <thead>
                                    <tr>
                                        <th>S.no</th>
                                        <th>User Id</th>

                                        
                                        <th>Name</th>
                                        <th>User type</th>
                                        <th>Language</th>
                                        <th>Email</th>
                                        <th>Pic </th>
                                        <th>User_verified</th>
                                        <th>Complaints count</th>

                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(user, index) in allUsers" :key="index">
                                        <td class="text-left">#{{index + 1}}</td>
                                        <td>
                                          {{user.id}}
                                        </td>
                                        <td> {{user.name}}</td>
                                        <td> <v-btn color="primary" small>{{user.user_type}}</v-btn></td>
                                        <td> {{user.language}}</td>
                                        <td> {{user.email}}</td>
                                        <td> <img :src="user.pic_url"  class="img-responsive" style="height:50px"></td>
                                        <td> {{user.user_verified}}</td>
                                        <td> {{user.complaints_count}}</td>



                                        <td>
                                            <router-link :to="`user/show/${user.id}`">
                                        <v-btn color="red" small dark>View</v-btn>
                                            </router-link>
                                            
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
            this.$store.dispatch('fetchUsers')
        },
        methods: {
            deleteSuperCategory() {
                
            }
        },
        computed: mapGetters(['allUsers']),
    }
</script>