#include "servotest.h"

// called this way, it uses the default address 0x40

static Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
static int g_servonumber;


void setupSpoiler(int servonumber){
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates    
  g_servonumber = servonumber;
}

void testServo() { 
  // map(value, fromLow, fromHigh, toLow, toHigh)
	double pulselength = map(random(0,71) - 35, -35, 35, SPOILER_SERVOMAX, SPOILER_SERVOMIN);	
	pwm.setPWM(g_servonumber, 0, pulselength);
}
