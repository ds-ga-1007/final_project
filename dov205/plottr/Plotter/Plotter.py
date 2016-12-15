import matplotlib
import typing
import pandas as pd

class Plotter:

    def __init__(self, input_file: str):

        self.input_data = input_file

        self.dataset = self._build_dataframe(self.input_data)


    def _build_dataframe(self):
        pass


