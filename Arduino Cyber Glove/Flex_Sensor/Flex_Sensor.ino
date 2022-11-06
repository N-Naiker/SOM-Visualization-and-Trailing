// Flex Sensor Test Code
const int PIN_FLEX_SENSOR = A0; // Pin connected to voltage divider output

const float VCC = 4.98; // Measured voltage of Ardunio 5V line
const float DIVIDER_RESISTANCE = 47500.0; // Measured resistance of 3.3k resistor

const float STR_RESISTANCE = 27412.86; // Resting Resistance (Resistance When Straight)
const float BENT_RESISTANCE = 90000.0; // resistance at 90 deg

void setup() 
{
  Serial.begin(9600); 
  pinMode(PIN_FLEX_SENSOR, INPUT);  // Setting Pin Mode For Flex Sensor
}

void loop() 
{
  int ADC_FLEX = analogRead(PIN_FLEX_SENSOR); // Reading Analog Value
  float V_FLEX = ADC_FLEX * VCC / 1023.0; // Calculate Voltage
  float R_FLEX = DIVIDER_RESISTANCE * (VCC / V_FLEX - 1.0); // Calculate Resistance
  float ANGLE = map(R_FLEX, STR_RESISTANCE, BENT_RESISTANCE, //Estimate bend Angle
                   0, 90.0);
  Serial.println("Resistance: " + String(R_FLEX) + " ohms");  // Display Resistance                 
  Serial.println("Angle: " + String(ANGLE) + " degrees"); // Display Angle
  Serial.println(); // Skip a Line

  delay(500);
  
}
