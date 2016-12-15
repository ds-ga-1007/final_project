
import numpy as np
from Model.FeedForwardNetwork.NetworkLayers.Layer import Layer

class FullyConnectedLayer(Layer):
    '''
    A FullyConnectedLayer is a Layer that represents a matrix multiplication
    of its inputs by a matrix it maintains of edge weights into its output.
    '''

    def __init__(self, num_in, num_out):
        Layer.__init__(self, num_in, has_bias=True)
        self.num_out = num_out
        self._init_weights(std = 10)

    def _init_weights(self, std):
        self._weights = np.random.randn(self.num_in, self.num_out) * std/self.num_in

    def propogate_forward(self, X):
        return np.matmul(X, self.weights)

    def get_weights_except_bias(self):
        return self.weights[:-1]

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, weights):
        self._weights = weights

    @property
    def num_out(self):
        return self._num_out

    @num_out.setter
    def num_out(self, num_out):
        if num_out < 1:
            raise ValueError("Layers need positive number of outputs")
        self._num_out = num_out

    @property
    def has_bias(self):
        return self._has_bias

    @has_bias.setter
    def has_bias(self, has_bias):
        self._has_bias = has_bias
