"""
An example for predicting review ratings for unseen user-business pairs using linear regression.
This example is a prediction focused example. The user can split the data into training and test. Then
using the linear_regression_reviews module the user can add features to the data and use
a linear regression for predicting ratings in the test data.
For running the example you can use either of the following two commands:
1) python linear_regression_example.py (if the mapping-yelp-data folder has been placed just under the root
   'mapping-yelp' directory).
2) python linear_regression_example.py -data_folder path
   In the above command path, is the path to 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/' folder.
"""
import os
import sys
import argparse
import logging
import pandas as pd
sys.path.append('../src')
import yelp_data
import linear_regression_reviews


def arguments_parser():
    parser = argparse.ArgumentParser()
    # Note that the unzipped data should be present at the location specified below.
    parser.add_argument('-data_folder', default='../mapping-yelp-data/yelp_dataset_challenge_academic_dataset/',
                        type=str)
    parser.add_argument('-state', default='NV', type=str)
    parser.add_argument('-load_train_test', default=False, type=bool)
    parser.add_argument('-save_train_test', default=False, type=bool)
    parser.add_argument('-train_df_save_path', default='../mapping-yelp-data/nevada_train_df.pickle')
    parser.add_argument('-test_df_save_path', default='../mapping-yelp-data/nevada_test_df.pickle')
    parser.add_argument('-train_df_load_path', default='../mapping-yelp-data/nevada_train_df.pickle')
    parser.add_argument('-test_df_load_path', default='../mapping-yelp-data/nevada_test_df.pickle')
    args = parser.parse_args()
    return args


def get_training_test_data(args, training_size):
    data = yelp_data.YelpData(args.data_folder)
    logging.info('Loading reviews data.')
    reviews_df = data.get_review_dataframe()
    logging.info('Loading business data.')
    business_df = data.get_business_dataframe()
    logging.info('Filtering out reviews for state ' + args.state + '.')
    review_location_df = data.merge_reviews_business_df(reviews_df, business_df[['business_id', 'city', 'state']],
                                                        on='business_id')
    reviews_location_filtered_state = pd.DataFrame(review_location_df[review_location_df['state'] == args.state])
    reviews_location_filtered_state.sort_values('date', inplace=True)
    split_point = int(reviews_location_filtered_state.shape[0] * training_size)
    cols = ['business_id', 'date', 'review_id', 'stars', 'user_id']
    train_df = reviews_location_filtered_state[:split_point][cols]
    test_df = reviews_location_filtered_state[split_point:][cols]
    return train_df, test_df


def main():
    try:
        args = arguments_parser()
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        linear_regression = linear_regression_reviews.LinearRegressionReviews()
        if args.load_train_test:
            logging.info('Loading train and test dataframes from pickle files.')
            train_df = pd.read_pickle(args.train_df_load_path)
            test_df = pd.read_pickle(args.test_df_load_path)
        else:
            logging.info('Creating training and test splits.')
            train_df, test_df = get_training_test_data(args, 0.8)
            logging.info('Featurizing training and test data. This might take some time.')
            train_df, test_df = linear_regression.featurize_data(train_df, test_df)
            if args.save_train_test:
                logging.info('Saving training and test pickles.')
                train_df.to_pickle(args.train_df_save_path)
                test_df.to_pickle(args.test_df_save_path)
        logging.info('Training linear regression.')
        linear_regression.fit(train_df)
        logging.info('Predicting using linear regression.')
        predictions = linear_regression.predict(test_df)
        rmse = linear_regression.calculate_rmse(test_df['stars'], predictions)
        print('rmse for', args.state, 'reviews:', rmse)
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == '__main__':
    main()
