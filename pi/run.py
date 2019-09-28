#!/usr/bin/env python3

import twitter
import serial
import sys
import re
import logging
from time import sleep

key_file = '/home/pi/twitter.key'
port = '/dev/serial1'
user = '@realDonaldTrump'
baud = 115200


def displayTweet(tweet):
	try:
		with serial.Serial(port, baud) as ser:
			ser.write(tweet.encode())
		logger.debug(f'Finished Transmitting: {tweet}')
	except Exception as e:
		logger.exception(f'Failed to Open Serial Device: {e}')
		sys.exit(1)


def cleanTweet(input):
	return re.sub(r"http\S+", "", input).replace('\"', '')


def getTweet():
	query = api.GetUserTimeline(screen_name=user)
	if(query and len(query)>0 and query[0].text):
		tweet = cleanTweet(query[0].text)
		if(tweet and len(tweet) > 0):
			return '*** TRUMP ALERT: '+ tweet +' ***'# remove http links from tweet
	return "Test"


def main():
	check_tweet = getTweet()
	cur_tweet = ''
	while True:
		if check_tweet and check_tweet != cur_tweet:
			cur_tweet = check_tweet
			displayTweet(cur_tweet)
		check_tweet = getTweet()
		sleep(10)# 40 ms to refresh column * ~10 columns for each character * 280+23 characters + plus 1s for tx delay


if __name__ == "__main__":

	logger = logging.getLogger(__name__)

	try:
		from systemd.journal import JournalHandler
		logger.addHandler(JournalHandler())
	except Exception:
		pass
	logger.addHandler(logging.FileHandler('/var/log/tweet.log'))
	logger.addHandler(logging.StreamHandler())
	logger.setLevel(logging.DEBUG)

	try:
		with open(key_file, 'r') as f:
			api_key = f.readline().strip()
			api_secret = f.readline().strip()
			token_key = f.readline().strip()
			token_secret = f.readline().strip()
	except Exception as e:
		logger.exception(f'Failed to get API secrets: {e}')
		sys.exit(1)
	logger.info('Read API key')

	try:
		with serial.Serial(port, baud) as ser:
			ser.write('Booting . . .'.encode())
	except Exception as e:
		logger.exception(f'Failed to open serial device: {e}')
		sys.exit(1)
	logger.info('Connected to arduino')

	api = twitter.Api(
		consumer_key=api_key,
		consumer_secret=api_secret,
		access_token_key=token_key,
		access_token_secret=token_secret
	)

	main()