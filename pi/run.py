#!/usr/bin/env python

import twitter
import serial
import sys
import re
from time import sleep

port = "/dev/ttyUSB0"
user = '@realDonaldTrump'
baud = 115200


def displayTweet(tweet):
	with serial.Serial(port, baud) as ser:
		print(tweet)
		ser.write(tweet.encode())


def cleanTweet(input):
	return re.sub(r"http\S+", "", input)


def main():
	check_tweet = cleanTweet(api.GetUserTimeline(screen_name=user)[0].text)
	cur_tweet = ''
	while True:
		if check_tweet != cur_tweet:
			cur_tweet = check_tweet
			displayTweet(cur_tweet)
		check_tweet = cleanTweet(api.GetUserTimeline(screen_name=user)[0].text)
		sleep(len(cur_tweet)*(8*0.04)) # 40 ms to refresh column * 8 columns for characters


if __name__ == "__main__":
	try:
		with open('twitter.key', 'r') as f:
			api_key = f.readline().strip()
			api_secret = f.readline().strip()
			token_key = f.readline().strip()
			token_secret = f.readline().strip()
	except Exception as e:
		print(f'Failed to get API secrets: {e}')
		sys.exit(1)

	api = twitter.Api(
	    consumer_key=api_key,
	    consumer_secret=api_secret,
	    access_token_key=token_key,
	    access_token_secret=token_secret
	)

	try:
		with serial.Serial(port, baud) as ser:
			pass
	except Exception as e:
		print(f'Unexpected error opening serial: {e}')
		sys.exit(1)

	try:
		main()
	except KeyboardInterrupt:
		print('Captured KeyboardInterrupt')
		sys.exit(0)
