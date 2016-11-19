
from .base import Transformer
import pandas as PD


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
    Transforms a tabular dataset according to given schema

    Parameters
    ----------
    schema : list of str, or dict of (str, str)
        Specifies the type of each column via a list of string, each
        element of which can be either "numeric" or "categorical".
        When giving a list, the column type is determined in order.
        When giving a dict, the column type is determined by matching
        column names.
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
            return self._transform_by_name(dataset)
        else:
            return self._transform_by_order(dataset)

    def _transform_by_name(self, dataset):
        for c in dataset.columns:
            op = _column_types[self._schema[c]]
            dataset[c] = op(dataset[c])
        return dataset

    def _transform_by_order(self, dataset):
        if len(dataset.columns) != len(self._schema):
            raise ValueError(
                    'number of columns does not match that of schema'
                    )
        for c, t in zip(dataset.columns, self._schema):
            op = _column_types[t]
            dataset[c] = op(dataset[c])
        return dataset

    def transform(self, *datasets):
        '''
        Transform a list of tabular datasets at once.

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
        datasets : list or any iterable of pandas.DataFrame

        Returns
        -------
        transformed : list of np.ndarray
            The number of elements in @transformed is the same as that
            of @datasets.
            The number of records in each element of @transformed matches
            that of the element in @datasets.
        '''
        return Transformer.transform(self, *datasets)
