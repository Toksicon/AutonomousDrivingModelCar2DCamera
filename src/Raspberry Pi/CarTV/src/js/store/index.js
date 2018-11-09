import Vue from 'vue';
import Vuex from 'vuex';

// monitor
//// can
import can from './modules/can';

// telemetry
//// cpu
import cpu_freq from './modules/cpu_freq';
import cpu_percent from './modules/cpu_percent';

//// memory
import virtual_memory from './modules/virtual_memory';


Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        can,

        cpu_freq,
        cpu_percent,

        virtual_memory,
    },
});

export const stores = ['can', 'cpu_freq', 'cpu_percent', 'virtual_memory'];
