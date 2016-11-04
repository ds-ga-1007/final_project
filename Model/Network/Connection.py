import numpy as np

class connection():

    def __init__(self, num_in, num_out):
        self._num_in = num_in
        self._num_out = num_out
        self._init_weights(std = 0.1)

    def _get_num_in(self):
        return self._num_in

    def _get_num_out(self):
        return self._num_out

    def _init_weights(self, std):
        self._weights = np.random.randn(self._get_num_in() + 1,
                                        self._get_num_out()) * std

