import numpy as np
from Model.utils import vect_with_bias

class FullyConnectedLayer():

    def __init__(self, num_in, num_out):
        self.num_in = num_in
        self.num_out = num_out
        self._init_weights(std = 0.01)

    def _init_weights(self, std):
        self._weights = np.random.randn(self.num_in + 1, self.num_out) * std

    def propogate_forward(self, X):
        return np.matmul(vect_with_bias(X), self.weights)

    def get_weights_except_bias(self):
        return self.weights[:-1]

    @property
    def weights(self):
        return self._weights

    @property
    def num_in(self):
        return self._num_in

    @num_in.setter
    def num_in(self, num_in):
        self._num_in = num_in

    @property
    def num_out(self):
        return self._num_out

    @num_out.setter
    def num_out(self, num_out):
        self._num_out = num_out
