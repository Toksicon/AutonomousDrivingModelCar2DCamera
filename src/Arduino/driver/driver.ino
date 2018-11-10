#include "ArduinoSTL.h"
#include "mcp_can.h"
#include <SPI.h>
#include <stdint.h>
#include <vector>

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
  return ((uint16_t)byte2 << 8) + byte1;
}

struct Sample
{
  uint16_t x;
  uint16_t y;
  Sample(uint16_t x, uint16_t y): x(x), y(y){}
};

struct Image
{
  uint16_t id;
  std::vector<Sample> samples;  
  Image(uint16_t imageId, uint8_t sampleCount);
  void push(const Sample& sample){ samples.push_back(sample);}
};
Image::Image(uint16_t imageId, uint8_t sampleCount): id(imageId){}

// Globals
unsigned char g_len = 0;
unsigned char g_buf[8];
Image* g_image = NULL;
MCP_CAN CAN(10);

void setup()
{
  Serial.begin(115200);
  CAN.begin(CAN_500KBPS);                       // init can bus : baudrate = 500k  
}

void loop()
{
    
    if(CAN_MSGAVAIL == CAN.checkReceive())                           // check if get data
    {
      CAN.readMsgBuf(&g_len, g_buf);            // read data,  len: data length, buf: data buf
      uint16_t id = CAN.getCanId();
      if(id == 0x200) {
          Serial.print("Image sample received! ");
          uint16_t image_id = bytesToInt16(g_buf[0], g_buf[1]);
          uint8_t sample_count = g_buf[2];
          uint8_t sample_cur = g_buf[3];
          uint16_t sample_x = bytesToInt16(g_buf[4], g_buf[5]);
          uint16_t sample_y = bytesToInt16(g_buf[6], g_buf[7]);   
          printReceivedMessage(id, image_id, sample_count, sample_cur, sample_x, sample_y);
          Sample sample(sample_x, sample_y);
          if(g_image == NULL)
          {
            g_image = new Image(image_id, sample_count);            
          }
          
          if(image_id != g_image->id)
          {
            delete g_image;
          }
          g_image->push(sample);
          
          
      }
      
      Serial.println();
    }
}
