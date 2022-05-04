import { BootstrapVue, BButtonGroup } from 'bootstrap-vue';
import VCalendar from 'v-calendar';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.css';

Vue.use(BootstrapVue);
Vue.use(VCalendar);

Vue.component('b-button-group', BButtonGroup);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
