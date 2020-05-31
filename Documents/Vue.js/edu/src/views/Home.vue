<template>
  <div class="home">
     <Navbar/>
      <Main/>
      <Footer/>
   
  </div>
</template>


<script>

 import Main from '@/components/Main.vue'


export default {

  components: {

    Main,
    
  }
  
}
</script>

<style>
  @import '../assets/index.css';

</style>

