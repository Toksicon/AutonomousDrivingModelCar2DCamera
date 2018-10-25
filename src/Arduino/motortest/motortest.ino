/*  Arduino DC Motor Control - PWM | H-Bridge | L298N  -  Example 01
    by Dejan Nedelkovski, www.HowToMechatronics.com
*/
#define in1 3
#define in2 4
#define enA 5
#define in3 7
#define in4 8
#define enB 9

int pulse = 0;

void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(enA, OUTPUT);
  // Set initial rotation direction
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}



void loop() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, pulse);
  
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enB, pulse);

  pulse += 5;
  if (pulse > 255) {
    pulse = 0;
  }

  delay(100);
}
