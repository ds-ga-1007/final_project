import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../src')
from average_rating import AverageRating


class InvalidBusinessName(Exception):
    """
    Custom exception for handling the invalid business name.
    """
    def __str__(self):
        return 'Not a valid business name; not in Yelp dataset'


def _calculate_rolling_average(df, df_column):
    """
    The function takes a particular variable (or column) in a dataframe and calculates the rolling average of
    the variable based on a 180-day interval. For example, it calculates the average of the variable within each
    180-day interval in our dataset. The function returns a new dataframe that lists the average within
    each time interval.
    :param df: dataframe
    :param df_column: column in the dataframe on which the average has to be calculated.
    :return: the rolling average of the column
    """
    rolling_average_df = AverageRating.calculate_average_ratings(df, window_days_size=180,
                                                                 ratings_column_name=df_column)
    return rolling_average_df


class CompanyRatings(object):
    @staticmethod
    def check_valid_business(name, combined_df):
        """
        :param name: business/franchise name
        :param combined_df: dataframe containing the names of business/franchises.
        :return: the name if it is valid.
        """
        if name not in np.array(combined_df['name']):
            raise InvalidBusinessName
        return name

    @staticmethod
    def calculate_moving_average(df, df_column):
        """
        :param df: dataframe
        :param df_column: column in the dataframe on which the moving average has to be calculated
        :return: the existing dataframe, with the addition of \'moving average\' as a new column
        """
        df['cumulative_sum'] = df[df_column].cumsum()
        df['moving_average'] = df['cumulative_sum']/(df.index+1)
        return df

    @staticmethod
    def plot_moving_average(dates, moving_average, name, company_names):
        """
        This method creates a plot that charts the moving average of a variable,
        labeling the x-axis as "Date" and the y-axis as "Moving Average".
        :param dates: dates for the x-axis
        :param moving_average: values on the y-axis
        :param name: name of business/franchise
        :param company_names: list of all the company names that have to plotted
        """
        plt.subplot(2, 1, 1)
        plt.plot(dates, moving_average, label=name)
        plt.xlabel('Date')
        plt.ylabel('Moving Average of Rating')
        plt.legend()
        plt.title('Moving Average of Rating for {0}'.format(str(company_names)[1:-1]))

    @staticmethod
    def plot_rolling_average(df, df_column, name, company_names):
        """
        This method creates a plot that charts the average of a variable during a particular time interval.
        The method labels the x-axis as "Dates" and the y-axis as "Average Rating".
        :param df: dataframe
        :param df_column: column in the dataframe on which the moving average has to be calculated
        :param name: name of the graph
        """
        df = _calculate_rolling_average(df, df_column)
        plt.subplot(2, 1, 2)
        plt.plot(df.index, df['average_rating'], label=name)
        plt.xlabel('Date')
        plt.ylabel('Average Rating in {0}-Day Period'.format(180))
        plt.legend()
        plt.title('Rolling {0}-Day Average Rating for {1}'.format(180, str(company_names)[1:-1]))
