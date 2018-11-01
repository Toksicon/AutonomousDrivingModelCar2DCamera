#!/usr/bin/python
import argparse
from camera import Camera


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CarTV & Camera Controller')

    # debug
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables debug mode')

    # image processor
    parser.add_argument('--process-images', type=int, default=1,
        help='Disables the image processor (camera and can)')

    # telemetry processor
    parser.add_argument('--process-telemetry', type=int, default=1,
        help='Disables the image telemetry (psutil)')

    args = parser.parse_args()

    image_id = 1

    with Camera((384, 240)) as camera:
        while True:
            captured_image = camera.capture()
            image_id += 1        
