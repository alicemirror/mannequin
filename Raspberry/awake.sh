#!/bin/bash
# Power on - awake
# -----------------------------------

# Phrases prefix
PREFIX="/home/pi/Phrases/Text"
SUFFIX=".wav"

# echo $(($RANDOM % 40))

aplay $PREFIX"29"$SUFFIX
aplay $PREFIX"40"$SUFFIX
aplay $PREFIX"41"$SUFFIX
