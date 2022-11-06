// Arduino Cyber Glove
#include <Mouse.h>      // Mouse Library

// Variables
const int PIN_FLEX_SENSOR = A0; // Flex Seneor Pin
const int PIN_Y = A2;   // Y Value Analog Pin  
const int PIN_X = A3;   // X Value Analog Pin

const int RANGE = 10;   // Output RANGE of X or Y movements for Mapped Values 
const int RESPONCE_DELAY = 8;  // Delay for mouse movements in milliseconds 
const int MOVEMENT_THRESHOLD = RANGE/8;    // Resting position threshold 
const int CENTRE =  RANGE/2;      // Resting position 

// Max and Mins set as not consistent for accelerometer
int MINIMA[] = {1023, 1023};   
int MAXIMA[] = {0, 0}; 

// Store Axis Pins
int AXES[] = {PIN_X, PIN_Y};   

// Values for calcuating and using resistance from voltage divider
const float VCC = 4.98; // Measured voltage of Ardunio 5V line
const float DIVIDER_RESISTANCE = 47500.0; // Measured resistance of 3.3k resistor
const float STR_RESISTANCE = 27412.86; // Resting Resistance (Resistance When Straight)
const float BENT_RESISTANCE = 90000.0; // resistance at 90 deg
const float RESISTANCE_THRESHOLD = 55000.0;

void setup() 
{
  Serial.begin(9600); // Initializing of Character Transfer Amount
  pinMode(PIN_FLEX_SENSOR, INPUT);  // Setting Pin Mode For Flex Sensor
  Mouse.begin();  // Run Mouse Extention
}

void loop() 
{
  // Get Acial DISTANCE From Centre.
    int X_DIST = getDISTANCE(0);
    int Y_DIST = getDISTANCE(1);
    
  /*
  // Accelerometer Print Statement
  Serial.print(analogRead(PIN_X));  
  Serial.print("\t");

  Serial.print(analogRead(PIN_Y));
  Serial.println();
  */
  
  Mouse.move(X_DIST, Y_DIST, 0); //Mouse.move(xPos, yPos, wheel); 
  delay(RESPONCE_DELAY);
  
  int ADC_FLEX = analogRead(PIN_FLEX_SENSOR); // READ Analog Value
  float V_FLEX = ADC_FLEX * VCC / 1023.0; // Calculate Voltage
  float R_FLEX = DIVIDER_RESISTANCE * (VCC / V_FLEX - 1.0); // Calculate Resistance
  float ANGLE = map(R_FLEX, STR_RESISTANCE, BENT_RESISTANCE, //Estimate bend Angle
                   0, 90.0);
  /*            
  // Resistance Print Statement
  Serial.println("The Resistance is : " + String(R_FLEX) + " ohms");  // Display Resistance              
  Serial.println("The Bend Angle is: " + String(ANGLE) + " degrees"); // Display Angle
  Serial.println();
  */

  // Left Click
  if (R_FLEX >= RESISTANCE_THRESHOLD) { 
      Mouse.click(MOUSE_LEFT);  // Triggering left Click   
      delay(180);           // Adding Delay
    }         

  delay(RESPONCE_DELAY);
}

// Method to Update MAXIMA and MINIMA
int getDISTANCE(int INDEX) {
  int DISTANCE = 0;    // DISTANCE from CENTRE of the output range 
  int READ = analogRead(AXES[INDEX]);

    // CHeck read value vs max and mins. Update accordingly
    if (READ < MINIMA[INDEX]) {
      MINIMA[INDEX] = READ; 
    }
  
    if (READ > MAXIMA[INDEX]) { 
        MAXIMA[INDEX] = READ; 
    }

    // Map the READ from the analog input range to the output range 
    READ = map(READ, MINIMA[INDEX], MAXIMA[INDEX], 0 , RANGE);
  
    // Calculate distance if threshold has been crossed 
    if (abs(READ - CENTRE) >= MOVEMENT_THRESHOLD) { 
      DISTANCE = (READ - CENTRE); 
    }

    // The X axis needs to be inverted in order to map the movement correctly
  if (INDEX == 1)  { 
    DISTANCE = -DISTANCE; 
  }
  
    return DISTANCE; 
}
