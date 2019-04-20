#!/usr/bin/python3
from pyclasses.twitter import SevenOfNineTwitter
from picamera import PiCamera

tweet = SevenOfNineTwitter()

tweet.connectTwitter()

camera = PiCamera()
camera.capture("/home/pi/images/twitter.jpg")

tweet.tweetGeneric(True)
