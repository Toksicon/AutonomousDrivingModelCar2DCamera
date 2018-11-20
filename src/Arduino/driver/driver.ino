#include "mcp_can.h"
#include <SPI.h>
#include <stdint.h>
#include "servotest.h"
#include "accelerometer.h"
#include <NewPing.h>
#include "LiquidCrystal_I2C.h"

#include "steering.h"


#define STEERING_SERVO_NUM 0
#define SPOILER_SERVO_NUM 1
#define PIN_X 2
#define PIN_Y 1
#define PIN_Z 0
#define SONAR_TRIGGER_PIN 2
#define SONAR_ECHO_PIN 6
#define SONAR_MAX_DISTANCE 200



NewPing sonar(SONAR_TRIGGER_PIN,SONAR_ECHO_PIN,SONAR_MAX_DISTANCE);

// Set the LCD address to 0x27 for a 16 chars and 2 line display
LiquidCrystal_I2C lcd(0x27, 16, 2);

void printReceivedMessage(uint16_t canID, uint16_t image_id, uint8_t sample_count, uint8_t sample_cur, uint16_t sample_x, uint16_t sample_y)
{
  if( canID == 0x200)
  {
    Serial.print("Printing received CAN Frame with ID: "); 
    Serial.println(canID);
    Serial.print(image_id);Serial.print("\t");
    Serial.print(sample_count);Serial.print("\t");
    Serial.print(sample_cur);Serial.print("\t");
    Serial.print(sample_x);Serial.print("\t");
    Serial.print(sample_y);Serial.print("\t");  
    Serial.println("");
  }  
}

uint16_t bytesToInt16(char byte1, char byte2)
{
  return ((uint16_t)byte2 << 8) + (uint16_t) byte1;
}

/*struct Sample
{
  uint16_t x;
  uint16_t y;
  Sample(uint16_t x, uint16_t y): x(x), y(y){}
};

struct Image
{
  uint16_t id;
 // std::vector<Sample> samples;  
  Image(uint16_t imageId, uint8_t sampleCount);
 // void push(const Sample& sample){ samples.push_back(sample);}
};
Image::Image(uint16_t imageId, uint8_t sampleCount): id(imageId){}*/

// Globals
unsigned char g_len = 0;
unsigned char g_buf[8];
// Image* g_image = NULL;
MCP_CAN CAN(10);
bool g_booted = false;
unsigned long g_time = 0;

void setup()
{
  randomSeed(analogRead(0));
  Serial.begin(115200);
  setupSpoiler(SPOILER_SERVO_NUM);
  // initialize the LCD
  lcd.begin();
  // Turn on the blacklight and print a message.
  lcd.backlight();

  setupSteering(STEERING_SERVO_NUM);
  
  CAN.begin(CAN_500KBPS);  // init can bus : baudrate = 500k  
}
void loop()
{    
    if(CAN_MSGAVAIL == CAN.checkReceive())                           // check if get data
    {
      g_booted = true;
      CAN.readMsgBuf(&g_len, g_buf);            // read data,  len: data length, buf: data buf
      int16_t id = CAN.getCanId();
      if(id == 0x200)
      {
          Serial.print("Correct frame received ");
          uint16_t image_id = bytesToInt16(g_buf[0], g_buf[1]);
          uint8_t sample_count = g_buf[2];
          uint8_t sample_cur = g_buf[3];
          uint16_t sample_x = bytesToInt16(g_buf[4], g_buf[5]);
          uint16_t sample_y = bytesToInt16(g_buf[6], g_buf[7]);
          if(sample_cur == 1 && sample_y > 45000) {
            Serial.print((sample_x) -32786);
            steer((int16_t)(sample_x-32786));
          }
          
               
      }
      else
      {
        Serial.print("CAN: RECEIVED TRASH from "); Serial.println(id);       
      }
      Serial.println();
    }
    
    Vec3D data = readAccelerometer(PIN_X, PIN_Y, PIN_Z);      
    char lcdBuf[16];
    
    if(g_time + 1000 < millis())
    {
      lcd.clear();
      sprintf(lcdBuf, "X=%5d  Y=%5d", data.x, data.y);  
      lcd.print(lcdBuf);
      lcd.setCursor(0,1);
      sprintf(lcdBuf, "Z=%5d  S=%5d ", data.z, (sonar.ping()/US_ROUNDTRIP_CM));
      lcd.print(lcdBuf);  
      g_time = millis();
    }
    if(!g_booted)
    {
      testServo();
    }
}
