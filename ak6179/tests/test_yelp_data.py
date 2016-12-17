"""
Unit tests for YelpData class.
Unit Tests for loading all the dataframes are not added because the loading methods are
directly using the Pandas library. Tests for loading of some small sized dataframes are
added below.
"""

import unittest
import sys
sys.path.append("src")
from yelp_data import YelpData


class YelpDataTests(unittest.TestCase):
    def test_constructor(self):
        """
        Test the YelpData constructor.
        Note that the data folder should be present at the location specified in the user-guide.
        """
        # Test valid file locations.
        data_folder_path = 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/'
        _ = YelpData(data_folder_path)
        _ = YelpData(data_folder_path,
                     checkin_filename='yelp_academic_dataset_checkin.json',
                     business_filename='yelp_academic_dataset_business.json',
                     review_filename='yelp_academic_dataset_review_remove_text.json',
                     review_sample_filename='yelp_academic_dataset_review_sample_0.25.csv',
                     user_filename='yelp_academic_dataset_user.json')
        # Test invalid file locations
        invalid_path = 'invalid_path'
        with self.assertRaises(FileNotFoundError):
            _ = YelpData(invalid_path)
        with self.assertRaises(FileNotFoundError):
            _ = YelpData(data_folder_path,
                         checkin_filename='yelp_academic_dataset_checkin.json',
                         business_filename=invalid_path,
                         review_filename='yelp_academic_dataset_review_remove_text.json')
        with self.assertRaises(FileNotFoundError):
            _ = YelpData(data_folder_path,
                         checkin_filename='yelp_academic_dataset_checkin.json',
                         user_filename=invalid_path)

    def test_get_review_sample_dataframe(self):
        """
        Test loading of a sample review data
        """
        data_folder_path = 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/'
        data = YelpData(data_folder_path)
        _ = data.get_review_sample_dataframe()
        invalid_path = 'invalid_path'
        with self.assertRaises(FileNotFoundError):
            _ = YelpData(data_folder_path, user_filename=invalid_path)

    def test_get_business_dataframe(self):
        """
        Test loading of business dataframe.
        """
        data_folder_path = 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/'
        data = YelpData(data_folder_path)
        _ = data.get_business_dataframe()
        invalid_path = 'invalid_path'
        with self.assertRaises(FileNotFoundError):
            _ = YelpData(data_folder_path, business_filename=invalid_path)

    def test_get_checkin_dataframe(self):
        """
        Test loading of checkin dataframe.
        """
        data_folder_path = 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/'
        data = YelpData(data_folder_path)
        _ = data.get_checkin_dataframe()
        invalid_path = 'invalid_path'
        with self.assertRaises(FileNotFoundError):
            _ = YelpData(data_folder_path, checkin_filename=invalid_path)

