"""
Date: 12/10/2016

Author: Lingzhi Meng(lm3226)
        Yifu Sun(ys1700)
        Yanan Shi(ys2506)

Description: This file contains code that is going to interact with user and plot some tweets analysis graphs based on user input.
"""
import matplotlib.pyplot as plt
import pandas as pd
import sys
from tweets_analysis_functions import *
from tweets_analysis_graphs import *

class InvalidInputException(Exception):
    pass

#check whether the input tweet's attribute is a valid attribute.
def validate_type(Type):
    TypeList = {'A':'language', 'B':'country', 'C':'city', 'D':'hashtag'}
    if Type.upper() in TypeList.keys():
       return TypeList[Type.upper()]
    elif Type.lower() in TypeList.values():
        return Type.lower()
    else:
        raise InvalidInputException


def main():
    tweets_frame = pd.read_pickle('tweets_frame.pkl')
    user_input = ''
    #interact with users and visulize tweets' attribute selected by users
    while True:
        try:
            #ask the user to choose the type of data by language, country, city, or hashtag. Input 'quit' to quit.
            type = input("Please choose a tweet attribute that you would like to see: ")
            if type == 'quit':
                sys.exit(0)
            try:
                user_input = validate_type(type)
            except InvalidInputException:
                print ('Invalid input. Please try it again: ')
                continue
            topfivegraph = tweets_analysis_graphs(user_input,tweets_frame)
            if user_input == 'hashtag':
                topfivegraph.generate_hashtag_top_five_histogram()
                topfivegraph.generate_hashtag_top_five_piechart()
            else:
                topfivegraph.generate_top_five_histogram()
                topfivegraph.generate_top_five_piechart()

            while True:
                try:
                    keyword = input("Would you like to see the graph for top 20 elements of your selected attribute? \n \
                                     Please enter 'yes' or 'no' or 'quit': \n")
                    if keyword == 'quit':
                        sys.exit(0)
                    elif keyword == 'no':
                        break
                    elif keyword == 'yes':
                        allgraph = tweets_analysis_graphs(user_input,tweets_frame)
                        if user_input == 'hashtag':
                            allgraph.generate_hashtag_histogram()
                            allgraph.generate_hashtag_piechart()
                        else:
                            allgraph.generate_tweets_histogram()
                            allgraph.generate_tweets_piechart()
                        break
                    else:
                        raise InvalidInputException
                except InvalidInputException:
                    print('Invalid input. Please try again: ')

        except KeyboardInterrupt:
            sys.exit(0)
        except EOFError:
            sys.exit(0)

if __name__ == "__main__":
    print("We would like to visualize the tweets that we collected through twitter API.")
    print("Each tweet has differnt attribute such as language, city, country, ect..")
    print("We would like to ask user which attribute they would like to see.")
    print("Pie charts and histograms would be generated to represent top five of each attribute.")
    print("There are four differnt attributes to visualize: A.language, B.country, C.city, D.hashtag.")
    print("For example: if you would like to choose language, you could enter 'A' or 'language'.")
    print("If you would like to quit, you can enter 'quit'.")
    main()
