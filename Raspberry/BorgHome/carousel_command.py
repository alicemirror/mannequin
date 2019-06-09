#!/usr/bin/python3
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time
import subprocess

# Mosquitto MKR1000 server IP Address - Set this value accordingly
mqttServer = "192.168.0.250"
# Mosquitto server channel name
mqttChannel = "carousel/start"

cmdRun = "mqtt_run"
cmdLights = "mqtt_lights"
cmdPlay = "mqtt_music"

# Send the command via mqtt
#
# Param: the command string
def mqttSendCommandCarousel(cmd):
    publish.single(mqttChannel, cmd, hostname=mqttServer)

# -----------------------------------------------
# Main process
# -----------------------------------------------
if __name__ == '__main__':

    # Infinite loop for continuous commands (delayed)
    while True:
        # Send the message to the server
        mqttSendCommandCarousel(cmdRun)

        time.sleep(20)
