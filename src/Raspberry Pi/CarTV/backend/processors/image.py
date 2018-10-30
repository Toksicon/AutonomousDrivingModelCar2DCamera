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
    with Camera((384, 240)) as camera:
        cpiclib = CPicLib()
        image_id = 1
        last_emit = 0

        with Can() as can:
            while True:
                t0 = time.time()
                captured_image = camera.capture()
                t1 = time.time()
                print("TIME: ", t1 - t0)

                print('camera.captured')
                gray_image = cpiclib.grayscale_filter(captured_image)
                edge_image = cpiclib.sobel_operator(gray_image)

                mid_points = cpiclib.detect_mid(edge_image)

                x_points = [int(p[0]) for p in mid_points]

                can.send_messages_for_image_samples(x_points, image_id)
                image_id += 1


                if last_emit < time.time() - 0.4:
                    socketio.emit('monitor', {
                        'images': [
                            {
                                'name': 'Captured',
                                'data': captured_image.tobytes(),
                                'format': 'rgb',
                                'width': len(captured_image[0]),
                                'height': len(captured_image)
                            },
                            {
                                'name': 'Grayscale',
                                'data': gray_image.tobytes(),
                                'format': 'grayscale',
                                'width': len(gray_image[0]),
                                'height': len(gray_image)
                            },
                            {
                                'name': 'Sobel Operator',
                                'data': edge_image.tobytes(),
                                'format': 'grayscale',
                                'width': len(edge_image[0]),
                                'height': len(edge_image)
                            }
                        ],
                        'median': mid_points
                    })

                    last_emit = time.time()

if __name__ == '__main__':
    processor()
