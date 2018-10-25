import Vue from 'vue';
import Vuex from 'vuex';
import monitor from './modules/monitor';


Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        monitor,
    },
});
