#!/bin/bash
# Output a random choice between a group
# of phrases related to the same context
# A multi-phrase is generated selecting
# multiple gouds of sentences
# -----------------------------------

# Phrases prefix
PREFIX="/home/pi/Phrases/Text"
SUFFIX=".wav"

# Welcome sentence
WELCOME_NUM=6
WELCOME=(29 30 31 32 33 33)
WNUM=NUM=$(($RANDOM % $WELCOME_NUM))

# Mirror related phrases
MIRROR_NUM=6
MIRROR=(42 43 44 45 46 46)
MNUM=$(($RANDOM % $MIRROR_NUM))

# Observe sentences
OBSERVE_NUM=8
OBSERVE=(47 48 49 50 51 52 53 54)
ONUM=$(($RANDOM % $OBSERVE_NUM))


# Play the phrase in sequence
aplay $PREFIX${WELCOME[WNUM]}$SUFFIX
aplay $PREFIX${MIRROR[MNUM]}$SUFFIX
aplay $PREFIX${OBSERVE[ONUM]}$SUFFIX

