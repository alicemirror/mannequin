# Start PiFace Digital
import time
import pifacedigitalio as pfio
pfio.init()

# Enable light fire for 60 sec
#
# Note: the light is connected to the Relay 1
# on output port 0
pfio.digital_write(0, 1)
time.sleep(60)
pfio.digital_write(0, 0)
