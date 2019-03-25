/**
 * @file commands.h
 * @brief Serial commands and control structure
 */

 typedef struct StepProfile {
  int torsoSpeed;
  int rotAngle;
  int lastAnglePos;
 };

//! Speed id low
#define ID_LOW 0
//! Speed id med
#define ID_MED 1
//! Speed id low
#define ID_HIGH 2
//! Speed id low
#define ID_ZERO 3
