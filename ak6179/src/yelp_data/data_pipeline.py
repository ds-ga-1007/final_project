"""
data_pipeline module.
"""
import os
import json
import pandas as pd
import numpy as np
from functools import reduce
from . import yelp_data_utils as utils


class YelpData(object):
    DEFAULT_CHECKIN_FILENAME = 'yelp_academic_dataset_checkin.json'
    DEFAULT_BUSINESS_FILENAME = 'yelp_academic_dataset_business.json'
    DEFAULT_REVIEW_FILENAME = 'yelp_academic_dataset_review_remove_text.json'
    DEFAULT_REVIEW_SAMPLE_FILENAME = 'yelp_academic_dataset_review_sample_0.25.csv'
    DEFAULT_USER_FILENAME = 'yelp_academic_dataset_user.json'

    @staticmethod
    def _update_filename(default_filename, new_filename):
        if new_filename is not None:
            return new_filename
        else:
            return default_filename

    def _validate_paths(self):
        """
        Checks if the directory and filepaths are valid.
        Throws FileNotFoundError if filepaths are invalid.
        """
        utils.check_directory_exists(self._datapath)
        utils.check_file_exists(self._checkin_datapath)
        utils.check_file_exists(self._business_datapath)
        utils.check_file_exists(self._review_datapath)
        utils.check_file_exists(self._user_datapath)

    def __init__(self, datapath,
                 checkin_filename=DEFAULT_CHECKIN_FILENAME,
                 business_filename=DEFAULT_BUSINESS_FILENAME,
                 review_filename=DEFAULT_REVIEW_FILENAME,
                 review_sample_filename=DEFAULT_REVIEW_SAMPLE_FILENAME,
                 user_filename=DEFAULT_USER_FILENAME):
        """
        Constructor for YelpData class. Sets filepaths and checks if the files exist at the specified locations
        :param datapath: Directory containing the Yelp data
        :param checkin_filename: File containing checkin information.
        :param business_filename: File containing information about businesses.
        :param review_filename: File containing reviews information.
        For getting information about data present in different files refer to class methods which load the
        corresponding dataframes.
        """
        self._datapath = datapath
        self._checkin_datapath = os.path.join(self._datapath, checkin_filename)
        self._business_datapath = os.path.join(self._datapath, business_filename)
        self._review_datapath = os.path.join(self._datapath, review_filename)
        self._review_sample_datapath = os.path.join(self._datapath, review_sample_filename)
        self._user_datapath = os.path.join(self._datapath, user_filename)
        self._validate_paths()

    def get_checkin_dataframe(self):
        """
        :return: Dataframe containing checkin data. The dataframe will contain the following columns:
        columns: ['business_id', 'checkin_info', 'type']
        """
        with open(self._checkin_datapath) as f:
            checkin_data = [json.loads(line) for line in f]
        checkin_df = pd.DataFrame(checkin_data)
        return checkin_df

    def generate_checkin_matrix(self, checkin_df):
        """
        :param checkin_df: Dataframe containing checkin data. Assumes that the dataframe contains checkin_info information
        :return: 7x24xlen(checkin_df) array with checkin info for each business in 7x24 numpy array format.
            results are saved as .npy file
        """
        checkin_matrixform = np.zeros((7,24,len(checkin_df)))
        for entry in range(len(checkin_df)):
            matrix = np.zeros((7,24))
            for days in range(7):
                for hours in range(24):
                    checkin_entry = str(hours) + '-' + str(days)
                    try:
                        matrix[days, hours] = checkin_df['checkin_info'][entry][checkin_entry]
                    except KeyError:
                        pass
            checkin_matrixform[:,:,entry] = matrix

        np.save(self._datapath + 'checkin_matrixform.npy', checkin_matrixform)
        return checkin_matrixform
    
    def load_checkin_matrix(self, checkin_df):
        """
        Attempts to read in numpy matrix form of checkin data if it has previously been stored.
        """
        try:
            checkin_matrixform = np.load(self._datapath + 'checkin_matrixform.npy')
        except FileNotFoundError:
            checkin_matrixform = self.generate_checkin_matrix(checkin_df)
        return checkin_matrixform

    def get_business_dataframe(self):
        """
        :return: Dataframe containing business data. The dataframe will contain the following:
        columns: ['attributes', 'business_id', 'categories', 'city', 'full_address', 'hours', 'latitude', 'longitude',
                  'name', 'neighborhoods', 'open', 'review_count', 'stars', 'state', 'type']
        """
        with open(self._business_datapath) as f:
            business_data = [json.loads(line) for line in f]
        business_df = pd.DataFrame(business_data)
        return business_df

    def get_category_array(self, business_df):
        """
        :param business_df: Dataframe containing business data. Assumes that the dataframe contains category information
        :return: Array containing the union of all categories in business_df 'categories' column if
            result was not previously cached.
        """
        try:
            category_array = np.load(self._datapath + 'category_array.npy')
        except FileNotFoundError:
            category_array = reduce(np.union1d, business_df['categories'].values)
            np.save(self._datapath + 'category_array.npy', category_array)
        return category_array


    @staticmethod
    def get_business_data_locations(business_df):
        """
        :param business_df: Dataframe containing business data. Assumes that the dataframe contains latitude,
                            longitude information
        :return: Dataframe containing only latitude and longitude information
        """
        return business_df[['latitude', 'longitude']]

    def get_review_dataframe(self):
        """
        :return: Dataframe containing reviews data. Note that text from review data has been removed to cut
        down size. The dataframe will contain the following
        columns: ['business_id', 'date', 'review_id', 'stars', 'type', 'user_id', 'votes']
        """
        with open(self._review_datapath) as f:
            review_data = json.load(f)
        review_df = pd.DataFrame(review_data)
        review_df['date'] = pd.to_datetime(review_df['date'])
        return review_df

    def get_review_sample_dataframe(self, index_col=0):
        """
        :return: Dataframe containing a sample of the reviews data. Note that text from review data has been
         removed to cut down size. The dataframe will contain the following
         columns: ['business_id, 'date', 'review_id', 'stars', 'type', 'user_id', 'votes']
        """
        review_sample_df = pd.read_csv(self._review_sample_datapath, index_col=index_col)
        review_sample_df['date'] = pd.to_datetime(review_sample_df['date'])
        return review_sample_df

    def get_user_dataframe(self):
        """
        :return: Dataframe containing user data. The dataframe will contain the following:
        columns: ['average_stars', 'compliments', 'elite', 'fans', 'friends', 'name',
                  'review_count', 'type', 'user_id', 'votes', 'yelping_since']
        """
        with open(self._user_datapath) as f:
            user_data = [json.loads(line) for line in f]
        user_df = pd.DataFrame(user_data)
        return user_df

    @staticmethod
    def merge_reviews_business_df(reviews_df, business_df, on='business_id', how='inner'):
        """
        Merges/joins reviews_df and business_df. Note that the merge_column should be present in both
        the reviews_df and business_df
        :param reviews_df: Dataframe containing reviews data.
        :param business_df: Dataframe containing business data.
        :param on: Column on which the dataframes are merged/joined.
        :param how: Type of merge/join.
        :return: merged/joined dataframe.
        """
        return pd.merge(reviews_df, business_df, on=on, how=how)

