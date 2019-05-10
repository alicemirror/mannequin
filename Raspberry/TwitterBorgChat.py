#!/usr/bin/python3
# Manage chats via direct message with the followed users
from pyclasses.borgtwitter import BorgTwitter
from collections import namedtuple
from pyclasses.ai import AI

def main():
    # Initialize the twitter class
    # (registration and connection to Twitter)
    tweet = BorgTwitter()
    # Establish a connection to the Twitter server APIs
    tweet.connectTwitter()
    # Initialize the AI class and load the trainer file for
    # the text processing engine
    # chat = AI()
    # chat.load('sevenofninetrainer.txt')

    tweet.sendMessage()

if __name__ == '__main__':
    main()
