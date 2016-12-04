from Model.FeedForwardNetwork import utils
from Model.FeedForwardNetwork.Network import Network
from Model.FeedForwardNetwork.NeuralNetworkLearner import NeuralNetworkLearner

class FeedForwardNetworkUI(object):
    '''
    This is the User Inferface for a user to create a neural network.
    A user can create the network, and then train the network for
    a specified number of epochs on a set of input output (X, Y) pairs.
    During training, the NeuralNetworkLearner updates the FeedForwardNetwork
    in accordance with its learning algorithm.
    A user can also predict the output of a list of inputs based on the current network
    '''

    def __init__(self, layers, trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-3,
                 learn_alg=utils.MOMENTUM_BP, learning_rate=1e-3):

        network = Network(layers, trans_fcns, loss_fcn, reg_const)
        self.neuralnetworklearner = \
            NeuralNetworkLearner(network=network,
                                 learning_rate=learning_rate, learn_alg=learn_alg)

    def train(self, X, Y, epochs=10):
        self.neuralnetworklearner.run_epochs(X, Y, epochs)

    def predict(self, X):
        return [self.network.predict(xi) for xi in X]

    @property
    def network(self):
        return self.neuralnetworklearner.network

    @network.setter
    def network(self, network):
        self.neuralnetworklearner.network = network

    @property
    def neuralnetworklearner(self):
        return self._neuralnetworklearner

    @neuralnetworklearner.setter
    def neuralnetworklearner(self, neuralnetworklearner):
        self._neuralnetworklearner = neuralnetworklearner
