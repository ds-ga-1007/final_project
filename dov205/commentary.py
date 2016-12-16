import sys
from Plotter.Plotter import *
from Plotter.InteractionError import *

VERBOSE = ('-v' in sys.argv) or ('--verbose' in sys.argv)


def main():

    # (a) Load non-trivial data into pandas.
    data = load_reddit_data()

    # (b) Perform meaningful analysis on data.
    # (c) Present results to user by saving plot as PNG in results directory.
    # TODO

    # (d) Hand user control of analysis and display of data.
    # TODO

    # TODO:
    #   Documentation
    #   Tests
    #   Lazy evaluation?
    #


def load_reddit_data():
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


def obtain_clean_header():
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


def obtain_clean_reddit_data(headers):
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


if __name__ == '__main__':
    main()
