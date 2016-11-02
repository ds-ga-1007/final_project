
from abc import ABCMeta, abstractmethod


class Metadata(object, metaclass=ABCMeta):
    '''
    Abstract base class for representing metadata of a dataset.

    This class (and all subclasses) should be read-only.
    '''
    pass


class Loader(object, metaclass=ABCMeta):
    '''
    Abstract base class for loading a file and converting the data into
    desired representation.
    '''
    def __init__(self, metadata=None):
        self._dataset = None
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

    @abstractmethod
    def _load_metadata(self):
        '''
        Internal function for figuring out the metadata automatically.

        The subclasses provide the implementation of this method.

        (Must never be called from outside)
        '''
        return None

    @property
    def metadata(self):
        '''
        read-only
            The metadata of this dataset.

        See also
        --------
            load, load_test : method
            Metadata        : class
        '''
        if self._metadata is None:
            self._metadata = self._load_metadata()
        return self._metadata
