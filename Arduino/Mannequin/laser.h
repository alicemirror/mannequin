/**
 * @file laser.h
 * @brief Control parameters and structures for the mannequin laser component
 */

/**
  Laser status structure.
*/
typedef struct LaserStatus {
  int value;          ///< current laser value
  boolean isOn;       ///< Laser status on/off
};

#define LASER_ON 1      ///< Laser is powered on
#define LASER_OFF 0    ///< Laser if powered off
#define LASER_DEFAULT 16   ///< Default laser value
#define LASER_FIRE 255     ///< Laser fire value (also when burst
#define LASER_FIRE_DURATION 1000    ///< Laser fire shot duration (ms)
#define LASER_OFF_BEFORE_FIRE 50    ///< Delay after powering out the laser before firing
#define LASER_BURST_DURATION 50     ///< Duration of a single burst
#define LASER_BURST_PAUSE 25     ///< Duration of a single burst
#define LASER_BURST_LENGHT 3       ///< Number of bursts
#define LASER_LONG_BURST 5        ///< Number of multiple bursts
#define LASER_FADE_DELAY 25      ///< Fade steps delay (ms)

