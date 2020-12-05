<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Change Admin password</h2>
            <section class="recent">
                <form v-on:submit.prevent="updateUser">
                    <div class="">
                        <div class="activity-card pad-1">
                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">User Name</label>
                                    <div>
                                        <input type="text" v-model="data.name" required class="form-control"
                                            placeholder="User name ">
                                    </div>
                                </div>

                                <div class="form-group col-md-6">
                                    <label for="">User mobile</label>
                                    <div>
                                        <input type="text" v-model="data.mobile"  class="form-control"
                                            placeholder="User mobile ">
                                    </div>
                                </div>
                            </div>



                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">User Email</label>
                                    <input type="text" v-model="data.email"  class="form-control"
                                        placeholder="User email ">
                                </div>
                                <div class="form-group col-md-6">
                                    <label for="">User pic_url</label>
                                    <div>
                                        <input type="text"  class="form-control"
                                            placeholder="User user_type ">
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">User language</label>
                                    <div>
                                        <input type="text" v-model="data.language"  class="form-control"
                                            placeholder="User language ">
                                    </div>
                                </div>

                                <div class="form-group col-md-6">
                                    <label for="">User provider_info</label>
                                    <div>
                                        <input type="text" v-model="data.provider_info"  class="form-control"
                                            placeholder="User provider_info ">
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">User user_type</label>
                                    <input type="text" v-model="data.user_type"  class="form-control"
                                        placeholder="User user_type ">
                                </div>
                                <div class="form-group col-md-6">
                                    <label for="">User pic_url</label>
                                    <div>
                                        <input type="text" v-model="data.pic_url"  class="form-control"
                                            placeholder="User user_type ">
                                    </div>
                                </div>
                            </div>


                            <div class="row">
                                <div class="form-group col-md-6">
                                    <label for="">User user_verified</label>
                                    <div>
                                        <input type="text" v-model="data.user_verified" readonly 
                                            class="form-control" placeholder="User language ">
                                    </div>
                                </div>
                                <div class="form-group col-md-6">
                                    <label for="">User rating</label>
                                    <div>
                                        <input type="text" v-model="data.rating" readonly  class="form-control"
                                            placeholder="User rating ">
                                    </div>
                                </div>


                            </div>

                            <div class="">

                                <v-chip class="ma-2" label small v-for="d in data.my_requests" :key="d" color="primary">
                                    {{d}}
                                </v-chip>

                            </div>
                            <div class="form-group">
                                <button type="submit" class="btn btn-main">Submit</button>
                            </div>
                        </div>
                    </div>
                </form>

            </section>
        </div>
    </dashboard-layout>

</template>

<script>
    import DashboardLayout from '@/components/Layouts/DashboardLayout'
    import axios from 'axios'
    export default {
        name: 'Password',
        components: {
            DashboardLayout,
        },
        data() {
            return {
                data: {}

            }
        },
        methods: {
            async getUser() {
                await axios.get(`${window.url}/api/admin/users?id=${this.$route.params.id}`)
                    .then(res => {
                        this.data = res.data
                    })
            },

           async updateUser (){
               console.log(this.data)
            await axios.put(`${window.url}/api/admin/users`, this.data)
            .then(res => {
                console.log(res.data)
            })
            }
        },
        mounted() {
            this.getUser()
        }
    }
</script>

<style lang="css">
    .pad-1 {
        padding: 1rem
    }
</style>