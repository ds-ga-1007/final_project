
from abc import ABCMeta, abstractmethod
from numbers import Integral


class Loader(object, metaclass=ABCMeta):
    '''
    Abstract base class for all Loader instances.

    Parameters
    ----------
    target : None or iterable of str or int
        If given, this function will return two pandas.DataFrame
        instances: the first one being the features and the last
        one being the labels.
    '''

    def __init__(self, target=None):
        str_columns = None

        if target is not None:
            if isinstance(target[0], str):
                str_columns = True
            elif isinstance(target[0], Integral):
                str_columns = False
            else:
                raise TypeError('target is not a list of str or ints')

            for t in target:
                if ((str_columns and isinstance(t, Integral)) or
                    (not str_columns and isinstance(t, str))):
                    raise TypeError('target is not a list of str or ints')

        self._target = target
        self._str_columns = str_columns

    def load_from_path(self, path):
        '''
        Load dataset from file.

        Parameters
        ----------
        path : str
            The path pointing to the *local* dataset file.

        Returns
        -------
        df : pandas.DataFrame, if target is None
        dfX, dfY : pandas.DataFrames, if target is not None
        '''
        df = self._load_from_path(path)

        if self._target is None:
            return [df]
        else:
            if self._str_columns:
                dfX = df.drop(self._target, axis=1)
            else:
                for i in range(len(self._target)):
                    if self._target[i] < 0:
                        self._target[i] += len(df.columns)
                dfX = df.drop(df.columns[self._target], axis=1)
            dfY = df.loc[:, self._target]

            return [dfX, dfY]

    @abstractmethod
    def _load_from_path(self, path):
        return None
