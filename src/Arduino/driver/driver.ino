#include "mcp_can.h"
#include <SPI.h>
#include <stdint.h>

unsigned char Flag_Recv = 0;
unsigned char len = 0;
unsigned char buf[8];
MCP_CAN CAN(10);

uint16_t bytesToInt16(char byte1, char byte2)
{
  return ((uint16_t)byte2 << 8) + byte1;
}

void setup()
{
  Serial.begin(115200);
  CAN.begin(CAN_500KBPS);                       // init can bus : baudrate = 500k  
}

void loop()
{
    if(CAN_MSGAVAIL == CAN.checkReceive())                           // check if get data
    {
      CAN.readMsgBuf(&len, buf);            // read data,  len: data length, buf: data buf
      Serial.print("Got a message from: ");
      uint16_t id = CAN.getCanId();
      Serial.println(id);

      if(id == 0x200) {
          Serial.print("Image sample received! ");
          uint16_t image_id = bytesToInt16(buf[0], buf[1]);
          uint8_t sample_count = buf[2];
          uint8_t sample_cur = buf[3];
          uint16_t sample_x = bytesToInt16(buf[4], buf[5]);
          uint16_t sample_y = bytesToInt16(buf[6], buf[7]);   
          Serial.print(image_id);Serial.print("\t");
          Serial.print(sample_count);Serial.print("\t");
          Serial.print(sample_cur);Serial.print("\t");
          Serial.print(sample_x);Serial.print("\t");
          Serial.print(sample_y);Serial.print("\t");
      }
      
      Serial.println();
    }
}
