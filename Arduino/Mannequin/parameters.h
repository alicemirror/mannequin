/**
 * @file parameters.h
 * @brief Control parameters and structures for the mannequin
 * 
 * @note As it is not used an end-stop switch we assume that when the
 * system is powered-on the torso position is in the middle.
 */

 //! Include the Arduino Stepper Library
#include <Stepper.h>

// =========================== 
// Stepper parameters
// =========================== 
#define STEP_PIN_A1 8     ///< STEPPER LIBRARY CONTROL PIN A+
#define STEP_PIN_A2 9     ///< STEPPER LIBRARY CONTROL PIN A-
#define STEP_PIN_B1 10    ///< STEPPER LIBRARY CONTROL PIN B+
#define STEP_PIN_B2 11    ///< STEPPER LIBRARY CONTROL PIN B-

#define ENDSWITCH_PIN 2   ///< End switch signal

// =========================== 
// Laser parameters
// =========================== 

#define LASER_PIN 3
