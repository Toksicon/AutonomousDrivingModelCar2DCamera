#!/usr/bin/python

from ctypes import *


class CPicRGB(Structure):
    _fields_ = [('r', c_float), ('g', c_float), ('b', c_float)]

    @staticmethod
    def create(rawRGB):
        if isinstance(rawRGB, list) or isinstance(rawRGB, tuple):
            return CPicRGB(rawRGB[0], rawRGB[1], rawRGB[2])
        elif isinstance(rawRGB, dict):
            return CPicRGB(rawRGB['r'], rawRGB['g'], rawRGB['b'])
        else:
            raise 'Failed to create CPicRBG from type ' + type(rawRGB)


class CPicLib:
    def __init__(self, dll='libcpiclib.dll'):
        self._dll = CDLL(dll)
        self._dll.luminanace.restype = c_float

        self._dll.contrast.argtypes = [CPicRGB, CPicRGB]
        self._dll.contrast.restype = c_float

    def luminanace(self, r, g, b):
        return self._dll.luminanace(c_float(r), c_float(g), c_float(b))

    def contrast(self, rgb1, rgb2):
        return self._dll.contrast(CPicRGB.create(rgb1), CPicRGB.create(rgb2))


def main():
    cpiclib = CPicLib()
    print(cpiclib.luminanace(0, 0, 0.1))
    print(cpiclib.contrast(
        (255, 255, 255),
        (0, 0, 0)
    ))

if __name__ == '__main__':
    main()
