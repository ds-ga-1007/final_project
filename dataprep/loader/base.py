
from abc import *


class Loader(metaclass=ABCMeta):
    '''
    Abstract base class for loading a file and converting the data into
    desired representation.
    '''
    def __init__(self, metadata=None):
        self._dataframe = None
        self._metadata = metadata

    @abstractmethod
    def load(self, filename):
        '''
        Load the dataset from file name provided.

        Changes the metadata of the loader to match the underlying dataset.

        Returns
        -------
        X, Y : numpy.ndarray
            X contains the encoded training set, and Y contains the training
            target variables.

        Examples
        --------

        Loading training dataset and testing dataset from separate CSV files.
        >>> csvloader = CSVLoader()
        >>> csvloader.schema = [
                TabularColumnType.categorical,
                TabularColumnType.numeric,
                TabularColumnType.numeric,
                ]
        >>> trainX, trainY = csvloader.load('train.csv')
        >>> testX, testY = csvloader.load_test('test.csv')

        See also
        --------
            metadata  : property
            load_test : method
        '''
        return None

    @abstractmethod
    def load_test(self, filename):
        '''
        Load the dataset from file name, with the same metadata.

        Returns
        -------
        X, Y : numpy.ndarray
            X contains the encoded training set, and Y contains the training
            target variables.

        See also
        --------
            metadata : property
            load     : method
        '''
        return None

    @abstractproperty
    def metadata(self):
        '''
        read-only
            The metadata of this dataset, including but not limited to
                * Schema
                * Record count
                * For categorical fields, the set of possible categories and
                  their encodings.

        See also
        --------
            load, load_test : method
        '''
        return None
