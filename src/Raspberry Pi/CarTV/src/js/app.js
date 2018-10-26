import bootstrap from 'bootstrap';
import Vue from 'vue';
import io from 'socket.io-client';

import store from './store';
import {routes, router} from './routes';


var socket = io(`${location.protocol}//${location.hostname}:${location.port}`);
socket.on('monitor', (data) => store.commit('monitor/push', data));

const app = new Vue({
    el: '#app',

    data: {
        routes,
    },

    store,
    router,
});
