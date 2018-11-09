import os
import pickle
import sys
import time

from pymemcache.client import base
from server import socketio


def processor():
    client = base.Client(('localhost', 11211))

    while True:
        message = client.get('can')

        if message:
            socketio.emit('can', pickle.loads(message))
            client.delete('can')

        time.sleep(1)
