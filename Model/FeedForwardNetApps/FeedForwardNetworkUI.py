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
        '''
        User interface for Feed Forward Networks
        :param layers: list of integers representing the layer sizes of the network
        :param trans_fcns: string name of a transfer function or a list of transfer function named strings.
        :param loss_fcn: string name of a loss function
        :param reg_const: numeric regularization constant
        :param learn_alg: numeric representation of a learning algorithm
        :param learning_rate: numeric representation of learning rate.
        '''

        network = Network(layers, trans_fcns, loss_fcn, reg_const)
        self.neuralnetworklearner = \
            NeuralNetworkLearner(network=network,
                                 learning_rate=learning_rate, learn_alg=learn_alg)

    def train(self, X, Y, epochs=10):
        '''
        Train the network using the neuralnetworklearner
        :param X: 2D numpy.ndarray of predictor variables
        :param Y: 2D numpy.ndarray of output variables
        :param epochs: integer-like number of epochs to run
        :return: None
        '''
        self.neuralnetworklearner.run_epochs(X, Y, epochs)

    def predict(self, X):
        '''
        Predict output Y variable for each column of input values in X
        :param X: 2D numpy.ndarray of predictor variables
        :return: 2D array of output variables
        '''
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
