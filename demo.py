
from dataprep import *
import sys
import tabview.tabview as TV
import tempfile

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
    print('If there is no target variable, enter "N" and enter a blank line in the next step.')
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
        while True:
            print('Please specify the indices for target column separated by comma.')
            print('Negative indices indicate columns starting from the right.')
            print('[Default: -1]')
            s = input()
            if len(s) == 0:
                target_list = [-1]
            else:
                try:
                    target_list = [int(x) for x in s.split(',')]
                except ValueError as e:
                    print('Invalid input: %s' % str(e))
                    continue
            break

    if len(target_list) == 0:
        print('No target column specified.')
        target_list = None

    print('Is there a header in the first line? [Y/N]')
    s = input_expect(['y', 'Y', 'n', 'N'])
    if s in ['y', 'Y']:
        header = 0
    else:
        header = None

    # Loads the file or throws error if it fails.
    loader = CSVLoader(target=target_list, delim=sep, header=header)
    try:
        dfs = loader.load_from_path(dataset_filename)
    except FileNotFoundError:
        print('ERROR: File %s not found' % dataset_filename)
        sys.exit(4)
    except IOError as e:
        print('ERROR: Unable to load %s: %s' % (dataset_filename, str(e)))
        sys.exit(4)

    if header is None:
        # assign default column names
        for df in dfs:
            df.rename(columns=lambda x: 'col'+str(x), inplace=True)

    return dfs


def menu(menu_items, title=None):
    if title is not None:
        print(title)

    for k in menu_items:
        print('%s - %s' % (k, menu_items[k]))

    return input_expect(menu_items.keys())

######################
# General Operations #
######################

def preview(df, pipeline, pipeline_names):
    # Tries to apply the transformations into a new DataFrame
    for tr, name in zip(pipeline, pipeline_names):
        print('Applying %s...' % name)
        try:
            df = tr.transform(df, to_dataframe=True)
        except (TypeError, ValueError, KeyError, IndexError):
            print('An error has occurred during the transformation in', name)
            print('Error type:', sys.exc_info()[0].__name__)
            print('Error message:', sys.exc_info()[1])
            return

    fp = tempfile.NamedTemporaryFile(mode='w+')
    df.to_csv(fp)

    TV.view(fp.name)

    fp.close()


def view_pipeline(df, pipeline, pipeline_names):
    print('Current pipeline:')
    for name in pipeline_names:
        print(name)


def undo_last(df, pipeline, pipeline_names):
    if len(pipeline) == 0:
        print('Nothing to undo')
        return

    print('The last step of transformation is', pipeline_names[-1])
    pipeline.pop()
    pipeline_names.pop()


##################
# Schema Editing #
##################

def rename_columns(df, pipeline, pipeline_names):
    menu_items = {
            'o': 'rename columns one-by-one',
            'n': 'rename columns by specifying old name and new name',
            }
    option = menu(menu_items)

    if option == 'o':
        print('Enter new column names line by line.')
        print('Enter a blank line to finish.')
        namelist = []
        while True:
            s = input()
            if len(s) == 0:
                break
            namelist.append(s)
        pipeline.append(ColumnRenamer(namelist))
        pipeline_names.append('Rename columns to %s' % repr(namelist))
    else:
        namedict = {}
        while True:
            print('Enter old column name to rename (blank to finish):')
            s = input()
            if len(s) == 0:
                break
            print('Enter the name you want to rename %s (blank to leave it as-is):' % s)
            n = input()
            if len(n) == 0:
                continue
            namedict[s] = n
        pipeline.append(ColumnRenamer(namedict))
        namelist = [repr(old) + ' -> ' + repr(new)
                    for old, new in namedict.items()]
        pipeline_names.append('Rename columns: %s' % '[' + ', '.join(namelist) + ']')


def edit_schema(df, pipeline, pipeline_names):
    menu_items = {
            'c': 'rename columns',
            'q': 'do nothing',
            }
    actions = {
            'c': rename_columns,
            }

    option = menu(menu_items)
    if option == 'q':
        return
    else:
        actions[option](df, pipeline, pipeline_names)


#########################
# Putting them together #
#########################

def preprocess_dataset(df):
    menu_items = {
            'p': 'preview result',
            'v': 'view pipeline',
            'u': 'undo last transformation',
            's': 'view/edit schema',
            'q': 'quit and proceed to next step',
            }
    pipeline = []
    # After some consideration I decided that it's not the responsibility of
    # the library to maintain the names for each transformer.  Doing so is
    # usually a headache, will unnecessarily create other problems (e.g.
    # the library has to decide how to represent a NullValueTransformer with
    # a heavily customized criteria), increases the chance of introducing
    # bugs, is often inextensible, and is not directly related to the job
    # of the library itself.
    # Which is why I'm maintaining a separate list to keep track of the names
    # for each transformer.
    pipeline_names = []

    # The keys of actions dict corresponds to menu items, and values are
    # a function which takes the DataFrame, the pipeline list and the pipeline
    # name list as arguments.
    # Also, note that @pipeline and @pipeline_names are *mutable*.  @df is
    # also mutable but it is not supposed to be changed.
    # I know this is ugly, but somehow I feel that writing a lot of if-elses
    # is even uglier.
    actions = {
            'p': preview,
            'v': view_pipeline,
            'u': undo_last,
            's': edit_schema,
            }

    while True:
        option = menu(menu_items, 'Data preprocessing:')
        if option == 'q':
            # Perform the actual transformation and try to return the
            # resulting numpy.ndarray.
            try:
                ppl = PipelineTransformer(*pipeline)
                return ppl.transform(df)
            except (TypeError, ValueError, KeyError, IndexError):
                # That pretty much covers all the usual errors types pandas
                # throw around...
                print('An error of type %s has occurred: %s' %
                        (sys.exc_info()[0].__name__, sys.exc_info()[1]))
                print('Preview the result to see which transformer has gone wrong.')
        else:
            actions[option](df, pipeline, pipeline_names)


def main():
    # Normally we would want to let the user specify which kind of format
    # the dataset is, but since we only support CSVs for now we directly
    # jump to read in CSV-specific options.
    dflist = read_csv()
    if len(dflist) == 1:
        # one dataset
        preprocess_dataset(dflist[0])
    elif len(dflist) == 2:
        # a feature set and a label set
        print('Preprocessing feature set')
        preprocess_dataset(dflist[0])
        print('Preprocessing label set')
        preprocess_dataset(dflist[1])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(2)
    except EOFError:
        print('EOF encountered, exiting')
        sys.exit(1)
