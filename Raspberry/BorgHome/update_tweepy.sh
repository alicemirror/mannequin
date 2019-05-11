#!/bin/bash
# -----------------------------------
# We suppose the command is lanched from the
# home folder and tweepy is a subfolder
# with the package cloned.

cd tweepy
sudo python3 setup.py clean
sudo python3 setup.py build
sudo python3 setup.py install

cd ..
echo "Tweepy Updated"

