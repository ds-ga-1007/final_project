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


def test_sine(verb=0):
    NN = NeuralNetworkUI([1, 200, 1], trans_fcns="tanh", reg_const=1e-5)
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

def test_encoding_regression(verb=0):
    num_x = 100
    X1h = np.random.rand(num_x)
    X2h = np.random.rand(num_x)
    size_encoding = 6
    X = np.zeros([num_x, size_encoding])
    for idx in range(num_x):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X[idx,:] = [X1, X2,X1 + X2, X1 - X2, X2 - X1, X1*X2]
    X = X/4 + np.random.rand(num_x, size_encoding)/100
    encoder = AutoEncoder(X)
    encoding_vals = encoder.get_encoding_vals(X)
    for _ in range(10):
        encoder.train(X, 10)
        if verb > 0:
            encoding_vals = encoder.get_encoding_vals(X)
            err1 = np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,0])[0,1]) + \
                   np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,1])[0,1])
            err2 = np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,0])[0,1]) + \
                   np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,1])[0,1])
            print(err1, err2)
        reconstruction = encoder.predict(X)
    return np.mean(np.square(reconstruction - X))
if (0):
    np.random.seed(1)
    encoding_regression_error = test_encoding_regression(1)
    print('autoencoding regression error = ', encoding_regression_error)

def test_encoding_categorical(verb=0):
    num_x = 100
    X1h = np.random.randint(0,2,num_x)
    X2h = np.random.randint(0,2,num_x)
    size_encoding = 6
    X = np.zeros([num_x, size_encoding])
    for idx in range(num_x):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X[idx,:] = [X1, X2,X1 + X2, X1 - X2, X2 - X1, X1*X2]
    X = X/4 + np.random.rand(num_x, size_encoding)/100
    encoder = AutoEncoder(X)
    encoding_vals = encoder.get_encoding_vals(X)
    for _ in range(10):
        encoder.train(X, 10)
        if verb > 0:
            encoding_vals = encoder.get_encoding_vals(X)
            err1 = np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,0])[0,1]) + \
                   np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,1])[0,1])
            err2 = np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,0])[0,1]) + \
                   np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,1])[0,1])
            print("correlation between true hidden and encoders: ", np.max([err1, err2])/2)
        reconstruction = encoder.predict(X)
    return np.mean(np.square(reconstruction - X))
if (1):
    np.random.seed(1)
    encoding_categorical_error = test_encoding_categorical(1)
    print('autoencoding regression error = ', encoding_categorical_error)
