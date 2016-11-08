
from abc import ABCMeta, abstractmethod


class Metadata(object, metaclass=ABCMeta):
    '''
    Abstract base class for representing metadata of a dataset.

    This class (and all subclasses) should be read-only.  One should
    *never* change any content inside once the instances are created.
    '''
    pass


class Loader(object, metaclass=ABCMeta):
    '''
    Abstract base class for loading a file and converting the data into
    desired representation.
    '''
    def __init__(self):
        self._dataset = None

    @abstractmethod
    def load(self, filename, metadata=None):
        '''
        Load the dataset from file name provided.

        Returns
        -------
        X, Y, m : numpy.ndarray, numpy.ndarray, Metadata instance
            X contains the encoded training set, and Y contains the training
            target variables.  m is a Metadata instance useful for reading
            the test set (see Examples section)

        Examples
        --------

        Loading training dataset and testing dataset from separate CSV files.
        >>> csvloader = CSVLoader()
        >>> csvloader.schema = [
                TabularColumnType.categorical,
                TabularColumnType.numeric,
                TabularColumnType.numeric,
                ]
        >>> trainX, trainY, metadata = csvloader.load('train.csv')
        >>> testX, testY = csvloader.load_test('test.csv', metadata)

        See also
        --------
            load_test : method
        '''
        return None

    @abstractmethod
    def load_test(self, filename, metadata):
        '''
        Load the dataset from file name, with the given metadata.

        Returns
        -------
        X, Y : numpy.ndarray
            X contains the encoded training set, and Y contains the training
            target variables.

        See also
        --------
            load     : method
        '''
        return None
