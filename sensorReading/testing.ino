#define TEST_PIN A0

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(TEST_PIN, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int value = analogRead(TEST_PIN);

  byte* byteData = (byte*)(&value);
  // Serial.write(byteData, 4);
  // Serial.write(byteData, 4);
  Serial.write(value);
}
