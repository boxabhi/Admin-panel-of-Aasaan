<template>
    <div class="admin-login-wrapper">
        <div class="admin-form-wrapper">
            <div class="text-center">
            <img src="@/assets/images/login.webp" style="height:250px" class="text-center" />
            </div>
            <div class="form-group">
                <label for="">Email</label>
                <input type="text" v-model="creds.email" class="form-control" placeholder="example@gmail.com" />
            </div>

            <div class="form-group">
                <label for="">Password</label>
                <input type="password" v-model="creds.password" class="form-control" placeholder="**********" />
            </div>

            <div class="form-group">
                <button class="btn btn-main btn-block" @click="signin">Sign in</button>
            </div>
            
         
        </div>
    </div>
</template>

<script>
export default {
    name: 'AdminLogin',
    data() {
        return {
            creds: {
                email: '',
                password: ''
            }
        }
    },
    methods: {
        signin() {
            const { email, password } = this.creds

            if(!email || !password) {
                return this.$alertify.error('Incomplete credentials');
            }

            this.$axios.post(`${this.$apiUrl}/auth/login`, {
                email, 
                password
            })
            .then(res => {
                const data = res.data

                if(data.user.role !== 'admin') {
                    return this.$alertify.error('Unauthorized access')
                }

                localStorage.authtoken = data.token
                localStorage.admin = JSON.stringify(data.user)
                this.$router.push('/admin/dashboard')
            })
            .catch(error => {
                this.$alertify.error(error.response.data.message)
            })
        },
    }
}
</script>