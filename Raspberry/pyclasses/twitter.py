# Class to manage tweets on twitter

import tweepy
import json
from random import randint

class SevenOfNineTwitter:

    # Constructor
    # Define the twitters predefined constants
    def __init__(self):
        print("SevenOfNineTwitter 2.0")
        # Author keys file
        self.authorkeys = "/home/pi/twitter_auth_WeAreBorg7of9.json"
        # MagicMirror sentences file
        self.mirrorsentences = "/home/pi/comment_mirror.json"
        # Generic sentences file
        self.genericsentences = "/home/pi/twitter_generic.json"
        # Predefined tags added before any twitter message
        self.tags = "#artatronic #picasso #designchallenge "
        # Predefined mentions added after any twitter message
        self.mentions = " @E14Community @e14presents @Elegoo_Official @LorenzoPMerlo1 @enricomiglno"
        # Default image name
        self.image = "/home/pi/images/twitter.jpg"

    # Load the authorization keys for the twitter account
    # and create a Pyton dictionary, then prepare the API connection
    def connectTwitter(self):

        # Create a Python dictionary from the json keys
        with open(self.authorkeys) as file:
            secrets = json.load(file)

        # Start the author API setting
        auth = tweepy.OAuthHandler(secrets['consumer_key'],
                                        secrets['consumer_secret'])
        auth.set_access_token(secrets['access_token'],
                                   secrets['access_token_secret'])

        # Send the parameters to Twitter and get the tweepy instance
        self.twitter = tweepy.API(auth)

    # MagicMirror related tweets. Creates a tweet when a visitor interact with
    # the MagicMirror adding a photo. Sentences are randomly selected from
    # a pre-built array
    def tweetMagicMirror(self, hasImage):
        # Create a Python dictionary from the json file
        with open(self.mirrorsentences) as file:
            sentences = json.load(file)
        # Send a tweet
        if hasImage is False:
            self.sendTweet(sentences)
        else:
            self.sendTweetImage(sentences)

    # MagicMirror related tweets. Creates a tweet when a visitor interact with
    # the MagicMirror adding a photo. Sentences are randomly selected from
    # a pre-built array
    def tweetGeneric(self, hasImage):
        # Create a Python dictionary from the json file
        with open(self.genericsentences) as file:
            sentences = json.load(file)
        # Send a tweet
        if hasImage is False:
            self.sendTweet(sentences)
        else:
            self.sendTweetImage(sentences)

    # Send a tweet including the predefined tags and mentions,
    # randomly selecting a string from the sentences Python dictionary
    # and attaching the default image
    def sendTweetImage(self, dictionary):
        num = dictionary['phrases']
        # Get the random phrase number
        randRange = randint(0, num - 1)

        # Create the full text message
        tText = self.tags + dictionary['list'][randRange] + ">> " + self.mentions
        self.twitter.update_with_media(self.image, tText)

    # Send a tweet including the predefined tags and mentions,
    # randomly selecting a string from the sentences Python dictionary
    def sendTweet(self, dictionary):
        num = dictionary['phrases']
        # Get the random phrase number
        randRange = randint(0, num - 1)

        # Create the full text message
        tText = self.tags + dictionary['list'][randRange] + ">> " + self.mentions
        self.twitter.update_status(tText)

    # Send a simple twitter text
    def tweetText(self, text):
        self.twitter.update_with_media(self.image, text)
        
    # Send a simple twitter text with the last captured image
    def tweetText(self, text):
        self.twitter.update_status(text)
