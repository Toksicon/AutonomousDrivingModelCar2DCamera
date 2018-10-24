#!/usr/bin/python

from ctypes import *
from PIL import Image, ImageDraw
import numpy as np
import os
import time


class CPicLib:
    def __init__(self, dll='libcpiclib'):
        self._dll = CDLL(dll)

        # (rgb, rgb) -> float
        self._dll.contrast.argtypes = [POINTER(c_uint8), POINTER(c_uint8)]
        self._dll.contrast.restype = c_float

        # (data, width, height) -> rgb[]
        self._dll.resolve_mid.argtypes = [np.ctypeslib.ndpointer(dtype=POINTER(c_uint8), ndim=1, flags='C'), c_uint, c_uint]
        self._dll.resolve_mid.restype = POINTER(c_uint)

    def contrast(self, rgb1, rgb2):
        return self._dll.contrast(np.asarray(rgb1), np.asarray(rgb2))

    def resolve_mid(self, image, samples=2):
        width = len(image[0])
        height = len(image)
        size = width * height * 3   # height * width * (r + g + b)

        ret = self._dll.resolve_mid(np.reshape(image, size), width, height)
        return np.ctypeslib.as_array(ret, shape=(height,))


if __name__ == '__main__':
    root_path = os.path.dirname(os.path.realpath(__file__))

    img = Image.open(os.path.join(root_path, 'image.png')).convert('RGB')
    image = np.asarray(img, dtype=c_uint8)
    # print(image)

    cpiclib = CPicLib()

    t0 = time.time()
    result = cpiclib.resolve_mid(image)
    t1 = time.time()

    print("Time: {:.3f}s".format((t1 - t0)))

    # result_arr = np.ctypeslib.as_array(result, shape=(_y,))
    # print(result_arr)

    draw = ImageDraw.Draw(img)

    for y in range(0, len(image)):
        mid = result[y]
        # print(mid)

        draw.line((mid, y) + (mid, y), fill=(255, 0, 0))

    img.save(os.path.join(root_path, 'out.png'))
    img.show()
