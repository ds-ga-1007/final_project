
from .base import Transformer
from ._util import _make_op, _apply_op
import pandas as PD
import numpy as NP
from numbers import Number, Integral    # for type checking
from collections import Iterable        # for type checking


def _none_criterion(criterion):
    return lambda x: PD.Series([False] * x.count())


def _numeric_criterion(criterion):
    return lambda x: x == criterion


def _categorical_criterion(criterion):
    return lambda x: (
            PD.Series([False] * x.count()) if x.dtype != NP.object
            else (x == criterion)
            )


def _predicate_criterion(criterion):
    return lambda x: x.apply(criterion)


def _make_single_criterion(criterion):
    if criterion is None:
        return _none_criterion(criterion)
    elif isinstance(criterion, Number):
        return _numeric_criterion(criterion)
    elif isinstance(criterion, str):
        return _categorical_criterion(criterion)
    elif callable(criterion):
        return _predicate_criterion(criterion)
    else:
        raise TypeError('invalid criterion type %r' % type(criterion))


class NullValueTransformer(Transformer):
    '''
    Replaces cells satisfying given criterion to null values for missing value
    handling.

    Parameters
    ----------
    criterion : number, str, callable, None, or dict/iterable of these
        If criterion is given a number (int, float, etc.), the transformer
        will replace all numeric values equal to the criterion with null
        values, leaving all other values untouched.
        The transformer does the same for criterion with str type, except
        that it now replaces categorical values equal to the criterion
        instead.
        If a callable (e.g. a function) is given, the transformer will apply
        the callable to all values, and replaces those values giving True with
        null values. The callable should be returning a bool, and
            * is either taking a single argument representing the cell value,
              or,
            * is a numpy.ufunc
        If None is given, the transformer will do nothing.  Useful when
        you want to skip some columns when supplying a list of criteria.
        If an iterable of these types are given, the transformer will
        compare or evaluate, and replace with null values in a per-column
        basis.  If the iterable is a dict, the transformer will match
        the column names and perform transformation.
    only : 'numeric', 'categorical', or None (default)
        If 'numeric', apply such transformation only on numeric values.
        If 'categorical', apply only on categorical values.

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
    >>> from dataprep.transformer import NullValueTransformer
    >>> NullValueTransformer(2).transform(df)
    [array([[1.0, 'a', -1.0],
           [nan, 'a', nan],
           [-3.0, 'b', 3.0]], dtype=object)]
    >>> NullValueTransformer('a').transform(df)
    [array([[1.0, nan, -1.0],
           [2.0, nan, 2.0],
           [-3.0, 'b', 3.0]], dtype=object)]
    >>> NullValueTransformer([None, None, -1]).transform(df)
    [array([[1.0, 'a', nan],
           [2.0, 'a', 2.0],
           [-3.0, 'b', 3.0]], dtype=object)]
    >>> NullValueTransformer({'A': 2}).transform(df)
    [array([[1.0, 'a', -1],
           [nan, 'a', 2],
           [-3.0, 'b', 3]], dtype=object)]

    When specifying function as criterion, it applies to all elements so
    it may throw errors.  To better control it's behavior, use the 'only'
    argument to control what kind of elements the function should filter,
    or specify columns by supplying a dict:
    >>> NullValueTransformer(lambda x: x < 0).transform(df)
    Traceback (most recent call last):
        ...
    TypeError: unorderable types: str() < int()
    >>> NullValueTransformer(lambda x: x < 0, only='numeric').transform(df)
    [array([[1.0, 'a', nan],
           [2.0, 'a', 2.0],
           [nan, 'b', 3.0]], dtype=object)]
    >>> NullValueTransformer({'A': lambda x: x < 0}).transform(df)
    [array([[1.0, 'a', -1],
           [2.0, 'a', 2],
           [nan, 'b', 3]], dtype=object)]
    '''

    def __init__(self, criterion, only=None):
        # Throws TypeError
        self._criterion = _make_op(criterion, _make_single_criterion)
        self._only = only

    def _skip(self, series):
        return (((self._only == 'numeric') and (series.dtype == NP.object)) or
                ((self._only == 'categorical') and (series.dtype != NP.object))
                )

    def _transform_column(self, dataset, column, crit):
        if not self._skip(dataset[column]):
            dataset.loc[crit(dataset[column]), column] = NP.nan

    def _transform(self, dataset):
        return _apply_op(
                self._criterion,
                dataset,
                'criteria',
                self._transform_column
                )


class NullIndicatorTransformer(Transformer):
    '''
    Search through columns and add a dummy variable for each column with
    NaN values to indicate that the value there is missing.

    Parameters
    ----------
    columns : Iterable of str or int, or None
        When None is given, the transformer will do this for every column.
    suffix : str (default = '_missing')
        The new column name for these indicator variable is
        original_column_name+suffix

    Examples
    --------
    >>> import pandas as PD
    >>> import numpy as NP
    >>> df = PD.DataFrame(
    ...         [[NP.nan, 2, 1], [1, NP.nan, 2]],
    ...         columns=['A', 'B', 'C']
    ...         )
    >>> df
         A    B    C
    0  NaN  2.0  1.0
    1  1.0  NaN  2.0
    >>> from dataprep.transformer import *
    >>> NullIndicatorTransformer().transform(df)
    [array([[ nan,   2.,   1.,   1.,   0.],
           [  1.,  nan,   2.,   0.,   1.]])]
    >>> NullIndicatorTransformer(['A']).transform(df)
    [array([[ nan,   2.,   1.,   1.],
           [  1.,  nan,   2.,   0.]])]
    >>> NullIndicatorTransformer([1, 2]).transform(df)
    [array([[ nan,   2.,   1.,   0.],
           [  1.,  nan,   2.,   1.]])]
    '''

    def __init__(self, columns=None, suffix='_missing'):
        if not ((columns is None) or
                (isinstance(columns, Iterable) and not
                    isinstance(columns, str))):
            raise TypeError('invalid columns type %r' % type(columns))
        elif columns is not None:
            # Check element types
            if isinstance(columns[0], Integral):
                indices = True
            elif isinstance(columns[0], str):
                indices = False
            else:
                raise TypeError('invalid element type %r' % type(columns[0]))

            for c in columns:
                if not ((isinstance(c, Integral) and indices) or
                        (isinstance(c, str) and not indices)):
                    raise TypeError('element types are not the same')

        if not isinstance(suffix, str):
            raise TypeError('suffix is not a string')

        self._columns = columns
        self._suffix = suffix

    def _transform(self, dataset):
        cols = self._columns if self._columns is not None else dataset.columns

        for c in cols:
            series = dataset.ix[:, c]
            newc = str(c) + self._suffix
            if series.isnull().any():
                dataset[newc] = series.isnull().astype(int)

        return dataset
