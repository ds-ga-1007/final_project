import matplotlib
import typing
import pandas as pd
import time

class Plotter:

    # valid_operations = {
    #     ['group by', 'groupby']: pd.groupby,
    #     ['sum']: sum,
    #     ['count', 'rows']:
    # }

    def __init__(self, data):

        self.data = data

        # Container for transformations performed on data
        self.transformations = []

    def plot(self):
        """Visualize user-defined transformation results

        :return:
        """

        pass


def build_dataset_prompt():

    print("")
    print("Let's start by choosing what features you'd like to look at/explore!")


def list_all_columns(data):

    print("\nFeatures in our original dataset include (one at a time, please!):")
    print("-" * 30)
    print("")

    for index, column in enumerate(data.columns.values):
        print("[{}] {}".format(index, column))
        time.sleep(0.25)

    # print("Alternatively, you can define a new calculated feature with `:new`.\n")
