#!/bin/bash
# sample a bunch of seconds from the USB mic
# then send them to speech to text google api

# Create the voice speech file
arecord --channels=1 -q -D plughw:1,0 -d 5 -t wav -f S16_LE -r 16000 "speech.wav"
# Play interlude sound while converting
./robot_interlude.sh &>/dev/null
# And convert it to json response'
gcloud ml speech recognize speech.wav --language-code='en-US'

