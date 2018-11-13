#include <Arduino.h>
#include "accelerometer.h"

Vec3D readAccelerometer(int pinX, int pinY, int pinZ) {

	Vec3D data;
	data.x = analogRead(pinX) - 332;
	data.y = analogRead(pinY) - 401;
	data.z = analogRead(pinZ) - 340;
	return data;
}
