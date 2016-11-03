
from .base import *

from enum import Enum
import numpy as NP


class TabularColumnType(Enum):
    '''
    A set of types for a column in a tabular dataset.

    Possible values
    ---------------
    drop
        Ignore the column altogether.  The column is not considered in the
        training set.
    categorical
        A column containing categorical values.  The values in the column
        are automatically encoded into a one-hot vector.
        Note that novel categories are treated as zero vectors.
    numeric
        A column containing (real-valued) numeric values.  Non-numeric
        values in this field are treated as NaN.
    ordered_categorical
        A column containing categorical values with an order relationship.
        The order must be specified by user.
        Currently, real values are converted to categories by rounding to
        the closest possible integer, while categories are always converted
        to integers 0..n-1, where n is the number of categories.
        Novel categories are not allowed in this case.
    explicit_categorical
        Like "categorical", but with novel categories as a separate "unknown"
        class.  So an N-valued categorical field is always encoded into a
        one-hot vector with N+1 dimensions.  Common for language modeling
        with fixed vocabulary etc.

    See also
    --------
        TabularLoader class
    '''
    drop = 0
    categorical = 1
    numeric = 2
    ordered_categorical = 3
    explicit_categorical = 4


class TabularColumnMetadata(Metadata):
    '''
    The (concrete) class representing metadata of a column in a tabular
    dataset.  It is the base element of a TabularMetadata instance.
    '''
    def __init__(self, t, a):
        '''
        t : TabularColumnType
        a : numpy.ndarray (1D), or pandas.Series
        '''
        self.type_ = t

    def is_categorical(self):
        '''
        Test whether a column contains categorical features, including
        "ordered categorical" and "explicit categorical".

        When a metadata contains information for categorical features,
        one can check the following member variables for further details:
            num_categories : int
                Number of (known) categories
            encoding : dict of (object, int) or (object, numpy.ndarray)
                Mapping between each category and its internal
                representation.  Note that in case of "explicit categorical"
                features, unknown categories have the key 'None'.

        Returns
        -------
        categorical : bool
        '''
        return self.type_ in [
                TabularColumnType.categorical,
                TabularColumnType.ordered_categorical,
                TabularColumnType.explicit_categorical,
                ]


class TabularCategoricalColumnMetadata(TabularColumnMetadata):
    '''
    Subclass for representing the metadata of a categorical feature.
    '''
    def __init__(self, t, a):
        super().__init__(t, a)
        assert self.type_ == TabularColumnType.categorical

        #: Number of categories
        self.num_categories = NP.unique(a).shape[0]
        #: dict : mapping between categories and internal representations
        self.encoding = dict(zip(a, NP.eye(self.num_categories)))


class TabularNumericColumnMetadata(TabularColumnMetadata):
    '''
    Subclass for representing the metadata of a numeric feature.
    '''
    def __init__(self, t, a):
        super().__init__(t, a)
        assert self.type_ == TabularColumnType.numeric


class TabularOrderedCategoricalColumnMetadata(TabularColumnMetadata):
    '''
    Subclass for representing the metadata of an ordered-categorical feature.
    '''
    def __init__(self, t, a, order):
        super().__init__(t, a)
        assert self.type_ == TabularColumnType.ordered_categorical

        #: Number of categories
        self.num_categories = NP.unique(a).shape[0]
        #: dict : mapping between categories and internal representations
        self.encoding = dict(zip(a, NP.arange(self.num_categories)))


class TabularExplicitCategoricalColumnMetadata(TabularColumnMetadata):
    '''
    Subclass for representing the metadata of a categorical feature with
    "unknown" as an explicit category.
    '''
    def __init__(self, t, a):
        super().__init__(t, a)
        assert self.type_ == TabularColumnType.explicit_categorical

        #: Number of categories
        self.num_categories = NP.unique(a).shape[0] # excluding unknown

        a = NP.concatenate([a, [None]])
        #: dict : mapping between categories and internal representations
        self.encoding = dict(zip(a, NP.eye(self.num_categories + 1)))


class TabularMetadata(Metadata):
    '''
    The class for representing metadata of a tabular dataset.  It is
    basically a (read-only) list of TabularColumnMetadata's.
    '''
    # TODO
    pass


class TabularLoader(Loader):
    '''
    Abstract base class for loading tabular data from a file.
    '''
    def __init__(self):
        self._schema = None
        self._target = -1

    @property
    def schema(self):
        '''
        list, tuple, or dict
            A table schema is a mapping from column to column type (with type
            TabularColumnType).
            If s is a list, a tuple, or any object derived from list or tuple,
            the elements should be the corresponding column type in that
            order.
            If s is a dict or any object derived from dict, the elements
            should be a key-value pair of column name and column type.
            The column names should be inferable from the data file, or
            the program will throw an error upon loading the file.

        See also
        --------
            TabularColumnType
        '''
        if self._schema is None:
            self._schema = self._guess_schema()
        return self._schema

    @schema.setter
    def schema(self, s):
        if (isinstance(s, list) or
                isinstance(s, tuple) or
                isinstance(s, dict)):
            self._schema = s
        else:
            raise ValueError("schema should be a list, a tuple, or a dict.")

    @property
    def target(self):
        '''
        int, or any iterable
            Specifies one or more columns as target variables.
        '''
        return self._target

    @target.setter
    def target(self, t):
        # TODO: type checks
        self._target = t

    def _guess_schema(self):
        '''
        Internal function of guessing the schema for a tabular dataset.
        '''
        # We don't want to guess the schema after setting it, do we?
        assert self._schema is None

        if self._dataset is None:
            raise AttributeError("schema not set and dataset not loaded")
        raise NotImplementedError("schema guessing is NYI")
