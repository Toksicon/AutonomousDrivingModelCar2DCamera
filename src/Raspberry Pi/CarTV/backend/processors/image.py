import os
import sys
import time

from ..server import socketio

root_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(root_path, '../../../')))
from Camera import Camera
from CAN import Can
from CPicLib import CPicLib


def processor():
    camera = Camera((384, 240))
    cpiclib = CPicLib()
    image_id = 1
    with Can() as can:
        while True:
            try:
                captured_image = camera.capture()

                gray_image = cpiclib.rgb_to_grayscale(captured_image)
                edge_image = cpiclib.sobel_operator(gray_image)

                mid_points = cpiclib.detect_mid(edge_image)

                x_points = [int(p[0]) for p in mid_points]

                can.send_messages_for_image_samples(x_points, image_id)
                image_id += 1

                socketio.emit('monitor', {
                    'images': [
                        {'name': 'Captured', 'data': captured_image.tolist(), 'format': 'rgb'},
                        {'name': 'Grayscale', 'data': gray_image.tolist(), 'format': 'grayscale'},
                        {'name': 'Sobel Operator', 'data': edge_image.tolist(), 'format': 'grayscale'}
                    ],
                    'median': mid_points
                })

                time.sleep(2)

            except Exception as e:
                print(e)
                exit()


if __name__ == '__main__':
    processor()
