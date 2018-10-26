#include "mcp_can.h"
#include <SPI.h>
#include <Stepper.h>

unsigned char Flag_Recv = 0;
unsigned char len = 0;
unsigned char buf[8];
MCP_CAN CAN(10);
Stepper myStepper(200,0,1,2,3,4);

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
      Serial.println("CAN_BUS GET DATA!");
      Serial.print("Got a message from: ");
      Serial.println(CAN.getCanId());
      Serial.print("data len = ");
      Serial.println(len);
      
      for(int i = 0; i<len; i++)            // print the data
      {
        Serial.print(buf[i]);Serial.print("\t");
      }
      Serial.println();
    }
    myStepper.setSpeed(100);
    myStepper.step(2);
}
