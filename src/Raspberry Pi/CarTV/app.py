from backend.server import app, socketio
from backend.processors import image, telemetry

if __name__ == '__main__':
    socketio.start_background_task(target=image.processor)
    socketio.start_background_task(target=telemetry.processor)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
