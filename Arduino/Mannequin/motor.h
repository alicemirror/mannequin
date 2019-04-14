/**
 * @file motor.h
 * @brief Stepper motor global parameters and constants
 */

 typedef struct StepProfile {
  int torsoSpeed;
  int rotAngle;
  int lastAnglePos;
 };

//! Number of steps per output rotation.
//! Ref.: Nema 17 1.8 DEG/Step
#define STEPS_PER_REVOLUTION 200
//! Demultiplier factor of the large rotating base. Accordingl with
//! the two pulleys diameters the reduction factor is 170:14
//! To make a full rotation of the base are needed about 12 stepper 
//! pulley rotations.
#define ANGLE_DEMULTIPLIER 12

//! Stepper predefined speed
#define SPEED_LOW 30    
//! Stepper predefined speed
#define SPEED_MED 35
//! Stepper predefined speed
#define SPEED_HIGH 45
//! Search zero stepper end point speed
#define SPEED_ZERO 20

//! Increment in angles when searching the endstop point
//! corresponding to the leftmost position
#define SEARCH_ZERO_STEPS -1

//! Max angle in both sides respect to the middel torso position
#define MAX_ANGLE 40
#define MIN_ANGLE 0



