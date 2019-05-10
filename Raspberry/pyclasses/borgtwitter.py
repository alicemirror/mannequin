# Class to manage tweets on twitter and chatting with the
# following users via direct messages

import tweepy
import json
from random import randint

class BorgTwitter:
    # Constructor
    # Define the twitters predefined constants
    def __init__(self):
        print("BorgTwitter 1.0")
        # Author keys file for the twitter account @WeAreBorg7of9
        self.authorkeys = "/home/pi/twitter_auth_WeAreBorg7of9.json"
        # The account screen name
        self.screenName = "WeAreBorg7of9"

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

    # Send a simple twitter text
    def tweetText(self, text):
        self.twitter.update_status(text)

    # Get the list of favorites
    def favUsers(self):
        favsList = self.twitter.favorites(self.screenName)

        # Loop on the list of favs and get infos
        for fav in favsList:
            print(fav)

    # Modified version, working
    def sendMessage(self):
        event = {
          "event": {
            "type": "message_create",
            "message_create": {
              "target": {
                "recipient_id": '18448354'
              },
              "message_data": {
                "text": 'This is a test'
              }
            }
          }
        }
        # self.twitter.send_direct_message_new(event)

        msg = self.twitter.get_direct_message_new()
        print(msg)

    # Get the list of the friends followed by the user
    def friendsList(self):
        friends = self.twitter.friends_ids(self.screenName)

        # Loop on the list of friends and check the friendship
        for friendId in friends:
            userInfo = self.twitter.get_user(friendId)
            if(userInfo.screen_name == "enricomiglino"):
                print(userInfo.name,  userInfo.screen_name, friendId)

    
