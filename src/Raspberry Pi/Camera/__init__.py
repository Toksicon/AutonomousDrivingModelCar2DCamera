import numpy as np

try:
    from picamera import PiCamera
except:
    PiCamera = None
    print('Failed to load picamera module!')


class Camera:
    def __init__(self, resolution):
        self._camera = None

        if PiCamera:
            self._resolution = resolution

    def __enter__(self):
        if PiCamera:
            self._camera = PiCamera()
            self._camera.resolution = self._resolution

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if PiCamera:
            self._camera.close()
            self._camera = None

    def capture(self):
        if self._camera:
            image_array = np.empty((self._camera.resolution[1], self._camera.resolution[0], 3), dtype=np.uint8)
            self._camera.capture(image_array, 'rgb', use_vide_port=True)
            return image_array
        else:
            return np.empty((1, 1, 3), dtype=np.uint8)
