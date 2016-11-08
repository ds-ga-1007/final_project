import matplotlib.pyplot as plt
import numpy as np

from Model import utils
from Model.Network.NeuralNetworkUI import NeuralNetworkUI


def test_xor(verb=0):
    NN = NeuralNetworkUI([2, 100, 1])
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])
    Y = np.array([np.array([x[0] ^ x[1]]) for x in X])
    NN.train(X, Y, epochs=10)
    y_predict = NN.predict(X)
    if verb > -1:
        utils.print_y(y_predict, Y)
    return np.mean(np.square(y_predict - Y))
np.random.seed(2)
xor_err = test_xor()
print('xor error = ', xor_err)
