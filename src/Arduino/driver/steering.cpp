#include "steering.h"

// called this way, it uses the default address 0x40

static Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
static int g_servonumber;

#define STEERING_SERVOMIN  150 // this is the 'minimum' pulse length count (out of 4096)
#define STEERING_SERVOMAX  260 // this is the 'maximum' pulse length count (out of 4096)

void setupSteering(int servonumber){
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates    
  g_servonumber = servonumber;
}

void steer(int16_t value) { 
  // map(value, fromLow, fromHigh, toLow, toHigh)
  int number = random(0,71) - 35;
  double angle = map(value, -32786, 32785,-35, 35);
  //double pulselength = map(value, -32786, 32785, STEERING_SERVOMAX, STEERING_SERVOMIN);
  double pulselength = map(value, -12000, 12000, STEERING_SERVOMAX, STEERING_SERVOMIN);
  Serial.print("Steered");
  Serial.println(angle);
  pwm.setPWM(g_servonumber, 0, pulselength);
}
