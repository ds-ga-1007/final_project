"""
Example for using the Data pipeline.
For running the example you can use either of the following two commands:
1) python data_pipeline_example.py
2) python data_pipeline_example.py -data_folder path (if the mapping-yelp-data folder has been placed just under the
   root 'mapping-yelp' directory).
   In the above command, path is the path to 'mapping-yelp-data/yelp_dataset_challenge_academic_dataset/' folder.
"""
import os
import sys
import argparse
import logging
sys.path.append('../src')
import yelp_data


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
        data = yelp_data.YelpData(args.data_folder)
        logging.info('Loading checkin data.')
        checkin_df = data.get_checkin_dataframe()
        print('Checkin dataframe first 2 rows')
        print('-' * 40)
        print(checkin_df.head(n=2))
        print('-' * 40)
        logging.info('Loading business data.')
        business_df = data.get_business_dataframe()
        print('Business dataframe first 2 rows')
        print('-' * 40)
        print(business_df.head(n=2))
        print('-' * 40)
        logging.info('Loading review data, this might take some time. The review data can take up upto 5GB RAM.')
        review_df = data.get_review_dataframe()
        print('Review dataframe first 2 rows')
        print('-' * 40)
        print(review_df.head(n=2))
        print('-' * 40)
        logging.info('Loading user data.')
        user_df = data.get_user_dataframe()
        print('User dataframe first 2 rows')
        print('-' * 40)
        print(user_df.head(n=2))
        print('-' * 40)
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting.")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    main()
