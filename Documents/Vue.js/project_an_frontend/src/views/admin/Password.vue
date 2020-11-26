<template>
    <dashboard-layout>
        <div slot="main-content">
            <h2 class="dash-title">Change Admin password</h2>
            <section class="recent">
                <form  v-on:submit.prevent="handleSubmit" >
                <div class="">
                    <div class="activity-card pad-1">
                        <div class="form-group">
                            <label for="">Your old Password</label>
                            <div>
                                <input type="password" required v-model="password.old_password" class="form-control"
                                    placeholder="Your old Password ">
                            </div>
                        </div>
                        <div class="form-group mt-5">
                            <label for="">Your new Password</label>

                            <div class="" >
                                <input type="password" required v-model="password.new_password" class="form-control"
                                    placeholder="Your new Password ">
                            </div>
                        </div>
                             <div class="form-group mt-5">
                            <label for="">Confirm new Password</label>

                            <div class="" >
                                <input type="password" required v-model="password.confirm_password" class="form-control"
                                    placeholder="Confirm new Password">
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
 
    export default {
        name: 'Password',
        components: {
            DashboardLayout,
        },
        data() {
            return {
                password : {
                    old_password : '',
                    new_password : '',
                    confirm_password : '',
                }
            }
        },
        methods: {
                handleSubmit(){
                        if(this.password.new_password != this.password.confirm_password){
                                this.$swal('Password not matched');
                        }
                }
        },
        mounted(){
                              
        }
    }
</script>

<style lang="css">
    .pad-1 {
        padding: 1rem
    }
</style>