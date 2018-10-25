/*************************************************** 
  Servo test for PCA9685  
  These drivers use I2C to communicate, 2 pins are required to  
  interface.
 ****************************************************/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  150 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  260 // this is the 'maximum' pulse length count (out of 4096)
#define SERVONUM  0 // our servo # counter

void setup() {
  Serial.begin(9600);
  Serial.println("Servotest!");

  pwm.begin();
  
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  delay(10);
}

void loop() {

  // map(value, fromLow, fromHigh, toLow, toHigh)
  double pulselength = map(-35, -35, 35, SERVOMAX, SERVOMIN);
  Serial.print(pulselength); Serial.println(" = Left");
  pwm.setPWM(SERVONUM, 0, pulselength);
  delay(5000);

  pulselength = map(0, -35, 35, SERVOMAX, SERVOMIN);
  Serial.print(pulselength); Serial.println(" = Center");
  pwm.setPWM(SERVONUM, 0, pulselength);
  delay(5000);

  pulselength = map(35, -35, 35, SERVOMAX, SERVOMIN);
  Serial.print(pulselength); Serial.println(" = Right");
  pwm.setPWM(SERVONUM, 0, pulselength);
  delay(5000);
  
}
