
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
    s = input().lower()
    if default is not None:
        return s if s in expect else default
    else:
        while s not in expect:
            print('Expected %s' % ', '.join([repr(x) for x in expect]))
            s = input()
        return s


def input_until_blank():
    # Returns a list of user inputs and continue accepting input until
    # the user enters a blank line.
    print('Enter a blank line to finish.')
    l = []
    while True:
        s = input()
        if len(s) == 0:
            break
        l.append(s)
    return l


def read_csv():
    # Reads a CSV file.
    print('Enter the filename you want to load the dataset from:')
    dataset_filename = input()
    if len(dataset_filename) == 0:
        print('None specified.  Exiting.')
        sys.exit(1)

    print('Enter the separator for the CSV file [default ","]:')
    sep = input_with_default(',')

    print('Is there a header in the first line? [Y/N]')
    s = input_expect(['y', 'n'])
    if s == 'y':
        header = 0
    else:
        header = None

    if header is not None:
        print('Would you like to specify target variables in terms of [N]ames or [I]ndices?')
        s = input_expect(['n', 'i'])
    else:
        print('Column names not available in header.')
        s = 'i'

    if s == 'n':
        print('Please specify the names for target column in one line at a time.')
        target_list = input_until_blank()
    else:
        while True:
            print('Please specify the indices for target column separated by comma.')
            print('Negative indices indicate columns starting from the right.')
            print('Enter a blank line to indicate that there is no target variable.')
            s = input()
            if len(s) == 0:
                target_list = []
                break       # no target variable
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


def preview_dataframe(df):
    fp = tempfile.NamedTemporaryFile(mode='w+')
    df.to_csv(fp)
    TV.view(fp.name)
    fp.close()


def preview(df, pipeline, pipeline_names, show=True):
    # Tries to apply the transformations into a new DataFrame
    try:
        ppl = PipelineTransformer(*pipeline)
        df = ppl.transform(df, to_dataframe=True)
    except (TypeError, ValueError, KeyError, IndexError) as e:
        print(e.args[0])
        print('Transformer: %s' % pipeline_names[e.args[1]])
        return None

    if show:
        preview_dataframe(df)

    return df


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


def display_schema(df):
    print('Displaying schema:')
    for c in df.columns:
        print('%s: %s' % (c, 'categorical' if df[c].dtype == NP.object else 'numeric'))


def rename_columns(df, pipeline, pipeline_names):
    menu_items = {
            'o': 'rename columns one-by-one',
            'n': 'rename columns by specifying old name and new name',
            }
    option = menu(menu_items)

    if option == 'o':
        print('Enter new column names line by line.')
        namelist = input_until_blank()
        pipeline.append(ColumnRenamer(namelist))
        pipeline_names.append('Rename columns to %r' % namelist)
    else:
        namedict = {}
        while True:
            # Actually different from the mechanism of input_until_blank() and
            # I'm not sure how to reuse that code.
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


def preview_schema(df, pipeline, pipeline_names):
    newdf = preview(df, pipeline, pipeline_names, show=False)
    display_schema(newdf)


def edit_schema(df, pipeline, pipeline_names):
    menu_items = {
            'c': 'rename columns',
            'g': 'guess schema',
            's': 'display schema',
            'd': 'drop columns',
            'm': 'change column type',
            'q': 'do nothing',
            }
    actions = {
            'c': rename_columns,
            'g': guess_schema,
            's': preview_schema,
            'd': drop_columns,
            'm': change_column_type,
            }

    option = menu(menu_items)
    if option == 'q':
        return
    else:
        actions[option](df, pipeline, pipeline_names)


def guess_schema(df, pipeline, pipeline_names):
    # Preview it first
    df = preview(df, pipeline, pipeline_names, show=False)

    guesser = TabularSchemaGuesser()
    newdf = guesser.transform(df, to_dataframe=True)
    display_schema(newdf)

    menu_items = {
            'y': 'proceed with this schema',
            'p': 'preview the result',
            'n': 'reject this schema and do nothing',
            }

    while True:
        option = menu(menu_items)
        if option == 'y':
            pipeline.append(guesser)
            pipeline_names.append('Automatic schema inference')
            return
        elif option == 'n':
            return
        elif option == 'p':
            preview_dataframe(newdf)


