import io from 'socket.io-client';
import store from './store';
import {stores} from './store';

let socket = io(`${location.protocol}//${location.hostname}:${location.port}`);

stores.forEach((state) => {
    socket.on(state, (data) => {
        console.log(state, data);
        store.commit(state + '/push', data)
    });
});

export default socket;
