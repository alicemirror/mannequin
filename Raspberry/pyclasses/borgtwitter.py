# Class to manage tweets on twitter and chatting with the
# following users via direct messages.
#
# ============================== IMPORTANT =============================
# Note: the direct message APIs in the new message-based asset only wotk
# cloning and installing the tweepy package including DM fixes after the
# July 2018 Twitter DM endpoints upgrade from the GitHub repository
# at the following address: https://github.com/bakayim/tweepy
#
# FOR STABILITY OF THE PROJECT AND CONVENIENCE THE REPOSITORY MENTIONED
# ABOVE HAS BEEN FORKED IN THE SAME ACCOUNT OF THIS ENTIRE PROJECT. YOU
# CANFIND THE TWEEPY FULL REPOSITORY OF THE PACKAGE USED IN THIS (AND
# OTHER) CLASS(ES) AT: https://github.com/alicemirror/tweepy
# ======================================================================

import tweepy
import json
from random import randint

class BorgTwitter:
    # =========================== Globals
    # The account screen name
    __screenName = "WeAreBorg7of9"
    # Author keys file for the twitter account @WeAreBorg7of9
    __authorkeys = "/home/pi/twitter_auth_WeAreBorg7of9.json"
    # Twitter ID of the account. Will be aasigned during the
    # connection
    __myId = ""
    # Twitter description of the account. Will be aasigned during the
    # connection
    __myDescription = ""
    # Twitter name of the account. Will be aasigned during the
    # connection
    __myName = ""
    
    # ============================= Constants
    # Keys used to retrieve values from the dictionaries
    # Names are self-explaining.
    __KEY_CONSUMER_KEY = 'consumer_key'
    __KEY_CONSUMER_SECRET = 'consumer_secret'
    __KEY_ACCESS_TOKEN = 'access_token'
    __KEY_TOKEN_SECRET = 'access_token_secret'

    # Max number of direct messages threads to retrieve when
    # checking for new messages in the list.
    __MAX_DIRECT_MESSAGES = 10
    
    # Constructor
    # Define the twitters predefined constants
    def __init__(self):
        print("BorgTwitter 1.0")

    # Load the authorization keys for the twitter account
    # and create a Pyton dictionary, then prepare the API connection
    def connectTwitter(self):

        # Create a Python dictionary from the json keys
        with open(self.__authorkeys) as file:
            secrets = json.load(file)

        # Start the author API setting
        auth = tweepy.OAuthHandler(secrets[self.__KEY_CONSUMER_KEY],
                                        secrets[self.__KEY_CONSUMER_SECRET])
        auth.set_access_token(secrets[self.__KEY_ACCESS_TOKEN],
                                   secrets[self.__KEY_TOKEN_SECRET])

        # Send the parameters to Twitter and get the tweepy instance
        self.twitter = tweepy.API(auth)

        # Update the global variables account info
        self.__getMyID()

    # Send a simple twitter text
    def tweetText(self, text):
        self.twitter.update_status(text)

    # Get the list of favorites IDs
    # Only print the list, if needed should be completed the implementation.
    def favUsers(self):
        favsList = self.twitter.favorites(self.screenName)

        # Loop on the list of favs and get infos
        for fav in favsList:
            print(fav)

    # Get the ID of the authenticated user (the messages sender)
    def __getMyID(self):
        # Get the information "user" object
        myInfo = self.twitter.me()
        infoDic = self.__jsonUserToDict(myInfo)
        self.__myId = infoDic["id"]
        self.__myDescription = infoDic["description"]
        self.__myName = infoDic["name"]

    # Convert the _json attribute of a user object to a dictionary
    # for further usage
    def __jsonUserToDict(self, user):
        # Extract the _json component
        info = user._json
        # Dump the json component to a json string, formatted
        infoJ = json.dumps(info, indent = 4, sort_keys=True)
        # Convert the json string to a dictionary
        return json.loads(infoJ)

    # Send DM to the desired recipient ID
    # The process to manage the identification (name, screen name)
    # of the recipient ID, if needed, should be managed outside of
    # the class. Twitter API don't care of the accessory information
    # and manage DMs only based on the respective recipient ID
    def sendMessage(self, userId, data):
        event = {
          "event": {
            "type": "message_create",
            "message_create": {
              "target": {
                "recipient_id": userId
              },
              "message_data": {
                "text": data
              }
            }
          }
        }

        # print(event)
        self.twitter.send_direct_message_new(event)

    # Retrieve the last set of DM messages and is some user sent a response
    # return the text string and the user id
    # If no user has responded, it is returned null
    def checkMessages(self):
        msg = self.twitter.direct_messages(count = self.__MAX_DIRECT_MESSAGES,
                                           full_text = True)

        # Flag set if at least one message is not answered
        # else the function return null instead of the list of
        # messages objects
        newMessages = False
        openMessages = []   # Empty list
        msgTempKeys = ['sender_id', 'text'] # Dictionary keys
        
        # Loop on the messages source list
        for message in msg:
            # Convert the string to a list
            listEvents = json.loads(
                json.dumps(message.events, indent = 4, sort_keys=True))            
            # For every event in the list extract a dictionary with the
            # event details.
            for event in listEvents:
                # Convert the json object to a dictionary with the
                # events details.
                dictEvent = json.loads(
                    json.dumps(event, indent = 4, sort_keys=True))
                # If the sender of the message is not the registered user
                # the message needs to be answered.
                # Create a dictionary with the two elements we need
                if int(dictEvent["message_create"]["sender_id"]) != int(self.__myId):
                    # print("SenderID ", dictEvent["message_create"]["sender_id"])           
                    newMessages = True
                    print(int(dictEvent["message_create"]["sender_id"]))
                    sId = dictEvent['message_create']['sender_id']
                    sMsg = dictEvent['message_create']['message_data']['text']
                    msgTempValues = [sId, sMsg]
                    # Add the disctionary to the return list
                    openMessages.append(dict(zip(msgTempKeys, msgTempValues)))

        return newMessages, openMessages

    # Get the list of the friends followed by the user
    # Only print the list, if needed should be completed the implementation.
    def friendsList(self):
        friends = self.twitter.friends_ids(self.screenName)

        # Loop on the list of friends and check the friendship
        for friendId in friends:
            userInfo = self.twitter.get_user(friendId)
            print(userInfo.name,  userInfo.screen_name, friendId)

    
