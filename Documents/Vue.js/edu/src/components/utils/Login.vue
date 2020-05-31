<template>
      <div class="modal-dialog">
          <h2>Login</h2>

                    <!-- Modal content-->
                    <div class="modal-content signinSection">
                        <div class="modal-header">

                            <button type="button" class="close" data-dismiss="modal">&times;</button>
                            <div class="modal-top">
                                <span class="modal-img">
                                    <!-- <img src="public/css/bg/coding.svg" alt="1">-->
                                    </span> 
                                <span class="modal-top-heading">Lets Get Start!!! </span>
                              </div>
                        </div>
                        <div class="modal-body">
                              <p v-if="error" class="text-danger text-center" >Wrong credentials</p>
                            
                            <form @submit.prevent="login()">
                                <input type="text" v-model="email" class="form-control" placeholder="USERNAME">
                                <div class="password-container">
                                    <input type="password" v-model="password" class="form-control psw" placeholder="PASSWORD">
                                    <button class="show-psw-btn">
                                        <i class="fa fa-eye-slash" aria-hidden="true"></i>
                                    </button>
                                </div>
                                <div>
                                    <input type="checkbox" name="cb">
                                    <span class="cb-remember">REMEMBER ME?</span>
                                </div>
                                <div class="modal-btn-container">
                                    <button class="btn  modal-btn">SIGN IN</button>
                                </div>
                                <div class="modal-bottom-link">
                                    <a href="#" class="form-bottom-link">FORGOT YOUR PASSWORD?</a>
                                </div>
                            </form>
                        </div>
                    </div>
                    <!-- forgot password section -->
                    <div class="modal-content forgot-psw">
                        <div class="modal-header">

                            <button type="button" class="close" data-dismiss="modal">&times;</button>
                            <div class="modal-top">
                                <span class="modal-img"><img src="public/css/bg/coding.svg" alt="1"></span>
                                <span class="modal-top-heading">Reset Password</span>
                            </div>
                        </div>
                        <div class="modal-body">

                            <div id="forgotpsw">
                                <span class="forgot-psw-content">
                                    Lost your password?No worries Just enter your email address below and we'll send you
                                    instructions on how to reset your password
                                </span>
                                <form>
                                    <input type="email" name="name" class="form-control" placeholder="your email">
                                    <div class="modal-btn-container">
                                        <button class="btn modal-btn">RESET PASSWORD</button>
                                    </div>
                                    <div class="modal-bottom-link">
                                        <a href="#" class="return-signIn-link">RETURN TO SIGN IN</a>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
</template>



<script>
import axios from "axios"
export default {
    data(){
        return{
           
            email : '',
            password : '',
            error : false
        }
    },
  
    methods : {
       async login(){    
           console.log("click")     
       
        var data = {
            email : this.email,
            password : this.password
        }

        try{
       const response =   await axios.post('https://cors-anywhere.herokuapp.com/https://boiling-garden-13643.herokuapp.com/posts/userLogin', data)
       

    if(response.status == 200){
        localStorage.setItem('token' , response.data.token)
        this.$router.push('/')
    }
        }
        catch{
    
       this.error = true
    
        }
        


        }
    }
}
</script>