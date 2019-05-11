#!/usr/bin/python3
# Manage chats via direct message with the followed users
from pyclasses.borgtwitter import BorgTwitter
from collections import namedtuple
from pyclasses.ai import AI
import time

def main():
    # Initialize the twitter class
    # (registration and connection to Twitter)
    tweet = BorgTwitter()
    # Establish a connection to the Twitter server APIs
    tweet.connectTwitter()
    # Initialize the AI class and load the trainer file for
    # the text processing engine
    chat = AI()
    chat.load('sevenofninetrainer.txt')

    # Execute a cycle processing all the queued message
    isNew, msgList = tweet.checkMessages()

    # print("New messages: ", isNew, msgList)

    # If there are messages awaiting answer, proceed answering
    # to them
    if isNew is True:
        for msg in msgList:
            ''' '''
            userId = msg['sender_id']
            userText = msg['text']
            # Send the message text to the language processor
            # engine
            response = chat.processDM(userText)
            tweet.sendMessage(userId, response)
            # Chat delay before processing the next message (due to the
            # anti-spam Twitter limitations)
            time.sleep(30)

if __name__ == '__main__':
    main()
