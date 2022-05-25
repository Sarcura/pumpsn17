
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//solenoids example: for 16 solenoids; controlled by PD (Pure Data) frontend; communication with OSC (open sound control)
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//pins:
/*
|      Teensy-Pin | connected to                    |
|-----------------+---------------------------------|
|               0 | Pin1 ULN-Chip1   (Solenoid1)    |
|               1 | Pin2 ULN-Chip1   (Solenoid2)    |
|               2 | Pin3 ULN-Chip1   (Solenoid3)    |
|               3 | Pin4 ULN-Chip1   (Solenoid4)    |
|               4 | Pin5 ULN-Chip1   (Solenoid5)    |
|               5 | Pin6 ULN-Chip1   (Solenoid6)    |
|               6 | Pin7 ULN-Chip1   (Solenoid7)    |
|               7 | Pin8 ULN-Chip1   (Solenoid8)    |
|                 |                                 |
|              20 | Pin1 ULN-Chip2   (Solenoid9)    |
|              19 | Pin2 ULN-Chip2   (Solenoid10)   |
|              18 | Pin3 ULN-Chip2   (Solenoid11)   |
|              17 | Pin4 ULN-Chip2   (Solenoid12)   |
|              16 | Pin5 ULN-Chip2   (Solenoid13)   |
|              15 | Pin6 ULN-Chip2   (Solenoid14)   |
|              14 | Pin7 ULN-Chip2   (Solenoid15)   |
|              13 | Pin8 ULN-Chip2   (Solenoid16)   |
|-----------------+---------------------------------|
*/


//initialize pins
//------------------------------
int s1=0;
int s2=1;
int s3=2;
int s4=3;
int s5=4;
int s6=5;
int s7=6;
int s8=7;
int s9=20;
int s10=19;
int s11=18;
int s12=17;
int s13=16;
int s14=15;
int s15=14;
int s16=13;

struct STRUCT {
  //define variables for solenoids, at the beginning 0 (=off)
  //------------------------------------------------------
  int inValue1 = 0;         
  int inValue2 = 0;         
  int inValue3 = 0;         
  int inValue4 = 0;         
  int inValue5 = 0;         
  int inValue6 = 0;         
  int inValue7 = 0;         
  int inValue8 = 0; 
  int inValue9 = 0;         
  int inValue10 = 0;         
  int inValue11 = 0;         
  int inValue12 = 0;  
  int inValue13 = 0;         
  int inValue14 = 0;         
  int inValue15 = 0;         
  int inValue16 = 0;
} ParsingStruct;

#include "SerialTransfer.h"

//int ledPin = 13;     // pin that the led is attached to
//int analogvalue = 0;

SerialTransfer myTransfer;

void setup()  
  {       
  
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);
  pinMode(s4, OUTPUT);
  pinMode(s5, OUTPUT);
  pinMode(s6, OUTPUT);
  pinMode(s7, OUTPUT);
  pinMode(s8, OUTPUT);
  pinMode(s9, OUTPUT);
  pinMode(s10, OUTPUT);
  pinMode(s11, OUTPUT);
  pinMode(s12, OUTPUT);
  pinMode(s13, OUTPUT);
  pinMode(s14, OUTPUT);
  pinMode(s15, OUTPUT);
  pinMode(s16, OUTPUT);
  
  Serial.begin(115200);
  myTransfer.begin(Serial);

  //for testing purposes
  //pinMode(ledPin, OUTPUT);  //set switch as input pin for rawdata-mode
  //digitalWrite (ledPin, LOW);
}

void loop()  
{

  if(myTransfer.available())
  {
    // find size of transferred message
    uint16_t recSize = 0;
    recSize = myTransfer.rxObj(ParsingStruct, recSize);
    
    // do the enable here, otherwise the stop condition and the motorX_en interfere

    digitalWrite(s1, ParsingStruct.inValue1);
    digitalWrite(s2, ParsingStruct.inValue2);
    digitalWrite(s3, ParsingStruct.inValue3);
    digitalWrite(s4, ParsingStruct.inValue4);
    digitalWrite(s5, ParsingStruct.inValue5);
    digitalWrite(s6, ParsingStruct.inValue6);
    digitalWrite(s7, ParsingStruct.inValue7);
    digitalWrite(s8, ParsingStruct.inValue8);
    digitalWrite(s9, ParsingStruct.inValue9);
    digitalWrite(s10, ParsingStruct.inValue10);
    digitalWrite(s11, ParsingStruct.inValue11);
    digitalWrite(s12, ParsingStruct.inValue12);
    digitalWrite(s13, ParsingStruct.inValue13);
    digitalWrite(s14, ParsingStruct.inValue14);
    digitalWrite(s15, ParsingStruct.inValue15);
    digitalWrite(s16, ParsingStruct.inValue16);
    
    // send all received data back to Python
    for(uint16_t i=0; i < myTransfer.bytesRead; i++)
      myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
    
    myTransfer.sendData(myTransfer.bytesRead);
  }

}  


