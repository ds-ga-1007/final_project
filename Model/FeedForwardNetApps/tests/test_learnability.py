
import matplotlib.pyplot as plt
import numpy as np
import six
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D

from Model.FeedForwardNetApps.AutoEncoder import AutoEncoder
from Model.FeedForwardNetwork import utils


import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork import *
from Model.FeedForwardNetwork.NetworkLayers import *

#The following are test cases to ensure correct functionality of intervals

def test_xor(verb=0):
    NN = FeedForwardNetworkUI([2, 100, 100, 1], reg_const=1e-4)
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
    print(y_predict)
    return np.mean(np.square(y_predict - Y))


def test_addition(verb=0):
    NN = FeedForwardNetworkUI([2, 100, 1], trans_fcns=["sigmoid", "purelin"],
                              learn_alg=utils.GRADIENT_DESCENT)
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])
    Y = np.array([np.array([x[0] + x[1]]) for x in X])
    print(Y.T)
    if verb > -1:
        pass
    for _ in range(10):
        NN.train(X, Y, epochs=100)
        if verb > 0:
            y_predict = NN.predict(X)
            print(y_predict)
    y_predict = NN.predict(X)
    print(y_predict)
    return np.mean(np.square(y_predict - Y))


def test_sine(verb=0):
    NN = FeedForwardNetworkUI([1, 200, 1], trans_fcns="tanh", reg_const=1e-5)
    X = np.linspace(0, 2 * np.pi, num=5)
    Y = np.array([np.sin(x) for x in X])
    if np.ndim(X) == 1:
        X = np.atleast_2d(X).T
        Y = np.atleast_2d(Y).T
    print(Y.T)
    for _ in range(10):
        NN.train(X, Y, epochs=100)
        if verb > 0:
            y_predict = NN.predict(X)
            print(y_predict)
    y_predict = NN.predict(X)
    print(y_predict)
    return np.mean(np.square(y_predict - Y))



class TestLearnability(unittest.TestCase):
    """unit tests for functions relating to the interval class
    These should be run by enterring the command "python -m unittest discover"
    from the root directory of this project
    """


    def test_learnability(self):

        xor_err = test_xor()
        print('xor error = ', xor_err)
        self.assertLess(xor_err, 1e-3)

        np.random.seed(1)
        add_error = test_addition()
        print('add error = ', add_error)
        self.assertLess(add_error, 1e-3)

        np.random.seed(1)
        sine_error = test_sine()
        print('sine error = ', sine_error)
        self.assertLess(sine_error, 1e-3)
