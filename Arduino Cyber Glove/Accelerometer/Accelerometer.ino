
// Accelerometer Test Code
const int PIN_X = A3;                  // x-axis 
const int PIN_Y = A2;                  // y-axis

void setup() {
  Serial.begin(9600); // Serial Communications Initialized
}

void loop() {
  Serial.print(analogRead(PIN_X));  
  Serial.print("\t");

  Serial.print(analogRead(PIN_Y));
  Serial.println();

  delay(100);
}
