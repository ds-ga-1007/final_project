import sys
from Explorer.Explorer import *
from Explorer.InteractionError import *
from Explorer.ExplorerError import *


def main():

    # (a) Load non-trivial data into pandas.
    data = load_reddit_data()

    # (b) Perform meaningful analysis on data.
    # (c) Present results to user by saving plot as PNG in results directory.
    # Note: (b) and (c) are in my Jupyter notebook under 'Explore.ipynb'

    # (d) Hand user control of analysis and display of data.
    interactive_analysis(data)


def load_reddit_data() -> pd.DataFrame:
    """Subroutine encapsulating the loading of clean Reddit data set.

    :return data: pandas Dataframe containing Reddit comments.
    """

    # Attempt to read and properly headers list.
    headers = obtain_clean_header()

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


def interactive_analysis(data: pd.DataFrame):
    """Allow the user to interactively control the analysis and display of the data.

    :param data: original DataFrame containing Reddit comment data
    :return outputs information pertaining to user's requested data analysis
    """

    # Welcome to the interactive prompt...
    initial_prompt()

    # Here's how you can start...
    help_prompt()

    # Assume we want to continue.
    keep_going = True

    while keep_going:

        try:
            # Build our subset from data set
            columns_of_interest = build_subset(data)

            # Extract columns from data
            subset_data = data[columns_of_interest]

            # Perform iterative loop on what transformations,
            # summarizations, and aggregations to execute.
            transform_and_visualize(subset_data)

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
          'a dataset containing Reddit comments!'
          '\n\nThis shell allows you to:'
          '\n\t- begin with a complete dataset'
          '\n\t- isolate what variables you would like to explore'
          '\n\t- define what transformations to perform, and'
          '\n\t- visualize your results.', sep="")


