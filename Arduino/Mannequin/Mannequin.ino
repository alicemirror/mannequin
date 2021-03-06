/**
 * @file Mannequin.ino
 * @brief Main application program
 */

#include <Stepper.h>
#include <Streaming.h>
#include "parameters.h"
#include "commands.h"
#include "microphone.h"
#include "laser.h"
#include "motor.h"
 
//! Create Instance of Stepper library
Stepper torsoStepper(STEPS_PER_REVOLUTION, STEP_PIN_A1, STEP_PIN_A2, STEP_PIN_B1, STEP_PIN_B2);
//! Motion control structure
StepProfile torsoControl;
//! Laser status structure
LaserStatus laser;

const int sampleWindow = SAMPLE_FREQ; ///< Microphone sample window width
//! Number of sample channels (left, right)
unsigned int sample[2];
unsigned int peakToPeak[2];   // peak-to-peak level
unsigned int signalMax[2];
unsigned int signalMin[2];
double volts[2];

int anglePos = MAX_ANGLE / 2;
int increment = 4;

//! Initialization
void setup()
{
  Serial.begin(9600);

  pinMode(A0, INPUT);
  pinMode(A1, INPUT);

  pinMode(LASER_PIN, OUTPUT);
  
  // Initialize the laser
  laser.value = LASER_DEFAULT;
  laser.isOn = LASER_OFF;
  setLaser();

  // Initialize the endswitch input
  pinMode(ENDSWITCH_PIN, INPUT_PULLUP);
  // Initialize the stepper class  
  torsoStepper.step(STEPS_PER_REVOLUTION);
  // Move to zero point
  setTorsoZero();
}

char dataString[50] = {0};
int a =0x64; 

void loop() {
  unsigned long startMillis = millis();  // Start of sample window

  if(Serial.available()) {
    char get = Serial.read();
    sprintf(dataString,"%01X",a); // convert a value to hexa 
    Serial.println(dataString);   // send the data
  }
  
  burstLaser();
  delay(1000);
  longBurstLaser();
  delay(1000);
  fireLaser();
  delay(1000);
  laser.value = 128;
  laserFadeOff();
  delay(1000);
  laser.value = 128;
  laserFadeOn();  
  delay(1000);
  laser.isOn = LASER_OFF;
  setLaser();
  delay(1000);

/* ---------------------------------------------------------------
  peakToPeak[0] = 0;
  peakToPeak[1] = 0;
  signalMax[0] = 0;
  signalMax[1] = 0;
  signalMin[0] = MAX_SIGNAL;
  signalMin[1] = MAX_SIGNAL;

   // collect data for 50 mS from both ears
   while ( (millis() - startMillis) < sampleWindow ) {
     // Check left sample
      sample[EAR_LEFT] = analogRead(A0);
      if (sample[EAR_LEFT] < MAX_SIGNAL) {
         if (sample[EAR_LEFT] > signalMax[EAR_LEFT]) {
            signalMax[EAR_LEFT] = sample[EAR_LEFT];
         } else if (sample[EAR_LEFT] < signalMin[EAR_LEFT]) {
            signalMin[EAR_LEFT] = sample[EAR_LEFT];
         }
      }
   }
   
   delay(50);

   while ( (millis() - startMillis) < sampleWindow ) {
     // Check right sample
      sample[EAR_RIGHT] = analogRead(A1);
      if (sample[EAR_RIGHT] < MAX_SIGNAL) {
         if (sample[EAR_RIGHT] > signalMax[EAR_RIGHT]) {
            signalMax[EAR_RIGHT] = sample[EAR_RIGHT];
         } else if (sample[EAR_RIGHT] < signalMin[EAR_RIGHT]) {
            signalMin[EAR_RIGHT] = sample[EAR_RIGHT];
         }
      }
   }
   
   // max - min = peak-peak amplitude
   peakToPeak[EAR_LEFT] = signalMax[EAR_LEFT] - signalMin[EAR_LEFT]; 
   peakToPeak[EAR_RIGHT] = signalMax[EAR_RIGHT] - signalMin[EAR_RIGHT];
   
   volts[EAR_LEFT] = double(peakToPeak[EAR_LEFT] * 5.0) / MAX_SIGNAL;
   volts[EAR_RIGHT] = double(peakToPeak[EAR_RIGHT] * 5.0) / MAX_SIGNAL;

   double diff = abs(volts[EAR_LEFT] - volts[EAR_RIGHT]);

   Serial << "Max left " << signalMax[EAR_LEFT] << " Min left " << signalMin[EAR_LEFT] << endl;
   Serial << "Max right " << signalMax[EAR_RIGHT] << " Min right " << signalMin[EAR_RIGHT] << endl;
   Serial << "peakToPeak left " << peakToPeak[EAR_LEFT] << " peakToPeak right " << peakToPeak[EAR_RIGHT] << endl;
   Serial << "V left " << volts[EAR_LEFT] << " V right " << volts[EAR_RIGHT] << endl;
   Serial << " V diff " << diff << endl ;
  --------------------------------------------------------------- */

  // Update the angle increment
  anglePos += increment;
  setTorsoSpeed(SPEED_LOW);

  // Check for the higher limit
  if(anglePos >= MAX_ANGLE) {
    increment = -4;
    anglePos += increment * 2;
    setTorsoSpeed(SPEED_ZERO);
    setTorsoZero();
  }
  
  // Check for the lower limit
  if(anglePos <= 5) {
    increment = 4;
    anglePos += increment;
    setTorsoSpeed(SPEED_ZERO);
    setTorsoZero();
  }

  // Set the new position
  torsoControl.rotAngle = anglePos;
  moveTorso();

  delay(10000);
}

