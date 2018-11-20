#!/usr/bin/env python
from flask import Flask, send_from_directory, Response
from time import sleep, time

from pymemcache.client import base
from PIL import Image

from logger import logger, logging

import argparse
import io
import numpy as np
import os
import pickle
import re
import sys

root_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(root_path, '../../../')))
from CPicLib import CPicLib


app = Flask('http')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if re.match(r'^(css|js|img|font)/', path):
        return send_from_directory(os.path.join(root_path, '../../static'), path)
    else:
        return send_from_directory(os.path.join(root_path, '../../static'), 'index.html')


def gen(image_key):
    cpiclib = CPicLib()

    client = base.Client(('localhost', 11211))
    last_image_id = 0

    while True:
        raw_data = client.get(image_key)
        if raw_data:
            # t = time()
            img = pickle.loads(raw_data)
            # print('loads', time() - t)

            if img['id'] != last_image_id:
                # t = time()
                fp = io.BytesIO()
                Image.fromarray(img['data']).save(fp, 'jpeg')
                # print('toJPEG', time() - t)

                # t = time()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + bytes(fp.getvalue()) + b'\r\n')
                # print('send', time() - t)


@app.route('/video_feed', defaults={'path': ''})
@app.route('/video_feed/', defaults={'path': ''})
@app.route('/video_feed/<path:path>')
def video_feed(path):
    keys = ['grayscaled_image', 'edge_detected_image', 'edge_detected_image_with_info']
    key = path if path in keys else 'captured_image'

    return Response(gen(key),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CarTV - HTTP Server')

    # debug
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables debug mode')

    # host
    parser.add_argument('--host', action='store', default='0.0.0.0',
        help='Specify the host for CarTV')

    # port
    parser.add_argument('--http-port', action='store', type=int, default=8080,
        help='Specify the port for the http server')

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    app.run(host=args.host, port=args.http_port, debug=args.debug, threaded=True, use_reloader=False)
