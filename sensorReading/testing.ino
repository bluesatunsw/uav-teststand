#define TEST_PIN A0
#include <stdlib.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(TEST_PIN, INPUT);
}

void loop() {
  if (Serial.available() > 0) {
    ser = Serial.read()
    if (ser == 0xF0F0) {
      // begin motor testing 
      Serial.println(ser, HEX);
      delay(1000);
    }
  }
}
