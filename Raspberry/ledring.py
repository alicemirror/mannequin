# Start PiFace Digital
import time
import pifacedigitalio as pfio
pfio.init()

# Rotate the blue leds through the PiFace Digital 2
# output pins 0-6
# All output off
for j in list(range(7)):
    pfio.digital_write(j+1, 0)

# Ten rotations
for k in list(range(100)):
    # Loop cycle
    for j in list(range(7)):
        pfio.digital_write(j+1, 1)
        time.sleep(0.05)
        pfio.digital_write(j+1, 0)
