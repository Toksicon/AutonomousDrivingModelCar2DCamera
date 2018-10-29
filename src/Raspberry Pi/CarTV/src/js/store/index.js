import Vue from 'vue';
import Vuex from 'vuex';

// monitor
import monitor from './modules/monitor';

// telemetry
//// cpu
import cpu_freq from './modules/cpu_freq';

//// memory
import virtual_memory from './modules/virtual_memory';


Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        cpu_freq,
        monitor,
        virtual_memory,
    },
});

export const stores = ['monitor', 'cpu_freq', 'virtual_memory'];
