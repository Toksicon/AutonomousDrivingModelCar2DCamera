#!/usr/bin/python
import argparse
import pickle
import json
import numpy as np
import time

from pymemcache.client import base

from camera import Camera


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CarTV & Camera Controller')

    # debug
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables debug mode')

    args = parser.parse_args()

    image_id = 1
    client = base.Client(('localhost', 11211))

    with Camera((384, 240)) as camera:
        while True:
            # print(image_id)
            # t0 = time.time()
            captured_image = camera.capture()
            # t1 = time.time()
            # print('capture', t1 - t0)
            data = {
                'id': image_id,
                'format': 'rgb',
                'data': captured_image,
                'width': len(captured_image[0]),
                'height': len(captured_image)
            }
            # t2 = time.time()
            # print('serialize', t2 - t1)

            client.set('captured_image', pickle.dumps(data), 1)
            
            # t3 = time.time()
            # print('set', t3 - t2)
            image_id += 1
