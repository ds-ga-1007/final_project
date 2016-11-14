
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

    def __init__(self, X):
        #MAKE THIS LOOK LIKE A PRIVATE VAREIABLE
        self.network = Network(layer_sizes = [X.shape[1], 100, 2, 100, X.shape[1]],
                               trans_fcns="tanh", reg_const=1e-5)
        self.neuralnetworklearner = \
            NeuralNetworkLearner(network = self.network)
        self.train(X, 1)

    def train(self, X, epochs = 10):
        self.neuralnetworklearner.run_epochs(X, X, epochs)

    def get_encoding_vals(self, X):
        hidden_repr = np.zeros([X.shape[0], 2])
        for x_idx, xi in enumerate(X):
            self.network.feed_forward(xi)
            hidden_repr[x_idx] = self.network.layers[1].act_vals
        return hidden_repr

    def predict(self, X):
        return np.array([self.network.predict(xi) for xi in X])

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
