import Vue from 'vue';
import Router from 'vue-router';
import PingPong from '../components/PingPong.vue';
import MainPlot from '../components/MainPlot.vue';
import MainView from '../components/MainView.vue';
import SummaryView from '../components/SummaryView.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'MainView',
      component: MainView,
    },
    {
      path: '/plot',
      name: 'MainPlot',
      component: MainPlot,
    },
    {
      path: '/ping',
      name: 'PingPong',
      component: PingPong,
    },
    {
      path: '/summary',
      name: 'SummaryView',
      component: SummaryView,
    },
  ],
});
