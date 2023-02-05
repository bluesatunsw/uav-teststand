// read sensor and send the reading over serial 

int sensorPin = A0;   // connect sensor to analog pin (A0)
int ledPin = 13;       // digital pin 13 (testing with LED)
int sensorValue;      // variable for storing sensor reading

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);           // set baudrate  
  Serial.println("Ready!!!");
}

void loop() {
  sensorValue = analogRead(sensorPin);  // read sensor value
  Serial.println(sensorValue);          // output reading to serial monitor
  if (sensorValue < 500) {
    digitalWrite(ledPin, LOW);          // turn LED off
  }
  else {
    digitalWrite(ledPin, HIGH);         // turn LED on
  }
  delay(100);                           // pause in ms before next reading  
}