def drop_columns(df, pipeline, pipeline_names):
    print('Do you wish to specify the columns to drop in [I]ndices or [N]ames?')
    option = input_expect(['i', 'n'])
    if option == 'n':
        print('Enter the name of column you wish to drop line by line.')
        columns = input_until_blank()
    else:
        print('Enter the indices of columns you wish to drop, separated by comma.')
        while True:
            try:
                s = input()
                columns = [int(x) for x in s.split(',')]
                break
            except ValueError as e:
                print('Invalid input: %s' % str(e))

    pipeline.append(DropColumnTransformer(columns))
    pipeline_names.append('Drop columns: %r' % columns)


def change_column_type(df, pipeline, pipeline_names):
    cols = {}
    while True:
        # Actually different from the mechanism of input_until_blank() and I'm
        # not sure how to reuse that code (same as before).
        print('Enter the name of the column you wish to change type.')
        print('Enter a blank line to finish.')
        s = input()
        if len(s) == 0:
            break
        print('Do you wish to make this column [C]ategorical or [N]umeric?')
        t = input_expect(['c', 'n'])
        cols[s] = 'numeric' if t == 'n' else 'categorical'

    pipeline.append(TabularSchemaTransformer(cols))
    pipeline_names.append('Change column type: %r' % cols)


###############
# Null values #
###############


def delete_values(df, pipeline, pipeline_names):
    menu_items = {
            'a': 'delete certain values in all columns',
            's': 'select a columnto delete values in',
            }
    option = menu(menu_items)
    if option == 'a':
        column = None
    else:
        print('Enter the name of column you wish to delete values in.')
        column = input()

    menu_items = {
            'n': 'delete all negative values in numeric columns',
            '0': 'delete all zeroes in numeric columns',
            'x': 'delete all values equal to some value',
            '?': 'delete all "?"s, "-"s, whitespaces, and "N/A" or "NA" in any case in categorical columns',
            'q': 'do nothing',
            }
    print('Please select the values you want to delete.')
    print('NOTE: for deleting non-numeric values in a numeric column identified as categorical, you can simply change the type there to numeric.')
    option = menu(menu_items)
    if option == 'q':
        return

    if option == 'n':
        criteria = lambda x: x < 0
        criteria_on = 'numeric'
        criteria_name = 'negative'
    elif option == '0':
        criteria = lambda x: x == 0
        criteria_on = 'numeric'
        criteria_name = 'zeroes'
    elif option == '?':
        criteria = lambda x: ((x.lower() in ['?', '-', 'n/a', 'na']) or x.isspace())
        criteria_on = 'categorical'
        criteria_name = 'default n/a values'
    elif option == 'x':
        print('Enter the value you wish to delete:')
        s = input()
        criteria = lambda x, s=s: x == s
        criteria_name = str(s)
        print('Is your value [N]umeric or [C]ategorical?')
        criteria_on = 'numeric' if input_expect(['c', 'n']) == 'n' else 'categorical'

    pipeline.append(
            NullValueTransformer(
                criteria if column is None else {column: criteria},
                only=criteria_on
                )
            )
    pipeline_names.append(
            'Delete %s for %s (%s)' %
            (criteria_name, 'all' if column is None else column, criteria_on)
            )


def add_null_indicator(df, pipeline, pipeline_names):
    print('Do you wish to add null indicator variables for')
    menu_items = {
            'a': 'all numeric columns',
            's': 'some of the columns (not necessarily numeric)',
            }
    option = menu(menu_items)

    if option == 'a':
        pipeline.append(NullIndicatorTransformer())
        pipeline_names.append('Add null indicator variable for all numeric columns')
    else:
        print('Enter the name of columns you wish to add such variables.')
        columns = input_until_blank()
        pipeline.append(NullIndicatorTransformer(columns, only_numeric=False))
        pipeline_names.append('Add null indicator for %r' % columns)


