
from .base import Transformer
from ._util import _make_op, _apply_op
import pandas as PD
import numpy as NP


def _mean_imputer(s):
    return s.mean()


def _median_imputer(s):
    return s.median()


def _zero_imputer(s):
    return 0


def _null_imputer(s):
    return NP.nan


_builtin_imputers = {
        None        : _null_imputer,
        'mean'      : _mean_imputer,
        'median'    : _median_imputer,
        'zero'      : _zero_imputer,
        }


def _make_single_by(by):
    if (by is None) or isinstance(by, str):
        try:
            return _builtin_imputers[by]
        except KeyError:
            raise KeyError('unknown imputation rule %s' % by)
    elif callable(by):
        return by
    else:
        raise TypeError('unknown rule type %r' % type(by))


class NumericImputationTransformer(Transformer):
    '''
    Replaces null cells in numeric columns with given rules.  Leaving
    categorical columns untouched.

    Parameters
    ----------
    by : None, str, callable, or dict/iterable of these
        @by can take the following strings for some default imputation rules:
            * 'mean' : Impute the data with mean of the column.
            * 'median' : Impute the data with median of the column.
            * 'zero' : Impute the data with zeros.
        Given None, the transformer will do nothing.  Useful when you want to
        skip some columns when supplying a list of rules.
        Given a callable (e.g. a function), the transformer will apply the
        callable to compute the filler value and fill the empty cells with
        that value.  The callable should take either a numpy.ndarray or a
        pandas.Series instance, and return a single scalar value.
        If an iterable of these types are given, the transformer will
        fill in empty cells by applying given rules to each column.  If
        the iterable is a dict, the transformer will match the column names
        and perform transformation.

    Examples
    --------
    >>> import pandas as PD
    >>> import numpy as NP
    >>> df = PD.DataFrame(
    ...         [[1, 'a', NP.nan], [2, 'a', 2], [NP.nan, 'b', 3]],
    ...         columns=['A', 'B', 'C']
    ...         )
    >>> df
         A  B    C
    0  1.0  a  NaN
    1  2.0  a  2.0
    2  NaN  b  3.0
    >>> from dataprep.transformer import NumericImputationTransformer
    >>> NumericImputationTransformer('mean').transform(df)
    [array([[1.0, 'a', 2.5],
            [2.0, 'a', 2.0],
            [1.5, 'b', 3.0]], dtype=object)]
    >>> NumericImputationTransformer(lambda s: NP.sum(s)).transform(df)
    [array([[1.0, 'a', 5.0],
            [2.0, 'a', 2.0],
            [3.0, 'b', 3.0]], dtype=object)]
    >>> NumericImputationTransformer(
    ...        ['mean', None, lambda s: NP.sum(s)]
    ...        ).transform(df)
    [array([[1.0, 'a', 5.0],
            [2.0, 'a', 2.0],
            [1.5, 'b', 3.0]], dtype=object)]
    >>> NumericImputationTransformer({'A': 'mean'}).transform(df)
    [array([[1.0, 'a', nan],
            [2.0, 'a', 2.0],
            [1.5, 'b', 3.0]], dtype=object)]
    '''
    def __init__(self, by):
        self._by = _make_op(by, _make_single_by)

    def _transform_column(self, dataset, column, byfunc):
        if dataset[column].dtype != NP.object:
            dataset[column].fillna(byfunc(dataset[column]), inplace=True)

    def _transform(self, dataset):
        return _apply_op(
                self._by,
                dataset,
                'imputation rules',
                self._transform_column
                )
