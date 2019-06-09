#!/usr/bin/python3
# manages the MagicMirror events through Mqtt protocol
import paho.mqtt.client as mqtt
import subprocess
import json
from random import randint
import pyclasses.twitter as SevenOfNineTwitter
from picamera import PiCamera

MQTT_SERVER = "localhost"
MQTT_PATH = "magic_mirror"
MIRROR_SERVER = "192.168.1.8"

# Text to speech command and parameters
# Parameters: -sp = speak, -n = narrator voice
TTS = [ 'trans', '-sp' ]
# MagicMirror sentences file
mirrorsentences = "/home/pi/comments_mirror.json"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # Create a Python dictionary from the json file
    with open(mirrorsentences) as file:
        dictionary = json.load(file)
    
    num = dictionary['phrases']
    # Get the random phrase number
    randRange = randint(0, num - 1)

    # Create the full text message
    tText = dictionary['list'][randRange]

    runCmd([TTS[0], TTS[1], tText])

# Execute a subprocess command managing the return value, stdout, stderr
# and the return code (0 or not 0 if error occurred)
def runCmd(cmd):
    proc = subprocess.Popen(cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
 
    return proc.returncode, stdout, stderr

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
     
    client.connect(MQTT_SERVER, 1883, 60)
     
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

if __name__ == "__main__":
    main()
