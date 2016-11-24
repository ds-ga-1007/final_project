
import numpy as np
from Model import utils
from Model.Network.Network import Network
from Model.Network.NeuralNetworkLearner import NeuralNetworkLearner

class AutoEncoder(object):
    '''
    This is the User Inferface for a user to create a neural network.
    A user can create the network, and then train the network for
    a specified number of epochs on a set of input output (X, Y) pairs.
    During training, the NeuralNetworkLearner updates the Network
    in accordance with its learning algorithm.
    A user can also predict the output of a list of inputs based on the current network

    Visualization description?
    '''

    def __init__(self, X, hidden_dim = 2):
        #MAKE THIS LOOK LIKE A PRIVATE VAREIABLE
        self.hidden_dim = hidden_dim
        self.X = X
        self.network = Network(layer_sizes = [X.shape[1], 100, hidden_dim, 100, X.shape[1]],
                               trans_fcns="tanh", reg_const=1e-1)
        self.neuralnetworklearner = \
            NeuralNetworkLearner(network = self.network, learning_rate=1e-5)

    def train(self, epochs = 10):
        self.neuralnetworklearner.run_epochs(self.X, self.X, epochs)

    def get_encoding_vals(self):
        hidden_repr = np.zeros([self.X.shape[0], self._hidden_dim])
        for x_idx, xi in enumerate(self.X):
            self.network.feed_forward(xi)
            hidden_repr[x_idx] = self.network.layers[1].act_vals
        return hidden_repr

    def predict(self):
        return np.array([self.network.predict(xi) for xi in self.X])

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
        self._hidden_dim = hidden_dim
