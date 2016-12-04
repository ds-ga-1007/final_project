import copy
import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork import *
from Model.FeedForwardNetwork.NetworkLayers import *

DELTA = 1e-7

def computationally_approximate_gradient(NN_frozen, l_idx, r_idx, c_idx,
                                         weight, X0, Y0):
    NN_plus = copy.deepcopy(NN_frozen)
    NN_minus = copy.deepcopy(NN_frozen)

    fullyconnectedplus = NN_plus.network.layers[l_idx].FullyConnectedLayer
    fullyconnectedminus = NN_minus.network.layers[l_idx].FullyConnectedLayer

    weights_plus = fullyconnectedplus.weights
    weights_minus = fullyconnectedminus.weights

    weights_plus[r_idx, c_idx] = weight + DELTA
    weights_minus[r_idx, c_idx] = weight - DELTA

    y_plus = NN_plus.network.predict(X0)
    y_minus = NN_minus.network.predict(X0)

    f_plus = (y_plus - Y0) ** 2
    f_minus = (y_minus - Y0) ** 2

    return (f_plus - f_minus) / (2 * DELTA)



def calculate_correct_output(NN, X):
    """calcualtes the correct output for network NN receiving input X"""

    activation_values = X

    for l_idx in range(NN.neuralnetworklearner.num_layers-1):
        activation_values = np.array(vect_with_bias(activation_values))
        active_layer = NN.neuralnetworklearner.network.layers[l_idx]
        active_weights = active_layer.FullyConnectedLayer.weights
        edge_output =  np.matmul(activation_values, active_weights)
        fwd_fcn = NN.neuralnetworklearner.network.trans_fcns[l_idx].forward_fcn
        activation_values = fwd_fcn(edge_output)
    return activation_values





class TestPropagation(unittest.TestCase):

    def test_backprop_gradient(self):
        """"""
        np.random.seed(1)
        NN = FeedForwardNetworkUI([2, 10, 1], learn_alg=utils.GRADIENT_DESCENT, reg_const=0,
                                  trans_fcns=["tanh", "purelin"])
        X = np.array([[0, 0],
                      [0, 1],
                      [1, 0],
                      [1, 1]])
        Y = np.array([np.array([x[0] + x[1]]) for x in X])
        NN.train(X, Y, epochs=10000)
        NN_frozen = copy.deepcopy(NN)

        X0 = X[-1]
        Y0 = Y[-1]

        NN.train(np.array([X0]), np.array(Y0), epochs=1)
        df_dx = NN.neuralnetworklearner.weight_deltas
        NN = copy.deepcopy(NN_frozen)
        for l_idx, layer in enumerate(NN.network.layers):
            fullyconnectedlayer = layer.FullyConnectedLayer
            weights = fullyconnectedlayer.weights
            for r_idx, row in enumerate(weights):
                for c_idx, weight in enumerate(row):

                    derivitive = computationally_approximate_gradient(
                        NN_frozen, l_idx, r_idx, c_idx, weight, X0, Y0)

                    self.assertLess(np.abs(derivitive - df_dx[l_idx][r_idx][c_idx]), 1e-2)

    def test_feed_forward(self):
        """test accurate forward propogation of the network containing
        sigmoid, tanh, and purelin transfer functions"""
        np.random.seed(1)
        NN1 = FeedForwardNetworkUI([2, 5, 1])
        NN2 = FeedForwardNetworkUI([2, 4, 3, 1], trans_fcns=["sigmoid", "tanh", "purelin"])
        for X in [np.ones(2),np.array([0, -.5])]:
            for NN in [NN1, NN2]:
                correct_output = calculate_correct_output(NN, X)
                NN.neuralnetworklearner.network._feed_forward(X)
                network_output = NN.neuralnetworklearner.layers[-1].act_vals
                self.assertLess(np.abs(correct_output-network_output), 1e-2)