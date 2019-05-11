#!/bin/bash
# Output a random choice between a group
# of phrases used periodically to attract
# the attention to speak with the box
# -----------------------------------

# Phrases prefix
PREFIX="/home/pi/Phrases/Text"
SUFFIX=".wav"

# Phrases array
SIZE=12
SENTENCE=(14 15 16 18 20 35 38 40 41 48 51 51)

# Chose a random phrase from the set
# Note that the modulos of the randome 
# number in the range is calculated based 
# on the range + 1 so the last array
# value is duplicated
NUM=$(($RANDOM % $SIZE))

# Play the phrase
mplayer $PREFIX${SENTENCE[NUM]}$SUFFIX
