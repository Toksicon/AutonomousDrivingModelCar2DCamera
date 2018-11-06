#!/usr/bin/python
import argparse
import pickle
import os
import sys
import time

from pymemcache.client import base

from lib import Can

root_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(root_path, '../')))
from CPicLib import CPicLib


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CarTV & Camera Controller')

    # debug
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables debug mode')

    args = parser.parse_args()

    cpiclib = CPicLib()
    client = base.Client(('localhost', 11211))
    last_image_id = 0

    with Can() as can:
        while True:
            raw_data = client.get('edge_detected_image')
            if raw_data:
                img = pickle.loads(raw_data)

                if img['id'] != last_image_id:
                    last_image_id = img['id']

                    mid_points = cpiclib.detect_mid(img['data'])
                    x_points = [int(p[0]) for p in mid_points]

                    can.send_messages_for_image_samples(x_points, img['id'])
                    time.sleep(0.5)  # delay for CAN
