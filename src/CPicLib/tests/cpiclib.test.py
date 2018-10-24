#!/usr/bin/python

from ctypes import *
from PIL import Image, ImageDraw
import numpy as np
import os
import time


class CPicRGB(Structure):
    _fields_ = [('r', c_ubyte), ('g', c_ubyte), ('b', c_ubyte)]

    @staticmethod
    def create(rawRGB):
        if isinstance(rawRGB, list) or isinstance(rawRGB, tuple) or isinstance(rawRGB, np.ndarray):
            return CPicRGB(rawRGB[0], rawRGB[1], rawRGB[2])
        elif isinstance(rawRGB, dict):
            return CPicRGB(rawRGB['r'], rawRGB['g'], rawRGB['b'])
        else:
            raise Exception('Failed to create CPicRGB from type {}'.format(type(rawRGB)))

class CPicImage(Structure):
    _fields_ = [('data', POINTER(CPicRGB)), ('width', c_uint), ('height', c_uint)]

    @staticmethod
    def create(raw_image):
        image = CPicImage()
        image.width = len(raw_image[0])
        image.height = len(raw_image)

        image_data = (CPicRGB * (image.width * image.height))()
        image.data = cast(image_data, POINTER(CPicRGB))

        i = 0

        for raw_line in raw_image:
            for raw_pixel in raw_line:
                image_data[i] = CPicRGB.create(raw_pixel)
                i += 1

        return image


class CPicLib:
    def __init__(self, dll='libcpiclib'):
        self._dll = CDLL(dll)

        # (rgb, rgb) -> float
        self._dll.contrast.argtypes = [CPicRGB, CPicRGB]
        self._dll.contrast.restype = c_float

        # (image, samples) -> rgb[]
        self._dll.resolve_mid.argtypes = [CPicImage, c_uint]

    def contrast(self, rgb1, rgb2):
        return self._dll.contrast(CPicRGB.create(rgb1), CPicRGB.create(rgb2))

    def resolve_mid(self, image, samples=2):
        self._dll.resolve_mid.restype = POINTER(c_uint * len(image))
        return self._dll.resolve_mid(CPicImage.create(image), c_uint(samples))


if __name__ == '__main__':
    root_path = os.path.dirname(os.path.realpath(__file__))

    img = Image.open(os.path.join(root_path, 'image.png')).convert('RGB')
    image = np.asarray(img, dtype=c_uint8)
    print(image.shape)
    _y, _x, _z = image.shape

    t0 = time.time()

    fn = CDLL('libcpiclib').resolve_mid
    fn.argtypes = [np.ctypeslib.ndpointer(dtype=POINTER(c_uint8), ndim=1, flags='C'), c_uint, c_uint]
    fn.restype = POINTER(c_uint)

    # print(image)

    width = len(image[0])
    height = len(image)
    size = width * height * 3   # height * width * (r + g + b)

    ret = fn(np.reshape(image, size), width, height)
    result = np.ctypeslib.as_array(ret, shape=(height,))

    # result_arr = np.ctypeslib.as_array(result, shape=(_y,))
    # print(result_arr)

    # cpiclib = CPicLib()

    t1 = time.time()

    print("Time: {:.3f}s".format((t1 - t0)))

    draw = ImageDraw.Draw(img)

    for y in range(0, len(image)):
        mid = result[y]
        # print(mid)

        draw.line((mid, y) + (mid, y), fill=(255, 0, 0))

    img.save(os.path.join(root_path, 'out.png'))
    img.show()
