/**
 * @file parameters.h
 * @brief Control parameters and structures for the mannequin
 * 
 * @note As it is not used an end-stop switch we assume that when the
 * system is powered-on the torso position is in the middle.
 */

 //! Include the Arduino Stepper Library
#include <Stepper.h>
#include <Adafruit_NeoPixel.h>

#define STEP_PIN_A1 8     ///< STEPPER LIBRARY CONTROL PIN A+
#define STEP_PIN_A2 9     ///< STEPPER LIBRARY CONTROL PIN A-
#define STEP_PIN_B1 10    ///< STEPPER LIBRARY CONTROL PIN B+
#define STEP_PIN_B2 11    ///< STEPPER LIBRARY CONTROL PIN B-

#define ENDSWITCH_PIN 2   ///< End switch signal

#define NEOPIXEL_PIN 7     ///< Neopixel array control channel
#define NEOPIXEL_COUNT 12  ///< Number of chained neopixel LEDs in the ring

// Lighting schemes ID
#define LIGHT_ROSE 1    ///< The default scheme wen the rose is running
#define LIGHT_DUCK 2    ///< The light scheme when the duck is running
#define LIGHT_STATIC 3  ///< The light scheme when nothing moves
#define LIGHT_TRAIN 4   ///< The light when the train runs

// Predefeined light delays
#define LIGHT_ROSE_DELAY 50       ///< Delay duration every color change
#define LIGHT_DUCK_DELAY 500      ///< Delay duration every color change
#define LIGHT_STATIC_DELAY 50     ///< Delay duration every color change
#define LIGHT_TRAIN_DELAY 10       ///< Delay duration every color change

//! Progressive fill color delay (ms)
#define FILL_COLOR_DELAY 10

//! Number of steps per output rotation.
//! Ref.: Nema 17 1.8 DEG/Step
#define STEPS_PER_REVOLUTION 200
//! Demultiplier factor of the large rotating base. Accordingl with
//! the two pulleys diameters the reduction factor is 170:14
//! To make a full rotation of the base are needed about 12 stepper 
//! pulley rotations.
#define ANGLE_DEMULTIPLIER 12

//! Stepper predefined speed
#define SPEED_LOW 20    
//! Stepper predefined speed
#define SPEED_MED 45
//! Stepper predefined speed
#define SPEED_HIGH 90
//! Search zero stepper end point speed
#define SPEED_ZERO 10

//! Increment in angles when searching the endstop point
//! corresponding to the leftmost position
#define SEARCH_ZERO_STEPS -1

//! Max angle in both sides respect to the middel torso position
#define MAX_ANGLE 60
#define MIN_ANGLE 0

/** 
 * \brief Defines all the parameters to control a light loop externally 
 * 
 * The stepDelay is  value in ms that should thick the next step of the 
 * loop. To void compromising the main application flow, the loop is replaced
 * by a time counter so the next step is launched when the timer reach the expected
 * value
 */
typedef struct {
  uint32_t color;             ///< The current color number in the loop
  int colorRGB;          ///< Train speed-color
  int stepDelay;              ///< The delay (ms) between every color shift operation
  unsigned long timerCounter; ///< The delay timer counter
  bool swapColor;             ///< If true, current color is swapped with white
} neoPixParameters;