###############
# Normalizing #
###############


def normalize(df, pipeline, pipeline_names):
    print('Choose the normalization method:')
    norm_menu_items = {
            '0': 'subtracting the mean',
            'n': 'subtracting the mean and dividing by standard deviation',
            '1': 'linearly normalizing to 0..1',
            '-': 'linearly normalizing to -1..1',
            }
    normalize_method = {
            '0': 'zeromean',
            'n': 'normal',
            '1': 'zeropos',
            '-': 'negpos',
            }
    option = menu(norm_menu_items)
    method = normalize_method[option]
    method_name = norm_menu_items[option]

    col_menu_items = {
            'a': 'all numeric columns',
            's': 'only some of the columns',
            }
    option = menu(col_menu_items)
    if option == 'a':
        pipeline.append(ColumnNormalizer(method))
        pipeline_names.append('Normalize by %s for all columns' % method_name)
    else:
        print('Enter the name of the columns you wish to normalize.')
        cols = input_until_blank()
        pipeline.append(ColumnNormalizer({col: method for col in cols}))
        pipeline_names.append('Normalize by %s for %r' % (method, cols))


##############
# Imputation #
##############


def numeric_impute(df, pipeline, pipeline_names):
    print('Choose whether you want to impute the missing values with:')
    print('(categorical columns are untouched)')
    impute_menu_items = {
            '0': 'zero',
            'm': 'median',
            'a': 'mean',
            }
    # Yes, the menu item description and the parameter for
    # NumericImputationTransformer happens to be the same.
    method = impute_menu_items[menu(impute_menu_items)]

    col_menu_items = {
            'a': 'all numeric columns',
            's': 'only some of the columns',
            }
    option = menu(col_menu_items)
    if option == 'a':
        pipeline.append(NumericImputationTransformer(method))
        pipeline_names.append('Impute by %s for all columns' % method)
    else:
        print('Enter the name of the columns you wish to impute.')
        cols = input_until_blank()
        pipeline.append(NumericImputationTransformer({col: method for col in cols}))
        pipeline_names.append('Impute by %s for %r' % (method, cols))


###########################
# Dummy variable encoding #
###########################


def dummy(df, pipeline, pipeline_names):
    print('Dummying out every categorical variables (including null values there)')
    pipeline.append(DummyTransformer(dummy_unknown=True))
    pipeline_names.append('Dummy out categorical values')


#########################
# Putting them together #
#########################


def preprocess_dataset(df):
    menu_items = {
            'p': 'preview result',
            'v': 'view pipeline',
            'u': 'undo last transformation',
            's': 'view/edit schema',
            'd': 'delete values',
            'a': 'add null indicator variables',
            'n': 'normalize columns',
            '1': 'dummy out (one-hot encode) categorical variables',
            'i': 'impute missing values in numeric columns',
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
            'd': delete_values,
            'a': add_null_indicator,
            'n': normalize,
            'i': numeric_impute,
            '1': dummy,
            }

    while True:
        option = menu(menu_items, 'Data preprocessing:')
        if option == 'q':
            # Perform the actual transformation and try to return the
            # resulting numpy.ndarray.
            try:
                ppl = PipelineTransformer(*pipeline)
                result = ppl.transform(df)
                if result.dtype == NP.object:
                    print('It seems that some categorical values are still left.')
                    print('Please preview the result or view the schema, and dummy out these values.')
                elif NP.isnan(result).any():
                    print('It seems that null values still exist.')
                    print('Please preview the result and impute those values.')
                else:
                    return result
            except (TypeError, ValueError, KeyError, IndexError) as e:
                print('%s has occurred: %s' % (e.__class__.__name__, e.args[0]))
                print('Preview the result and see where it goes wrong.')
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
