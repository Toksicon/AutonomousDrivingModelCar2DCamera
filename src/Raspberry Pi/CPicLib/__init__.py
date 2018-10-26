#!/usr/bin/python

from ctypes import *
from PIL import Image, ImageDraw
import numpy as np
import os
import time


class CPicLib:
    def __init__(self, dll='libcpiclib'):
        dll_path = os.path.dirname(os.path.realpath(__file__))

        if os.name == 'nt':
            dll_path = os.path.join(dll_path, 'build/' + dll + '.dll')
        else:
            dll_path = os.path.join(dll_path, 'build/' + dll + '.so')

        dll_path = os.path.abspath(dll_path)
        self._dll = CDLL(dll_path)

        # (data, width, height) -> rgb[]
        self._dll.resolve_mid.argtypes = [
            np.ctypeslib.ndpointer(  # data
                dtype=c_uint8, ndim=1, flags='C_CONTIGUOUS'),
            c_uint,  # width
            c_uint,  # height
            c_uint,  # samples
            np.ctypeslib.ndpointer(  # out
                dtype=c_uint, ndim=1, flags='C_CONTIGUOUS')
        ]
        self._dll.resolve_mid.restype = None

        self._dll.sobel_operator.argtypes = [
            np.ctypeslib.ndpointer(  # data
                dtype=c_uint8, ndim=1, flags='C_CONTIGUOUS'),
            c_uint,  # width
            c_uint,  # height
            np.ctypeslib.ndpointer(  # out
                dtype=c_uint8, ndim=1, flags='C_CONTIGUOUS')
        ]
        self._dll.sobel_operator.restype = None

        self._dll.rgb_to_grayscale.argtypes = [
            np.ctypeslib.ndpointer(  # data
                dtype=c_uint8, ndim=1, flags='C_CONTIGUOUS'),
            c_uint,  # width
            c_uint,  # height
            np.ctypeslib.ndpointer(  # out
                dtype=c_uint8, ndim=1, flags='C_CONTIGUOUS')
        ]
        self._dll.rgb_to_grayscale.restype = None

    def resolve_mid(self, image, samples=10):
        width = len(image[0])
        height = len(image)
        size = width * height

        output = np.empty(dtype=c_uint, shape=(samples * 2,))
        self._dll.resolve_mid(np.reshape(image, size), width, height, samples, output)

        mids = []

        for i in range(0, samples):
            mid = (output[i * 2], output[i * 2 + 1])

            if mid[1] < width:
                mids.append((int(mid[0]), int(mid[1])))

        return mids

    def rgb_to_grayscale(self, image):
        # uint8_t* image, uint_t width, uint_t height, uint8_t* out
        width = len(image[0])
        height = len(image)
        size = width * height * 3
        data = np.reshape(image, size)

        output = np.empty(dtype=c_uint8, shape=(height * width,))
        self._dll.rgb_to_grayscale(data, width, height, output)
        return np.reshape(output, (height, width))

    def sobel_operator(self, image):
        width = len(image[0])
        height = len(image)
        size = width * height
        data = np.reshape(image, size)

        output = np.empty(dtype=c_uint8, shape=((height - 2) * (width - 2),))
        self._dll.sobel_operator(data, width, height, output)
        return np.reshape(output, (height - 2, width - 2))


if __name__ == '__main__':
    root_path = os.path.dirname(os.path.realpath(__file__))

    img = Image.open(os.path.join(root_path, 'image.png')).convert('RGB')
    image = np.asarray(img, dtype=c_uint8)
    # print(image)

    cpiclib = CPicLib()

    t0 = time.time()

    image = cpiclib.rgb_to_grayscale(image)
    Image.fromarray(image).show()
    sobel_result = cpiclib.sobel_operator(image)
    mids = cpiclib.resolve_mid(sobel_result)

    t1 = time.time()
    print("Time: {:.3f}s".format((t1 - t0)))

    # print(mids)
    # print(sobel_result)
    sobel_image = Image.fromarray(sobel_result).convert('RGB')

    draw = ImageDraw.Draw(sobel_image)

    for mid in mids:
        draw.line((mid[1] - 1, mid[0] - 1) + (mid[1] + 1, mid[0] + 1), fill=(255, 0, 0))
        draw.line((mid[1] - 1, mid[0] + 1) + (mid[1] + 1, mid[0] - 1), fill=(255, 0, 0))

    sobel_image.save(os.path.join(root_path, 'out.png'))
    sobel_image.show()
