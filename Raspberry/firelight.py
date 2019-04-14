# Start PiFace Digital
import time
import pifacedigitalio as pfio
from random import randint

# Number of LED rotations
ledRotations = 10
# Range min/max for randm rotations
ledMinRotations = 10
ledMaxRotations = 30

# PiFace Digital library initialization
pfio.init()

# Power on the fire Light. Remain on until the LED sequence
# does not end
def fireLight(isOn):
    fireLightPin=0
    
    if isOn is True:
        pfio.digital_write(fireLightPin, 1)
    else:
        pfio.digital_write(fireLightPin, 0)

# Power off al the LEDs
def clearLeds():
    for j in list(range(7)):
        pfio.digital_write(j+1, 0)

# Rotate the LEDs clockwise or counterclockwise
# 'direction' can be 1 or -1
def rotateLeds(direction):
    # Seconds to pause every LED step
    rotationPause=0.08
    
    # Initializes the starting point (depends on the direction)    
    if(direction < 0):
        startLed = 7
    else:
        startLed = 1

    # Loop on the seven LEDs
    for j in list(range(7)):
        pfio.digital_write(startLed, 1)
        time.sleep(rotationPause)
        pfio.digital_write(startLed, 0)
        startLed += direction    

# Executes the Fibonacci sequence up to 5
# on the 7 LEDs (0, 1, 1, 2, 3, 5}
# Note that the first pause is for 0 of the sequence
def fibonacci():
    pause = 0.025 # ms delay between every light sequence

    # 0
    time.sleep(pause)

    # 1
    pfio.digital_write(7, 1)
    time.sleep(pause)
    pfio.digital_write(7, 0)
    time.sleep(pause)

    # 1
    pfio.digital_write(7, 1)
    time.sleep(pause)
    pfio.digital_write(7, 0)
    time.sleep(pause)

    # 2
    pfio.digital_write(6, 1)
    time.sleep(pause)
    pfio.digital_write(6, 0)
    time.sleep(pause)

    # 3
    pfio.digital_write(5, 1)
    time.sleep(pause)
    pfio.digital_write(5, 0)
    time.sleep(pause)

    # 5
    pfio.digital_write(3, 1)
    time.sleep(pause)
    pfio.digital_write(3, 0)
    time.sleep(pause)

# -------------------------- Main process
fireLight(True)
clearLeds()
fibonacci()
clearLeds()
# Loops on the seven LEDs
for j in list(range(ledRotations)):
    rotateLeds(1)

clearLeds()

for j in list(range(ledRotations)):
    rotateLeds(-1)

clearLeds()
fibonacci()
clearLeds()

# Calculate the random number or double rotations
randRange = randint(ledMinRotations, ledMaxRotations)

for j in list(range(randRange)):
    rotateLeds(1)
    rotateLeds(-1)

clearLeds()
fireLight(False)

# -------------------------- END
