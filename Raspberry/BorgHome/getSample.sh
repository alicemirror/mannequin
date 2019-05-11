#!/bin/bash
# sample a bunch of seconds from the USB mic
# to test the silence

arecord --channels=1 -q -D plughw:1,0 -d 3 -t wav -f S16_LE -r 16000 "speechtest.wav" &>/dev/null
sox "speechtest.wav" -n stat