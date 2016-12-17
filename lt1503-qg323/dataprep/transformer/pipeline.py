
from .base import Transformer, LearnableTransformer


class PipelineTransformer(Transformer):
    '''
    A transformer which applies transformations in a pipeline (i.e. one by
    one)

    Parameters
    ----------
    *transformers : list of Transformer instances
        Transformations will take place in the given order.

    Examples
    --------
    The following example first imputes numeric null values by column
    means, then encodes categorical values into indicator variables.
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
    >>> from dataprep.transformer import DummyTransformer
    >>> from dataprep.transformer import PipelineTransformer
    >>> imputer = NumericImputationTransformer('mean')
    >>> dummy = DummyTransformer()
    >>> PipelineTransformer(imputer, dummy).transform(df)
    array([[ 1. ,  2.5,  1. ,  0. ],
           [ 2. ,  2. ,  1. ,  0. ],
           [ 1.5,  3. ,  0. ,  1. ]])
    '''
    def __init__(self, *transformers):
        self._transformers = transformers

    def _transform(self, dataset):
        for i, t in enumerate(self._transformers):
            try:
                if isinstance(t, LearnableTransformer):
                    t._fit(dataset)
                dataset = t._transform(dataset)
            except (TypeError, ValueError, IndexError) as e:
                # Add the transformer index for the exception and re-raise it
                msg = 'Error in transformer %d: %s' % (i, str(e))
                raise type(e)(msg, i)
            except KeyError as e:
                # As above but with a better message
                msg = 'Error in transformer %d: %s does not exist' % (i, str(e))
                raise type(e)(msg, i)
        return dataset
