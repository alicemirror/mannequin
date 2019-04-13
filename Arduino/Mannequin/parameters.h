/**
 * @file parameters.h
 * @brief Control parameters and structures for the mannequin
 * 
 * @note As it is not used an end-stop switch we assume that when the
 * system is powered-on the torso position is in the middle.
 */

 //! Include the Arduino Stepper Library
#include <Stepper.h>

#define STEP_PIN_A1 8     ///< STEPPER LIBRARY CONTROL PIN A+
#define STEP_PIN_A2 9     ///< STEPPER LIBRARY CONTROL PIN A-
#define STEP_PIN_B1 10    ///< STEPPER LIBRARY CONTROL PIN B+
#define STEP_PIN_B2 11    ///< STEPPER LIBRARY CONTROL PIN B-

#define ENDSWITCH_PIN 2   ///< End switch signal

//! Number of steps per output rotation.
//! Ref.: Nema 17 1.8 DEG/Step
#define STEPS_PER_REVOLUTION 200
//! Demultiplier factor of the large rotating base. Accordingl with
//! the two pulleys diameters the reduction factor is 170:14
//! To make a full rotation of the base are needed about 12 stepper 
//! pulley rotations.
#define ANGLE_DEMULTIPLIER 12

//! Stepper predefined speed
#define SPEED_LOW 25    
//! Stepper predefined speed
#define SPEED_MED 30
//! Stepper predefined speed
#define SPEED_HIGH 40
//! Search zero stepper end point speed
#define SPEED_ZERO 20

//! Increment in angles when searching the endstop point
//! corresponding to the leftmost position
#define SEARCH_ZERO_STEPS -1

//! Max angle in both sides respect to the middel torso position
#define MAX_ANGLE 40
#define MIN_ANGLE 0

