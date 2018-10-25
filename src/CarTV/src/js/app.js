import Vue from 'vue';
import store from './store';
import {routes, router} from './routes';

const app = new Vue({
    el: '#app',

    data: {
        routes,
    },

    store,
    router,
});
