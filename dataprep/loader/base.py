
from abc import ABCMeta, abstractmethod


class Loader(object, metaclass=ABCMeta):
    '''
    Abstract base class for all Loader instances.
    '''

    def __init__(self):
        pass

    @abstractmethod
    def load_from_path(self, path):
        '''
        Load dataset from file.

        Parameters
        ----------
        path : str
            The path pointing to the *local* dataset file.

        Returns
        -------
        df : pandas.DataFrame
        '''
        return None
