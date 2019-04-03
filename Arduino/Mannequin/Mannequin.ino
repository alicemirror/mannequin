/**
 * @file Mannequin.ino
 * @brief Main application program
 */

#include <Streaming.h>
#include "parameters.h"
#include "commands.h"
 
//! Create Instance of Stepper library
Stepper torsoStepper(STEPS_PER_REVOLUTION, STEP_PIN_A1, STEP_PIN_A2, STEP_PIN_B1, STEP_PIN_B2);
//! Motion control structure
StepProfile torsoControl;

//! Interactive Neopixel control parameters
neoPixParameters lightsControl;

//! Creates the Neopixel strip instance
Adafruit_NeoPixel lights = Adafruit_NeoPixel(NEOPIXEL_COUNT, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);

//! Initialization
void setup()
{
  Serial.begin(9600);

  // Initialize the endswitch input
  pinMode(ENDSWITCH_PIN, INPUT_PULLUP);
  // Initialize the stepper class  
   torsoStepper.step(STEPS_PER_REVOLUTION);
  // Move to zero point
  // setTorsoZero();

  lights.begin();
  lights.show(); // Initialize all pixels to 'off'

  lightsControl.color = 0;
  lightsControl.stepDelay = LIGHT_STATIC_DELAY;
  lightsControl.timerCounter = 0;
}

void loop() 
{
//  // Run test
//  setTorsoZero();
//  delay(5000);

  interactiveFlashColor(lights.Color(0, 16, 128));
  interactiveLights();
//  delay(10);

}

//==================================================
// Command functions
//==================================================

//! Set speed for the motor. Speed must  be one of
//! the predefined speed
void setTorsoSpeed(int mSpeed) {
 switch(mSpeed) {
  case ID_LOW:
    torsoControl.torsoSpeed = SPEED_LOW;
  break;
  case ID_MED:
    torsoControl.torsoSpeed = SPEED_MED;
  break;
  case ID_HIGH:
    torsoControl.torsoSpeed = SPEED_HIGH;
  break;
  case ID_ZERO:
    torsoControl.torsoSpeed = SPEED_ZERO;
  break;
 }
}

/**
 * Search the endstop switch moving to left then 
 * move to the middle and start accepting commands.
 * This function is used once on startup
 */
void setTorsoZero() {
  // Initialize the parameters for zero search
  torsoControl.rotAngle = 0;
  torsoControl.lastAnglePos = 0;
  torsoControl.torsoSpeed = SPEED_ZERO;

  // Search loop
  while(checkEndStop() == false) {
    torsoControl.rotAngle += SEARCH_ZERO_STEPS;
    moveTorso();
  } // Search loop
  torsoControl.lastAnglePos = MIN_ANGLE;
  torsoControl.torsoSpeed = SPEED_HIGH;
  torsoControl.rotAngle = MAX_ANGLE;
  moveTorso();
  torsoControl.torsoSpeed = SPEED_MED;
  torsoControl.rotAngle = MIN_ANGLE;
  moveTorso();
  torsoControl.torsoSpeed = SPEED_LOW;
  torsoControl.rotAngle = MAX_ANGLE / 2;
  moveTorso();
}

//! Check if the endstop switch is set
//!
//! @return True if the switch is set else return false.
bool checkEndStop() {
  if(digitalRead(ENDSWITCH_PIN) == false) {
    return true;
  } else {
    return false;
  }
}

/**
 * Move the motor to the new angle, if differs from the last.
 * The new position is the difference between the last angle and
 * the new rotation angle. The angle value is converted to motor
 * steps.
 */
void moveTorso() {
  if(torsoControl.rotAngle != torsoControl.lastAnglePos) {
    // Set the motion speed
    torsoStepper.setSpeed(torsoControl.torsoSpeed);
    //! Calculate the number of steps corresponding to the algebraic difference
    //! between the new angle and the current position
    int newAngle = torsoControl.rotAngle - torsoControl.lastAnglePos;
    
    //! Number of steps based on the new position    
    double moveSteps = 360 / STEPS_PER_REVOLUTION * ANGLE_DEMULTIPLIER * newAngle;
    
    // Move the motor testing the entire rotation range.
    torsoStepper.step(moveSteps);
    torsoControl.lastAnglePos = torsoControl.rotAngle;
  }
}

//==================================================
// NeoPixel
//==================================================

//! Manage the light effects depending on the last user interaction
void interactiveLights(){

//  switch(unreal.lightScheme){
//    case LIGHT_STATIC:
//      interactiveRotatingRainbow();
//    break;
//    case LIGHT_ROSE:
//      interactiveColorCycle();
//    break;
//    case LIGHT_DUCK:
//      interactiveFlashColor(lights.Color(0, 16, 128));
//    break;
//    case LIGHT_TRAIN:
//      if(unreal.isTrainOn){
//        interactiveColor(lights.Color(lightsControl.colorRGB, 256 - lightsControl.colorRGB, 128 - lightsControl.colorRGB));
//        #ifdef _DEBUG
//        Serial << "TrainOn - colorRGB " << lightsControl.colorRGB << endl;
//        #endif
//      }
//    break;
//  }
}


