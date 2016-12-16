"""
This program allows users to analyze how the "ratings" of certain companies on Yelp have evolved over time.
When the user is done entering companies, the program will produce two subplots. The first subplot indicates how
the moving average of ratings for each of the selected companies has changed. The second subplot illustrates how
the 180-day "rolling average" for each company's rating has changed over time. We initially wanted to use 90 days
as the interval length (since companies typically issue quarterly reports), but we thought the data was too sparse,
so we went with 180. Importantly, the user must input only one company name at a time! For example, if a user wants
to compare McDonald's and Burger King, he should enter "McDonald's" first, then wait for a second prompt to
enter "Burger King." Each of the two subplots (moving average and 180-day) will include a trendline for each company
selected. The user must type "plot" to view the plots.

For running the example you can use either of the following two commands:
1) python company_rating_example.py (if the mapping-yelp-data folder has been placed just under the root
   'mapping-yelp' directory).
2) python company_rating_example.py -data_folder path
   In the above command path, is the path to 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/' folder.
"""
import os
import sys
from matplotlib import pyplot as plt
import argparse
import logging
sys.path.append('../src')
import yelp_data
import company_ratings


def arguments_parser():
    parser = argparse.ArgumentParser()
    # Note that the unzipped data should be present at the location specified below.
    parser.add_argument('-data_folder', default='../mapping-yelp-data/yelp_dataset_challenge_academic_dataset/',
                        type=str)
    args = parser.parse_args()
    return args


def main():
    try:
        args = arguments_parser()
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        # Load the data
        logging.info("Loading the data. This might take some time.")
        data = yelp_data.YelpData(args.data_folder)
        business_df = data.get_business_dataframe()
        review_df = data.get_review_dataframe()
        combined_df = data.merge_reviews_business_df(review_df, business_df)
        combined_df = combined_df.rename(columns={'stars_x': 'user_rating', 'stars_y': 'business_rating'})
        # Adjusting the size of plot.
        plt.figure(figsize=(20, 10))
        company_names = []
        ratings = company_ratings.CompanyRatings()
        while True:
            user_message = "Please enter the name of a Yelp-reviewed company." + \
                           "Enter the word \"plot\" to exit the program and view the plots: "
            response = input(user_message)
            if response == 'plot':
                # Display the plot.
                plt.show()
                break
            try:
                # Test whether the input is a valid business name.
                name = ratings.check_valid_business(response, combined_df)
            except company_ratings.InvalidBusinessName:
                print('Invalid input for business name. Please enter the full name of a Yelp-reviewed company.')
                continue
            # Take subset of data corresponding to that business name
            company_df = combined_df[combined_df['name'] == name]
            company_df = company_df.sort_values(by='date')
            company_df.index = range(len(company_df))
            company_df = ratings.calculate_moving_average(company_df, 'user_rating')
            print("\nTHERE are {0} individual {1} units in the database, with {2} total reviews".format(
                len(company_df['business_id'].unique()), name, len(company_df)))
            print('The current average rating of {0} is {1}.'.format(name, company_df['user_rating'].mean()))
            # Add company name to the list of establishments that will be plotted.
            company_names.append(name)
            ratings.plot_moving_average(company_df['date'], company_df['moving_average'], name, company_names)
            ratings.plot_rolling_average(company_df, 'business_rating', name, company_names)
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    main()
