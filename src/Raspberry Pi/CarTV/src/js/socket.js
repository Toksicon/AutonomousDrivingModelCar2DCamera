import io from 'socket.io-client';
import store from './store';
import {stores} from './store';

let socket = io(`${location.protocol}//${location.hostname}:${location.port}`);

socket.on('connect', (socket) => console.log('connected'))
socket.on('message', function (message) {
    console.log(message);
  });
stores.forEach((state) => {
    socket.on(state, (data) => {
        console.log(state, data);
        store.commit(state + '/push', data)
    });
});

socket.on('monitor', (data) => {
    console.log('monitor', data);
    store.dispatch('monitor/push', data);
});

export default socket;
