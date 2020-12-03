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
                                        <th>Request Id</th>


                                        <th>Category id</th>
                                        <th>User ID</th>
                                        <th>New_interest_count</th>
                                        <th>Is_completed</th>
                                        <th>Share_mobile </th>

                                        <th>Complaints count</th>

                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(request, index) in getRequests.results" :key="index">
                                        <td class="text-left">#{{index + 1}}</td>
                                        <td>
                                            {{request.id}}
                                        </td>
                                        <td> {{request.category_id}}</td>
                                        <td>
                                            <v-btn color="primary" small>{{request.user_id}}</v-btn>
                                        </td>
                                        <td> {{request.new_interest_count}}</td>
                                        <td> {{request.is_completed}}</td>

                                        <td> {{request.share_mobile}}</td>
                                        <td> {{request.complaints_count}}</td>



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
                links: {}
            }
        },
        mounted() {
            this.$store.dispatch('fetchRequests')
            this.links.next = this.$store.state.Global.requests.next
            this.links.prev = this.$store.state.Global.requests.previous



        },
        methods: {
            deleteSuperCategory() {

            }
        },
        computed: mapGetters(['getRequests']),
    }
</script>