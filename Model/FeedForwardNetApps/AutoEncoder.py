import numpy as np

from Model.FeedForwardNetwork.Network import Network
from Model.FeedForwardNetwork.NeuralNetworkLearner import NeuralNetworkLearner


class AutoEncoder(object):
    '''
    AutoEncoder class for using a Network to autoencode data

    AutoEncoders should utilize Networks to reduce the dimenisonality of data
    By reconstructing a dataset utilizing a narrow

    Parameters
    ----------
    X : numpy.ndarray instance
        2D array of data to be autoencoded
    hidden_dim : int
        Dimensionality of latent representation
    '''

    def __init__(self, X, hidden_dim=2):
        '''
        Create an autoencoder for a high dimensional dataset
        represented as a 2d matrix
        :param X: 2D numpy.ndarray of the data to be autoencoded
        :param hidden_dim: int of the most narrow hidden layer within the autoencoder
        '''
        self.hidden_dim = hidden_dim
        self.X = X
        width = X.shape[1]

        layer_sizes = [width,(width + hidden_dim) // 2, hidden_dim,
                       (width + hidden_dim) // 2, width]

        network = Network(layer_sizes = layer_sizes,
                          trans_fcns="tanh", reg_const=1e-1)

        self.neuralnetworklearner = \
            NeuralNetworkLearner(network = network, learning_rate=1e-5)

    def train(self, epochs = 10):
        '''
        Train the network

        :param epochs: integer number of epochs
        :return: None
        '''
        self.neuralnetworklearner.run_epochs(self.X, self.X, epochs)

    def get_encoding_vals(self):
        '''
        Get the embedded trained representation of the data
        :return: 2D numpy.ndarray of size hidden_dim by number of samples
        '''
        hidden_repr = np.zeros([self.X.shape[0], self._hidden_dim])
        for x_idx, xi in enumerate(self.X):
            self.neuralnetworklearner.network._feed_forward(xi)
            hidden_repr[x_idx] = self.neuralnetworklearner.network.layers[1].act_vals
        return hidden_repr

    def predict(self):
        '''
        Get the reconstructed representation of the data
        :return: 2D numpy.ndarray of the same shape as X
        '''
        return np.array([self.neuralnetworklearner.network.predict(xi) for xi in self.X])

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    @property
    def neuralnetworklearner(self):
        return self._neuralnetworklearner

    @neuralnetworklearner.setter
    def neuralnetworklearner(self, neuralnetworklearner):
        self._neuralnetworklearner = neuralnetworklearner

    @property
    def hidden_dim(self):
        return self._hidden_dim

    @hidden_dim.setter
    def hidden_dim(self, hidden_dim):
        if hidden_dim < 1:
            raise ValueError("auto encoder hidden dimension must be positive")
        self._hidden_dim = hidden_dim

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, X):
        if not isinstance(X, np.ndarray):
            raise ValueError("auto encoder data must be a numpy array")
        self._X = X