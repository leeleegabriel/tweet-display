#!/usr/bin/env python

import twitter
import serial
import sys
import re
import logging
from time import sleep

key_file = '/home/pi/twitter.key'
port = '/dev/ttyUSB0'
user = '@realDonaldTrump'
baud = 115200


def displayTweet(tweet):
	try:
		with serial.Serial(port, baud) as ser:
			ser.write(tweet.encode())
			logger.debug(f'Transmitting: {tweet}')
	except Exception as e:
		logger.exception(f'Failed to Open Serial Device: {e}')
		sys.exit(1)


def getTweet():
	query = api.GetUserTimeline(screen_name=user)
	if(query and len(query) > 0 and query[0]):
		return '* TRUMP ALERT * '+re.sub(r"http\S+", "", query[0].text)+' *' # remove http links from tweet
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
		sleep(280*12*0.04 + 1) # 40 ms to refresh column * ~10 columns for each character * 280 characters + plus 1s for tx delay


if __name__ == "__main__":

	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()

	try:
		from systemd.journal import JournalHandler
		logger.addHandler(JournalHandler(level=logging.DEBUG))
	except:
		logger.addHandler(logging.FileHandler('/var/log/twitter.log'))

	try:
		with open(key_file, 'r') as f:
			api_key = f.readline().strip()
			api_secret = f.readline().strip()
			token_key = f.readline().strip()
			token_secret = f.readline().strip()
	except Exception as e:
		logger.exception(f'Failed to get API secrets: {e}')
		sys.exit(1)

	try:
		with serial.Serial(port, baud) as ser:
			pass
	except Exception as e:
		logger.exception(f'Failed to Open Serial Device: {e}')
		sys.exit(1)

	api = twitter.Api(
		consumer_key=api_key,
		consumer_secret=api_secret,
		access_token_key=token_key,
		access_token_secret=token_secret
	)

	main()

