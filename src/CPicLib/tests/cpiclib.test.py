#!/usr/bin/python

from ctypes import *


class CPicRGB(Structure):
    _fields_ = [('r', c_ubyte), ('g', c_ubyte), ('b', c_ubyte)]

    @staticmethod
    def create(rawRGB):
        if isinstance(rawRGB, list) or isinstance(rawRGB, tuple):
            return CPicRGB(rawRGB[0], rawRGB[1], rawRGB[2])
        elif isinstance(rawRGB, dict):
            return CPicRGB(rawRGB['r'], rawRGB['g'], rawRGB['b'])
        else:
            raise 'Failed to create CPicRGB from type ' + rawRGB

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
        self._dll.resolve_mid.restype = POINTER(CPicRGB)

    def contrast(self, rgb1, rgb2):
        return self._dll.contrast(CPicRGB.create(rgb1), CPicRGB.create(rgb2))

    def resolve_mid(self, image, samples=2):
        return self._dll.resolve_mid(CPicImage.create(image), c_uint(samples))
        


def main():
    cpiclib = CPicLib()
    print(cpiclib.resolve_mid(
        (
            (   (0, 0, 10), (10, 0, 0), (0, 0, 10), (0, 4, 0)  ),
            (   (0, 4, 2),  (0, 5, 2),  (0, 4, 2),  (4, 4, 0)  ),
        )
    ))

if __name__ == '__main__':
    main()
