
from .base import Loader
import h5py
import pandas as PD


class HDFArrayFlattenLoader(Loader):
    '''
    Load a dataset from an HDF file stored as numpy.ndarrays, flatten
    each record in the process.

    This class does not support specification of @target property;
    it requires a "key" property instead, for indicating the key
    of the dataset.

    Parameters
    ----------
    key : str
    '''

    def __init__(self, key=None):
        self._key = key
        self._target = None

    def _load_from_path(self, path):
        # Read the numpy.ndarray from the HDF
        f = h5py.File(path)
        dataset = f[self._key].value
        f.close()

        # Flatten each record
        num_samples = dataset.shape[0]
        flattened_dataset = dataset.reshape([num_samples, -1])

        # Convert it into a pandas.DataFrame
        return PD.DataFrame(flattened_dataset)
