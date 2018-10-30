from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import re

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if re.match(r'^(css|js|img|font)/', path):
        return send_from_directory('../static', path)
    else:
        return send_from_directory('../static', 'index.html')
