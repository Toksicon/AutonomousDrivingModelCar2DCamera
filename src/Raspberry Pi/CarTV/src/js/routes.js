import Vue from 'vue';
import VueRouter from 'vue-router';


Vue.use(VueRouter);


export const routes = [
    {
        name: 'Dashboard',
        path: '/',
        component: (resolve) => require(['./components/dashboard'], resolve),
    },
    {
        name: 'Monitor',
        path: '/monitor',
        component: (resolve) => require(['./components/monitor'], resolve),
    },
    {
        name: 'Telemetry',
        path: '/telemetry',
        component: { template: 'Telemetry' },
    }
];


export const router = new VueRouter({
    mode: 'history',
    routes,
});
