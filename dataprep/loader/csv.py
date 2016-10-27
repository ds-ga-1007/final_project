
from .tabular import *

import pandas as PD
import numpy as NP


class CSVLoader(TabularLoader):
    '''
    Dataset loader for reading CSV files.
    '''
    def __init__(self, sep=','):
        '''
        Parameters
        ----------
        sep : string
            Delimiter
        '''
        self.header = None
        self.seperator = sep

    def load(self, filename):
        self._dataset = PD.read_csv(
                filename,
                header=self.header,
                sep=self.separator,
                )
