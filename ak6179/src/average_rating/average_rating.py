import pandas as pd
import datetime


def _validate_window(window_days_size):
    if not isinstance(window_days_size, int) or window_days_size <= 0:
        raise ValueError('Window size should be a positive integer.')


class AverageRating(object):
    @staticmethod
    def check_valid_period(period):
        """
        Checks whether period is a positive integer.
        :param period
        """
        try:
            int(period)
            if int(period) > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    @staticmethod
    def calculate_average_ratings(reviews_df, window_days_size=30, ratings_column_name='stars', sorted_date=False):
        """
        Calculates the average rating for windows of length window_days_size.
        :param reviews_df: reviews dataframe, it should contain date column.
        :param window_days_size: duration in days of the window
        :param ratings_column_name: name of the ratings column.
        :param sorted_date: indicates whether the dataframe is sorted according to time.
        :return: starting date of a sample window, average rating during that window.
        """
        _validate_window(window_days_size)
        average_ratings_df = pd.DataFrame(reviews_df[['date', ratings_column_name]])
        if not sorted_date:
            average_ratings_df.sort_values('date', inplace=True)
        first_date = average_ratings_df.iloc[0]['date']

        def map_date_bucket(current_date):
            delta = current_date - first_date
            bucket = int(delta.days / window_days_size)
            return bucket

        def map_bucket_date(bucket):
            date = first_date + datetime.timedelta(days=bucket * window_days_size)
            return date

        average_ratings_df['date_bucket'] = reviews_df['date'].map(map_date_bucket)
        ratings = average_ratings_df.groupby('date_bucket')[ratings_column_name].mean()
        counts_reviews = average_ratings_df.groupby('date_bucket')[ratings_column_name].count()
        buckets_dates = ratings.index.map(map_bucket_date)
        average_data = {'average_rating': ratings.values, 'count_reviews': counts_reviews.values}
        dates_average_rating_df = pd.DataFrame(average_data, index=buckets_dates)
        return dates_average_rating_df
