<template>
    <div class="mt-0">
        <div class="trainer-section">
            <div class="trainer-container">
                <div class="trainer-header">
                    <div class="container">
                        <div class="trainer-header-card">
                            <div class="trainer-card-heading">
                                Trainer Details
                            </div>
                            <p class="trainer-heading-summary">Just provide your basic information and course related
                                details</p>
                        </div>
                    </div>
                </div>
                
                <div class="trainer-details-section">
                    <div class="container">
                        <div class="row">
                            <div class="col-md-7">
                                <div class="trainer-pagination" id="page1">
                                    <div class="page-heading">Basic Information</div>
                                    <div class="row">
                                        <div class="col-md-9">
                                            <div class="trainer-basic-form">
                                                <form>
                                                    <div class="form-group">
                                                        <div><label for="name">Enter your full name:</label> </div>
                                                        <input type="text" name="name" class="form-control"
                                                            placeholder="Full Name">
                                                    </div>
                                                    <div class="form-group">
                                                        <div><label for="company">Enter your Company name : </label>
                                                        </div>
                                                        <input type="text" name="company-name" class="form-control"
                                                            placeholder="Company Name">
                                                    </div>
                                                    <div class="form-group">
                                                        <div><label for="pohoneNo">Enter your Mobile No : </label></div>
                                                        <input type="text" name="phone-name" class="form-control"
                                                            placeholder="Mobile No">
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="experience">Enter your experience :</label>
                                                        <select class="form-control">
                                                            <option value="India">0-1 Year</option>
                                                        </select>
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="skills">Enter your skillset : </label>
                                                        <textarea class="form-control" rows="4" id="skills"></textarea>
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="address">Enter your Address :</label>
                                                        <textarea class="form-control" rows="4" id="address"></textarea>
                                                    </div>


                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="trainer-pagination" id="page2">
                                    <div class="page-heading">Course details</div>
                                    <div class="row">
                                        <div class="col-md-9">
                                            <div class="trainer-basic-form">
                                                <form>
                                                    <div class="form-group">
                                                        <label for="course-name">Course Name:</label>
                                                        <input type="text" name="name" class="form-control">
                                                    </div>
                                                    <div class="form-group">
                                                        <div><label for="course-summary">Course Summary : </label></div>
                                                        <input type="text" name="course-summary" class="form-control"
                                                            placeholder="">
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="course-desc">Course description : </label>
                                                        <textarea class="form-control" rows="4"
                                                            id="course-desc"></textarea>
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="what-learn">What participant will learn :</label>
                                                        <textarea class="form-control" rows="4"
                                                            id="what-learn"></textarea>
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="prerequisite">Any Prerequisite :</label>
                                                        <textarea class="form-control" rows="4"
                                                            id="prerequisite"></textarea>
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="price">Price of the Course :</label>
                                                        <input type="text" name="price" class="form-control">
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="trainer-pagination" id="page3">
                                    <div class="page-heading">Timings details</div>
                                    <div class="row">
                                        <div class="col-md-9">
                                            <div class="trainer-basic-form">
                                                <form>
                                                    <div class="form-group">
                                                        <label for="Topic-name">Topic Name:</label>
                                                        <input type="text" name="Topic-name" class="form-control">
                                                    </div>
                                                    <div class="form-group">
                                                        <div><label for="Topic-agrend">Topic Agenda : </label></div>
                                                        <input type="text" name="Topic-agenda" class="form-control"
                                                            placeholder="">
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="date-time">Start Date & time : </label>
                                                        <input type="date" name="date-time" class="form-control"
                                                            placeholder="">
                                                    </div>
                                                    <div class="form-group">
                                                        <label for="duration">Course Duration :</label>
                                                        <select class="form-control">
                                                            <option value="1">1 hour</option>
                                                            <option value="1">2 hour</option>
                                                            <option value="1">3 hour</option>
                                                        </select>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-5">

                                <ul id="pagein" class="paging">
                                </ul>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-7"></div>
                            <form id="main-form">
                                <div class="trainer-btn-container">
                                    <button class="submit_btn prev-btn">Previous</button>
                                    <button type="submit" class="submit_btn submit-next-btn" id="next-submit-btn">Next &
                                        Submit</button>
                                    <button type="submit" class="submit_btn submit-next-btn" id="final-submit-btn"
                                        disabled>Final Submit</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {

    }
</script>


<style scoped>
    /*Trainer pagination*/

    /*trainer skills card*/
    .trainer-header {
        height: 200px;
        background-color: #242633;
        padding: 40px 0;
    }

    .trainer-header-card {
        color: white;
        padding: 0 20px;
    }

    .trainer-card-heading {
        padding: 10px 0;
        font-size: 28px;
        color: #fff;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: capitalize;
    }

    .trainer-heading-summary {
        font-size: 18px;
        letter-spacing: 1px;
    }

    .trainer-details-section {
        margin: 50px 0;
    }

    .page-heading {
        font-weight: 600;
        font-size: 18px;
        padding-bottom: 40px;
        letter-spacing: 1px;
    }

    .trainer-basic-form .form-group {
        padding-bottom: 20px;
    }

    .trainer-btn-container .submit_btn {
        font-size: 14px;
        font-weight: 500;
        padding: 8px 28px;
        background-color: #fff;
        border: 1px solid grey;
        color: #3F51B5 !important;
        ;
        text-transform: capitalize;

    }

    .trainer-btn-container .submit-next-btn {
        color: #fff !important;
        background-image: linear-gradient(315deg, #ee9617 0%, #fe5858 74%);
        border: 1px solid;
        border-image: linear-gradient(315deg, #ee9617 0%, #fe5858 74%);
        margin-left: 10px;
    }

    .trainer-btn-container .submit_btn:hover,
    .submit_btn:focus {
        background-color: #fff;
        border-color: 1px solid #0b1c39;
        outline: none;
        transition: 0.5s;
        color: #0b1c39 !important;
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

    .fix {
        position: fixed;
        top: 0;

        z-index: 10 !important;
    }

    @media screen and (max-width:768px) {
        .navbar-right .dropdown-menu {
            display: block;
            right: -125px;
            top: 27px;
            width: 250px;
        }
    }

    .current {
        background-color: #009688;
        color: white;
    }

    ul.paging {
        list-style-type: none;
        display: inline-block;
    }

    .paging li {
        display: inline-block;
    }

    .paging li a {

        margin-right: 10px;
        border: 1px solid #009688;
        padding: 6px 12px;
        font-size: 16px;
    }
</style>