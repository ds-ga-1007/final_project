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

        self.data.plot(title='Result of applying {} onto data set')
        plt.tight_layout()
        plt.savefig("results/{}.png".format(filename))
        plt.close()

    def dispatch(self, response: [List[str], str]) -> pd.DataFrame:

        action = response[0]
        potential_feature = response[-1]
        on_all = potential_feature == action

        apply_to_features = potential_feature if not on_all else \
            [feature for feature in self.data.columns.values]

        self.transformations.append({action: apply_to_features})

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

    def summarize(self, features: [str, List[str]]):
        return self.data[[features]].describe()

    def groupby(self, feature: str):
        return self.data.groupby(by=feature)

    def sum(self, features: [str, List[str]]):
        return self.data[[features]].sum()

    def count(self, features: [str, List[str]]):
        return self.data[[features]].count()

    def mean(self, features: [str, List[str]]):
        return self.data[[features]].mean()

    def median(self, features: [str, List[str]]):
        return self.data[[features]].median()

    def min(self, features: [str, List[str]]):
        return self.data[[features]].min()

    def max(self, features: [str, List[str]]):
        return self.data[[features]].max()

    def sort(self, features: [str, List[str]]):
        return self.data[[features]].sort_values(inplace=True,
                                                 ascending=False)


def build_dataset_prompt():

    print("")
    print("Let's start by choosing what features you'd like to look at/explore!")


def list_all_columns(data):

    print("\nFeatures in our original dataset include (one at a time, please!):")
    print("-" * 30)
    print("")

    for index, column in enumerate(data.columns.values):
        print("[{}] {}".format(index, column))
        time.sleep(0.20)

    # print("Alternatively, you can define a new calculated feature with `:new`.\n")
