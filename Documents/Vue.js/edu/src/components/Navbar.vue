<template>
    <div>
        <div class="header">
            <div class="header-upper">
                <div class="container">
                    <div class="header-upper-content">
                        <div class="row">

                            <div class="head-txt-right">
                                <a href="#" class="txt-right">Grab 20% Offer click here</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="header-middle">
                <div class="container">
                    <nav class="navbar">

                        <div class="container-fluid">
                            <div class="navbar-header">
                                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                                    data-target="#navbar1" aria-expanded="false">
                                    <span class="icon-bar"></span>
                                    <span class="icon-bar"></span>
                                    <span class="icon-bar"></span>
                                </button>
                            </div>
                            <div class="collapse navbar-collapse" id="navbar1">
                                <form class="mt-3"> 
                                <span class="search-bar-container">

                                   <div class="autocomplete" style="width:300px;">
   
   
   
   <input type="text" @input="getSearch()" v-model="search" name="search" id="search-entire" placeholder="Search">                        
  </div>


<div v-if="results.length > 0">
  <div  v-for="(result,index) in results" :key="index">
      <input  :value="result">
  </div>
</div>

                                    
                                    <button class="search-icon">
                                        <i class="fa fa-search" aria-hidden="true"></i>
                                    </button>
                                   
                                </span>
                                </form>
                                <nav class="navbar navbar-right">
                                    <div class="get-start-link">
                                        <a href="#" data-toggle="modal" data-target="#myModal" class="btn start_btn">
                                            Log In
                                        </a>
                                        <a href="#" data-toggle="modal" data-target="#myModal1"
                                            class="btn start_btn sign-up-btn">
                                            Sign Up Now
                                        </a>
                                    </div>
                                </nav>
                            </div>
                        </div>
                    </nav>
                </div>
            </div>
            <!-- lower header -->
            <div class="header-lower">
                <div class="container">
                    <nav class="navbar">

                        <div class="container-fluid">
                            <div class="navbar-header">
                                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                                    data-target="#navbar1" aria-expanded="false">
                                    <span class="icon-bar"></span>
                                    <span class="icon-bar"></span>
                                    <span class="icon-bar"></span>
                                </button>
                            </div>
                            <div class="collapse navbar-collapse" id="navbar1">
                                <ul class="nav navbar-nav">
                                    <li><a href="#">Live Sessions</a></li>
                                    <li><a href="#">Industry UseCase</a></li>
                                    <li><a href="#">Interview Questions</a></li>
                                    <li><a href="#">Get Mentor</a></li>
                                    <li><a href="#">Learning Support</a></li>
                                </ul>
                            </div>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
        <!---SIGN In Sign Up popup Modal--->

        <!-- Modal content-->
        <div class="modal-content">
            <div id="myModal" class="modal fade" role="dialog">
                <div class="modal-dialog">

                    <!-- Modal content-->
                    <div class="modal-content signinSection">
                        <div class="modal-header">

                            <button type="button" class="close" data-dismiss="modal">&times;</button>
                            <div class="modal-top">
                                <span class="modal-img">
                                    <!-- <img src="public/css/bg/coding.svg" alt="1">-->
                                    </span> 
                                <span class="modal-top-heading">Lets Get Start! </span>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form>
                                <input type="text" name="name" class="form-control" placeholder="USERNAME">
                                <div class="password-container">
                                    <input type="password" name="name" class="form-control psw" placeholder="PASSWORD">
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
            </div>
        </div>
        <!-- Sign  up MODAL -->
        <div id="myModal1" class="modal fade" role="dialog">
            <div class="modal-dialog">

                <!-- Modal content-->
                <div class="modal-content">
                    <div class="modal-header">

                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="modal-top">
                            <span class="modal-img">
                                <img src="public/css/bg/coding.svg" alt="1">
                            </span>
                            <span class="modal-top-heading">Lets Get Start! </span>
                        </div>

                    </div>
                    <div class="modal-body">
                        <form>
                            <input type="text" name="name" class="form-control" placeholder="Enter Name">
                            <input type="text" name="email" class="form-control" placeholder="Enter Email">

                            <div class="password-container">
                                <input type="password" name="name" class="form-control psw" placeholder="Password">
                                <button class="show-psw-btn">
                                    <i class="fa fa-eye-slash" aria-hidden="true"></i>
                                </button>

                                <select class="form-control">
                                    <option value="Select Country" disabled selected>Select Country</option>
                                    <option value="India">India</option>
                                </select>
                            </div>
                            <div class="modal-btn-container">
                                <button class="btn modal-btn">CREATE NEW ACCOUNT
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

            </div>
        </div>
    </div>



    <!-- Banner -->
</template>


<script>
import axios from 'axios';

export default {
    data(){
        return {
            search : "",
            results : []
        }
    },
    methods: {
       async getSearch() {
           if(this.search === ''){
               this.results = []
           }
           if(this.search != ''){
            var proxy = 'https://cors-anywhere.herokuapp.com/'
            var url = proxy +`https://boiling-garden-13643.herokuapp.com/course/autocomplete?search=${this.search}`
            var search = await axios.get(url)
            console.log(search.data.label)
            this.results = search.data.label
           }
        }
    },
    created() {
        this.getSearch()
        
  }
}
</script>



<style scoped>
.autocomplete {
  /*the container must be positioned relative:*/
  position: relative;
  display: inline-block;
}
input {
  border: 1px solid transparent;
  background-color: #f1f1f1;
  padding: 10px;
  font-size: 16px;
}
input[type=text] {
  background-color: #f1f1f1;
  width: 100%;
}
input[type=submit] {
  background-color: DodgerBlue;
  color: #fff;
}
.autocomplete-items {
  position: absolute;
  border: 1px solid #d4d4d4;
  border-bottom: none;
  border-top: none;
  z-index: 99;
  /*position the autocomplete items to be the same width as the container:*/
  top: 100%;
  left: 0;
  right: 0;
}
.autocomplete-items div {
  padding: 10px;
  cursor: pointer;
  background-color: #fff;
  border-bottom: 1px solid #d4d4d4;
}
.autocomplete-items div:hover {
  /*when hovering an item:*/
  background-color: #e9e9e9;
}
.autocomplete-active {
  /*when navigating through the items using the arrow keys:*/
  background-color: DodgerBlue !important;
  color: #ffffff;
}
</style>