// Fill the dots one after the other with a color
/**
 * \brief Progressive fill all the LEDs with the same color
 * 
 * \param c The 320-bit encoded color
 * \param wait The step delay (ms)
 */
void color(uint32_t c, uint8_t wait) {
  
  for(uint16_t i = 0; i < lights.numPixels(); i++) {
    lights.setPixelColor(i, c);
    lights.show();
    delay(wait);
  }
}

/**
 * Cycle all the lights LEDS in sequence over all the 256 RGB combinations
 * 
 * \param low The lowest color value of the cycle range
 * \param high The highest color values of the cycle range
 * \param delay The delay cycle changing colors
 */
void rainbow(uint8_t low, uint8_t high, uint8_t wait) {
  uint16_t i, j;

  for(j = low; j < high; j++) {
    for(i = 0; i < lights.numPixels(); i++) {
      lights.setPixelColor(i, calcColor((i+j) & 255));
    }
    lights.show();
    delay(wait);
  }
}

/**
 * \brief Progressive fill all the LEDs with the same color, then alternatively
 * flash the sequence with white
 * 
 * This methodd uses the global lightsControl structure and should be called
 * during the loop cycle
 */
void interactiveFlashColor(uint32_t c) {
  
    unsigned long now = millis();
    if((now - lightsControl.timerCounter) > lightsControl.stepDelay){
      lightsControl.timerCounter = now;

      for(uint16_t i = 0; i < lights.numPixels(); i++) {
        if(lightsControl.swapColor){
          lights.setPixelColor(i, lights.Color(127, 127, 127));
        }
        else{
          lights.setPixelColor(i, c);
        }
        lights.show();
      }
      lightsControl.swapColor = !lightsControl.swapColor;
    }
}

/**
 * \brief Progressive fill all the LEDs with the same color
 * 
 * This methodd uses the global lightsControl structure and should be called
 * during the loop cycle
 */
void interactiveColor(uint32_t c) {
  
  for(uint16_t i = 0; i < lights.numPixels(); i++) {
      lights.setPixelColor(i, c);
    }
    lights.show();
}

/**
 * \brief Rotating rainbow interactive (no parameters from external)
 * 
 * This methodd uses the global lightsControl structure and should be called
 * during the loop cycle
 */
void interactiveRotatingRainbow() {
  
  for (int q=0; q < 3; q++) {
    for (int i=0; i < lights.numPixels(); i=i+3) {
      lights.setPixelColor(i + q, calcColor( (i + lightsControl.color) % 255));
    }
    lights.show();

      unsigned long now = millis();
      if((now - lightsControl.timerCounter) > lightsControl.stepDelay){
        lightsControl.timerCounter = now;
        
        for (int i = 0; i < lights.numPixels(); i = i + 3) {
          lights.setPixelColor(i + q, 0);        //turn every third pixel off

        lightsControl.color++;
        if(lightsControl.color > 255)
          lightsControl.color = 0;
      }
    }
    else {
      return;
    }
  }
}

/**
 * \brief Continuous color shaing
 * 
 * This methodd uses the global lightsControl structure and should be called
 * during the loop cycle
 */
void interactiveColorCycle() {
  uint16_t i;

  unsigned long now = millis();
  if((now - lightsControl.timerCounter) > lightsControl.stepDelay){
    lightsControl.timerCounter = now;

    for(i=0; i< lights.numPixels(); i++) {
      lights.setPixelColor(i, calcColor(((i * 256 / lights.numPixels()) + lightsControl.color) & 255));
    }

    lights.show();

    lightsControl.color++;
    if(lightsControl.color > (256 * 5))
      lightsControl.color = 0;
  } // Timer tick
}

/**
 * \brief Utility function to manage the neopixels lights
 * 
 * Using the Neopixels library calculates the color of a generic
 * LED position. The 32 bit unsigned integer is the resulting color
 * that can be used to set a LED of the Neopixel stream
 * 
 * \param position The LED position in the stream
 * \return The uint32_t 32 bit integer with the color value
 */
uint32_t calcColor(byte pos) {
  pos = 255 - pos;
  if(pos < 85) {
    return lights.Color(255 - pos * 3, 0, pos * 3);
  }
  if(pos < 170) {
    pos -= 85;
    return lights.Color(0, pos * 3, 255 - pos * 3);
  }
  pos -= 170;
  return lights.Color(pos * 3, 255 - pos * 3, 0);
}
