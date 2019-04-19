#!/usr/bin/python3
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time
import subprocess
from picamera import PiCamera

GPIO.setmode(GPIO.BOARD)
PIN_TRIGGER = 7 # Distance sensor trigger pin
PIN_ECHO = 11 # Distance sensor echo pin
# Mosquitto server IP Address - Set this value accordingly
mqttServer = "192.168.0.241"
# Mosquitto server channel name
mqttChannel = "magic_mirror"
# Distance detection pause duration after a valid movement
# has been detected and a message has been sent to the mqtt
# server (7of9) in minutes
mqttPause = 2.5
camera = PiCamera()

# Shows the camera preview for a number of seconds
def camPreview(sec):
    camera.rotation = 180 # Image is bottom-top

    # Show the camera preview    
    camera.start_preview(alpha=192)
    # And brightness 0
    camera.brightness = 0

    # Progressively increase the brightness
    # to the maximum
    for i in range(0, 50):
        camera.brightness = i
        time.sleep(0.1)
    # Leave the preview visibile for the desired
    # number of seconds
    time.sleep(sec)
    camera-stop_preview()

# Initialize the GPIO pins for the distance sensor
def sensorInit():
    # Disable warnings if the program is launched twice
    # and the channel is already in use. It is anyway reset by the
    # new process.
    GPIO.setwarnings(False)

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    time.sleep(2)

# Executes a sensor reading cycle, inclusing the pause
# for the sensor settle.
# If the distance is between 2 and 400 cm (4 m) the reading
# is valid, else zero is returned.
#
# if isPause is true, after a reading pauses for a fixes period
# else return immediately to the callse
def checkDistance(isPause):
    # Set trigger to high then after 0.1 ms
    # set it to low as the sensor needs a
    # pulse of this length to start
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    # define start/end time variables before excturing
    # a distance reading. This is unnecessary, but if
    # the variables are not initialized randomly an error
    # of variable use before its definition may occur.
    # This is probably due in cases when the start time
    # reading is not yet been finished processing and the
    # echo (end time) reading while is already started.
    pulse_start_time = 0
    pulse_end_time = 0

    # Save start time until a transitio does not occur
    # then save the time after the transition from the
    # echo input
    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO) == 1 :
        pulse_end_time = time.time()

    # Calculate the pulse duration then calculate the distance
    # in cm accordingly to the ultrasound speed
    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)

    # Ignore out of range calculations, distance should be
    # detected between 2 and 400 cm
    if(distance <= 2 or distance > 400):
        distance = 0

    # Wait the sensor to settle before starting another
    # reading cycle
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    if(isPause):
        time.sleep(0.5)

    # Return che reading
    return distance

# Send the distance value to the mqtt server
#
# Param: distance The value to send to the mqtt server
def mqttDistance(distance):
    publish.single(mqttChannel, distance, hostname=mqttServer)

# -----------------------------------------------
# Main process
# -----------------------------------------------
if __name__ == '__main__':
    # Initializes the distance sensor pins
    sensorInit()
    checkDistance(True)
    # Disable the monitor

    # Infinite loop for continuous distance detection
    while True:
        dist = checkDistance(False)
        time.sleep(0.05)
        # If the flag is true at the end of the distance
        # check cycle, a message is sent to 7of9
        comingThru = True
        # Minimum/Maximum distance ranges in cm to consider a
        # movement (no matter the direction)
        minDelta = 1
        maxDelta = 100

        # If the distance is in the range, executes other
        # five readings. If the disance remain in range,
        # this means that it is true that something - maybe
        # human? - is moving respect the mirror.
        for moving in range(0, 5):
            newDist = checkDistance(False)
            time.sleep(0.05)
            delta = abs(dist - newDist)
            if( (delta >= minDelta) and
                (delta <= maxDelta) and
                (newDist <= maxDelta) ):
                comingThru = True
            else:
                comingThru = False
                
            # Update last distance read. Thie will be the sent
            # value if a movement around has been detected
            dist = newDist

        # If the coming is true, the mqtt message is sent
        if(comingThru):
            # Send the message to the server
            mqttDistance(dist)
            # Show a camera preview
            camPreview(10)
            # After sending the message, the cycle pauses for about
            # one minute to avoid a continuous sequence of voice messages
            time.sleep(mqttPause)
            # Disable the monitor
