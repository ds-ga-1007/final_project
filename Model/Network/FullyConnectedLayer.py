import numpy as np

class FullyConnectedLayer():

    def __init__(self, num_in, num_out):
        self.num_in = num_in
        self.num_out = num_out
        self._init_weights(std = 0.1)

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

    def _init_weights(self, std):
        self._weights = np.random.randn(self.num_in + 1, self.num_out) * std

    def propogate_forward(self, X):
        return np.matmul(X, self.weights)

