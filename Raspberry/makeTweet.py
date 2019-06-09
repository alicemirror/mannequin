#!/usr/bin/python3
from pyclasses.twitter import SevenOfNineTwitter
from picamera import PiCamera

tweet.connectTwitter()

camera = PiCamera()
camera.rotation = 180
camera.capture("/home/pi/images/twitter.jpg")

tweet.tweetGeneric(True)
