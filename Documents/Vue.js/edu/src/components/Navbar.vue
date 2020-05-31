<template>
    <div>
        <div v-show="logged">
            <div class="header">
                <div class="header-upper">
                    <div class="container">
                        <nav class="navbar">
                            <div class="container-fluid">
                                <div class="navbar-header">
                                    <div class="header-upper-content">
                                    </div>

                                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                                        data-target="#navbar1" aria-expanded="false">
                                        <span class="icon-bar"></span>
                                        <span class="icon-bar"></span>
                                        <span class="icon-bar"></span>
                                    </button>
                                </div>
                                <div class="collapse navbar-collapse" id="navbar1">
                                    <span class="search-bar-container">
                                        <input type="text" name="search" id="search-entire" placeholder="Search">
                                        <button class="search-icon">
                                            <i class="fa fa-search" aria-hidden="true"></i>
                                        </button>

                                    </span>
                                    <a href="#" class="btn header_btn trainer-btn">
                                        Become A Trainer
                                    </a>
                                    <a href="#" class="btn header_btn course-btn">
                                        My Courses
                                    </a>
                                    <nav class="navbar navbar-right">

                                        <a href="#" class="cart-btn" id="cart-top">
                                            <i class="fa fa-shopping-bag" aria-hidden="true"></i>
                                        </a>

                                        <div class="dropdown">
                                            <a href="$" target="_blank" class="droplink usr-btn" data-hover="dropdown"
                                                type="link" data-toggle="dropdown"><i class="fa fa-user-o"
                                                    aria-hidden="true"></i></a>
                                            <ul class="dropdown-menu">
                                                <li>
                                                    <span class="c">
                                                        <a href="#" target="blank"> Rishabh Agrawal</a>
                                                        <a href="#" target="blank"
                                                            class="user-email">rishabh.agrawal@gmail.com</a>
                                                    </span>
                                                    <span class="dropdown-btn"><i class="fa fa-user-o"
                                                            aria-hidden="true"></i></span>
                                                </li>
                                                <li><a href="#" target="_blank">Purchase History</a></li>
                                                <li><a href="#" target="_blank">Credits</a></li>
                                                <li><a href="#" target="_blank">Messages</a></li>
                                                <li><a href="#" target="_blank">Notificaions</a></li>
                                                <li><a href="#" target="_blank">Log out</a></li>
                                            </ul>
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
        </div>
        <div v-show="!logged">
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



                                                <input type="text" @input="getSearch()" v-model="search" name="search"
                                                    id="search-entire" placeholder="Search">
                                            </div>


                                            <div v-if="results.length > 0">
                                                <div v-for="(result,index) in results" :key="index">
                                                    <input :value="result">
                                                </div>
                                            </div>


                                            <button class="search-icon">
                                                <i class="fa fa-search" aria-hidden="true"></i>
                                            </button>

                                        </span>
                                    </form>
                                    <nav class="navbar navbar-right">
                                        <div class="get-start-link" v-if="!logged">
                                            <a href="#" data-toggle="modal" data-target="#myModal"
                                                class="btn start_btn">
                                                Log In
                                            </a>
                                            <a href="#" data-toggle="modal" data-target="#myModal1"
                                                class="btn start_btn sign-up-btn">
                                                Sign Up Now
                                            </a>
                                        </div>
                                        <a href="#" data-toggle="modal" data-target="#myModal1"
                                            class="btn start_btn sign-up-btn">
                                            Logout
                                        </a>
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
        </div>
        <!---SIGN In Sign Up popup Modal--->

        <!-- Modal content-->
        <div class="modal-content">
            <div id="myModal" class="modal fade" role="dialog">
                <Login />
            </div>
        </div>
        <!-- Sign  up MODAL -->
        <div id="myModal1" class="modal fade" role="dialog">
            <Register />
        </div>
    </div>



    <!-- Banner -->
</template>


<script>
    import axios from 'axios';
    import Login from './utils/Login'
    import Register from './utils/Register'
    export default {
        components: {
            Login,
            Register
        },
        data() {
            return {
                search: "",
                results: [],
                logged: false
            }
        },
        methods: {
            async getSearch() {
                if (this.search === '') {
                    this.results = []
                }
                if (this.search != '') {
                    var proxy = 'https://cors-anywhere.herokuapp.com/'
                    var url = proxy +
                        `https://boiling-garden-13643.herokuapp.com/course/autocomplete?search=${this.search}`
                    var search = await axios.get(url)
                    console.log(search.data.label)
                    this.results = search.data.label
                }
            },
            check() {
                if (localStorage.getItem('token') != null) {
                    this.logged = true
                }
            }
        },
        created() {
            this.getSearch()
            this.check()

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