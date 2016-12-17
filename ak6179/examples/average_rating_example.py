"""
An example to analyze trends in average ratings over time. You can enter different cities for analysis.
Initially the required dataset will be loaded. Then you will be asked to enter a period window. This is the
number of days for the window. Then you will be prompted for a comma separated list of cities. You can
enter a string like "Phoenix, Las Vegas". After entering this a graph will be shown. You can close the
graph and continue entering cities for the visualization. Enter 'quit' to exit the visualization.

For running the example you can use either of the following two commands:
1) python average_rating_example.py (if the mapping-yelp-data folder has been placed just under the root
   'mapping-yelp' directory).
2) python average_rating_example.py -data_folder path
   In the above command path, is the path to 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/' folder.
"""
import os
import argparse
import logging
import pandas as pd
from matplotlib import pyplot as plt
from pylab import rcParams
import sys
sys.path.append('../src')
import yelp_data
from average_rating import AverageRating


def arguments_parser():
    parser = argparse.ArgumentParser()
    # Note that the unzipped data should be present at the location specified below.
    parser.add_argument('-data_folder', default='../mapping-yelp-data/yelp_dataset_challenge_academic_dataset/',
                        type=str)
    parser.add_argument('-sample_reviews', default=0, type=int)
    args = parser.parse_args()
    return args


def filter_reviews_by_date(reviews_df):
    start_date = pd.tslib.Timestamp(2007, 1, 1)
    mask = reviews_df['date'] >= start_date
    filtered_reviews_df = pd.DataFrame(reviews_df[mask])
    return filtered_reviews_df


def display_program_info(candidate_cities):
    print("Enter cities and window_days_size to look at the pattern of corresponding average ratings.")
    print("The ratings data is split into buckets according to window_days_size.")
    print("The value of window_days_size should be in days.")
    print("You can enter any of the following cities:\n" + str(candidate_cities))
    print("Entered cities should be comma separated. eg: \'Phoenix, Urbana-Champaign, Las Vegas\'")
    print("Once the plot is displayed close it for continuing the program.")
    print("Enter \'quit\' to exit the visualization.")


def get_period(period_message):
    while True:
        period = input(period_message)
        if not AverageRating.check_valid_period(period):
            print("ValueError, please enter a positive integer as period.")
        else:
            period = int(period)
            return period


def plot_graphs_cities(cities, candidate_cities, reviews_business_df, period):
    count_plotted = 0
    for city in cities:
        try:
            city = city.strip().title()
            if city not in candidate_cities:
                raise ValueError('Entered city %s not present in the dataset.' % city)
            city_mask = reviews_business_df['city'] == city
            city_reviews_df = reviews_business_df[city_mask]
            dates_average_rating_df = AverageRating.calculate_average_ratings(city_reviews_df,
                                                                              window_days_size=period)
            plt.plot(dates_average_rating_df.index,
                     dates_average_rating_df['average_rating'].values, label=city)
            plt.xlabel('Date')
            plt.ylabel('Average Rating')
            plt.ylim(-0.5, 5.5)
            plt.title('Rating Time Series')
            count_plotted += 1
        except ValueError as e:
            print(e)
            continue
    if count_plotted > 0:
        plt.legend(loc=4)
        print('Graph plotted')
        plt.show()
    plt.clf()


def analyze_ratings(reviews_business_df):
    candidate_cities = ['Edinburgh', 'Karlsruhe', 'Montreal', 'Waterloo', 'Pittsburgh',
                        'Urbana-Champaign', 'Phoenix', 'Las Vegas', 'Madison']
    period_message = "Enter period/window_days_size in days, (suggested value= 30): "
    quit_string = 'quit'
    period_string = 'change period'
    display_program_info(candidate_cities)
    period = get_period(period_message)
    while True:
        cities = input('Enter comma separated cities: ')
        if cities.lower() == period_string:
            period = get_period(period_message)
        elif cities.lower() == quit_string:
            print('Exiting')
            break
        cities = cities.split(',')
        print('Computing...')
        plot_graphs_cities(cities, candidate_cities, reviews_business_df, period)


def main():
    try:
        args = arguments_parser()
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        data = yelp_data.YelpData(args.data_folder)
        if args.sample_reviews == 1:
            logging.info('Loading sample review data.')
            reviews_df = data.get_review_sample_dataframe()
        else:
            logging.info('Loading review data, this might take some time. The review data can take up upto 5GB RAM.')
            reviews_df = data.get_review_dataframe()
        reviews_df = filter_reviews_by_date(reviews_df)
        logging.info('Loading business data.')
        business_df = data.get_business_dataframe()
        logging.info('Merging reviews_df and business_df.')
        reviews_business_df = pd.merge(reviews_df, business_df[['business_id', 'city']], on='business_id', how='inner')
        # Resizing the plot
        rcParams['figure.figsize'] = 10, 10
        analyze_ratings(reviews_business_df)
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    main()
