from tweets_analysis import *


if __name__ == "__main__":
	tweets_data = read_tweets_toDataframe()
	tweets_frame = tweets_analyze(tweets_data)
	save_dataframe_to_CSV(tweets_frame)