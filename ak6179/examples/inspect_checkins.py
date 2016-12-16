"""
This program allows users to get an overview of the distribution of "checkins" for each hour of the day for each
of the 9 cities in the Yelp database. The program will produce a plot initially showing the fraction of each city's
checkins that occur in the hour starting at 12pm. The user can adjust the hour of interest using the
slider below the plot.

For running the example you can use either of the following two commands:
1) python inspect_checkins_example.py (if the mapping-yelp-data folder has been placed just under the root
   'mapping-yelp' directory).
2) python inspect_checkins_example.py -data_folder path
   In the above command path, is the path to 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/' folder.
"""
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from matplotlib.widgets import Slider
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
    logging.info('Collecting checkins across 9 cities and plotting results (interactive).')
    time_series.yelp_plotting.plot_total_checkins_9cities(business_df, checkin_df, checkin_matrixform)

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
