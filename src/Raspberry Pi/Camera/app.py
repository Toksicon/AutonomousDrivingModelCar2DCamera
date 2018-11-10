#!/usr/bin/python
import argparse
import numpy as np
import os
import pickle
import sys

from pymemcache.client import base
from PIL import Image, ImageDraw
from time import time

from camera import Camera
from logger import logger, logging

root_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(root_path, '../')))
from CPicLib import CPicLib


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

    cpiclib = CPicLib()

    with Camera((384, 240)) as camera:
        while True:
            logger.info('>>> image {}'.format(image_id))

            # capture image
            t = time()
            captured_image = camera.capture()
            logger.debug('capturing time: {}'.format(time() - t))

            # grayscale image
            t = time()
            grayscaled_image = cpiclib.grayscale_filter(captured_image)
            logger.debug('grayscale time: {}'.format(time() - t))

            # detect edges
            t = time()
            edge_detected_image = cpiclib.sobel_operator(grayscaled_image)
            logger.debug('edge_operator: {}'.format(time() - t))

            mid_points = cpiclib.detect_mid(edge_detected_image)
            mid_points_image = Image.fromarray(edge_detected_image)
            draw = ImageDraw.Draw(mid_points_image)
            for point in mid_points:
                draw.line((point[0] - 2, point[1] - 2, point[0] + 2, point[1] + 2), fill=255)
                draw.line((point[0] - 2, point[1] + 2, point[0] + 2, point[1] - 2), fill=255)
            del draw
            edge_detected_image = np.asarray(mid_points_image)

            # serialize captured image
            t = time()
            data = {
                'id': image_id,
                'format': 'rgb',
                'data': captured_image,
                'width': len(captured_image[0]),
                'height': len(captured_image)
            }

            client.set('captured_image', pickle.dumps(data), 1)
            logger.debug('captured image serialization time: {}'.format(time() - t))

            # serialize grayscaled image
            t = time()
            data['format'] = 'grayscale'
            data['data'] = grayscaled_image

            client.set('grayscaled_image', pickle.dumps(data), 1)
            logger.debug('grayscaled image serialization time: {}'.format(time() - t))

            # serialize edge detected image
            t = time()
            data['data'] = edge_detected_image

            client.set('edge_detected_image', pickle.dumps(data), 1)
            logger.debug('edge detected image serialization time: {}'.format(time() - t))

            image_id += 1
