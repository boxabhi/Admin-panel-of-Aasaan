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
                                            <router-link :to="`/super/show/${super_category.id}`">
                                            <a href="">
                                            <v-btn color="primary" class="mr-2">
                                                View
                                            </v-btn>
                                            </a>
                                            </router-link>
                                            <button class="btn btn-main-gradient"
                                                v-on:click="deleteSuperCategory(super_category.id)">
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
            }
        },
        mounted() {
            this.$store.dispatch('fetchSuper')
        },
        methods: {
            deleteSuperCategory(id) {
                this.$swal.fire({
                    title: '<p>Do you really want to delete?</p>',
                    showDenyButton: true,
                    confirmButtonText: `Yes`,
                    denyButtonText: `No`,
                }).then((result) => {
                    if (result.isConfirmed) {
                        var data = {'id': id}
                        console.log(data)
                        axios.delete(`${window.url}/super`, {data: {id: id}})
                        .then(res => { console.log(res) })
                        this.$swal.fire({ icon: 'error', title: 'Deleted',text: 'Super category deleted',})
                        this.$store.dispatch('fetchSuper')

                    }
                })
            }
        },
        computed: mapGetters(['allSuper']),
    }
</script>