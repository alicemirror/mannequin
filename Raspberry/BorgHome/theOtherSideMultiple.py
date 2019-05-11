#!/usr/bin/python3
# Updated version of theOtherSide.py program to manage multiple
# clients. SevenOfNine act as a server receiving messages from the
# MagicMirror and the Borg Access Terminal.
#
# Note: Depending on the performances of the server processor, memory, etc.
# the server can manage as many connection as needed with different clients
import paho.mqtt.client as mqtt
import subprocess
import time
import pyclasses.ai
from pyclasses.twitter import SevenOfNineTwitter
from picamera import PiCamera

# Seven Of Nine MQTT server. 
MQTT_SERVER = "localhost"
# MagicMirror MQTT client
MQTT_MIRRORPATH = "magic_mirror"
# Borg Access Terminal MQTT client
MQTT_TERMINALPATH = "borg_access_termnal"
# Seven Of Nine MQTT IP address on the LAN
# Not needed in this context but used by the clients
# Should be changed accordingly with the LAN WiFi connection
# Set here as a reminder.
IP_SERVER = "192.168.0.241"
# Set the isProduction variable to True to run the program
# automatically in produciton mode, else leave if to False
inProduction = False
# MagicMirror client
mirror = mqtt.Client()
# Borg Access terminal client
terminal = mqtt.Client()
# Initialize the AI library, only for text to speach, no
# training file initialization is needed.
chat = pyclasses.ai.AI()

# The callback function when the MaigcMirror client ask for a CONNACK
# to connect to the server.
def on_connect_mirror(client, userdata, flags, rc):
    if inProduction is False:
        print("MagicMirror connected with result code " + str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_MIRRORPATH)

# The callback function when the Borg Access terminal client ask for a CONNACK
# to connect to the server.
def on_connect_terminal(client, userdata, flags, rc):
    if inProduction is False:
        print("Borg Access Terminal connected with result code " + str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TERMINALPATH)
 
# The callback for when a PUBLISH message is received from the
# MagicMirror client.
# Note that we don't care of the content of the message. It is the
# message event itself that trigger the response to the event on the client
def on_message_mirror(client, userdata, msg):
    if inProduction is False:
        print("MagicMirror triggered a tweet with the message " + str(msg))
 
    # say a phrase from those selected for the Magic Mirror
    subprocess.call(["/home/pi/mirror.sh"])

    # Create a Twitter library instance and start a connection
    # to the Twitter server
    tweet = SevenOfNineTwitter()
    tweet.connectTwitter()

    # Capture an image of the environment with a fixed name
    camera = PiCamera()
    camera.capture("/home/pi/images/twitter.jpg")

    # Send a tweet with the caputred image
    tweet.tweetGeneric(True)

# The callback for when a PUBLISH message is received from the Borg
# Access Terminal client.
def on_message_terminal(client, userdata, msg):
    if inProduction is False:
        print("Borg Access terminal sent a message to speak: " + str(msg.payload))
 
    # say a phrase from those selected for the Magic Mirror
    chat.tts(msg.payload)

# Main setup function for the server and connection with the clients
# through the respective callback functions. Every client loop is started
# in a separate background thread. Used in production mode
def main():
    # Setup the MagicMirror client
    mirror.on_connect = on_connect_mirror
    mirror.on_message = on_message_mirror
    mirror.connect(MQTT_SERVER, 1883, 60)
    # Setup the Borg Access Terminal client
    terminal.on_connect = on_connect_terminal
    terminal.on_message = on_message_terminal
    terminal.connect(MQTT_SERVER, 1883, 60)
    
    # For every client, we launch a background loop for connection and
    # messages management accordingly with the respective callback funcitons.
    # The background thread of the clients can be stopped with a
    # loop_stop() call, accodingly with the eclipse paho documentation
    # but we don't need as the server will run indefinitely when launched
    mirror.loop_start()
    terminal.loop_start()

# Main function, developer version for testing purposes.
# See main() for commens and description
def developer():
    main()
    
    # *** FOR TESTING PURPOSES ONLY ***************************************
    # The loop will be stopped by timeout after one minute to see if
    # clients work as expected.
    time.sleep(60)
    mirror.loop_stop() # Halt the background client thread and program ends.
    terminal.loop_stop() # Halt the background client thread and program ends.
    # *********************************************************************

if __name__ == "__main__":

    # Runs forever
    if inProduction:
        print("Production mode: connections started in background")
        main()
    else:
        chat.tts("Entered developer mode")
        print("Developer mode: server run for 60 seconds then exit")
        developer()
        print("Developer mode: exiting from server mode")

