<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Create new Admin for Aasaan</h2>
            {{data}}
            <section class="recent">
                <form v-on:submit.prevent="handleSubmit">
                    <div class="">
                        <div class="activity-card pad-1">
                            <div class="row">
                            <div class="form-group col-md-6">
                                <label for="">Category ID</label>
                                <div>
                                    <input type="text" required v-model="data.category_id" class="form-control"
                                        placeholder="Username for new admin">
                                </div>
                            </div>
                          
                            <div class="form-group col-md-6">
                                <label for="">User id</label>

                                <div class="">
                                    <input type="text" required v-model="data.user_id" class="form-control"
                                        placeholder="User ID ">
                                </div>
                            </div>
                              </div>

                                <div class="row">
                            <div class="form-group col-md-6">
                                <label for="">Complaints_count</label>
                                <div>
                                    <input type="text" required v-model="data.complaints_count" class="form-control"
                                        placeholder="Is_completed">
                                </div>
                            </div>
                          
                            <div class="form-group col-md-6">
                                <label for="">Share_mobile</label>

                                <div class="">
                                    <input type="text" required v-model="data.share_mobile" class="form-control"
                                        placeholder="User ID ">
                                </div>
                            </div>
                              </div>

                               <div class="row">
                            <div class="form-group col-md-6">
                                <label for="">Is completed</label>
                                <div>
                                    <input type="text" required v-model="data.is_completed" class="form-control"
                                        placeholder="Is_completed">
                                </div>
                            </div>
                          
                            <div class="form-group col-md-6">
                                <label for="">New Interest Count</label>

                                <div class="">
                                    <input type="text" required v-model="data.new_interest_count" class="form-control"
                                        placeholder="User ID ">
                                </div>
                            </div>
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
                data : {},
                admin: {
                    new_password: '',
                    confirm_password: '',
                    username: '',
                }

            }
        },
        methods: {
           getRequests(){
               axios.get(`${window.url}/api/admin/requests?id=${this.$route.params.id}`)
               .then(response =>{
                   this.data = response.data
               })
           },
           handleSubmit(){
               axios.put(`${window.url}/api/admin/requests`, this.data)
               .then(response =>{
                     this.$swal.fire({
                            icon: 'success',
                            title: 'Hurray',
                            text: response.data.message,
                        })
                        
               })
           }
        },
        mounted() {
            this.getRequests()
        }
    }
</script>

<style lang="css">
    .pad-1 {
        padding: 1rem
    }
</style>