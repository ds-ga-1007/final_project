import numpy as np

from Model import utils
from Model.Network.NeuralNetworkUI import NeuralNetworkUI


def test_xor(verb=0):
    NN = NeuralNetworkUI([2, 100, 100, 1], reg_const=1e-4)
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
if (1):
    np.random.seed(1)
    xor_err = test_xor()
    print('xor error = ', xor_err)

def test_addition(verb=0):
    NN = NeuralNetworkUI([2, 100, 1], trans_fcns=["sigmoid", "purelin"], learn_alg=utils.GRADIENT_DESCENT)
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
if (1):
    np.random.seed(1)
    add_error = test_addition()
    print('add error = ', add_error)
