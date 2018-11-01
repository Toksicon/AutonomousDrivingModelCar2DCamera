#!/usr/bin/python
import argparse

from backend.server import app, socketio
from backend.processors import image, telemetry


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CarTV')

    # debug
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables debug mode')

    # host (CarTV only)
    parser.add_argument('--host', action='store', default='0.0.0.0',
        help='Specify the host for CarTV')

    # port (CarTV only)
    parser.add_argument('--port', action='store', type=int, default=5000,
        help='Specify the port for CarTV')

    # image processor
    parser.add_argument('--process-images', type=int, default=1,
        help='Disables the image processor (camera and can)')

    # telemetry processor
    parser.add_argument('--process-telemetry', type=int, default=1,
        help='Disables the image telemetry (psutil)')

    

    args = parser.parse_args()

    if args.process_images:
        socketio.start_background_task(target=image.processor)

    if args.process_telemetry:
        socketio.start_background_task(target=telemetry.processor)

    try:
        socketio.run(app, host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        exit(0)
