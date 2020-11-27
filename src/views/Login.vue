<template>
    <div class="admin-login-wrapper">
        <form v-on:submit.prevent="handleSubmit">
            <div class="admin-form-wrapper">
                <div class="text-center">
                    <img src="@/assets/images/login.webp" style="height:250px" class="text-center" />
                </div>
                <div class="form-group">
                    <label for="">Email</label>
                    <input required type="text" v-model="creds.username" class="form-control"
                        placeholder="Enter your username" />
                </div>

                <div class="form-group">
                    <label for="">Password</label>
                    <input required type="password" v-model="creds.password" class="form-control"
                        placeholder="Enter your password" />
                </div>

                <div class="form-group">
                    <button class="btn btn-main btn-block" type="submit">Sign in</button>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import axios from "axios"

    export default {
        name: 'AdminLogin',
        data() {
            return {
                creds: {
                    username: '',
                    password: ''
                }
            }
        },
        methods: {
            handleSubmit() {
                var url = window.url
                //var data = this.creds
                axios.post(`${url}/api/token/`, this.creds)
                    .then(response => {
                        var admin = {
                            isLogged: true,
                            refresh: response.data.refresh,
                            access: response.data.access,
                            timeLoggedIn: Date.now(),
                        }
                        this.$store.dispatch('loginAdmin', (admin))
                        this.$swal.fire({
                            icon: 'success',
                            title: 'Hurray',
                            text: 'Welcome! Admin',
                        })
                        
                        setTimeout(() =>{
                            window.location = '/dashboard'
                        },2000)

                    }).catch(err => {
                        console.log(err)
                        this.$swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: 'Are your really a admin? ',
                        })
                    })
            }

        },
    }
</script>