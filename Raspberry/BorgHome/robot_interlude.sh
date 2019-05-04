#!/bin/bash
# Output a robot sound after the user spoke
# a sentence while the system recognize the
# test
# -----------------------------------

# Phrases prefix
PREFIX="/home/pi/Sounds/Robot"
SUFFIX=".wav"

# Phrases array
SIZE=4
SENTENCE=(01 02 03 03)

# Chose a random sound from the set
# Note that the modulos of the randome 
# number in the range is calculated based 
# on the range + 1 so the last array
# value is duplicated
NUM=$(($RANDOM % $SIZE))

# Play the phrase
mplayer $PREFIX${SENTENCE[NUM]}$SUFFIX
