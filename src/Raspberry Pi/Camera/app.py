#!/usr/bin/python
import argparse
import pickle
import json
import numpy as np

from pymemcache.client import base
from time import time

from camera import Camera
from logger import logger, logging


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CarTV & Camera Controller')

    # debug
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables debug mode')

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    image_id = 1
    client = base.Client(('localhost', 11211))

    with Camera((384, 240)) as camera:
        while True:
            logger.info('>>> image {}'.format(image_id))

            t = time()
            captured_image = camera.capture()
            logger.debug('capturing time: {}'.format(time() - t))

            t = time()
            data = {
                'id': image_id,
                'format': 'rgb',
                'data': captured_image,
                'width': len(captured_image[0]),
                'height': len(captured_image)
            }

            client.set('captured_image', pickle.dumps(data), 1)
            logger.debug('serialization time: {}'.format(time() - t))

            image_id += 1
