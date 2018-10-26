// initial state, as return value, because copy is required
// access state through $store.state.monitor.<property>
function initialState() {
    return {
        record_limit: 10,
        records: [],
    };

    /* record = {
        // ...
    }
    */
}

// getters (for computed states)
const getters = {

};

// actions (async, usually call mutations)
// call with $store.dispatch('monitor/<...>'[, args...])
const actions = {
    // ...
};

// mutations (can manipulate store)
// call with $store.commit('cpu/<...>', value)
const mutations = {
    // resets to initial state
    reset(state) {
        const initState = initialState();
        for (const key in initState) {
            state[key] = initState[key];
        }
    },

    push(state, update) {
        state.records.push(update);

        while (state.records.length > state.record_limit) {
            state.records.shift();
        }
    },
};

export default {
    namespaced: true,
    state: initialState(),
    getters,
    actions,
    mutations,
};
