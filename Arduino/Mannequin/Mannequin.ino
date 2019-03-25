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

//! Initialization
void setup()
{
  Serial.begin(9600);

  // Initialize the endswitch input
  pinMode(ENDSWITCH_PIN, INPUT_PULLUP);
  // Initialize the stepper class  
  torsoStepper.step(STEPS_PER_REVOLUTION);
  // Move to zero point
  setTorsoZero();
}

void loop() 
{
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
