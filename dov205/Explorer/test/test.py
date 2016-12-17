import unittest
from commentary import *


class CommentaryTest(unittest.TestCase):
    """Unit-testing class that allows us to run tests with expected outcomes.

    Run the test in the project's root directory (e.g. pwd should be '.../dov205/')
    with the following command:

        $ python -m unittest discover
    """

    @classmethod
    def setUpClass(cls):
        """Setup testing class to have our dataset as a class variable."""
        super(CommentaryTest, cls).setUpClass()
        cls.data = load_reddit_data()

    def test_valid_header_sourcing(self):
        """Test the valid sourcing of our header file."""

        # Read our headers file.
        with open('data/headers.txt', 'r') as f:
            header = f.readline().strip()

        # Establish answer key.
        should_be = "text,id,subreddit,meta,time,author,ups,downs,authorlinkkarma,authorkarma,authorisgold"

        # Our headers text should not be empty.
        self.assertNotEqual(header, "", "Error: unable to source header.txt")

        # Our headers text should be the same as the answer key.
        self.assertEqual(header, should_be, "Error: header is not what it should be")

    def test_valid_file_sourcing(self):
        """Test the valid sourcing of our CSV file."""

        # Ensure correct setUp and ability to read comments DataFrame.
        self.assertTrue(isinstance(CommentaryTest.data, pd.DataFrame))

    def test_valid_subset_dataframe(self):
        """Test whether subsetting our DataFrame with valid features is successful."""

        # Ensure that all columns we might be interested in for analysis
        # are subscriptable and valid.
        columns_of_interest = ['text', 'id', 'subreddit', 'meta', 'date', 'author',
                               'ups', 'downs', 'authorlinkkarma', 'authorkarma',
                               'authorisgold']

        # Assume none are valid.
        valid_features = 0

        # With each successful validation, increment our valid count.
        for feature in columns_of_interest:
            validate_valid_feature(feature, CommentaryTest.data)
            valid_features += 1

        # By the end, our valid count should equal the length of (proposed)
        # valid features
        self.assertEqual(len(columns_of_interest), valid_features, "Error: valid feature was invalid.")

    def test_invalid_subset_dataframe(self):
        """Test whether subsetting our DataFrame with invalid features is rightfully unsuccessful."""

        # Define columns we would expect to not be index-able.
        invalid_columns = ['time', 'hour', 'upds']

        # Assume none are valid.
        valid_features = 0

        # For each candidate, assert that they'll raise an InvalidFeatureRequest
        # exception. Increment our valid features counter if they don't.
        for feature in invalid_columns:
            with self.assertRaises(InvalidFeatureRequest):
                validate_valid_feature(feature, CommentaryTest.data)
                valid_features += 1

        # Hence, by here our valid count should still be 0 because
        # none of the invalid features should have been validated.
        self.assertEqual(valid_features, 0, "Error: invalid feature was valid.")
