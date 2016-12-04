import numpy as np

from Model.FeedForwardNetwork.Network import Network
from Model.FeedForwardNetwork.NeuralNetworkLearner import NeuralNetworkLearner


class AutoEncoder(object):
    '''
    AutoEncoder class for using a Network to autoencode data

    Parameters
    ----------
    X : Numpy 2d array of the data to be autoencoded
    hidden_dim : non
    '''
    '''
    This is the User Inferface for a user to create a neural network.
    A user can create the network, and then train the network for
    a specified number of epochs on a set of input output (X, Y) pairs.
    During training, the NeuralNetworkLearner updates the FeedForwardNetwork
    in accordance with its learning algorithm.
    A user can also predict the output of a list of inputs based on the current network
    Visualization description?
    '''

    def __init__(self, X, hidden_dim = 2):
        #MAKE THIS LOOK LIKE A PRIVATE VAREIABLE
        self.hidden_dim = hidden_dim
        self.X = X
        network = Network(layer_sizes = [X.shape[1], (X.shape[1] + hidden_dim) // 2,
                                         hidden_dim,
                                         (X.shape[1] + hidden_dim) // 2, X.shape[1]],
                               trans_fcns="tanh", reg_const=1e-1)
        self.neuralnetworklearner = \
            NeuralNetworkLearner(network = network, learning_rate=1e-5)

    def train(self, epochs = 10):
        self.neuralnetworklearner.run_epochs(self.X, self.X, epochs)

    def get_encoding_vals(self):
        hidden_repr = np.zeros([self.X.shape[0], self._hidden_dim])
        for x_idx, xi in enumerate(self.X):
            self.neuralnetworklearner.network.feed_forward(xi)
            hidden_repr[x_idx] = self.neuralnetworklearner.network.layers[1].act_vals
        return hidden_repr

    def predict(self):
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