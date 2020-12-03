<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Create new Admin for Aasaan</h2>
            <section class="recent">
                <form v-on:submit.prevent="handleSubmit">
                    <div class="">
                        <div class="activity-card pad-1">
                            <div class="form-group">
                                <label for="">Username for admin</label>
                                <div>
                                    <input type="password" required v-model="admin.username" class="form-control"
                                        placeholder="Username for new admin">
                                </div>
                            </div>
                            <div class="form-group mt-5">
                                <label for="">Admin  Password</label>

                                <div class="">
                                    <input type="password" required v-model="admin.new_password" class="form-control"
                                        placeholder="Password ">
                                </div>
                            </div>
                            <div class="form-group mt-5">
                                <label for="">Confirm  Password</label>

                                <div class="">
                                    <input type="password" required v-model="admin.confirm_password"
                                        class="form-control" placeholder="Confirm Password">
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
                admin: {
                    new_password: '',
                    confirm_password: '',
                    username: '',
                }

            }
        },
        methods: {
           async handleSubmit() {
               if(this.admin.new_password != this.admin.confirm_password){
                   this.$swal.fire({
                            icon: 'error',
                            title: 'Password',
                            text: 'Password must be same'
                        })
                        return;
               }
                var url= window.url
                var token = JSON.parse(localStorage.getItem('admin'))
                axios.post(`${url}/api/admin`,this.admin , {
                    headers: {
                        'Authorization': `Bearer ${token.access} `
                    },
                   
                }).then(res =>{ 
                    if(res.data.status){
                    this.$swal.fire({
                            icon: 'success',
                            title: 'Success...',
                            text: res.data.message
                        })
                    this.admin = {new_password: '',confirm_password: '',username: '',}
                    }else{
                         this.$swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: res.data.message
                        })
                         this.password = {new_password: '',confirm_password: '',username: '',}
                    }
                })
            }
        },
        mounted() {

        }
    }
</script>

<style lang="css">
    .pad-1 {
        padding: 1rem
    }
</style>