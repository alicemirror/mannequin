#!/bin/bash
# Launch Magic Mirror as we don't want
# to start it as a service but scheduled
# in crong at boot
# -----------------------------------

cd /home/pi/MagicMirror
npm start
cd /home/pi

# That's all!