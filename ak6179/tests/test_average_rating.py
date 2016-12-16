"""
Unit tests for AverageRating class.
"""

import unittest
import sys
sys.path.append("src")
from yelp_data import YelpData
from average_rating import AverageRating


class AverageRatingTests(unittest.TestCase):
    def test_calculate_average_ratings(self):
        """
        Tests for the calculate_average_ratings method.
        """
        data_folder_path = 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/'
        data = YelpData(data_folder_path)
        sample_reviews_df = data.get_review_sample_dataframe()
        _ = AverageRating.calculate_average_ratings(sample_reviews_df, 180)
        with self.assertRaises(ValueError):
            _ = AverageRating.calculate_average_ratings(sample_reviews_df, -100)
        with self.assertRaises(ValueError):
            _ = AverageRating.calculate_average_ratings(sample_reviews_df, 0)
        with self.assertRaises(ValueError):
            _ = AverageRating.calculate_average_ratings(sample_reviews_df, "30")
        with self.assertRaises(ValueError):
            _ = AverageRating.calculate_average_ratings(sample_reviews_df, "thirty")
        with self.assertRaises(ValueError):
            _ = AverageRating.calculate_average_ratings(sample_reviews_df, None)
