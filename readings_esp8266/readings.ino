#include "dhtnew.h"

// https://github.com/RobTillaart/DHTNew/blob/master/examples/dhtnew_minimum/dhtnew_minimum.ino
DHTNEW airSensor(D6);

void setup() {
  // put your setup code here, to run once:
  setupSerial();
}

void setupSerial() {
  // Serial output for debugging
  Serial.begin(9600);
  while (!Serial) { delay(100); } // Wait for serial console to open!
}

void loop() {
  // air sensor
  if (DHTLIB_OK != airSensor.read()) {
    delay(500);
    return;
  }

  Serial.print(airSensor.getHumidity(), 2);
  Serial.print(",");
  Serial.print(airSensor.getTemperature(), 2);

  // moisture sensor
  Serial.print(",");
  Serial.println(analogRead(A0));
  
  // put your main code here, to run repeatedly:
  delay(2000);
}

