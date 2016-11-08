import matplotlib.pyplot as plt
import numpy as np

from Model import utils
from Model.Network.NeuralNetworkUI import NeuralNetworkUI


def test_xor(verb=0):
    NN = NeuralNetworkUI([2, 10, 10, 1])
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])
    Y = np.array([np.array([x[0] ^ x[1]]) for x in X])
    for _ in range(100):
        NN.train(X, Y, epochs=10)
        y_predict = NN.predict(X)
        print(y_predict)
    return np.mean(np.square(y_predict - Y))
if (1):
    np.random.seed(2)
    xor_err = test_xor()
    print('xor error = ', xor_err)

def test_addition(verb=0):
    NN = NeuralNetworkUI([2, 10, 1], reg_const = 1e-9)
    X = np.array([[0, 0],
                  [0, .5],
                  [.5, 0],
                  [.5, .5]])
    Y = np.array([np.array([x[0] + x[1]]) for x in X])
    #Y = np.array([np.array([0]), np.array([1]), np.array([1]), np.array([1])])
    NN.train(X, Y, epochs=1)
    y_predict = NN.predict(X)
    print(Y.T)
    if verb > -1:
        pass#print(y_predict)
    for _ in range(100):
        NN.train(X, Y, epochs=10)
        y_predict = NN.predict(X)
        print(y_predict)
    return np.mean(np.square(y_predict - Y))
if (0):
    np.random.seed(2)
    add_error = test_addition()
    print('add error = ', add_error)
