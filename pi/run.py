#!/usr/bin/env python

import twitter
import serial
import sys
import re
from time import sleep

key_file = '/home/pi/twitter.key'
port = '/dev/ttyUSB0'
user = '@realDonaldTrump'
baud = 115200


def displayTweet(tweet):
	with serial.Serial(port, baud) as ser:
		print(tweet)
		ser.write(tweet.encode())


def getTweet():
	query = api.GetUserTimeline(screen_name=user)
	if(query and len(query) > 0 and query[0]):
		return '* TRUMP ALERT * '+re.sub(r"http\S+", "", query[0].text)+' *'
	else:
		return False


def main():
	check_tweet = getTweet()
	cur_tweet = ''
	while True:
		if check_tweet and check_tweet != cur_tweet:
			cur_tweet = check_tweet
			displayTweet(cur_tweet)
		check_tweet = getTweet()
		sleep(len(cur_tweet)*(12*0.04)) # 40 ms to refresh column * ~12 columns for each character


if __name__ == "__main__":
	try:
		with open(key_file, 'r') as f:
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
