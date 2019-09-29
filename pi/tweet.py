#!/usr/bin/env python3

import loggin
import re
import requests
import sys
import twitter
from time import sleep

key_file = '/home/pi/twitter.key' 		# put your api key file here
url = 'http://192.168.1.23:80/body'		# put your arduino's ip address here
user = '@realDonaldTrump'				#

cur_tweet = ''

def display(msg, boot):
	try:
		res = requests.post(url=url, data=msg)
		if(msg not in res.text):
			raise requests.HTTPError(res.text)
		logger.debug(f'Finished Transmitting: {msg}')
	except Exception as e:
		logger.exception(f'Failed to connect to ESP8266: {e}')
		if(boot):
			sys.exit(1)
		global cur_tweet
		cur_tweet = ''


def cleanTweet(input):
	return re.sub(r"http\S+", "", input).replace('\"', '')


def getTweet():
	query = api.GetUserTimeline(screen_name=user)
	if(query and len(query)>0 and query[0].text):
		tweet = cleanTweet(query[0].text)
		if(tweet and len(tweet) > 0):
			return '*** TRUMP ALERT: '+tweet+' ***'# remove http links from tweet
	return False


def main():
	global cur_tweet
	check_tweet = getTweet()
	while True:
		if check_tweet and check_tweet != cur_tweet:
			cur_tweet = check_tweet
			display(cur_tweet, False)
			sleep(float(len(cur_tweet)) * 0.035 * 12)	
		check_tweet = getTweet()


if __name__ == "__main__":
	logger = logging.getLogger(__name__)
	try:
		from systemd.journal import JournalHandler
		logger.addHandler(JournalHandler())
	except Exception:
		pass
	logger.addHandler(logging.FileHandler('/var/log/tweet.log'))
	#logger.addHandler(logging.StreamHandler())
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

	display("Booting Pi.", True)
	sleep(10)

	api = twitter.Api(
		consumer_key=api_key,
		consumer_secret=api_secret,
		access_token_key=token_key,
		access_token_secret=token_secret
	)

	try:
		main()
	except KeyboardInterrupt as e:
		logger.info('Detected keyboard interrupt, exiting . . . ')
