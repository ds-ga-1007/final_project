"""
This program allows users to generate and compare time series for the distribution of "checkins" throughout the day 
for businesses in different cities and categories. The user will initially be prompted to enter the name of a city 
then prompted to enter the name of a category. When the user is done entering these a plot of the fraction of checkins
for businesses in that category that occur in each hour of the day. The user can re-enter a city and category to
generate  new time series until satisfied, then must type "finished" to move on to the comparison of time series. Upon
typing "finish", the user will be prompted twice to enter the names of cities and twice to enter the names of business
categories. The program will then generate a plot containing the time series for both city/category combinations
together. The user can re-enter their choice of cities and categories to generate new plots until satisfied. The user
must then type "quit" to exit. Note that for any prompt the user can type "All" to specify all cities/categories in
the database. Also note that the user must only enter one name at each prompt.

For running the example you can use either of the following two commands:
1) python time_series_example.py (if the mapping-yelp-data folder has been placed just under the root
   'mapping-yelp' directory).
2) python time_series_example.py -data_folder path
   In the above command path, is the path to 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/' folder.
"""
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import matplotlib
import seaborn
import sys
import argparse
import logging
sys.path.append('../src')
import yelp_data
import time_series


def arguments_parser():
    parser = argparse.ArgumentParser()
    # Note that the unzipped data should be present at the location specified below.
    parser.add_argument('-data_folder', default='../mapping-yelp-data/yelp_dataset_challenge_academic_dataset/',
                        type=str)
    args = parser.parse_args()
    return args


def main():
    args = arguments_parser()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    data = yelp_data.YelpData(args.data_folder)
    logging.info('Loading checkin data.')
    checkin_df = data.get_checkin_dataframe()
    print('-' * 40)
    logging.info('Converting checkin data to matrix form, this might take some time.')
    checkin_matrixform = data.load_checkin_matrix(checkin_df)
    print('-' * 40)
    logging.info('Loading business data.')
    business_df = data.get_business_dataframe()
    print('-' * 40)
    logging.info('Aggregating list of business categories.')
    category_list = data.get_category_array(business_df)
    print('-' * 40)
    
    candidate_cities = ['Edinburgh', 'Karlsruhe', 'Montreal', 'Waterloo', 'Pittsburgh',
                        'Urbana-Champaign', 'Phoenix', 'Las Vegas', 'Madison']
    
    finish_string = 'finish'
    quit_string = 'quit'
    
    print("You can now generate time series for the distribution of checkins")
    print("for businesses in a particular city/business category.")
    print("You can enter any of the following cities:\n" + str(candidate_cities) + "\n")
    print("Categories can be any viable yelp business category. \n")
    print("Type 'finish' to move to next analysis.")

    while True:
        city = input('Enter city name (or All to see all cities): ')
        if city.lower() == finish_string:
            print('Moving to next analysis.')
            break
        category = input('Enter business category (or All to see all categories): ')
        if category.lower() == finish_string:
            print('Moving to next analysis.')
            break
        
        if city.lower() == 'all':
            city = None
        if category.lower() == 'all':
            category = None
        
        city_label, category_label = time_series.yelp_plotting.generate_labels(city,category)
        print('Plotting time series for category-' + str(category_label) +
              ' in city-' + str(city_label))
        try:
            time_series.yelp_plotting.generate_Time_Series(business_df, checkin_df, checkin_matrixform, category_list, city=city, category=category)
        except KeyError:
            print("Invalid city/category")


    print('-' * 40)
    print("You can now compare two city/category combinations:")
    print("You can enter any of the following cities:\n" + str(candidate_cities) + "\n")
    print("Categories can be any viable yelp business category. \n")
    print("Type 'quit' to finish analysis.")
    
    while True:
        city1 = input('Enter city1 (or All to select all cities): ')
        if city1.lower() == quit_string:
            print('Exiting')
            break
        city2 = input('Enter city2 (or All to select all cities): ')
        if city2.lower() == quit_string:
            print('Exiting')
            break
        category1 = input('Enter category1 (or All to select all categories): ')
        if category1.lower() == quit_string:
            print('Exiting')
            break
        category2 = input('Enter category2 (or All to select all categories): ')
        if category2.lower() == quit_string:
            print('Exiting')
            break

        if city1.lower() == 'all':
            city1 = None
        if city2.lower() == 'all':
            city2 = None
        if category1.lower() == 'all':
            category1 = None
        if category2.lower() == 'all':
            category2 = None
        
        city_label1, category_label1 = time_series.yelp_plotting.generate_labels(city1,category1)
        city_label2, category_label2 = time_series.yelp_plotting.generate_labels(city2,category2)
        print('Plotting time series for category-' + str(category_label1) + ' in city-' + str(city_label1) +
              ' vs. category-' + str(category_label2) + ' in city-' + str(city_label2))
        try:
            time_series.yelp_plotting.compare_Time_Series(business_df, checkin_df, checkin_matrixform, category_list, city1=city1, category1=category1, city2=city2, category2=category2)
        except KeyError:
            print("Invalid city/category")



#borrowed from http://stackoverflow.com/questions/21120947/catching-keyboardinterrupt-in-python-during-program-shutdown
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
