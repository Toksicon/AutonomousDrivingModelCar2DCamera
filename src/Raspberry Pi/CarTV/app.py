#!/usr/bin/python
import argparse
import os
import subprocess
import sys

import http
import socket


root_path = os.path.dirname(os.path.realpath(__file__))


def start_http_server():
    call = [sys.executable, os.path.join(root_path, 'backend/http/app.py')]
    call.extend(sys.argv[1:])

    return subprocess.Popen(call)


def start_socket_server():
    call = [sys.executable, os.path.join(root_path, 'backend/socket/app.py')]
    call.extend(sys.argv[1:])

    return subprocess.Popen(call)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CarTV')

    # debug
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables debug mode')

    # host
    parser.add_argument('--host', action='store', default='0.0.0.0',
        help='Specify the host for the http and socket server')

    # http-port
    parser.add_argument('--http-port', action='store', type=int, default=8080,
        help='Specify the port for the http server')

    # http-port
    parser.add_argument('--socket-port', action='store', type=int, default=8081,
        help='Specify the port for the websocket')

    # http server
    parser.add_argument('--http', type=int, default=1,
        help='Disables the http server')

    # websocket
    parser.add_argument('--socket', type=int, default=1,
        help='Disables the websocket')

    args = parser.parse_args()

    http = None
    socket = None

    try:
        if args.http:
            http = start_http_server()

        if args.socket:
            socket = start_socket_server()

        if http:
            http.wait()

        if socket:
            socket.wait()

    except Exception as e:
        print(e)

        if http:
            http.terminate()

        if socket:
            socket.terminate()
