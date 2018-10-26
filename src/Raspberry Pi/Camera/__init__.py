import numpy as np

try:
    from picamera import PiCamera
except:
    PiCamera = None
    print('Failed to load picamera module!')


class Camera:
    def __init__(self, resolution):
        if PiCamera:
            self._camera = PiCamera()
            self._camera.resolution = resolution

    def capture(self):
        if PiCamera:
            image_array = np.empty((self._camera.resolution[1], self._camera.resolution[0], 3), dtype=np.uint8)
            self._camera.capture(image_array, 'rgb')
            return image_array
        else:
            return np.empty((1, 1, 3), dtype=np.uint8)
