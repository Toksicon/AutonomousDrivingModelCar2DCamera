#!/usr/bin/python
import argparse
import subprocess
import sys


def start_car_tv():
    call = [sys.executable, 'CarTV/app.py']
    call.extend(sys.argv[1:])

    return subprocess.Popen(call)


def start_camera():
    call = [sys.executable, 'Camera/app.py']
    # call.extend(sys.argv[1:])

    return subprocess.Popen(call)


def start_can():
    call = [sys.executable, 'CAN/app.py']
    # call.extend(sys.argv[1:])

    return subprocess.Popen(call)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CarTV & Camera Controller')

    # TODO: disable CarTV option
    # TODO: fix passthrough args

    # debug
    parser.add_argument('-d', '--debug', action='store_true',
        help='Enables debug mode')

    # CAN processor
    parser.add_argument('--process-can', type=int, default=1,
        help='Enables/Disables CAN module')

    # image processor
    parser.add_argument('--process-images', type=int, default=1,
        help='Enables/Disables the image processor (camera and can)')

    # telemetry processor
    parser.add_argument('--process-telemetry', type=int, default=1,
        help='Enables/Disables the image telemetry (psutil)')

    args = parser.parse_args()

    can = None
    car_tv = None
    camera = None

    try:
        if args.process_images:
            camera = start_camera()

        if args.process_can:
            can = start_can()

        car_tv = start_car_tv()

        if camera:
            camera.wait()

        if car_tv:
            car_tv.wait()

    except Exception as e:
        print(e)

        if args.process_can:
            can.terminate()

        if car_tv:
            car_tv.terminate()

        if camera:
            camera.terminate()
