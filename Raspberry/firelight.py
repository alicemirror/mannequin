#!/usr/bin/python3
# Executes a series of lighting sequences activated by cron

# Import the external classes
from pyclasses.pifacelights import PiFaceLights
import pifacedigitalio as pfio
from random import randint

# Number of LED rotations
ledRotations = 10
# Range min/max for randm rotations
ledMinRotations = 10
ledMaxRotations = 30

def main():
    # Initialize the PiFace Digital 2 library
    pfio.init()
    # Initializa the class
    piFace = PiFaceLights(pfio)
    
    piFace.fireLight(True)
    piFace.clearLeds()
    piFace.fibonacci()
    piFace.clearLeds()

    # Loops on the seven LEDs
    for j in list(range(ledRotations)):
        piFace.rotateLeds(1)

    piFace.clearLeds()

    for j in list(range(ledRotations)):
        piFace.rotateLeds(-1)

    piFace.clearLeds()
    piFace.fibonacci()
    piFace.clearLeds()

    # Calculate the random number or double rotations
    randRange = randint(ledMinRotations, ledMaxRotations)

    for j in list(range(randRange)):
        piFace.rotateLeds(1)
        piFace.rotateLeds(-1)

    piFace.clearLeds()
    piFace.fireLight(False)

if __name__ == "__main__":
    main()