def help_prompt():
    """Print information header to help user with interface.

    :return: prints information to console, the main interface for Commentary.
    """

    print("\nHelp menu:",
          "\n",
          "-" * 12,
          "\nHere are some keywords to get you started:",
          "\n\t:help  -- access this help page!",
          "\n\t:start -- begin the task of identifying what features you'd like to use",
          "\n\t:abort -- abort your current plot/visualization and start over",
          "\n\t:exit  -- exit the interactive portion of this program", sep=""
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

    # Keep going until user passes termination signal `:done`.
    while True:

        # Receive input and perform conditional checks.
        response = input("\nName the feature you would like to use (enter :done to finish):\n"
                         ">>> ").lower()

        # Remind user of available features if requested.
        if response == ':columns':
            list_all_columns(data)

        # Remind user of main
        elif response == ':help':
            help_prompt()

        # Exit from entire program if requested.
        elif response == ':exit':
            raise UserExitError()

        # Break from loop if termination signal is sent.
        elif response == ':done':
            break

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

    # If our feature is in our data set, return safely.
    if response in data.columns.values:
        return

    # Otherwise, raise an error.
    else:
        raise InvalidFeatureRequest(response)


def validate_not_repeat(response, already_requested):
    """Ensure feature has not already been requested.

    :param response: user-requested feature to be validated
    :param already_requested: list of features already requested
    :return: raises a RedundantFeatureRequest if feature has already been requested.
    """

    # If our feature has not been requested before, return safely.
    if response not in already_requested:
        return

    # Otherwise, raise an error.
    else:
        raise RedundantFeatureRequest(response)


def transform_and_visualize(subset_data: pd.DataFrame):
    """Wrapper for data aggregation/transformation and visualization/output.

    :param subset_data: data taken from our
    :return:
    """

    # Inform user of how the interactivity will work and
    # list all available actions.
    build_transformations_prompt()
    actions = list_all_actions()

    # Initialize our Explorer instance that'll help with
    # interactive data analysis.
    explorer = Explorer(subset_data)

    while True:

        # Receive input and perform conditional checks.
        response = input("\nName a command (or :help for options, :done to finish, :exit to exit):\n"
                         ">>> ").lower().split()

        # Isolate action from our provided input.
        action = response[0]

        # Provide help instructions if requested.
        if action == ':help':
            list_all_actions()

        elif action == ':exit':
            raise UserExitError()

        # Reset state to initial configurations by
        # re-printing the prompt/actions, and re-creating
        # the Explorer object.
        elif action == ':abort':
            build_transformations_prompt()
            list_all_actions()
            explorer = Explorer(subset_data)

        elif action == ':done':
            break

        # If our user's action is in the list of valid actions:
        else:

            # Validate all aspects of our response are applicable,
            # including the action and (potentially) on what feature.
            try:

                # GroupBy functions need a bit more validation.
                if action == ':groupby':
                    validate_groupby(response, actions, explorer)

                # Validate action and feature validity for other actions.
                else:
                    validate_action_and_feature(response, actions, explorer)

                # Execute data analysis/aggregation.
                explorer.data = explorer.dispatch(response)

                # Handle plotting task elsewhere to preserve modularity.
                plotting_subroutine(explorer)

            # If the action is not supported, print the error.
            except InvalidActionError as iae:
                print(iae, file=sys.stderr)

            # If the feature is not in our data set, print the error.
            except InvalidFeatureError as ife:
                print(ife, file=sys.stderr)

            # If our GroupBy feature is invalid, print the error.
            except InvalidGroupbyFeature as igf:
                print(igf, file=sys.stderr)

            # If our GroupBy combinator is invalid, print the error.
            except InvalidGroupbyCombinator as igc:
                print(igc, file=sys.stderr)

            # Handle termination errors and interrupts.
            except (EOFError, KeyboardInterrupt, SystemExit):
                print("")
                sys.exit(1)


def build_transformations_prompt():
    """Print information header to help user with analysis interface.

    :return prints information to console.
    """

    print("-" * 30)
    print("\nGreat! Now we can actually do some exploring on the data.")
    print("\nAt each prompt you'll be able to define an aggregation, summarization,\n"
          "or visualization/output command to save the results of your analysis thus far.\n")
    print("Each aggregation will modify a copy of the data set you're using,\n"
          "but you can always start from your original data set. Aggregate away!")


def list_all_actions():
    """Inform user of all potential data analysis 'verbs' our shell supports.

    :return list of valid verbs supported by interactive analysis shell.
    """

    # Define all supported actions.
    action_instruction = [':help -- access this help page!',
                          ':summarize -- Provide summary statistics for each feature in data set',
                          ':groupby -- Aggregate data set on similar values. Note: feature and combinator arguments required',
                          ':count -- Provide number of non-NaN values in the group',
                          ':sum -- Provide sum of values',
                          ':mean -- Provide arithmetic mean of values',
                          ':median -- Provide arithmetic median of values',
                          ':min -- Provide minimum of values',
                          ':max -- Provide maximum of values',
                          ':sort -- Sort values in data set. Note: feature argument required'
                          ]

    # Some whitespace.
    print('\n')

    # Print each action and its instructions.
    for line in action_instruction:
        print("\t{}".format(line))
        time.sleep(0.20)

    # Print some more information regarding optional features.
    print("\nNote: for all keywords except :help and :groupby, a feature is optional:\n",
          "if none is provided, we evaluate the action over the entire data set.\n",
          "Hence, `:min date` will give us the minimum value from the date field *only*.",
          sep=""
          )

    # Split our original :action_instruction list to isolate just the
    # verbs -- this will be used for input validation.
    actions = [line.split('--')[0].strip() for line in action_instruction]

    # Return our list of verbs.
    return actions


def validate_groupby(response: List[str], actions: List[str], explorer: Explorer):
    """GroupBy requires that both feature and combinator is valid, so we test separately.

    :param response: user-provided input denoting what action to take on data set
    :param actions: list of valid actions supported by our shell
    :param explorer: validator that, if provided, the feature is in our data set
    :return raises an exception if the feature or combinator is invalid.
    """

    # Establish conditionals that will tell us if both required
    # components are valid.
    feature_is_valid = response[1] in explorer.data.columns.values
    combinator_is_valid = response[2] in actions and response[2] != ':groupby'

    # If our feature is not valid, raise an error.
    if not feature_is_valid:
        raise InvalidGroupbyFeature(response[1])

    # If our combinator is not valid, raise an error.
    elif not combinator_is_valid:
        raise InvalidGroupbyCombinator(response[2])

    # Otherwise, return safely.
    else:
        return


def validate_action_and_feature(response: List[str], actions: List[str], explorer: Explorer):
    """Two-layer validation on a user action request.

    :param response: user-provided input denoting what action to take on data set
    :param actions: list of valid actions supported by our shell
    :param explorer: validator that, if provided, the feature is in our data set
    :return raises an exception if the action or feature is invalid, otherwise continues program
    """

    # Ensure our user's action is a valid one to apply.
    validate_action(response, actions)

    # Ensure our user's feature (if provided) is in our data set.
    validate_feature(response, explorer)


def validate_action(response: List[str], potential_actions: List[str]):
    """Ensure our user's action is a valid one to apply.

    :param response: user-provided input denoting what action to take on data set
    :param potential_actions: list of valid actions supported by our shell
    :return returns if response is valid, otherwise raises an InvalidActionError
    """

    # If our action is in our list of potential actions, return safely.
    if response[0] in potential_actions:
        return

    # Otherwise, raise an error since our action is not supported.
    else:
        raise InvalidActionError(response[0])


def validate_feature(response: List[str], explorer: Explorer):
    """Ensure our user's feature (if provided) is a valid one to operate on.

    :param response: user-provided input denoting what to do on a data set
    :param explorer: validator that, if provided, the feature is in our data set
    :return:
    """

    # We note that if the length of response is just 1,
    # then the user wants this action over the entire dataset.
    on_all_features = len(response) == 1

    # If our action is valid and applied on all features or
    # just applied on a single feature, return safely.
    if on_all_features or response[-1] in explorer.data.columns.values:
        return

    # Otherwise, raise an error since the feature is not in the data set.
    elif response[-1] not in explorer.data.columns.values:
        raise InvalidFeatureError(response[-1])


def plotting_subroutine(explorer: Explorer):

    # Offer to plot/output these results
    want_to_plot = input("Would you like to output your intermediate analysis?").lower()

    if want_to_plot in ['y', 'yes']:

        filename = input("Please enter a filename (no extension -- .png, .pdf, etc. -- required): ").lower()

        explorer.output_results(filename)


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
