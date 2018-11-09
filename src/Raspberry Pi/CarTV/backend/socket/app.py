#!/usr/bin/env python
import argparse

from logger import logger, logging
import can_processor
import telemetry_processor
from server import app, socketio


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CarTV - Socket Server')

    # debug
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables debug mode')

    # host (CarTV only)
    parser.add_argument('--host', action='store', default='0.0.0.0',
        help='Specify the host for CarTV')

    # port
    parser.add_argument('--socket-port', action='store', type=int, default=8081,
        help='Specify the port for the webserver')

    # telemetry processor
    parser.add_argument('--process-can', type=int, default=1,
        help='Disables the can logging')

    # telemetry processor
    parser.add_argument('--process-telemetry', type=int, default=1,
        help='Disables the telemetry (psutil)')

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.process_can:
        print('Starting CAN logger')
        socketio.start_background_task(target=can_processor.processor)

    if args.process_telemetry:
        print('Starting telemetry processor')
        socketio.start_background_task(target=telemetry_processor.processor)

    socketio.run(app, host=args.host, port=args.socket_port, debug=args.debug, use_reloader=True)
