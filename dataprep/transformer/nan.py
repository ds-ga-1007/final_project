
from .base import Transformer
import pandas as PD
import numpy as NP
from numbers import Number          # for type checking
from collections import Iterable    # for type checking


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


def _make_criterion_dict(criterion):
    newcrit = {}
    for k, v in criterion.items():
        newcrit[k] = _make_single_criterion(v)
    return newcrit


def _make_criterion_list(criterion):
    newcrit = []
    for crit in criterion:
        newcrit.append(_make_single_criterion(crit))
    return newcrit


def _make_criterion(criterion):
    if isinstance(criterion, dict):
        return _make_criterion_dict(criterion)
    elif isinstance(criterion, Iterable) and not isinstance(criterion, str):
        return _make_criterion_list(criterion)
    else:
        return _make_single_criterion(criterion)


class NullValueTransformer(Transformer):
    '''
    Replaces cells satisfying given criterion to null values for missing value
    handling.

    Parameters
    ----------
    criterion : number, str, callable, or dict/iterable of these
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
           [nan, 'b', 3.0]], dtype=object)]
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
        self._criterion = _make_criterion(criterion)
        self._only = only

    def _skip(self, series):
        return (((self._only == 'numeric') and (series.dtype == NP.object)) or
                ((self._only == 'categorical') and (series.dtype != NP.object))
                )

    def _transform(self, dataset):
        if isinstance(self._criterion, Iterable):
            if isinstance(self._criterion, dict):
                pairs = self._criterion.items()
            elif len(dataset.columns) != len(self._criterion):
                raise ValueError(
                        "number of columns does not match that of criteria"
                        )
            else:
                pairs = zip(dataset.columns, self._criterion)
            for c, crit in pairs:
                if self._skip(dataset[c]):
                    continue
                dataset.loc[crit(dataset[c]), c] = NP.nan
        else:
            for c in dataset.columns:
                if self._skip(dataset[c]):
                    continue
                dataset.loc[self._criterion(dataset[c]), c] = NP.nan
        return dataset
