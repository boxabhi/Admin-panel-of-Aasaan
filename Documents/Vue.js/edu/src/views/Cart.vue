<template>
    <div>
        <!----Shopping Cart----->
        <div class="cart-section">
            <div class="container">
                <div class="card-container">
                    <!-- empty cart -->
                    <div id="emptycart" class="empty-card">
                        <div class="empty-cart-icon">
                            <i class="fa fa-shopping-bag" aria-hidden="true"></i>
                        </div>
                        <div class="empty-cart-title">
                            There Are No Courses In Your Cart
                        </div>
                        <div class="empty-cart-btn">
                            <button class="btn">
                                <a href="index.html">RETURN TO HOME</a>
                            </button>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-8">
                            <div class="shop-cart" id="shop-cart">

                                <!--Wish list  -->
                                <div id="mycart" class="shop-cart">
                                    <div class="flex-container">
                                        <button class="close">
                                            <i class="fa fa-times" aria-hidden="true"></i>
                                        </button>
                                        <div class="card">
                                            <div class="flex-wrapper">
                                                <div class="row">
                                                    <div class="col-md-3">
                                                        <div class="flex-img">
                                                            <img src="public/css/bg/laptop_1.svg">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-9">
                                                        <div class="flex-content">
                                                            <div class="session-heading">
                                                                <span id="session-topic"
                                                                    class="session-heading">JavaScript Short
                                                                    Session</span>
                                                            </div>
                                                            <div class="training">By Sumit Training Services </div>

                                                            <p><span><strike>$19.99 </strike></span><span
                                                                    class="price">$10</span>
                                                            </p>
                                                            <div class="session-datetime">
                                                                <span class="timings-title">Date</span>
                                                                        <span class="timings">20/03/2020</span>
                                                                        <div class="session-timing">
                                                                            <span class="timings-title">Timings</span>
                                                                            <span class="timings">9:00PM</span>
                                                                            <span>-</span>
                                                                            <span class="timings">11:00PM</span>
                                                                        </div>

                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="chk-card-container">
                                <div class="cart-card">

                                    <div class="cart-card-heading">Total : </div>

                                    <p class="price">$10</p>
                                    <p><strike>$19.99</strike></p>
                                    <p><button>Checkout</button></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


