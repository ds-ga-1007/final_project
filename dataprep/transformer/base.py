
from abc import ABCMeta, abstractmethod
import pandas as PD
import numpy as NP


class Transformer(object, metaclass=ABCMeta):
    '''
    Abstract base class for all Transformer instances.
    '''

    def __init__(self):
        pass

    def transform(self, *datasets):
        '''
        Transform a set of datasets at once.

        Parameters
        ----------
        datasets : list or any iterable of pandas.DataFrame

        Returns
        -------
        transformed : list of np.ndarray
            The number of elements in @transformed is the same as that
            of @datasets.
            The number of records in each element of @transformed matches
            that of the element in @datasets.
        '''
        if len(datasets) == 0:
            raise ValueError('empty list of dataset')
        single_dataset = len(datasets) == 1

        # Concatenate all datasets together, and record the number of
        # records in each dataset so that we can restore the concatenation
        # back.
        records = []
        df = PD.DataFrame(None)
        for _ in datasets:
            records.append(len(_))
            df = df.append(_)

        # Relay the concatenation to concrete implementations
        newdf = self._transform(df)

        restored = []
        i = 0
        for _ in records:
            # TODO:
            # Shall we check if the transformed elements are all numeric?
            restored.append(NP.array(newdf.iloc[i:i+_]))
            i += _

        if single_dataset:
            return restored[0]      # strip off the list
        else:
            return restored

    @abstractmethod
    def _transform(self, dataset):
        '''
        Internal interface for transforming a single pandas DataFrame
        dataset into another pandas DataFrame.

        Parameters
        ----------
        dataset : pandas.DataFrame instance

        Returns
        -------
        transformed : pandas.DataFrame
        '''
        return None
