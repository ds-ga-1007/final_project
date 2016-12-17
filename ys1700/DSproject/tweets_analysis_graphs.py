"""
Date: 12/10/2016

Authors:Lingzhi Meng(lm3226)
        Yifu Sun(ys1700)
        Yanan Shi(ys2506)

Description: This file generates pie chart and histogram as data anlysis graphs for different tweets' attributes that we collected.
"""
import matplotlib as plt
from tweets_analysis_functions import *

class tweets_analysis_graphs():
    def __init__(self, input_string,data_frame):
        self.input_string = input_string
        self.tweet_frame = data_frame

    def generate_tweets_piechart(self):
        #This function generates pie chart for different attributs of tweets that we collected.
        tweet_attribute = tweets_by_attribute(self.tweet_frame, self.input_string)
        fig = tweet_attribute[0: 20].plot.pie(figsize=(10,10))
        fig.set_title('Pie chart of Top 20 ' + str(self.input_string))
        plt.savefig('Pie chart of Top 20 ' + str(self.input_string) + '.pdf')
        plt.show()
        plt.close()

    def generate_top_five_piechart(self):
        #This function generates pie chart for different attributs of tweets that we collected.
        tweet_attribute = tweets_by_attribute(self.tweet_frame, self.input_string)
        fig = tweet_attribute[0: 5].plot.pie(figsize=(10,10))
        fig.set_title('Pie chart of Top 5 ' + str(self.input_string))
        plt.savefig('Pie chart of Top 5' + str(self.input_string) + '.pdf')
        plt.show()
        plt.close()

    def generate_tweets_histogram(self):
        #This function generates histogram for different attributs of tweets that we collected.
        tweet_attribute = tweets_by_attribute(self.tweet_frame, self.input_string)
        fig,ax= plt.subplots()
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_xlabel(str(self.input_string), fontsize=15)
        ax.set_ylabel('Number of tweets' , fontsize=15)
        ax.set_title('Top 20 '+ str(self.input_string) , fontsize=15, fontweight='bold')
        tweet_attribute[0: 20].plot(ax=ax, kind='bar', color='blue')
        plt.savefig('Histogram of Top 20 ' + str(self.input_string) + '.pdf')
        plt.show()
        plt.close()

    def generate_top_five_histogram(self):
        #This function generates histogram for different attributs of tweets that we collected.
        tweet_attribute = tweets_by_attribute(self.tweet_frame, self.input_string)
        fig,ax= plt.subplots()
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_xlabel(str(self.input_string), fontsize=15)
        ax.set_ylabel('Number of tweets' , fontsize=15)
        ax.set_title('Top 5 '+ str(self.input_string) , fontsize=15, fontweight='bold')
        tweet_attribute[0: 5].plot(ax=ax, kind='bar', color='blue')
        plt.savefig('Histogram of Top 5 ' + str(self.input_string) + '.pdf')
        plt.show()
        plt.close()

    def generate_hashtag_piechart(self):
        #This function generates pie chart for different attributs of tweets that we collected.
        tweet_attribute = tweets_by_hashtag(self.tweet_frame)
        fig = tweet_attribute[0: 20].plot.pie(figsize=(10,10))
        fig.set_title('Pie chart of Top 20 ' + str(self.input_string))
        plt.savefig('Pie chart of Top 20 ' + str(self.input_string) + '.pdf')
        plt.show()
        plt.close()


    def generate_hashtag_top_five_piechart(self):
        #This function generates pie chart for different attributs of tweets that we collected.
        tweet_attribute = tweets_by_hashtag(self.tweet_frame)
        fig = tweet_attribute[0: 5].plot.pie(figsize=(10,10))
        fig.set_title('Pie chart of Top 5 ' + str(self.input_string))
        plt.savefig('Pie chart of Top 5 ' + str(self.input_string) + '.pdf')
        plt.show()
        plt.close()


    def generate_hashtag_histogram(self):
        #This function generates histogram for different attributs of tweets that we collected.
        tweet_attribute = tweets_by_hashtag(self.tweet_frame)
        fig,ax= plt.subplots()
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_xlabel('hashtag', fontsize=15)
        ax.set_ylabel('Number of tweets' , fontsize=15)
        ax.set_title('Top 20 hashtags', fontsize=15, fontweight='bold')
        tweet_attribute[0: 20].plot(ax=ax, kind='bar', color='blue')
        plt.savefig('Histogram of Top 20 ' + str(self.input_string) + '.pdf')
        plt.show()
        plt.close()

    def generate_hashtag_top_five_histogram(self):
        #This function generates histogram for different attributs of tweets that we collected.
        tweet_attribute = tweets_by_hashtag(self.tweet_frame)
        fig,ax= plt.subplots()
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_xlabel('hashtag', fontsize=15)
        ax.set_ylabel('Number of tweets' , fontsize=15)
        ax.set_title('Top 5 hashtags', fontsize=15, fontweight='bold')
        tweet_attribute[0: 5].plot(ax=ax, kind='bar', color='blue')
        plt.savefig('Histogram of Top 5 ' + str(self.input_string) + '.pdf')
        plt.show()
        plt.close()
