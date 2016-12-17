"""
Unit Tests for CompanyRating class
"""
import unittest
import sys
sys.path.append("src")
import yelp_data
import company_ratings

data = yelp_data.YelpData('mapping-yelp-data/yelp_dataset_challenge_academic_dataset/')
business_df = data.get_business_dataframe()
review_df = data.get_review_sample_dataframe()
combined_df = data.merge_reviews_business_df(review_df, business_df)
combined_df = combined_df.rename(columns={'stars_x': 'user_rating', 'stars_y': 'business_rating'})


class Test(unittest.TestCase):
    def test_valid_business_class(self):
        """
        Tests for checking valid business names.
        """
        ratings = company_ratings.CompanyRatings()
        self.assertEqual(ratings.check_valid_business('Starbucks', combined_df), 'Starbucks')
        with self.assertRaises(company_ratings.InvalidBusinessName) as message:
            ratings.check_valid_business("Staaaaarbucks", combined_df)
        self.assertTrue('Not a valid business name; not in Yelp dataset' in str(message.exception))
