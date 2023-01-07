#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

const uint64_t pipe = 0xE8E8F0F0E1LL;

RF24 radio(9, 10); // CE, CSN
float data[6];

double LX;
double LY;
int A;
int RX;
int RY;
double netF;
int netA;



void setup() {
  Serial.begin(19200);
  radio.begin();
  radio.openReadingPipe(1, pipe);
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
}

void loop() {
  if (radio.available()) {
    radio.read( data, sizeof(data));

    if (data[0] == 900)
    {
      LX = data[1];
      LY = data[2];
      A = data[3];
      
      netF = sqrt(sq(LX)+sq(LY));
      netF = sq(LX);
      netF += sq(LY);
      netF = sqrt(netF);
      
      netA = round( atan2 (LX, LY) * 180/3.14159265 ); // radians to degrees and rounding
    }
    
    if (data[0] == 1000)
    {
      RX = data[1];
      RY = data[2];
    }
Serial.print(LX);
Serial.print(" ");
Serial.print(LY);
Serial.print(" ");
Serial.print(A);
Serial.print(" ");
Serial.print(RX);
Serial.print(" ");
Serial.println(RY);
//Serial.print(" ");
//Serial.println(netF);
//Serial.print(" ");
//Serial.println(netA);
}
delay(50);
}
