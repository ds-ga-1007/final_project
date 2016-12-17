
from .base import Transformer
import pandas as PD
from collections import Iterable
from numbers import Number, Integral


def _to_numeric(column):
    return PD.to_numeric(column, errors='coerce')


def _to_categorical(column):
    return column.astype(str)


_column_types = {
        "numeric": _to_numeric,
        "categorical": _to_categorical,
        }


def _check_types(schema_values):
    for t in schema_values:
        if t not in _column_types:
            raise ValueError('unknown column type %s' % t)


class TabularSchemaTransformer(Transformer):
    '''
    Transforms a tabular dataset according to given schema.

    For each column, if the column type given in the schema is "numeric",
    TabularSchemaTransformer would try converting the values there into
    real numbers, replacing those "invalid" values by NaNs.  If the
    column type is "categorical", the transformer would convert values
    there into strings, and treat each distinct string as a category.

    If the schema is given as a dict, the transformer will transform
    all the columns whose names are given, leaving other columns
    untouched.

    If the schema is given as a list, the number of elements in the
    schema should match the number of columns in the dataset, or an
    ValueError would be thrown otherwise.

    Parameters
    ----------
    schema : list of str, or dict of (str, str)
        Specifies the type of each column via a list of string, each
        element of which can be either "numeric" or "categorical".
    '''

    def __init__(self, schema):
        # Throws ValueError if the schema is not in correct format
        if isinstance(schema, dict):
            _check_types(schema.values())
        else:
            _check_types(schema)

        self._schema = schema

    def _transform(self, dataset):
        if isinstance(self._schema, dict):
            pairs = self._schema.items()
        else:
            if len(dataset.columns) != len(self._schema):
                raise ValueError(
                        'number of columns does not match that of schema'
                        )
            pairs = zip(dataset.columns, self._schema)
        for c, t in pairs:
            op = _column_types[t]
            dataset[c] = op(dataset[c])
        return dataset


class TabularSchemaGuesser(TabularSchemaTransformer):
    '''
    Guess the schema of a tabular dataset by counting the number of elements
    looking like numeric values.  If the number of numeric-like values takes
    a large portion of a column, then the column is treated as a numeric
    column.  Otherwise it is treated as a categorical column.

    Use this at your own risk.

    Parameters
    ----------
    threshold : float, between 0 and 1.  Default 0.5
        The lower bound of numeric-like value proportion for a column to be
        treated as numeric.

    Examples
    --------
    >>> import pandas as PD
    >>> df = PD.DataFrame(
    ...         [[1, 'a', '?'], [2, 'a', 2], ['?', 'b', 3]],
    ...         columns=['A', 'B', 'C']
    ...         )
    >>> df
       A  B  C
    0  1  a  ?
    1  2  a  2
    2  ?  b  3
    >>> from dataprep.transformer import TabularSchemaGuesser
    >>> TabularSchemaGuesser().transform(df)
    array([[1.0, 'a', nan],
           [2.0, 'a', 2.0],
           [nan, 'b', 3.0]], dtype=object)
    '''

    def __init__(self, threshold=0.5):
        if not isinstance(threshold, Number):
            raise TypeError('threshold is not a number')
        if not (0 <= threshold <= 1):
            raise ValueError('invalid threshold value')
        self._threshold = threshold
        self._schema = None

    def _transform(self, dataset):
        new = dataset.apply(lambda c: PD.to_numeric(c, errors='coerce'))
        counts = new.count()
        self._schema = {
                c: ('numeric' if counts[c] / dataset.shape[0] > self._threshold
                    else 'categorical')
                for c in dataset.columns
                }
        return TabularSchemaTransformer._transform(self, dataset)


class DropColumnTransformer(Transformer):
    '''
    Drop columns in a tabular dataset.

    Parameters
    ----------
    columns : list-like of int or str
        When given a list of ints, each element represent the index of the
        column (0-based).
        When given a list of strs, each element is the name of the column.
        Non-existent indices and/or names will throw a ValueError for list of
        strs, or IndexError for list of ints, *upon transformation*.

    Examples
    --------
    >>> import pandas as PD
    >>> df = PD.DataFrame(
    ...         [[1, 'a', '?'], [2, 'a', 2], ['?', 'b', 3]],
    ...         columns=['A', 'B', 'C']
    ...         )
    >>> df
       A  B  C
    0  1  a  ?
    1  2  a  2
    2  ?  b  3
    >>> from dataprep.transformer import DropColumnTransformer
    >>> df.drop('A')
    array([['a', '?'],
           ['a', 2],
           ['b', 3]], dtype=object)
    '''

    def __init__(self, columns):
        if not isinstance(columns, Iterable):
            raise TypeError('columns is not iterable')
        if isinstance(columns[0], Integral):
            int_columns = True
        elif isinstance(columns[0], str):
            int_columns = False
        else:
            raise TypeError('the elements in columns is neither int nor str')

        for c in columns:
            if int_columns and not isinstance(c, Integral):
                raise TypeError('the elements in columns are not all ints')
            if not int_columns and not isinstance(c, str):
                raise TypeError('the elements in columns are not all strs')

        self._columns = columns
        self._int_columns = int_columns

    def _transform(self, dataset):
        # Throws ValueError or IndexError on non-existent columns.
        # I think the error message generated by pandas is pretty clear.
        if self._int_columns:
            dataset.drop(dataset.columns[self._columns], axis=1,
                         inplace=True)
        else:
            dataset.drop(self._columns, axis=1, inplace=True)
        return dataset


class ColumnRenamer(Transformer):
    '''
    Changes the names of the column while keeping the cells intact.

    This is a wrapper of pandas.DataFrame.rename method.

    Parameters
    ----------
    columns : list of new column names, or dict of old and new column names.
        Non-existent old column names in the dict are ignored.
        If the number of elements in list are more than n, the number of
        columns in the DataFrame, then the elements beyond n are ignored.

    Examples
    --------
    >>> import pandas as PD
    >>> df = PD.DataFrame(
    ...         [[1, 'a', '?'], [2, 'a', 2], ['?', 'b', 3]],
    ...         columns=['A', 'B', 'C']
    ...         )
    >>> df
       A  B  C
    0  1  a  ?
    1  2  a  2
    2  ?  b  3
    >>> from dataprep.transformer import ColumnRenamer
    >>> cr = ColumnRenamer(['a', 'b', 'c'])
    >>> cr.transform(df, to_dataframe=True)
       a  b  c
    0  1  a  ?
    1  2  a  2
    2  ?  b  3
    '''
    def __init__(self, columns):
        if not isinstance(columns, Iterable):
            raise TypeError('columns is not iterable')
        self._columns = columns

    def _transform(self, dataset):
        if isinstance(self._columns, dict):
            dataset.rename(columns=self._columns, inplace=True)
        else:
            dataset.rename(columns=dict(zip(dataset.columns, self._columns)),
                           inplace=True)
        return dataset
