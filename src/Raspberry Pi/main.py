#!/usr/bin/python
from CarTV.backend.server import app, socketio
from CarTV.backend.processors import image


if __name__ == '__main__':
    socketio.start_background_task(target=image.processor)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
