'''
dataprep : nn-uf data preparation module

The data preparation is separated into mainly two parts:
    1. `Loader`
        Extracts a pandas DataFrame from a given data source.
    2. `Transformer`
        Converts the pandas DataFrame to numpy.ndarray instances for
        training and testing.  Data preprocessing falls into this category
        as decorators of base `Transformer` instances.
'''

from .loader import *
