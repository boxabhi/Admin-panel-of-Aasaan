<template>
    <div>

        <img style="margin-top:-230px; width:100%"
            src="https://uploads-ssl.webflow.com/5a8513e420c95100013e3170/5c5defe8e314be4fe3ae2af6_Teachable-Vs-Udemy-Banner.jpg"
            alt="2">


       

        <Features />
        <Card />



    </div>
</template>


<script>
    import Card from './Card'
    import Features from './utils/Features.vue'
    export default {
        components: {
            Card,
            Features

        }
    }
</script>