import numpy as np
from picamera import PiCamera


class Camera:
    def __init__(self, resolution):
        self._camera = PiCamera()
        self._camera.resolution = resolution

    def capture(self):
        image_array = np.empty((self._camera.resolution[1], self._camera.resolution[0], 3), dtype=np.uint8)
        self._camera.capture(image_array, 'rgb')
        return image_array
