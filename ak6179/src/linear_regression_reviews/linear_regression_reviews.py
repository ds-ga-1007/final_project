import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


class LinearRegressionReviews(object):
    @staticmethod
    def _offset_rolling_mean(series):
        """
        :param series: Takes a time sorted series of ratings.
        :return: Rolling averages at different time points for the series.
        """
        count = 0
        new_series = series.copy()
        for ind, x in enumerate(series):
            if ind == 0:
                new_series.iloc[0] = 0
            else:
                new_series.iloc[ind] = count / ind
            count += x
        return new_series

    def featurize_data(self, train_df, test_df):
        """
        Adds rolling average rating features for businesses and users. Adds column indicating the first review
        for a business and a first review for the user.
        :param train_df: Training dataframe
        :param test_df: Testing dataframe
        :return: Dataframe with added feature columns
        """
        rolling_user_means = train_df.groupby('user_id')['stars'].apply(self._offset_rolling_mean)
        rolling_business_means = train_df.groupby('business_id')['stars'].apply(self._offset_rolling_mean)
        train_df['user_average'] = rolling_user_means.reset_index().set_index('index')['stars'].replace(np.nan, 0)
        train_df['business_average'] = rolling_business_means.reset_index().set_index('index')['stars'].replace(np.nan, 0)
        train_df['first_user_review'] = (train_df.user_average == 0).astype(int)
        train_df['first_business_review'] = (train_df.business_average == 0).astype(int)

        test_df = test_df.merge(train_df.groupby('user_id')['stars'].mean().reset_index(), on='user_id', how='left')
        test_df = test_df.merge(train_df.groupby('business_id')['stars'].mean().reset_index(),
                                on='business_id', how='left')
        test_df.columns = ['business_id', 'date', 'review_id', 'stars', 'user_id', 'user_average', 'business_average']
        test_df['user_average'] = test_df.user_average.replace(np.nan, 0)
        test_df['business_average'] = test_df.business_average.replace(np.nan, 0)
        test_df['first_user_review'] = (test_df.user_average == 0).astype(int)
        test_df['first_business_review'] = (test_df.business_average == 0).astype(int)
        return train_df, test_df

    @staticmethod
    def _limit_ratings(ratings):
        """
        Limits the predicted ratings to a range of 1 to 5
        :param ratings
        """
        limited_ratings = []
        for r in ratings:
            if r > 5:
                limited_ratings.append(5)
            elif r < 1:
                limited_ratings.append(1)
            else:
                limited_ratings.append(r)
        return limited_ratings

    def fit(self, train_df,
            train_cols=['user_average', 'business_average', 'first_user_review', 'first_business_review'],
            test_col='stars'):
        """
        Training function for Linear Regression.
        :param train_df
        :param train_cols
        :param test_col
        """
        self._lr.fit(train_df[train_cols], train_df[test_col])

    def predict(self, test_df,
                test_cols=['user_average', 'business_average', 'first_user_review', 'first_business_review']):
        """
        Prediction function for Linear Regression.
        :param test_df:
        :param test_cols:
        """
        predictions = self._lr.predict(test_df[test_cols])
        predictions = self._limit_ratings(predictions)
        return predictions

    @staticmethod
    def calculate_rmse(truth, predictions):
        rmse = mean_squared_error(truth, predictions) ** 0.5
        return rmse

    def __init__(self):
        self._lr = LinearRegression()
