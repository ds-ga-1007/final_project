
from dataprep import *
import sys

def input_with_default(default):
    # Accepts user input or returns default value if left blank.
    s = input()
    return s if len(s) > 0 else default


def input_expect(expect, default=None):
    # Returns user input if it falls in specified list of expected inputs,
    # or either returns default value if specified, or keep asking until
    # the user follows the rule or gives up.
    s = input()
    if default is not None:
        return s if s in expect else default
    else:
        while s not in expect:
            print('Expected %s' % ', '.join([repr(x) for x in expect]))
            s = input()
        return s


def read_csv():
    # Reads a CSV file.
    print('Enter the filename you want to load the dataset from:')
    dataset_filename = input()
    if len(dataset_filename) == 0:
        print('None specified.  Exiting.')
        sys.exit(1)

    print('Enter the separator for the CSV file [default ","]:')
    sep = input_with_default(',')

    print('Would you like to specify target variables in terms of [N]ames or [I]ndices?')
    s = input_expect(['n', 'N', 'i', 'I'])

    target_list = []

    if s in ['n', 'N']:
        print('Please specify the names for target column in one line at a time.')
        print('Enter a blank line to proceed to next step.')
        s = input()
        while len(s) > 0:
            target_list.append(s)
            s = input()
    else:
        print('Please specify the indices for target column separated by comma.')
        print('Negative indices indicate columns starting from the right.')
        s = input()
        target_list = [int(x) for x in s.split(',')]

    if len(target_list) == 0:
        print('No target column specified.')
        target_list = None

    print('Is there a header in the first line? [Y/N]')
    s = input_expect(['y', 'Y', 'n', 'N'])
    if s in ['y', 'Y']:
        header = 0
    else:
        header = None

    loader = CSVLoader(target=target_list, delim=sep, header=header)

    return loader.load_from_path(dataset_filename)


def main():
    # Normally we would want to let the user specify which kind of format
    # the dataset is, but since we only support CSVs for now we directly
    # jump to read in CSV-specific options.
    df = read_csv()
    print(df)

    # TODO


if __name__ == '__main__':
    main()
