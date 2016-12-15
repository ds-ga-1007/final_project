
from abc import ABCMeta, abstractmethod, abstractclassmethod
import pandas as PD
import numpy as NP
import pickle


class Transformer(object, metaclass=ABCMeta):
    '''
    Abstract base class for all Transformer instances.
    '''

    def __init__(self):
        pass

    def _concatenate_dataframes(self, *datasets):
        if len(datasets) == 0:
            raise ValueError('empty list of dataset')
        single_dataset = len(datasets) == 1

        records = []
        df = PD.DataFrame(None)
        for _ in datasets:
            records.append(len(_))
            df = df.append(_)
        return df, records, single_dataset

    def _restore_dataframes(self, df, records, single_dataset,
                            to_dataframe=False):
        cols = df.columns
        restored = []
        i = 0

        for _ in records:
            # TODO:
            # Shall we check if the transformed elements are all numeric?
            if not to_dataframe:
                result = NP.array(df.iloc[i:i+_])
            else:
                result = PD.DataFrame(df.iloc[i:i+_], columns=cols)
                result = result.reset_index(drop=True)
            restored.append(result)
            i += _
        if single_dataset:
            return restored[0]      # strip off the list
        else:
            return restored

    def transform(self, *datasets, to_dataframe=False):
        '''
        Transform a set of datasets at once.

        Parameters
        ----------
        datasets : list or any iterable of pandas.DataFrame
        to_dataframe : bool
            If True, returns pandas.DataFrame instances instead of
            numpy.ndarray instances.

        Returns
        -------
        transformed : list of np.ndarray or pandas.DataFrame
            The number of elements in @transformed is the same as that
            of @datasets.
            The number of records in each element of @transformed matches
            that of the element in @datasets.
        '''
        df, records, single_dataset = self._concatenate_dataframes(*datasets)
        # Relay the concatenation to concrete implementations
        newdf = self._transform(df)
        restored = self._restore_dataframes(newdf, records, single_dataset,
                                            to_dataframe)
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


class LearnableTransformer(Transformer):
    '''
    Abstract transformer which keep track of some characteristics of given
    datasets.
    '''
    def fit(self, *datasets):
        '''
        Learn some characteristics from the provided datasets.

        Parameters
        ----------
        datasets : list or any iterable of pandas.DataFrame
        '''
        df, _, _ = self._concatenate_dataframes(*datasets)
        self._fit(df)
        return self

    @abstractmethod
    def _fit(self, dataset):
        pass

    def dump(self, file_):
        '''
        Save the transformer into a file.
        This is a wrapper for pickle.dump()

        Parameters
        ----------
        file_ : object
            must have a write() method that accepts a single bytes argument
            (identical requirement to pickle.dump)
        '''
        pickle.dump(self, file_)

    @classmethod
    def load(cls, file_):
        '''
        Load the transformer from a file.
        This is a wrapper for pickle.load()

        Parameters
        ----------
        file_ : object
            must have a read() method that takes an integer, and a readline()
            method that require no arguments, both of which returning bytes
            (identical requirement to pickle.load)

        Returns
        -------
        transformer : LearnableTransformer instance
        '''
        return pickle.load(self, file_)


class InvertibleTransformer(Transformer):
    '''
    Abstract transformer which supports an inverse transform operation.
    If given a dataset @df, and an InvertibleTransformer instance @it, then

    it.inverse_transform(it.transform(df)) == numpy.array(df)
    '''
    def inverse_transform(self, *datasets, to_dataframe=False):
        '''
        Inverse-transform a set of a datasets at once.

        Parameters
        ----------
        datasets : list or any iterable of pandas.DataFrame
        to_dataframe : bool
            If True, returns pandas.DataFrame instances instead of
            numpy.ndarray instances.

        Returns
        -------
        transformed : list of np.ndarray or pandas.DataFrame
            The number of elements in @transformed is the same as that
            of @datasets.
            The number of records in each element of @transformed matches
            that of the element in @datasets.
        '''
        df, records, single_dataset = self._concatenate_dataframes(*datasets)
        # Relay the concatenation to concrete implementations
        newdf = self._inverse_transform(df)
        restored = self._restore_dataframes(newdf, records, single_dataset)
        return restored

    @abstractmethod
    def _inverse_transform(self, dataset):
        pass
