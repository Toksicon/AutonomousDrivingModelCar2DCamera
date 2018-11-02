// initial state, as return value, because copy is required
// access state through $store.state.monitor.<property>
function initialState() {
    return {
        rendered: true,
        images: [],
        median: [],
    };

    /* record = {
        images: [
            { name: "Captured", data: "blob", },
            { name: "Sobel Operator", data: "blob", },
        ],

        median: [
            { x: 50, y: 0 },
            // ...
        ],
    }
    */
}

// getters (for computed states)
const getters = {

};


let nextUpdate = null;


// actions (async, usually call mutations)
// call with $store.dispatch('monitor/<...>'[, args...])
const actions = {
    push(context, update) {
        console.log('push(context)');
        if (context.state.rendered) {
            console.log('commit(...)');
            context.commit('push', update);
        } else {
            console.log('nu=u');
            nextUpdate = update;
        }
    },

    update(context) {
        console.log('update(context)');
        if (nextUpdate) {
            console.warn('nu');
            context.commit('push', nextUpdate);
        } else {
            context.state.rendered = true;
        }
    },
};

// mutations (can manipulate store)
// call with $store.commit('monitor/<...>', value)
const mutations = {
    // resets to initial state
    reset(state) {
        const initState = initialState();
        for (const key in initState) {
            state[key] = initState[key];
        }
    },

    push(state, update) {
        console.warn('push(state, update)');
        state.rendered = false;
        state.images = update.images;
        state.median = update.median;
    },
};

export default {
    namespaced: true,
    state: initialState(),
    getters,
    actions,
    mutations,
};
