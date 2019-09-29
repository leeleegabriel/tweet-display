#!/usr/bin/env python3

import logging
import re
import requests
import sys
import twitter
from time import sleep

key_file = '/home/pi/twitter.key' 		# put your api key file here
url = 'http://192.168.1.23:80/body'		# put your arduino's ip address here
user = '@realDonaldTrump'				#

def display(msg):
	try:
		res = requests.post(url=url, data=msg)
		if msg not in res.text:
			raise requests.HTTPError(res.text)
		logger.debug(f'Finished Transmitting: {msg}')
	except Exception as e:
		logger.exception(f'Failed to connect to ESP8266: {e}')
		return False


def getTweet():
	query = api.GetUserTimeline(screen_name=user)
	if query and len(query)>0:
		for tweet in query:
			tweet = re.sub(r"http\S+", "", tweet.text).replace('\"', '')
			if(tweet and len(tweet) > 0):
				return '*** TRUMP ALERT: ' + tweet + ' ***'# remove http links from tweet
	return False


def main():
	old_tweet = ''
	new_tweet = getTweet()
	while True:
		if new_tweet and new_tweet != old_tweet:
			display(new_tweet)
			old_tweet = new_tweet
			sleep(float(len(new_tweet)) * 0.045 * 12.0)	
		new_tweet = getTweet()
		sleep(60)


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

	display("Booting Pi.")
	sleep(10)
	api = twitter.Api(
		consumer_key=api_key,
		consumer_secret=api_secret,
		access_token_key=token_key,
		access_token_secret=token_secret,
		sleep_on_rate_limit=True
	)

	try:
		main()
	except KeyboardInterrupt as e:
		logger.info('Detected keyboard interrupt, exiting . . . ')