</template>

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    .navbar-toggle {
        background-color: #fff;
    }

    .navbar-toggle .icon-bar {
        background-color: #fff;
    }

    .header {
        color: #0b1c39;
        background-color: #fff;
    }

    .header-upper {
        padding-top: 10px;
    }

    nav.navbar {
        margin: 0;
    }

    .logo {}

    .search-bar-container {
        position: relative;
    }

    .search-icon {
        position: absolute;
        border: none;
        background: none;
        top: -11px;
        padding: 7px 24px;
        font-size: 15px;
        right: 0px;
        color: #fff;
        background-color: #ee9617;
        background-image: linear-gradient(315deg, #ee9617 0%, #fe5858 74%);
        border: 1px solid;
        border-image: linear-gradient(315deg, #ee9617 0%, #fe5858 74%);
    }

    input#search-entire {
        width: 500px;
        padding: 4px 12px;
        background: transparent;
        border: 1px solid grey;
        font-size: 18px;

    }

    input#search-entire:focus {
        outline: none;
    }

    input#search-entire::placeholder {

        color: lightgrey;
    }

    .header_btn {
        font-size: 14px;
        font-weight: 500;
        padding: 8px 28px;
        background-color: #fff;
        border: 1px solid grey;
        color: #3F51B5 !important;
        ;
        text-transform: capitalize;
        margin-left: 25px;

    }

    .trainer-btn {
        color: #fff !important;
        background-image: linear-gradient(315deg, #ee9617 0%, #fe5858 74%);
        border: 1px solid;
        border-image: linear-gradient(315deg, #ee9617 0%, #fe5858 74%);
        margin-left: 60px;
    }

    .header_btn:hover,
    .header_btn:focus {
        background-color: #fff;
        border-color: 1px solid #0b1c39;
        outline: none;
        transition: 0.5s;
        color: #0b1c39 !important;
    }

    .cart-btn {
        /*background-color: #f26d21;
    border: 2px solid #f26d21;*/
        color: #505050 !important;
        background: none;
        border: none;
        font-size: 28px;
    }

    .usr-btn,
    .dropdown-btn {
        background-color: #9E9E9E;
        color: white;
        border-radius: 50%;
        padding: 12px 16px;
        margin-left: 25px;
    }

    #cart-top {
        position: relative;
    }

    #cart-top::before {
        position: absolute;
        content: '1';
        background-color: #F44336;
        color: white;
        border-radius: 50%;
        top: -10px;
        font-weight: 600;
        right: 0;
        font-size: 10px;
        padding: 4px 8px;
    }


    .header-dropdown,
    .dropdown {
        display: inline-block;
    }

    .dropdown:hover .dropdown-menu,
    .navbar-right .dropdown-men {
        display: block;
        right: -125px;
        top: 27px;
        width: 250px;
    }

    .dropdown:focus .dropdown-menu {
        display: none;
    }

    .dropdown-menu li {
        padding: 10px 10px;
        border-bottom: 1px solid lightgrey;
    }

    .dropdown-menu>li>a {
        padding: 0px;
    }

    a.user-email {
        font-size: 12px;
        color: #9E9E9E !important;
    }

    a:focus,
    a:hover {
        outline: none;
        text-decoration: none;
    }

    .dropdown-menu li a {
        color: #333;
    }

    .header-lower {
        background-color: #2338ad;
    }

    .header-lower nav.navbar {
        padding: 10px 0px;
        min-height: 0;
    }

    .header-lower .nav>li>a {
        color: #fff;
        margin: 0;
        padding: 4px 15px;
        line-height: 5px;
        letter-spacing: 1px;
        font-size: 1.5rem;
    }

    .header-lower li a:hover {
        color: #9E9E9E;
        background: none;
    }

    /*Shopping Cart*/
    .empty-card {

        display: none;
    }

    .empty-cart-icon {
        text-align: center;
        font-size: 100px;
        color: lightgray;
        padding: 50px;
    }

    .empty-cart-title {
        font-size: 18px;
        color: gray;
        padding: 0 30px;
        text-align: center;
    }

    .empty-cart-btn {
        padding: 30px 0;
        text-align: center;
    }

    .empty-cart-btn .btn {
        background-color: linear-gradient(315deg, #ee9617 0%, #fe5858 74%);
        padding: 8px 70px;
        font-size: 14px;
        border-radius: 0;
    }

    .empty-cart-btn .btn a {
        color: white;
    }


    /*Session card Section*/
    .cart-section {
        background-color: whitesmoke;
    }

    .flex-container {
        position: relative;
        background-color: white;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    }

    .card-container {
        padding: 25px 0;
    }

    button.close {
        position: absolute;
        top: 0;
        font-size: 15px;
        right: 0;
        opacity: 1;
        color: #F44336;
        z-index: 999 !important;
    }

    .training {

        font-size: 1.1em;
        color: #a6a6a6;
        ;
        margin: 2px;

    }

    .timings-title {
        font-size: .9em;
        color: #a6a6a6;
        margin: 2px;
    }

    .timings {

        font-size: 1.1em;
        color: #000080;
        margin: 2px;

    }

    .flex-wrapper {
        height: 180px;
    }

    .flex-img {
        position: relative;
        overflow: hidden;
    }

    .flex-wrapper img {
        width: 100%;
        height: 180px;
        transition: 1s;
    }

    .flex-content {
        background-color: white;
    }

    .session-heading {
        font-size: 20px;
        /* text-align: center; */
        font-weight: 800;
        margin-top: 10px;
        color: #0b1c39
    }

    .session-desc {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: gray;
    }

    .session-desc:hover {
        overflow: visible;
        word-wrap: break-word;
    }

    .session-datetime {
        color: #0b1c39;
    }

    .checked {
        color: #f09d11;
    }

    .session-ratings {}

    .section {
        background-color: #f8f9fa;
        padding-top: 50px;
    }

    .session-section-head {
        font-size: 25px;
        font-weight: 600;
        position: relative;
        text-align: center;
    }

    .session-section-head::after {
        content: '';
        display: block;
        background-color: black;
        height: 2px;
        width: 25px;
        position: absolute;
        transform: translate(-50%, -50%);
        left: 50%;
        top: calc(100% + 5px);
    }

    /*checkout card*/
    .cart-card {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        font-family: arial;
        width: 280px;
        height: auto;
        border: 1px solid #f1f1f1;
        padding: 10px;
        overflow: hidden;
        background-color: #fff
    }

    .cart-card-heading {
        font-size: 25px;
        padding: 10px 0;
        text-align: left;
        display: inline-block;
        vertical-align: middle;
        line-height: 1.3;
        font-weight: bold;

    }

    .price {
        color: #ff3f40;
        font-size: 28px;
        font-weight: bolder;
    }

    .cart-card button {
        border: none;
        outline: 0;
        padding: 12px;
        color: white;
        background-color: #ee9617;
        background-image: linear-gradient(315deg, #ee9617 0%, #fe5858 74%);
        text-align: center;
        cursor: pointer;
        width: 100%;
        font-size: 18px;
    }

    .session-card button:hover {
        opacity: 0.7;
    }

    .card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
    }

    /*-------FOOTER SECTION---------*/
    .footer {
        color: #0b1c39;
        padding: 80px 0;
        background: #f8f9fa;
    }

    .footer li a {
        color: #0b1c39;
    }

    .footer li a:focus,
    .footer li a:hover {
        color: Blue;
        text-decoration: none;
    }

    .footer h4 {
        color: #0b1c39;
    }

    .footer li {
        list-style-type: none;
        padding-top: 20px;
    }

    .list-inline li a {
        color: #0b1c39;
        font-size: 20px;
        padding-left: 10px;
    }

    .list-inline li a:hover,
    .list-inline li a:focus {
        color: #f09d11;
    }

    .footer-end {
        text-align: center;
        background-color: black;
        padding: 10px 0;
        color: #b5b3b3;
    }

    .scrollbtn {
        background: none;
        font-size: 30px;
        border: none;
        position: fixed;
        display: block;
        bottom: 10px;
        right: 20px;
        color: #0b1c39;
    }

    .scrollbtn:hover,
    .scrollbtn:focus {
        color: #f09d11;
        outline: none;
    }

    @media screen and (max-width:768px) {
        .navbar-right .dropdown-menu {
            display: block;
            right: -125px;
            top: 27px;
            width: 250px;
        }
    }
</style>