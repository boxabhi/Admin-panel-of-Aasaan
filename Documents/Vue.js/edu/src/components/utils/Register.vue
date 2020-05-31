<template>
     <div class="modal-dialog">

                <!-- Modal content-->
                <div class="modal-content">
                    <div class="modal-header">

                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="modal-top">
                            
                            <span class="modal-top-heading">Lets Get Start! </span>
                        </div>

                    </div>
                    <div class="modal-body">
                        <form id="signup-form" @submit.prevent="register()">
                           
    <p class="text-danger text-center m-0 p-0" v-if="error"> Fill in all Details</p>

                            <input type="text" v-model="name" class="form-control" placeholder="Enter Name">
                            <input type="text" v-model="email" class="form-control" placeholder="Enter Email">

                            <div class="password-container">
                                <input type="password" v-model="password" class="form-control psw" placeholder="Password">
                                <button class="show-psw-btn">
                                    <i class="fa fa-eye-slash" aria-hidden="true"></i>
                                </button>

                            </div>
                            <div class="modal-btn-container">
              <button class="btn modal-btn" >CREATE NEW ACCOUNT
                                </button>
                            
                            </div>
                        </form>
                    </div>
                </div>

            </div>
</template>

<script>
import axios from "axios"
export default {
    data(){
        return{
            name : '',
            email : '',
            password : '',
            error : false
        }
    },
  
    methods : {
       async register(){         
        
        var data = {
            fullName : this.name,
            email : this.email,
            password : this.password
        }

         
         await axios.post('https://cors-anywhere.herokuapp.com/https://boiling-garden-13643.herokuapp.com/posts/UserRegistration', data).then(response =>{
             console.log(response)
             if(response.data.status == 200){
                 this.$router.push('/')
             }
         })

        


        }
    }
}
</script>