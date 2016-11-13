
from .base import *

import pandas as PD


# Basically a prettier Java-ish wrapper for pandas.read_csv function.
class CSVLoader(Loader):
    '''
    Concrete class for loading a CSV file.
    '''

    def __init__(self, delim=',', header=None, index_col=None):
        '''
        Parameters
        ----------
        delim : str
            The field, or column, separator
        header : int or None
            Whether there is a header row in the dataset, and if so, on
            which line.
        '''
        self._delim = delim
        self._header = header

    @property
    def delim(self):
        return self._delim

    @delim.setter
    def delim(self, delim):
        self._delim = delim

    def load_from_path(self, path):
        return PD.read_csv(path, sep=self._delim, header=self._header)
