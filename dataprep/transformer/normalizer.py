
from .base import Transformer, InvertibleTransformer, LearnableTransformer
from ._util import _apply_op
import pandas as PD
import numpy as NP


class ColumnNormalizer(InvertibleTransformer, LearnableTransformer):
    '''
    Normalize numeric features

    Parameters
    ----------
    which : None, str, or iterable of these (default 'normal')
        @which (or each element of @which) can take the following values:
            * None
                does nothing
            * 'negpos'
                linearly normalize the column so that the minimum value
                becomes -1 and maximum value becomes 1
            * 'zeropos'
                linearly normalize the column so that the minimum value
                becomes 0 and maximum value becomes 1
            * 'zeromean'
                normalize the column by subtracting the mean
            * 'normal'
                normalize the column by subtracting the mean and dividing
                by standard deviation

    Examples
    --------
    >>> import pandas as PD
    >>> df = PD.DataFrame(
    ...         [[1, 'a', -1], [2, 'a', 2], [-3, 'b', 3]],
    ...         columns=['A', 'B', 'C']
    ...         )
    >>> df
       A  B  C
    0  1  a -1
    1  2  a  2
    2 -3  b  3
    >>> from dataprep.transformer import ColumnNormalizer
    >>> norm = ColumnNormalizer('zeropos')
    >>> norm.fit(df)
    <dataprep.transformer.normalizer.ColumnNormalizer at 0x...>
    >>> arr = norm.transform(df)
    >>> arr
    array([[0.8, 'a', 0.0],
           [1.0, 'a', 0.75],
           [0.0, 'b', 1.0]], dtype=object)
    >>> df2 = PD.DataFrame(arr, columns=['A', 'B', 'C'])
    >>> df2
         A  B     C
    0  0.8  a     0
    1    1  a  0.75
    2    0  b     1
    >>> norm.inverse_transform(df2)
    array([[1.0, 'a', -1.0],
           [2.0, 'a', 2.0],
           [-3.0, 'b', 3.0]], dtype=object)
    >>> norm2 = ColumnNormalizer({'A': 'zeropos'})
    >>> norm2.fit(df)
    <dataprep.transformer.normalizer.ColumnNormalizer at 0x...>
    >>> norm2.transform(df)
    array([[0.8, 'a', -1],
           [1.0, 'a', 2],
           [0.0, 'b', 3]], dtype=object)
    '''
    def __init__(self, which='normal'):
        self._which = which
        self._mean = None
        self._std = None
        self._min = None
        self._max = None
        self._fitted = False

    def _transform_column(self, dataset, column, which):
        if not self._fitted:
            raise ValueError('transform before fitting')

        if column not in self._available_columns:
            return

        min_ = self._min[column]
        max_ = self._max[column]
        mean = self._mean[column]
        std = self._std[column]

        if which is None:
            return
        elif which == 'negpos':
            if max_ == min_:
                dataset[column] = 0
            else:
                dataset[column] = (dataset[column] - min_) / (max_ - min_)
                dataset[column] = dataset[column] * 2 - 1
        elif which == 'zeropos':
            if max_ == min_:
                dataset[column] = 0
            else:
                dataset[column] = (dataset[column] - min_) / (max_ - min_)
        elif which == 'zeromean':
            dataset[column] -= mean
        elif which == 'normal':
            if std == 0:
                dataset[column] -= mean
            else:
                dataset[column] = (dataset[column] - mean) / std

    def _transform(self, dataset):
        return _apply_op(
                self._which,
                dataset,
                'normalization',
                self._transform_column
                )

    def _fit(self, dataset):
        desc = dataset.describe(include=[NP.number])
        self._mean = desc.loc['mean']
        self._std = desc.loc['std']
        self._max = desc.loc['max']
        self._min = desc.loc['min']
        self._available_columns = desc.columns
        self._fitted = True

    def _inverse_transform(self, dataset):
        return _apply_op(
                self._which,
                dataset,
                'normalization',
                self._inverse_transform_column
                )

    def _inverse_transform_column(self, dataset, column, which):
        if not self._fitted:
            raise ValueError('inverse transform before fitting')

        if column not in self._available_columns:
            return

        min_ = self._min[column]
        max_ = self._max[column]
        mean = self._mean[column]
        std = self._std[column]

        if which is None:
            return
        elif which == 'negpos':
            # When min == max, all elements are equal to min, so the
            # following still works
            dataset[column] = (dataset[column] + 1) / 2
            dataset[column] = dataset[column] * (max_ - min_) + min_
        elif which == 'zeropos':
            # When min == max, all elements are equal to min, so the
            # following still works
            dataset[column] = dataset[column] * (max_ - min_) + min_
        elif which == 'zeromean':
            dataset[column] += mean
        elif which == 'normal':
            # When std == 0, all elements are equal to mean.
            dataset[column] = dataset[column] * std + mean


class GlobalLinearNormalizer(InvertibleTransformer):
    '''
    Normalize every cell according to the following rule:

    new = (old - vmin) / (vmax - vmin) * (nmax - nmin) + nmin

    where vmin, vmax, nmin and nmax are all given by user.

    Parameters
    ----------
    vmin, vmax, nmin, nmax : float
    '''
    def __init__(self, vmin, vmax, nmin=0, nmax=1):
        self._vmin = float(vmin)
        self._vmax = float(vmax)
        self._nmin = float(nmin)
        self._nmax = float(nmax)

    def _transform(self, dataset):
        return ((dataset - self._vmin) / (self._vmax - self._vmin) *
                (self._nmax - self._nmin) + self._nmin)

    def _inverse_transform(self, dataset):
        return ((dataset - self._nmin) / (self._nmax - self._nmin) *
                (self._vmax - self._vmin) + self._vmin)
