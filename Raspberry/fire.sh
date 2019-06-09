#!/bin/bash
# Use burst laser
# -----------------------------------

# Phrases prefix
PREFIX="/home/pi/Phrases/Text"
SUFFIX=".wav"

echo $(($RANDOM % 40))

# Activate Laser!
aplay $PREFIX"26"$SUFFIX

# Laser cutting begin 
aplay $PREFIX"28"$SUFFIX
