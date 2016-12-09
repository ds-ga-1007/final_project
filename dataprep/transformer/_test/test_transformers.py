
from unittest import TestCase
import pandas as PD
import numpy as NP
from .util import generic_array_equal
from dataprep.transformer import *


class TestTransformer(TestCase):
    def test_dummy(self):
        df = PD.DataFrame({'A': ['A', 'B', NP.nan], 'B': ['a', NP.nan, 'c']})

        # ordinary
        ans = NP.array([[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
        res = DummyTransformer().transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        # dummy unknown
        ans = NP.array(
                [[1, 0, 0, 1, 0, 0],
                 [0, 1, 0, 0, 0, 1],
                 [0, 0, 1, 0, 1, 0]]
                )
        res = DummyTransformer(dummy_unknown=True).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

    def test_impute(self):
        df = PD.DataFrame(
                [[1, 'a', NP.nan], [2, 'a', 2], [NP.nan, 'b', 3]],
                columns=['A', 'B', 'C']
                )

        ans = NP.array(
                [[1.0, 'a', 2.5], [2.0, 'a', 2.0], [1.5, 'b', 3.0]],
                dtype=NP.object
                )
        res = NumericImputationTransformer('mean').transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        ans = NP.array(
                [[1.0, 'a', 5.0], [2.0, 'a', 2.0], [3.0, 'b', 3.0]],
                dtype=NP.object
                )
        res = NumericImputationTransformer(lambda s: NP.sum(s)).transform(df)
        self.assertTrue(generic_array_equal(ans, res))

        ans = NP.array(
                [[1.0, 'a', 5.0], [2.0, 'a', 2.0], [1.5, 'b', 3.0]],
                dtype=NP.object
                )
        res = NumericImputationTransformer(
               ['mean', None, lambda s: NP.sum(s)]
               ).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        ans = NP.array(
                [[1.0, 'a', NP.nan], [2.0, 'a', 2.0], [1.5, 'b', 3.0]],
                dtype=NP.object
                )
        res = NumericImputationTransformer({'A': 'mean'}).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

    def test_nullvalue(self):
        df = PD.DataFrame(
                [[1, 'a', -1], [2, 'a', 2], [-3, 'b', 3]],
                columns=['A', 'B', 'C']
                )

        ans = NP.array(
                [[1, 'a', -1], [NP.nan, 'a', NP.nan], [-3, 'b', 3]],
                dtype=NP.object
                )
        res = NullValueTransformer(2).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        ans = NP.array(
                [[1, NP.nan, -1], [2, NP.nan, 2], [-3, 'b', 3]],
                dtype=NP.object
                )
        res = NullValueTransformer('a').transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        ans = NP.array(
                [[1, 'a', NP.nan], [2, 'a', 2], [-3, 'b', 3]],
                dtype=NP.object
                )
        res = NullValueTransformer([None, None, -1]).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        ans = NP.array(
                [[1, 'a', -1], [NP.nan, 'a', 2], [-3, 'b', 3]],
                dtype=NP.object
                )
        res = NullValueTransformer({'A': 2}).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        with self.assertRaises(TypeError):
            NullValueTransformer(lambda x: x < 0).transform(df)

        ans = NP.array(
                [[1, 'a', NP.nan], [2, 'a', 2], [NP.nan, 'b', 3]],
                dtype=NP.object
                )
        res = NullValueTransformer(lambda x: x < 0, only='numeric').transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        ans = NP.array(
                [[1, 'a', -1], [2, 'a', 2], [NP.nan, 'b', 3]],
                dtype=NP.object
                )
        res = NullValueTransformer({'A': lambda x: x < 0}).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

    def test_nullindicate(self):
        df = PD.DataFrame(
                [[NP.nan, 2, 1], [1, NP.nan, 2]],
                columns=['A', 'B', 'C']
                )

        ans = NP.array([[NP.nan, 2, 1, 1, 0], [1, NP.nan, 2, 0, 1]])
        res = NullIndicatorTransformer().transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        ans = NP.array([[NP.nan, 2, 1, 1], [1, NP.nan, 2, 0]])
        res = NullIndicatorTransformer(['A']).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        ans = NP.array([[NP.nan, 2, 1, 0], [1, NP.nan, 2, 1]])
        res = NullIndicatorTransformer([1, 2]).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

    def test_column_norm(self):
        df = PD.DataFrame(
                [[1, 'a', -1], [2, 'a', 2], [-3, 'b', 3]],
                columns=['A', 'B', 'C']
                )

        norm = ColumnNormalizer('zeropos')
        norm.fit(df)
        ans = NP.array(
                [[0.8, 'a', 0], [1, 'a', 0.75], [0, 'b', 1]],
                dtype=NP.object
                )
        arr = norm.transform(df)
        self.assertTrue(generic_array_equal(arr, ans))
        df2 = PD.DataFrame(arr, columns=['A', 'B', 'C'])
        arr2 = norm.inverse_transform(df2)
        self.assertTrue(generic_array_equal(arr2, df.values))

        norm2 = ColumnNormalizer({'A': 'zeropos'})
        norm2.fit(df)
        arr = norm2.transform(df)
        ans = NP.array(
                [[0.8, 'a', -1], [1, 'a', 2], [0, 'b', 3]],
                dtype=NP.object
                )
        self.assertTrue(generic_array_equal(ans, arr))

    def test_pipeline(self):
        df = PD.DataFrame(
                [[1, 'a', NP.nan], [2, 'a', 2], [NP.nan, 'b', 3]],
                columns=['A', 'B', 'C']
                )

        imputer = NumericImputationTransformer('mean')
        dummy = DummyTransformer()
        ans = NP.array([[1, 2.5, 1, 0], [2, 2, 1, 0], [1.5, 3, 0, 1]])
        res = PipelineTransformer(imputer, dummy).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

    def test_schema_guess(self):
        df = PD.DataFrame(
                [[1, 'a', '?'], [2, 'a', 2], ['?', 'b', 3]],
                columns=['A', 'B', 'C']
                )
        ans = NP.array(
                [[1, 'a', NP.nan], [2, 'a', 2], [NP.nan, 'b', 3]],
                dtype=NP.object
                )
        res = TabularSchemaGuesser().transform(df)
        self.assertTrue(generic_array_equal(res, ans))

    def test_tabular(self):
        df = PD.DataFrame(
                [[1, 'a', '?'], [2, 'a', 2], ['?', 'b', 3]],
                columns=['A', 'B', 'C']
                )
        ans = NP.array([['a', '?'], ['a', 2], ['b', 3]], dtype=NP.object)
        res = DropColumnTransformer(['A']).transform(df)
        self.assertTrue(generic_array_equal(res, ans))
        res = DropColumnTransformer([0]).transform(df)
        self.assertTrue(generic_array_equal(res, ans))

        with self.assertRaises(TypeError):
            DropColumnTransformer([2.3])
        with self.assertRaises(IndexError):
            res = DropColumnTransformer([4]).transform(df)
        with self.assertRaises(ValueError):
            res = DropColumnTransformer(['D']).transform(df)
