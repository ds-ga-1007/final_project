import sys
from typing import List
from Plotter.Plotter import *
from Plotter.InteractionError import *

VERBOSE = ('-v' in sys.argv) or ('--verbose' in sys.argv)


def main():

    # (a) Load non-trivial data into pandas.
    data = load_reddit_data()

    # (b) Perform meaningful analysis on data.
    # (c) Present results to user by saving plot as PNG in results directory.
    meaningful_analysis(data)

    # (d) Hand user control of analysis and display of data.
    interactive_analysis(data)

    # TODO:
    #   Documentation
    #   Tests
    #   Lazy evaluation?
    #


def load_reddit_data() -> pd.DataFrame:
    """Subroutine encapsulating the loading of clean Reddit data set.

    :return data: pandas Dataframe containing Reddit comments.
    """

    if VERBOSE:
        print("Attempting to read headers file...")

    # Attempt to read and properly headers list.
    headers = obtain_clean_header()

    if VERBOSE:
        print("Just a second, reading in the Reddit comments data set...")

    # Attempt to read Reddit comments data.
    data = obtain_clean_reddit_data(headers)

    # Return Reddit DataFrame if we successfully read it in
    # and did some basic datetime cleaning.
    return data


def obtain_clean_header() -> List[str]:
    """Modular routine used to load headers from `data/headers.txt`.

    :return headers: list of column labels for comments data set.
    """

    # (Try to) Read contents of file containing header labels.
    try:
        with open('data/headers.txt', 'r') as f:
            headers = f.readlines()

        # If successful, split our only line on commas to get right format.
        headers = headers[0].strip().split(',')

        # Return our headers if we were successful
        return headers

    # If we can't find the headers file, we should NOT continue.
    except FileNotFoundError:
        raise MissingHeadersError()

    # Handle termination errors and interrupts.
    except (EOFError, KeyboardInterrupt, SystemExit):
        print("")
        sys.exit(1)


def obtain_clean_reddit_data(headers: List[str]) -> pd.DataFrame:
    """Modular routine to read core Reddit comments data set.

    :param headers: list of strings representing dataset's column names.
    :return data: lightly cleaned DataFrame of Reddit comments.
    """

    # (Try to) Read Reddit comments dataset.
    try:
        data = pd.read_csv('data/comments.csv', header=None,
                           index_col=None, names=headers)

        # Convert date column with seconds since UNIX epoch to datetime.
        data['date'] = pd.to_datetime(data['time'], unit='s')

        # Drop old time column, it's not welcome here.
        data = data.drop('time', axis=1)

        # If we've made it this far, return our clean data set.
        return data

    # If we can't find the core data file, we should NOT continue.
    except FileNotFoundError:
        raise MissingDatasetError('data/comments.csv')

    # Handle termination errors and interrupts.
    except (EOFError, KeyboardInterrupt, SystemExit):
        print("")
        sys.exit(1)


def meaningful_analysis(data: pd.DataFrame):
    """Perform meaningful analysis of our dataset using Plotters!

    :param data:
    :return:
    """

    # TODO
    pass


def interactive_analysis(data: pd.DataFrame):
    """Allow the user to interactively control the analysis and display of the data.


    :param data: original DataFrame containing Reddit comment data
    :return outputs information pertaining to user's requested data analysis
    """

    # Welcome to the interactive prompt...
    initial_prompt()

    # Here's how you can start...
    help_prompt()

    keep_going = True

    while keep_going:

        try:
            # Build our subset from data set
            columns_of_interest = build_subset(data)

            # Extract columns from data
            subset_data = data[columns_of_interest]

            # Perform iterative loop on what transformations,
            # summarizations, and aggregations to execute.
            # transform_and_visualize(subset_data)

            # Ask if user would like to restart the analysis.
            keep_going = continue_prompt()

        # Handle termination errors and interrupts.
        except (EOFError, KeyboardInterrupt, SystemExit):
            print("")
            sys.exit(1)

        except UserExitError:
            print("Exiting...", file=sys.stderr)
            sys.exit(1)


def initial_prompt():
    """Print informative header on how we'll be performing interactive analysis.

    :return: prints information to console, the main interface for Commentary.
    """

    print("")
    print("=" * 30)
    print('Welcome! Commentary allows you to interactively explore '
          'a dataset containing Reddit comments!\n'
          'This shell allows you to:\n'
          '\t- begin with a complete dataset\n'
          '\t- isolate what variables you would like to explore\n'
          '\t- define what transformations to perform, and\n'
          '\t- visualize your results.\n')


