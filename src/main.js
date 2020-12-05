import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
//import ShardsVue from 'shards-vue'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'shards-ui/dist/css/shards.css'
import '../src/assets/main.css'
import axios from 'axios'
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import '@/assets/scss/main.scss'

Vue.prototype.$apiUrl = 'https://aasaan-app.com/'
Vue.prototype.$axios = axios

window.url = 'https://aasaan-app.com/'

import VueAlertify from 'vue-alertify';
import vuetify from './plugins/vuetify';
Vue.use(VueSweetalert2);
Vue.use(VueAlertify, {
  // notifier defaults
  notifier: {
    // auto-dismiss wait time (in seconds)
    delay: 5,
    // default position
    position: 'top-right',
    // adds a close button to notifier messages
    closeButton: false,
  },
});

Vue.config.productionTip = false
// Vue.use(ShardsVue);
new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
