"""
Unit tests for time_series package.
"""

import unittest
import sys
sys.path.append("src")
import numpy as np
from time_series import yelp_plotting
from yelp_data import YelpData


class TestTimeSeries(unittest.TestCase):
    def setUp(self):
        data_folder_path = 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/'
        data = YelpData(data_folder_path)
        self.business_df = data.get_business_dataframe()
        self.category_list = data.get_category_array(self.business_df)
    
    def test_filterByCategory_mask(self):
        """
        Test whether filterByCategory_mask() properly filters business data by category
        """
        mask = yelp_plotting.filterByCategory_mask(self.business_df, 'Zoos')
        valid = True
        for business_categories in self.business_df[mask].categories.values:
            if 'Zoos' not in business_categories:
                valid = False
        self.assertEqual(valid, True)

    def test_check_city(self):
        """
        Test check on valid city
        """
        # Test valid city
        valid_city = 'Montreal'
        _ = yelp_plotting.check_city(valid_city)
        # Test invalid city
        invalid_city = 'New York'
        with self.assertRaises(KeyError):
            _ = yelp_plotting.check_city(invalid_city)

    def test_check_category(self):
        """
        Test check on valid category
        """
        # Test valid category
        valid_category = 'Zoos'
        _ = yelp_plotting.check_category(valid_category, self.category_list)
        # Test invalid city
        invalid_category = 'not-a-category'
        with self.assertRaises(KeyError):
            _ = yelp_plotting.check_category(invalid_category, self.category_list)

    def test_get_timezone_shift(self):
        """
        Test check on proper timezone shifting
        """
        San_fran_time = 12
        Edinburgh_time = 20
        shifted_San_fran_time = np.mod(San_fran_time - yelp_plotting.get_timezone_shift('Edinburgh'), 24)
        self.assertEqual(shifted_San_fran_time, Edinburgh_time)
        


