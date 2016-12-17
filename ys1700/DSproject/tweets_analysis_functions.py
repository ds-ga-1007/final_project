"""
Date: 12/12/2016

Authors:Lingzhi Meng(lm3226)
        Yifu Sun(ys1700)
        Yanan Shi(ys2506)

Description: This file contains a function to convert json files to DataFrame. Since each tweet has different attributes, such as hashtag, and language ect., we want to find the top 5 most frequent appeared information for each attribute.
"""

import json,os
import pandas as pd
import matplotlib.pyplot as plt

#read multiple json files in the specific folder
def read_tweets_toDataframe():
	path_to_tweets = 'tweets/'
	tweets_files = [pos_tweets for pos_tweets in os.listdir(path_to_tweets) if pos_tweets.endswith('.json')]
	tweets_data = []
	for index, js in enumerate(tweets_files):
		with open(os.path.join(path_to_tweets, js)) as tweets_file:
			tweets_text = json.load(tweets_file)
			tweets_data.extend(tweets_text)
	return tweets_data

#load tweets into Pandas DataFrame
def tweets_analyze(tweets_data):
	tweets_frame = pd.DataFrame(columns = ['country','city','language','coordinate','text','time','hashtags'])
	counter = 0
	for tweets in tweets_data:
		try:
			country = tweets['fields']['location']['country']
			city = tweets['fields']['location']['name']
			language = tweets['fields']['language']
			coordinate = tweets['fields']['coordinate']
			tweet = tweets['fields']['tweet']
			time = tweets['fields']['time']
			temphashtag = tweets['fields']['hashtag']
			hashtag = get_hashtags_text(temphashtag)
			tweets_frame.loc[counter] = [country, city, language,coordinate, tweet, time, hashtag]
			counter = counter + 1
			print (counter)
		except:
			continue
	return tweets_frame

def save_dataframe_to_CSV(tweets_frame):
	tweets_frame.to_pickle('tweets_frame.pkl')


# count tweets by its attribute
def tweets_by_attribute(tweets_frame, attribute):
    tweets_by_attribute = tweets_frame[attribute].value_counts()
    return tweets_by_attribute

# count tweets by hashtags
def tweets_by_hashtag(tweets_frame):
	hashtag_list = []
	hashtag_frame = tweets_frame.dropna(subset=['hashtags'])
	print
	for hashtag in hashtag_frame['hashtags']:
		hashtag_list.extend(hashtag)
	hashtag_series = pd.Series(hashtag_list)
	tweets_by_hashtag = hashtag_series.value_counts()
	return tweets_by_hashtag


# extract hashtag text from hashtags attribute
def get_hashtags_text(hashtags):
	if len(hashtags) != 0 :
		texts = list(map(get_hashtag_text, hashtags))
		return texts
	else:
		return None

def get_hashtag_text(hashtag):
	return hashtag['text']
