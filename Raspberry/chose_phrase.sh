#!/bin/bash
# Output a random choice between a group
# of phrases used periodically to attract
# the attention. Phrases are not
# context-specific.
# -----------------------------------

# Phrases prefix
PREFIX="/home/pi/Phrases/Text"
SUFFIX=".wav"

# Phrases array
SIZE=8
SENTENCE=(04 14 15 36 38 39 40 12 16 16)

# Chose a random phrase from the set
# Note that the modulos of the randome 
# number in the range is calculated based 
# on the range + 1 so the last array
# value is duplicated
NUM=$(($RANDOM % $SIZE))

# Play the phrase
aplay $PREFIX${SENTENCE[NUM]}$SUFFIX
