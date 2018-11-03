from flask import Flask
from flask_socketio import SocketIO

app = Flask('socketio')
socketio = SocketIO(app, async_mode='gevent')