//==================================================
// Command functions
//==================================================



//==================================================
// Motor functions
//==================================================

//! Set speed for the motor. Speed must  be one of
//! the predefined speed
void setTorsoSpeed(int mSpeed) {
    torsoControl.torsoSpeed = mSpeed;
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
  torsoControl.torsoSpeed = SPEED_LOW;
  torsoControl.rotAngle = MAX_ANGLE;
  moveTorso();
  torsoControl.torsoSpeed = SPEED_LOW;
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
    
    // Move the motor testing the entire rotation range.S
    torsoStepper.step(moveSteps);
    torsoControl.lastAnglePos = torsoControl.rotAngle;
  }
}

//==================================================
// Laser functions
//==================================================

/**
  Set the laser state. If the state is set to on, the laser level is
  assigned else the level value has no effect.
*/
void setLaser() {
 if(laser.isOn) {
   analogWrite(LASER_PIN, laser.value);
 } // Laser is on, set the value
 else {
   analogWrite(LASER_PIN, 0);
 } // Laser disabled
}

/** 
  Laser single shot with variable duration
  
  @param fireDuration The duration of the fire. The function is used
  both by the fireLaser() and burstLaser()
  */
void fireLaser(int fireDuration) {
  // Save the current laser values
  LaserStatus laserBackup;
  
  laserBackup.value = laser.value;
  laserBackup.isOn = laser.isOn;
  
  // First, disable the laser
  if(laser.isOn) {
    laser.isOn = LASER_OFF;
    setLaser();
    delay(LASER_OFF_BEFORE_FIRE);
  }
  // Set the fire value then executes the action
  laser.value = LASER_FIRE;
  laser.isOn = LASER_ON;
  setLaser();
  delay(fireDuration);
  // Restore the previous laser status
  laser.value = laserBackup.value;
  laser.isOn = laserBackup.isOn;
  setLaser();
}

//! Execute the single shot
void fireLaser() {
  fireLaser(LASER_FIRE_DURATION);
}

//! Execute a burst sequence
void burstLaser() {
  int j;
  
  for(j = 0; j < LASER_BURST_LENGHT; j++) {
    fireLaser(LASER_BURST_DURATION);
    delay(LASER_BURST_PAUSE);
  }
}

//! Execute multiple bursts
void longBurstLaser() {
 int j;
 
 for(j = 0; j < LASER_LONG_BURST; j++) {
   burstLaser();
 }
}

//! Fade off the laser from the current value
void laserFadeOff() {
 int j;

 laser.isOn = LASER_ON;

 // Fade off loop
 for(j = laser.value; j >= 0; j--) {
   laser.value = j;
   setLaser();
   delay(LASER_FADE_DELAY);
 }
}

//! Fade on the laser to the current value
void laserFadeOn() {
 int j, value;

 laser.isOn = LASER_ON;
 value = laser.value;

 // Fade off loop
 for(j = 0; j <= value; j++) {
   laser.value = j;
   setLaser();
   delay(LASER_FADE_DELAY);
 }
}
  
  
