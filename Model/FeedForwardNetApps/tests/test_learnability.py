
import matplotlib.pyplot as plt
import numpy as np
import six
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D

from Model.FeedForwardNetApps.AutoEncoder import AutoEncoder
from Model.FeedForwardNetwork import utils

import copy
import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork import *
from Model.FeedForwardNetwork.NetworkLayers import *

#The following are test cases to ensure correct functionality of intervals

def test_xor(verb=0):
    NN = FeedForwardNetworkUI([2, 100, 100, 1],
                              reg_const=1e-4)
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])
    Y = np.array([np.array([x[0] ^ x[1]]) for x in X])
    for _ in range(10):
        NN.train(X, Y, epochs=500)
        if verb > 0:
            y_predict = NN.predict(X)
            print(y_predict)
    y_predict = NN.predict(X)
    return np.mean(np.square(y_predict - Y))


def test_addition(verb=0):
    NN = FeedForwardNetworkUI([2, 100, 1],
                              trans_fcns=["sigmoid", "purelin"],
                              learn_alg=utils.GRADIENT_DESCENT)
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])
    Y = np.array([np.array([x[0] + x[1]]) for x in X])
    if verb > -1:
        pass
    for _ in range(10):
        NN.train(X, Y, epochs=100)
        if verb > 0:
            y_predict = NN.predict(X)
            print(y_predict)
    y_predict = NN.predict(X)
    return np.mean(np.square(y_predict - Y))


def test_sine(verb=0):
    NN = FeedForwardNetworkUI([1, 200, 1],
                              trans_fcns="tanh", reg_const=1e-5)
    X = np.linspace(0, 2 * np.pi, num=5)
    Y = np.array([np.sin(x) for x in X])
    if np.ndim(X) == 1:
        X = np.atleast_2d(X).T
        Y = np.atleast_2d(Y).T
    for _ in range(10):
        NN.train(X, Y, epochs=100)
        if verb > 0:
            y_predict = NN.predict(X)
            print(y_predict)
    y_predict = NN.predict(X)
    return np.mean(np.square(y_predict - Y))





    '''
    if verb > 0:
        y_predict = NN.predict(X)
        print(y_predict)
    y_predict = NN.predict(X)
    print(y_predict)
    return np.mean(np.square(y_predict - Y))
    '''
delta = 1e-3
NN = FeedForwardNetworkUI([2, 3, 1], learn_alg=utils.GRADIENT_DESCENT,
                          trans_fcns=["tanh", "purelin"])
X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])
Y = np.array([np.array([x[0] + x[1]]) for x in X])
NN.train(X, Y, epochs=100)
NN_frozen = copy.deepcopy(NN)




class TestLearnability():
    """
    Tests for functions relating to the interval class
    These should be run by enterring the command
    "python -m unittest discover"
    from the root directory of this project
    """

    def test_gradient_simple(self):
        np.random.seed(1)
        delta = 1e-7
        NN = FeedForwardNetworkUI([2, 1], learn_alg=utils.GRADIENT_DESCENT, reg_const = 0,
                                  trans_fcns=["purelin"])
        X = np.array([[0, 0],
                      [0, 1],
                      [1, 0],
                      [1, 1]])
        Y = np.array([np.array([x[0] + x[1]]) for x in X])
        NN.train(X, Y, epochs=1000)
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
                    NN_plus = copy.deepcopy(NN_frozen)
                    NN_minus = copy.deepcopy(NN_frozen)

                    fullyconnectedplus = NN_plus.network.layers[l_idx].FullyConnectedLayer
                    fullyconnectedminus = NN_minus.network.layers[l_idx].FullyConnectedLayer

                    weights_plus = fullyconnectedplus.weights
                    weights_minus = fullyconnectedminus.weights

                    weights_plus[r_idx, c_idx] = weight + delta
                    weights_minus[r_idx, c_idx] = weight - delta

                    y_plus = NN_plus.network.predict(X0)
                    y_minus = NN_minus.network.predict(X0)

                    f_plus = (y_plus - Y0) ** 2
                    f_minus = (y_minus - Y0) ** 2

                    derivitive = (f_plus - f_minus) / (2 * delta)
                    self.assertLess(np.abs(derivitive - df_dx[l_idx][r_idx][c_idx]), 1e-2)

    def test_gradient(self):
        np.random.seed(1)
        delta = 1e-7
        NN = FeedForwardNetworkUI([2, 5, 1], learn_alg=utils.GRADIENT_DESCENT, reg_const = 0,
                                  trans_fcns=["tanh", "purelin"])
        X = np.array([[0, 0],
                      [0, 1],
                      [1, 0],
                      [1, 1]])
        Y = np.array([np.array([x[0] + x[1]]) for x in X])
        NN.train(X, Y, epochs=1000)
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
                    NN_plus = copy.deepcopy(NN_frozen)
                    NN_minus = copy.deepcopy(NN_frozen)

                    fullyconnectedplus = NN_plus.network.layers[l_idx].FullyConnectedLayer
                    fullyconnectedminus = NN_minus.network.layers[l_idx].FullyConnectedLayer

                    weights_plus = fullyconnectedplus.weights
                    weights_minus = fullyconnectedminus.weights

                    weights_plus[r_idx, c_idx] = weight + delta
                    weights_minus[r_idx, c_idx] = weight - delta

                    y_plus = NN_plus.network.predict(X0)
                    y_minus = NN_minus.network.predict(X0)

                    f_plus = (y_plus - Y0) ** 2
                    f_minus = (y_minus - Y0) ** 2

                    derivitive = (f_plus - f_minus) / (2 * delta)

                    self.assertLess(np.abs(derivitive - df_dx[l_idx][r_idx][c_idx]), 1e-3)

    def test_learn_xor(self):
        '''
        System Level test verifying the networks
        ability to learn the xor function.
        '''
        np.random.seed(1)
        xor_err = test_xor()
        self.assertLess(xor_err, 1e-3)

    def test_learn_add(self):
        '''
        System Level test verifying the networks
        ability to learn the addition function.
        Core system level function test with
        the gradient descent backpropagation algorithm
        '''
        np.random.seed(1)
        add_error = test_addition()
        self.assertLess(add_error, 1e-3)

    def test_learn_sine(self):
        '''
        System Level test verifying the networks
        ability to learn the sine function.
        '''
        np.random.seed(1)
        sine_error = test_sine()
        self.assertLess(sine_error, 1e-3)


