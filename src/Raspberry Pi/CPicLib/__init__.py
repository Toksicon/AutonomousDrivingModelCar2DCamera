#!/usr/bin/python

from ctypes import *
from PIL import Image, ImageDraw
import numpy as np
import os
import time


class CPicLib:
    def __init__(self, dll='libcpiclib'):
        # resolve c-lib: absolute path is required for *nix,
        # as it doesn't search in working directory
        dll_path = os.path.dirname(os.path.realpath(__file__))

        if os.name == 'nt':  # on windows: assume .dll
            dll_path = os.path.join(dll_path, 'build/' + dll + '.dll')
        else:   # on non-windows: assume .so
            dll_path = os.path.join(dll_path, 'build/' + dll + '.so')

        dll_path = os.path.abspath(dll_path)

        # open dll and define the available function signatures
        self._dll = CDLL(dll_path)

        image_ptr = np.ctypeslib.ndpointer(dtype=c_uint8, ndim=1, flags='C_CONTIGUOUS')
        pxlist_ptr = np.ctypeslib.ndpointer(dtype=c_uint, ndim=1, flags='C_CONTIGUOUS')
        float_ptr = np.ctypeslib.ndpointer(dtype=c_float, ndim=1, flags='C_CONTIGUOUS')

        operator_argtypes = [
            image_ptr,  # data
            c_uint,     # width
            c_uint,     # height
            image_ptr   # out
        ]

        detection_argtypes = [
            image_ptr,  # data
            c_uint,     # width
            c_uint,     # height
            c_uint,     # samples
            pxlist_ptr  # out
        ]

        self._dll.detect_mid.argtypes = detection_argtypes

        self._dll.kernel_operator.argtypes = [
            image_ptr,  # data
            c_uint,     # width
            c_uint,     # height
            float_ptr,  # kernel_x[9]
            float_ptr,  # kernel_y[9]
            image_ptr   # out
        ]

        self._dll.prewitt_operator.argtypes = operator_argtypes
        self._dll.sobel_operator.argtypes = operator_argtypes
        self._dll.canny_edge_detection.argtypes = [
            image_ptr,  # data
            c_uint,     # width
            c_uint,     # height

            c_int,      # tmin
            c_int,      # tmax

            c_float,    # sigma

            image_ptr   # out
        ]
        self._dll.grayscale_filter.argtypes = operator_argtypes

    def _image_shape(self, image):
        width = len(image[0])
        height = len(image)
        size = width * height

        return (width, height, size)

    ''' Generic kernel operator (used in Sobel and Prewitt).
        @param image     2-dimensional numpy array [y][x] (grayscale).

        @param kernel_x  2-dimensional numpy array [3][3]
        @param kernel_y  2-dimensional numpy array [3][3]

        @return     2-dimensional numpy array [y][x] (grayscale).
    '''
    def kernel_operator(self, image, kernel_x, kernel_y):
        (width, height, size) = self._image_shape(image)

        output = np.empty(dtype=c_uint8, shape=(size,))
        self._dll.kernel_operator(
            np.reshape(image, size), width, height,
            np.reshape(kernel_x, (9,)), np.reshape(kernel_y, (9,)),
            output)

        return np.reshape(output, (height, width))

    ''' Creates an image with applied Prewitt operator to the given image.
        @param image     2-dimensional numpy array [y][x] (grayscale).

        @return     2-dimensional numpy array [y][x] (grayscale).
    '''
    def sobel_operator(self, image):
        (width, height, size) = self._image_shape(image)

        output = np.empty(dtype=c_uint8, shape=(size,))
        self._dll.sobel_operator(
            np.reshape(image, size), width, height,
            output)

        return np.reshape(output, (height, width))

    ''' Creates an image with applied Sobel operator to the given image.
        @param image     2-dimensional numpy array [y][x] (grayscale).

        @return     2-dimensional numpy array [y][x] (grayscale).
    '''
    def prewitt_operator(self, image):
        (width, height, size) = self._image_shape(image)

        output = np.empty(dtype=c_uint8, shape=(size,))
        self._dll.prewitt_operator(
            np.reshape(image, size), width, height,
            output)

        return np.reshape(output, (height, width))

    ''' TODO: comments
    '''
    def canny_edge_detection(self, image, tmin=45, tmax=50, sigma=1.0):
        (width, height, size) = self._image_shape(image)

        output = np.empty(dtype=c_uint8, shape=(size,))
        self._dll.canny_edge_detection(
            np.reshape(image, size), width, height,
            c_int(tmin), c_int(tmax), c_float(sigma),
            output)

        return np.reshape(output, (height, width))

    ''' Detects mids of the road for a given count of samples.
        @param image     2-dimensional numpy array [y][x] (grayscale).
        @param samples   Amount of samples to take from the image (samples < (height - 2))

        @return     List of mids (y, x) of the road.
    '''
    def detect_mid(self, image, samples=10):
        (width, height, size) = self._image_shape(image)

        output = np.empty(dtype=c_uint, shape=(samples * 2,))
        self._dll.detect_mid(
            np.reshape(image, size), width, height,
            samples,
            output)

        mids = []

        for i in range(0, samples):
            mid = (output[i * 2], output[i * 2 + 1])

            if mid[1] < width:
                mids.append((int(mid[0]), int(mid[1])))

        return mids

    ''' Creates a grayscaled image from a rgb image.
        @param image     3-dimensional numpy array [y][x][RGB]

        @return     2-dimensional numpy array [y][x] (grayscale).
    '''
    def grayscale_filter(self, image):
        (width, height, size) = self._image_shape(image)

        output = np.empty(dtype=c_uint8, shape=(size,))
        self._dll.grayscale_filter(
            np.reshape(image, size * 3), width, height,
            output)

        return np.reshape(output, (height, width))


if __name__ == '__main__':
    root_path = os.path.dirname(os.path.realpath(__file__))

    img = Image.open(os.path.join(root_path, 'samples/image.png')).convert('RGB')
    image = np.asarray(img, dtype=c_uint8)
    # print(image)

    cpiclib = CPicLib()

    t0 = time.time()

    image = cpiclib.grayscale_filter(image)
    # Image.fromarray(image).show()
    sobel_result = cpiclib.canny_edge_detection(image, tmin=45, tmax=50, sigma=1)
    mids = cpiclib.detect_mid(sobel_result)

    t1 = time.time()
    print("Time: {:.3f}s".format((t1 - t0)))

    # print(mids)
    # print(sobel_result)
    sobel_image = Image.fromarray(sobel_result).convert('RGB')

    draw = ImageDraw.Draw(sobel_image)

    for mid in mids:
        draw.line((mid[1] - 1, mid[0] - 1) + (mid[1] + 1, mid[0] + 1), fill=(255, 0, 0))
        draw.line((mid[1] - 1, mid[0] + 1) + (mid[1] + 1, mid[0] - 1), fill=(255, 0, 0))

    sobel_image.save(os.path.join(root_path, 'samples/out.png'))
    sobel_image.show()
