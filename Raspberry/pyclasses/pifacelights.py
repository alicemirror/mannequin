# Class to manage the LED lights of the Seven Of Nine
# eye implant and the body internal fire light.
# Uses the PiFace Digital 2 Python 3 library. The library should
# be initialized by the caller

import time

class PiFaceLights:
    # Constructor
    # Param: the PiFaceDigital 2 classe
    def __init__(self, piFace):
        print("PiFaceLights 1.0")
        self.pfio = piFace

    # Power on the fire Light. Remain on until the LED sequence
    # does not end
    def fireLight(self, isOn):
        fireLightPin = 0
        
        if isOn is True:
            self.pfio.digital_write(fireLightPin, 1)
        else:
            self.pfio.digital_write(fireLightPin, 0)

    # Power off al the LEDs
    def clearLeds(self):
        for j in list(range(7)):
            self.pfio.digital_write(j+1, 0)

    # Rotate the LEDs clockwise or counterclockwise
    # 'direction' can be 1 or -1
    def rotateLeds(self, direction):
        # Seconds to pause every LED step
        rotationPause=0.08
        
        # Initializes the starting point (depends on the direction)    
        if(direction < 0):
            startLed = 7
        else:
            startLed = 1

        # Loop on the seven LEDs
        for j in list(range(7)):
            self.pfio.digital_write(startLed, 1)
            time.sleep(rotationPause)
            self.pfio.digital_write(startLed, 0)
            startLed += direction    

    # Executes the Fibonacci sequence up to 5
    # on the 7 LEDs (0, 1, 1, 2, 3, 5}
    # Note that the first pause is for 0 of the sequence
    def fibonacci(self):
        pause = 0.025 # ms delay between every light sequence

        # 0
        time.sleep(pause)

        # 1
        self.pfio.digital_write(7, 1)
        time.sleep(pause)
        self.pfio.digital_write(7, 0)
        time.sleep(pause)

        # 1
        self.pfio.digital_write(7, 1)
        time.sleep(pause)
        self.pfio.digital_write(7, 0)
        time.sleep(pause)

        # 2
        self.pfio.digital_write(6, 1)
        time.sleep(pause)
        self.pfio.digital_write(6, 0)
        time.sleep(pause)

        # 3
        self.pfio.digital_write(5, 1)
        time.sleep(pause)
        self.pfio.digital_write(5, 0)
        time.sleep(pause)

        # 5
        self.pfio.digital_write(3, 1)
        time.sleep(pause)
        self.pfio.digital_write(3, 0)
        time.sleep(pause)

