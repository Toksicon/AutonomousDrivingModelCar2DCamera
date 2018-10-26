from PIL import Image

import numpy as np
import os
import sys
import time

from ..server import socketio

root_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(root_path, '../../../CPicLib/py/')))
from cpiclib import CPicLib


def processor():
    root_path = os.path.dirname(os.path.realpath(__file__))
    cpiclib = CPicLib()

    while True:
        img = Image.open(os.path.join(root_path, '../../../CPicLib/py/image.png')).convert('L')
        image = np.asarray(img, dtype=np.uint8)

        sobel_result = cpiclib.sobel_operator(image)
        mids = cpiclib.resolve_mid(sobel_result)

        socketio.emit('monitor', {
            'images': [
                {'name': 'Captured', 'data': image.tolist()},
                {'name': 'Sobel Operator', 'data': sobel_result.tolist()}
            ],
            'median': mids
        })

        time.sleep(1)


if __name__ == '__main__':
    processor()
