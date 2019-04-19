#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

try:
    GPIO.setmode(GPIO.BOARD)

    PIN_TRIGGER = 7
    PIN_ECHO = 11

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    print ("Waiting for sensor to settle")
    time.sleep(2)
    print ("Calculating distance loop")

    while True:
        # Set trigger to high then after 0.1 ms
        # set it to low as the sensor needs a
        # pulse of this length to start
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        # Save start time until a transitio does not occur
        # then save the time after the transition from the
        # echo input
        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

        # Calculate the pulse duration then calculate the distance
        # in cm accordingly to the ultrasound speed
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)

        # Ignore out of range calculations, distance should be
        #detected between 2 and 400 cm
        if(distance > 2 and distance < 400):
            print ("Distance: ",distance,"cm")

        # Wait the sensor to settle before starting another
        # reading cycle
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        time.sleep(0.5)

finally:
    GPIO.cleanup()
      
