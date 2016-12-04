import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork import *
from Model.FeedForwardNetwork.NetworkLayers import *

class TestLearner(unittest.TestCase):

    def test_network_learner_constructor(self):

        network = Network([1, 2, 1])
        self.neuralnetworklearner = \
            NeuralNetworkLearner(network = network, learning_rate = 1, learn_alg = utils.GRADIENT_DESCENT)
        self.neuralnetworklearner = \
            NeuralNetworkLearner(network = network, learning_rate = 1, learn_alg = utils.MOMENTUM_BP)
        self.neuralnetworklearner = \
            NeuralNetworkLearner(network = network)

    def test_network_learner_errors(self):

        with self.assertRaises(TypeError):
            network = Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-3)
            learner = NeuralNetworkLearner(network)
            learner.loss_fcn = 2
        with self.assertRaises(TypeError):
            network = Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-3)
            learner = NeuralNetworkLearner(network)
            learner.loss_fcn = []

        with self.assertRaises(ValueError):
            NeuralNetworkLearner(network, learning_rate=-1)
        with self.assertRaises(ValueError):
            NeuralNetworkLearner(network, learning_rate=0)
        with self.assertRaises(TypeError):
            NeuralNetworkLearner(network, learning_rate='a')
        with self.assertRaises(TypeError):
            NeuralNetworkLearner(network, learning_rate=[])

        with self.assertRaises(ValueError):
            learner = NeuralNetworkLearner(network)
            learner.learning_rate = 0

        with self.assertRaises(TypeError):
            NeuralNetworkLearner()
