'''
Doctesting transformers

>>> import pandas as PD
>>> import numpy as NP
>>> from dataprep.transformer._test.util import generic_array_equal
>>> df = PD.DataFrame({'A': ['A', 'B', NP.nan], 'B': ['a', NP.nan, 'c']})
>>> df2 = PD.DataFrame({'A': ['A', 'B', 'A'], 'B': ['a', 'b', 'c']})
>>> from dataprep.transformer import DummyTransformer
>>> ans = NP.array([[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
>>> generic_array_equal(DummyTransformer().transform(df), ans)
True
>>> ans = NP.array(
...         [[1, 0, 0, 1, 0, 0],
...          [0, 1, 0, 0, 0, 1],
...          [0, 0, 1, 0, 1, 0]]
...         )
>>> generic_array_equal(
...         DummyTransformer(dummy_unknown=True).transform(df),
...         ans
...         )
True
>>> ans = NP.array([[0, 0, 0], [1, 1, 0], [0, 0, 1]])
>>> generic_array_equal(DummyTransformer(drop_first=True).transform(df2), ans)
True
>>> df = PD.DataFrame(
...         [[1, 'a', NP.nan], [2, 'a', 2], [NP.nan, 'b', 3]],
...         columns=['A', 'B', 'C']
...         )
>>> from dataprep.transformer import NumericImputationTransformer
>>> ans = NP.array(
...         [[1.0, 'a', 2.5], [2.0, 'a', 2.0], [1.5, 'b', 3.0]],
...         dtype=NP.object
...         )
>>> res = NumericImputationTransformer('mean').transform(df)
>>> generic_array_equal(res, ans)
True
>>> ans = NP.array(
...         [[1.0, 'a', 5.0], [2.0, 'a', 2.0], [3.0, 'b', 3.0]],
...         dtype=NP.object
...         )
>>> res = NumericImputationTransformer(lambda s: NP.sum(s)).transform(df)
>>> generic_array_equal(ans, res)
True
>>> ans = NP.array(
...         [[1.0, 'a', 5.0], [2.0, 'a', 2.0], [1.5, 'b', 3.0]],
...         dtype=NP.object
...         )
>>> res = NumericImputationTransformer(
...        ['mean', None, lambda s: NP.sum(s)]
...        ).transform(df)
>>> generic_array_equal(res, ans)
True
>>> ans = NP.array(
...         [[1.0, 'a', NP.nan], [2.0, 'a', 2.0], [1.5, 'b', 3.0]],
...         dtype=NP.object
...         )
>>> res = NumericImputationTransformer({'A': 'mean'}).transform(df)
>>> generic_array_equal(res, ans)
True
>>> df = PD.DataFrame(
...         [[1, 'a', -1], [2, 'a', 2], [-3, 'b', 3]],
...         columns=['A', 'B', 'C']
...         )
>>> from dataprep.transformer import NullValueTransformer
>>> ans = NP.array(
...         [[1, 'a', -1], [NP.nan, 'a', NP.nan], [-3, 'b', 3]],
...         dtype=NP.object
...         )
>>> res = NullValueTransformer(2).transform(df)
>>> generic_array_equal(res, ans)
True
>>> ans = NP.array(
...         [[1, NP.nan, -1], [2, NP.nan, 2], [-3, 'b', 3]],
...         dtype=NP.object
...         )
>>> res = NullValueTransformer('a').transform(df)
>>> generic_array_equal(res, ans)
True
>>> ans = NP.array(
...         [[1, 'a', NP.nan], [2, 'a', 2], [-3, 'b', 3]],
...         dtype=NP.object
...         )
>>> res = NullValueTransformer([None, None, -1]).transform(df)
>>> generic_array_equal(res, ans)
True
>>> ans = NP.array(
...         [[1, 'a', -1], [NP.nan, 'a', 2], [-3, 'b', 3]],
...         dtype=NP.object
...         )
>>> res = NullValueTransformer({'A': 2}).transform(df)
>>> generic_array_equal(res, ans)
True
>>> NullValueTransformer(lambda x: x < 0).transform(df)
Traceback (most recent call last):
    ...
TypeError: unorderable types: str() < int()
>>> ans = NP.array(
...         [[1, 'a', NP.nan], [2, 'a', 2], [NP.nan, 'b', 3]],
...         dtype=NP.object
...         )
>>> res = NullValueTransformer(lambda x: x < 0, only='numeric').transform(df)
>>> generic_array_equal(res, ans)
True
>>> ans = NP.array(
...         [[1, 'a', -1], [2, 'a', 2], [NP.nan, 'b', 3]],
...         dtype=NP.object
...         )
>>> res = NullValueTransformer({'A': lambda x: x < 0}).transform(df)
>>> generic_array_equal(res, ans)
True
>>> df = PD.DataFrame(
...         [[NP.nan, 2, 1], [1, NP.nan, 2]],
...         columns=['A', 'B', 'C']
...         )
>>> from dataprep.transformer import NullIndicatorTransformer
>>> ans = NP.array([[NP.nan, 2, 1, 1, 0], [1, NP.nan, 2, 0, 1]])
>>> res = NullIndicatorTransformer().transform(df)
>>> generic_array_equal(res, ans)
True
>>> ans = NP.array([[NP.nan, 2, 1, 1], [1, NP.nan, 2, 0]])
>>> res = NullIndicatorTransformer(['A']).transform(df)
>>> generic_array_equal(res, ans)
True
>>> ans = NP.array([[NP.nan, 2, 1, 0], [1, NP.nan, 2, 1]])
>>> res = NullIndicatorTransformer([1, 2]).transform(df)
>>> generic_array_equal(res, ans)
True
>>> df = PD.DataFrame(
...         [[1, 'a', -1], [2, 'a', 2], [-3, 'b', 3]],
...         columns=['A', 'B', 'C']
...         )
>>> from dataprep.transformer import ColumnNormalizer
>>> norm = ColumnNormalizer('zeropos')
>>> norm.fit(df) # doctest: +ELLIPSIS
<dataprep.transformer.normalizer.ColumnNormalizer ...>
>>> ans = NP.array(
...         [[0.8, 'a', 0], [1, 'a', 0.75], [0, 'b', 1]],
...         dtype=NP.object
...         )
>>> arr = norm.transform(df)
>>> generic_array_equal(arr, ans)
True
>>> df2 = PD.DataFrame(arr, columns=['A', 'B', 'C'])
>>> arr2 = norm.inverse_transform(df2)
>>> generic_array_equal(arr2, df.values)
True
>>> norm2 = ColumnNormalizer({'A': 'zeropos'})
>>> norm2.fit(df) # doctest: +ELLIPSIS
<dataprep.transformer.normalizer.ColumnNormalizer ...>
>>> arr = norm2.transform(df)
>>> ans = NP.array(
...         [[0.8, 'a', -1], [1, 'a', 2], [0, 'b', 3]],
...         dtype=NP.object
...         )
>>> generic_array_equal(ans, arr)
True
>>> df = PD.DataFrame(
...         [[1, 'a', NP.nan], [2, 'a', 2], [NP.nan, 'b', 3]],
...         columns=['A', 'B', 'C']
...         )
>>> from dataprep.transformer import NumericImputationTransformer
>>> from dataprep.transformer import DummyTransformer
>>> from dataprep.transformer import PipelineTransformer
>>> imputer = NumericImputationTransformer('mean')
>>> dummy = DummyTransformer()
>>> ans = NP.array([[1, 2.5, 1, 0], [2, 2, 1, 0], [1.5, 3, 0, 1]])
>>> res = PipelineTransformer(imputer, dummy).transform(df)
>>> generic_array_equal(res, ans)
True
>>> df = PD.DataFrame(
...         [[1, 'a', '?'], [2, 'a', 2], ['?', 'b', 3]],
...         columns=['A', 'B', 'C']
...         )
>>> from dataprep.transformer import TabularSchemaGuesser
>>> ans = NP.array(
...         [[1, 'a', NP.nan], [2, 'a', 2], [NP.nan, 'b', 3]],
...         dtype=NP.object
...         )
>>> res = TabularSchemaGuesser().transform(df)
>>> generic_array_equal(res, ans)
True
'''
