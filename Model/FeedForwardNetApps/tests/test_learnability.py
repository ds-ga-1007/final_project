import copy
import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork import *
from Model.FeedForwardNetwork.NetworkLayers import *


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

class TestLearnability(unittest.TestCase):
    """
    Tests for functions relating to the interval class
    """


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


