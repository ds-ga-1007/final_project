import matplotlib.pyplot as plt
from typing import List
import pandas as pd
import time
from Explorer.ExplorerError import *


class Explorer:

    def __init__(self, data):

        # Bind data set to instance.
        self.data = data

        # Container for transformations performed on data
        self.transformations = []

    def output_results(self, filename):
        """Visualize user-defined transformation results.

        :return outputs plot to `results` directory.
        """

        self.data.plot(title='Result of applying {} onto data set'.format(self.transformations[-1]))
        plt.savefig("results/{}.png".format(filename))
        plt.close()

    def dispatch(self, response: [List[str], str]) -> pd.DataFrame:

        action = response[0]
        potential_feature = response[-1]
        on_all = potential_feature == action

        apply_to_features = [potential_feature] if not on_all else \
            [feature for feature in self.data.columns.values]

        self.transformations.append(action)

        # Attempt to match our provided :action on one of our
        # implemented functions below.

        if action == ':summarize':
            return self.summarize(apply_to_features)

        elif action == ':groupby':
            feature = response[1]
            combinator = response[2]

            group_by_intermed = self.groupby(feature)
            self.data = group_by_intermed

            return self.dispatch([combinator])

        elif action == ':count':
            return self.count(apply_to_features)

        elif action == ':sum':
            return self.sum(apply_to_features)

        elif action == ':mean':
            return self.mean(apply_to_features)

        elif action == ':median':
            return self.median(apply_to_features)

        elif action == ':min':
            return self.min(apply_to_features)

        elif action == ':max':
            return self.max(apply_to_features)

        elif action == ':sort':
            return self.sort(apply_to_features)

        else:
            raise InvalidActionError(action)

    # Define functions for interactive data analysis task.

    def summarize(self, features: List[str]):
        return self.data[features].describe()

    def groupby(self, feature: str):
        return self.data.groupby(by=feature)

    def sum(self, features: List[str]):
        return self.data[features].sum()

    def count(self, features: List[str]):
        return self.data[features].count()

    def mean(self, features: List[str]):
        return self.data[features].mean()

    def median(self, features: List[str]):
        return self.data[features].median()

    def min(self, features: List[str]):
        return self.data[features].min()

    def max(self, features: List[str]):
        return self.data[features].max()

    def sort(self, features: List[str]):
        return self.data[features].sort_values(inplace=True,
                                               ascending=False)


def build_dataset_prompt():
    """Provide informative first output to user.

    :return print to console.
    """

    print("")
    print("Let's start by choosing what features you'd like to look at/explore!")


def list_all_columns(data):
    """List all columns if requested by user.

    :param data: our dataframe of reddit comments
    :return prints column information to the user
    """

    # Print columns to user.
    print("\nFeatures in our original dataset include (one at a time, please!):")
    print("-" * 30)
    print("")

    # Print each column in our DataFrame.
    for index, column in enumerate(data.columns.values):
        print("[{}] {}".format(index, column))
        time.sleep(0.20)
