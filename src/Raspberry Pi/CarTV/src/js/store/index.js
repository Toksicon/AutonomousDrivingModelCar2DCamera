import Vue from 'vue';
import Vuex from 'vuex';

// telemetry
//// cpu
import cpu_freq from './modules/cpu_freq';

//// memory
import virtual_memory from './modules/virtual_memory';


Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        cpu_freq,
        virtual_memory,
    },
});

export const stores = ['cpu_freq', 'virtual_memory'];
