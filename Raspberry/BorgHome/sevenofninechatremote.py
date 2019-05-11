#!/usr/bin/python3
import random
import re
from collections import namedtuple
import pyclasses.ai

def main():
    chat = pyclasses.ai.AI()
    chat.load('sevenofninetrainer.txt')

    # Run forever 12 sentences sessions, consuming
    # one minute of the daily hour available from
    # the speech_to_text services on Google APIs
    while True:
        chat.runSpeechRemote()

if __name__ == '__main__':
    main()
