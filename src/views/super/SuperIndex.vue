<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Super Category</h2>

            <div class="page-action">
                <button class="btn btn-main" @click="$router.push('/super/add')"><span class="ti-plus"></span> Add super
                    category</button>
            </div>


            <section class="recent">
                <div class="">
                    <div class="activity-card">
                        <h3>Added Super Category</h3>

                        <div class="table-responsive">
                            <table>
                                <thead>
                                    <tr>
                                        <th>S.no</th>
                                        <th>Question</th>
                                        <th>Default view count</th>

                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(super_category, index) in allSuper" :key="index">
                                        <td class="text-left">#{{index + 1}}</td>
                                        <td>
                                            <p>{{super_category.name.english}} | {{super_category.name.hindi}}</p>
                                        </td>
                                        <td> {{super_category.default_view_count}}</td>
                                        <td>
                                            <v-btn color="primary" class="mr-2">
                                                View
                                            </v-btn>
                                            <button class="btn btn-main-gradient"><i class="fa fa-trash-o"
                                                    aria-hidden="true"></i></button>
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
            this.$store.dispatch('fetchSuper')
        },
        methods: {

        },
        computed: mapGetters(['allSuper']),
    }
</script>