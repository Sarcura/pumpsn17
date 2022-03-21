#include "SerialTransfer.h"

const int ledPin = 13;

SerialTransfer myTransfer;

struct STRUCT {
  float motor0_enable
  float motor0_direction;
  float motor0_speed;
  float motor1_enable
  float motor1_direction;
  float motor1_speed;
  float motor2_enable
  float motor2_direction;
  float motor2_speed;
  float motor3_enable
  float motor3_direction;
  float motor3_speed;
} testStruct;

void setup()
{
  Serial.begin(115200);
  myTransfer.begin(Serial);
  //for testing purposes
  pinMode(ledPin, OUTPUT);  //set switch as input pin for rawdata-mode
}

int counter = 0;
int average_nr = 10000;
int resolution = 12; //resolution in bit, 12bit = 4096 steps

//uint16_t arr[15] = {};

void loop()
{

  if(myTransfer.available())
  {
    // find size of transferred message
    uint16_t recSize = 0;
    recSize = myTransfer.rxObj(testStruct, recSize);
    
    //resolution = arr[2];
    //datapin_light1 = HIGH;
    //analogReadResolution(resolution);
    //analogReadAveraging(average_nr);
    //analogvalue = analogRead(datapin_light1); //read the incoming value from sensor 

    // send all received data back to Python
    for(uint16_t i=0; i < myTransfer.bytesRead; i++)
      myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
    
    myTransfer.sendData(myTransfer.bytesRead);

  }
}
