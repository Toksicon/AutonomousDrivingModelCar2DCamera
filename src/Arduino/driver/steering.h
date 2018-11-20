/***************************************************
Servo test for PCA9685
These drivers use I2C to communicate, 2 pins are required to
interface.
****************************************************/
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>


#define SPOILER_SERVOMIN  200 // this is the 'minimum' pulse length count (out of 4096)
#define SPOILER_SERVOMAX  250 // this is the 'maximum' pulse length count (out of 4096)

void setupSteering(int servonumber);

void steer(int16_t value);
