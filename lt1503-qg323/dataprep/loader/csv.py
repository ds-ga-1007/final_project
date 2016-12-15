
from .base import *

import pandas as PD


# Basically a prettier Java-ish wrapper for pandas.read_csv function.
class CSVLoader(Loader):
    '''
    Concrete class for loading a CSV file.
    '''

    def __init__(self, target=None, delim=',', header=None):
        '''
        Parameters
        ----------
        delim : str
            The field, or column, separator
        header : int or None
            Whether there is a header row in the dataset, and if so, on
            which line.
        '''
        Loader.__init__(self, target=target)
        self._delim = delim
        self._header = header

    @property
    def delim(self):
        return self._delim

    @delim.setter
    def delim(self, delim):
        self._delim = delim

    def _load_from_path(self, path):
        # I think the exception raised by pandas is pretty self-explanatory
        # so I don't handle it here.
        return PD.read_csv(path, sep=self._delim, header=self._header)
