
from .base import Transformer
import pandas as PD
import numpy as NP


class DummyTransformer(Transformer):
    '''
    Encode categorical features into indicator variables.

    This is a wrapper for pandas.get_dummies function.

    Parameters
    ----------
    columns : None (default) or iterable of str
        Column names in the DataFrame to be encoded, or None for encoding
        all categorical columns.
    dummy_unknown : bool, default False
        Whether or not to treat NaN as a separate category.
    drop_first : bool, default False
        Whether or not to get only n-1 indicator variables for n
        categories.  Useful if your algorithm depends on linear
        dependency, but not recommended otherwise.
        It is usually a bad idea to set drop_first to True and dummy_unknown
        to False when some columns may have null values.

    Examples
    --------
    >>> import pandas as PD
    >>> import numpy as NP
    >>> df = PD.DataFrame({'A': ['A', 'B', NP.nan], 'B': ['a', NP.nan, 'c']})
    >>> df2 = PD.DataFrame({'A': ['A', 'B', 'A'], 'B': ['a', 'b', 'c']})
    >>> df
         A    B
    0    A    a
    1    B  NaN
    2  NaN    c
    >>> df2
       A  B
    0  A  a
    1  B  b
    2  A  c
    >>> from dataprep.transformer import DummyTransformer
    >>> DummyTransformer().transform(df)
    array([[ 1.,  0.,  1.,  0.],
           [ 0.,  1.,  0.,  0.],
           [ 0.,  0.,  0.,  1.]])
    >>> DummyTransformer(dummy_unknown=True).transform(df)
    array([[ 1.,  0.,  0.,  1.,  0.,  0.],
           [ 0.,  1.,  0.,  0.,  0.,  1.],
           [ 0.,  0.,  1.,  0.,  1.,  0.]])
    >>> DummyTransformer(drop_first=True).transform(df2)
    array([[ 0.,  0.,  0.],
           [ 1.,  1.,  0.],
           [ 0.,  0.,  1.]])
    '''
    def __init__(self, columns=None, dummy_unknown=False, drop_first=False):
        self._dummy_unknown = dummy_unknown
        self._drop_first = drop_first
        self._columns = columns

    def _transform(self, dataset):
        return PD.get_dummies(
                dataset,
                dummy_na=self._dummy_unknown,
                drop_first=self._drop_first,
                columns=self._columns
                )


# Alias
OneHotEncoderTransformer = DummyTransformer
