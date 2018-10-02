from picamera import PiCamera

camera = PiCamera()
camera.resolution = (360,240)
camera.capture("/home/pi/test.jpg")
print("Photo taken")
