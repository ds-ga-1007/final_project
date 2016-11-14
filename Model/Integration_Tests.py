import numpy as np

from Model import utils
from Model.Network.NeuralNetworkUI import NeuralNetworkUI
from Model.Network.AutoEncoder import AutoEncoder


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
if (0):
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
if (0):
    np.random.seed(1)
    add_error = test_addition()
    print('add error = ', add_error)


def test_sine(verb=1):
    NN = NeuralNetworkUI([1, 2000, 1], trans_fcns="tanh", reg_const=1e-6)
    X = np.linspace(0, 2*np.pi, num=5)
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
if (0):
    np.random.seed(1)
    sine_error = test_sine()
    print('sine error = ', sine_error)

def test_encoding(verb=0):
    X1h = np.random.rand(20)
    X2h = np.random.rand(20)
    X = np.zeros([20, 5])
    for idx in range(20):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X[idx,:] = [X1*X2, X1+X2, X1/(1+X2), X2/(1+X1), X1-X2]
    X = X/2
    X1h = np.atleast_2d(X1h)
    X2h = np.atleast_2d(X2h)
    encoder = AutoEncoder(X)
    encoding_vals = encoder.get_encoding_vals(X)
    for _ in range(10):
        encoder.train(X, 100)
        encoding_vals = encoder.get_encoding_vals(X)
        reconstruction = np.round(encoder.predict(X), 3)
        #print("reconstruction error: ", np.mean(np.square(reconstruction - X)))
        err1 = np.mean(np.square(np.concatenate([X1h, X2h]).T - encoding_vals))
        err2 = np.mean(np.square(np.concatenate([X2h, X1h]).T - encoding_vals))
        print(err1, err2)
        #print("encoding error: ", np.min([err1, err2]))
        #print("encoding_vals:   ", encoding_vals)
        #print(np.mean(np.square(reconstruction - X)))
    print(X)
    return np.mean(np.square(reconstruction - X))
if (1):
    np.random.seed(1)
    encoding_error = test_encoding()
    print('autoencoding error = ', encoding_error)
