import os
import pickle
import sys
import time

from pymemcache.client import base
from server import socketio

root_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(root_path, '../../../')))
from CAN import Can
from CPicLib import CPicLib


def processor():
    cpiclib = CPicLib()

    client = base.Client(('localhost', 11211))
    last_image_id = 0

    with Can() as can:
        while True:
            raw_data = client.get('captured_image')
            if raw_data:
                img = pickle.loads(raw_data)
                gray_image = cpiclib.grayscale_filter(img['data'])
                edge_image = cpiclib.sobel_operator(gray_image)

                mid_points = cpiclib.detect_mid(edge_image)

                x_points = [int(p[0]) for p in mid_points]

                # TODO: move this to a standalone app
                can.send_messages_for_image_samples(x_points, img['id'])

            time.sleep(0.5)

if __name__ == '__main__':
    processor()
