import picamera
import picamera.array
from picamera.color import Color

def luminanace(r, g, b):
	def normalize_RGB(v):
		v /= 255
		return v / 12.92 if v <= 0.03928 else pow( (v + 0.055) / 1.055, 2.4 )
	a = list(map(normalize_RGB, list([r, g, b])))
	return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722

def contrast(rgb1, rgb2):
	return (luminanace(rgb1[0], rgb1[1], rgb1[2]) + 0.05) / (luminanace(rgb2[0], rgb2[1], rgb2[2]) + 0.05)

contrast([255, 255, 255], [255, 255, 0]) # 1.074 for yellow
contrast([255, 255, 255], [0, 0, 255]) # 8.592 for blue
# minimal recommended contrast ratio is 4.5, or 3 for larger font-sizes

with picamera.PiCamera() as camera:
	camera.resolution = (360,240)
	camera.capture("/home/pi/testimage.jpg")
	with picamera.array.PiRGBArray(camera) as output:
		camera.capture(output, 'rgb')
		print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))
		for RGB_matrix_y in range(240):
			last_pixel = None
			max_contrast = 0
			max_contrast_pixel = None
			for RGB_matrix_x in range(360):
				pixel = output.array[RGB_matrix_y][RGB_matrix_x]
				pixel = Color(pixel[0],pixel[1],pixel[2])
				if last_pixel is None:
					last_pixel = pixel
					continue
				#actual_contrast = contrast(last_pixel,output.array[RGB_matrix_y][RGB_matrix_x])
				actual_contrast = pixel.difference(last_pixel)
				print(actual_contrast)
				if actual_contrast > max_contrast:
					max_contrast = actual_contrast
					max_contrast_pixel = (RGB_matrix_x,RGB_matrix_y)
			print(max_contrast_pixel)
