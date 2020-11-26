<template>
  <div class="home">
    <SideNav />
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import SideNav from '@/components/Navs/SideNav.vue'


export default {
  name: 'Home',
  components: {
    HelloWorld,
    SideNav
  }
}
</script>
