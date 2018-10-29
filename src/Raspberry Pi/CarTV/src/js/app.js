import bootstrap from 'bootstrap';
import Vue from 'vue';

import store from './store';
import socket from './socket';
import {routes, router} from './routes';


const app = new Vue({
    el: '#app',

    data: {
        routes,
    },

    store,
    router,
});