def help_prompt():
    """Print information header to help user with interface.

    :return: prints information to console, the main interface for Commentary.
    """

    print("Help menu:",
          "\n-------------",
          "\nHere are some keywords to get you started:",
          "\n\t:help -- access this help page!",
          "\n\t:start -- begin the task of identifying what features you'd like to use",
          "\n\t:abort -- abort your current plot/visualization and start over",
          "\n\t:exit -- exit the interactive portion of this program"
          )


def build_subset(data: pd.DataFrame) -> List[str]:
    """Part 1 of our Analysis: isolate the user's required features for analysis.

    :param data: entire DataFrame -- in this case, the Reddit comment dataset.
    :return valid_features: list of valid features requested from :data.
    """

    # Let's start by choosing what features...
    build_dataset_prompt()

    # Here are the features you can choose from.
    list_all_columns(data)

    # Start by assuming no requested features.
    valid_features = []

    response = ""

    # Keep going until user passes termination signal `:done`.
    while True:

        # Receive input and perform conditional checks.
        response = input("\nName the feature you would like to use (enter :done to finish):\n"
                         ">>> ").lower()

        # Remind user of available features if requested.
        if response == ':columns':
            list_all_columns(data)

        # Exit from entire program if requested.
        elif response == ':exit':
            raise UserExitError()

        # Break from loop if termination signal is sent.
        elif response == ':done':
            break

        # TODO?
        # elif response == ':new':
        #     new_col = create_calculated_column(data)

        # Otherwise, if we have reason to believe the user
        # has passed a feature, try adding it.
        else:
            try:
                # First, validate that feature to make sure it's in
                # our feature list AND it hasn't been added already.
                validate_feature_request(response, valid_features, data)

                # If the feature makes it through validation, we can safely
                # add it to our feature container and inform the user.
                valid_features.append(response)
                print("...Success! Added {} to your feature list.".format(response))

            # If the feature is not in our source data set, print the error.
            except InvalidFeatureRequest as ifr:
                print(ifr, file=sys.stderr)

            # If the feature has already been requested, print the error.
            except RedundantFeatureRequest as rfr:
                print(rfr, file=sys.stderr)

            # Handle termination errors and interrupts.
            except (EOFError, KeyboardInterrupt, SystemExit):
                print("")
                sys.exit(1)

    # If the user signals `:done`, return the
    # list of valid features.
    return valid_features


def validate_feature_request(response, already_requested, data):
    """Two-layer validation on a user feature request.

    :param response: user-requested feature
    :param already_requested: list of features already requested
    :param data: entire DataFrame -- in this case, the Reddit comment dataset
    :return: raises an exception if the feature is invalid, otherwise continues program
    """

    # Ensure feature is in our data set.
    validate_valid_feature(response, data)

    # Ensure feature has not already been requested and added.
    validate_not_repeat(response, already_requested)


def validate_valid_feature(response, data):
    """Ensure feature is in our data set.

    :param response: user-requested feature to be validated
    :param data: entire DataFrame -- in this case, the Reddit comment dataset
    :return: raises an InvalidFeatureRequest if feature not a column in :data's.
    """

    if response in data.columns.values:
        return
    else:
        raise InvalidFeatureRequest(response)


def validate_not_repeat(response, already_requested):
    """Ensure feature has not already been requested.

    :param response: user-requested feature to be validated
    :param already_requested: list of features already requested
    :return: raises a RedundantFeatureRequest if feature has already been requested.
    """

    if response not in already_requested:
        return
    else:
        raise RedundantFeatureRequest(response)

    # keywords = {':columns': 'Print list of columns.',
    #             ':help': 'Display initial prompt message.',
    #             ':pivot': 'Perform pivot on data set. Must provide values for index and columns. Optional: values.',
    #             ':groupby', ':explain',
    #             ':summarize', ':export', ':exit'
    #             }


def continue_prompt():
    """Prompt user on whether they would like to continue interactive analysis.

    :return keep_going: boolean denoting whether to continue (True) or not (False).
    """

    # Initialize soon-to-be-updated values
    response, keep_going = "", None

    # While our user's response to continuing is
    # not a variation of 'yes/no', keep asking.
    while keep_going not in [True, False]:

        # Receive user input on whether they'd like to continue or quit.
        response = input("\nWould you want to continue with another feature list?\n"
                         ">>> ").lower()

        # Exit from entire program if requested.
        if response == ':exit':
            raise UserExitError()

        # If continue, set :keep_going to True and effectively break loop.
        if response in ['yes', 'y']:
            keep_going = True

        # Likewise, if not set :keep_going to False and break loop.
        elif response in ['no', 'n']:
            keep_going = False

        # If invalid response, inform user of their mistake and try again.
        else:
            print(InvalidContinuityResponse(), file=sys.stderr)

    # Return our user's specified value.
    return keep_going


if __name__ == '__main__':
    main()
