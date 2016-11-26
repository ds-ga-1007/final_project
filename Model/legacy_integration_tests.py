import matplotlib.pyplot as plt
import numpy as np
import six
from .FeedForwardNetApps import *
from .FeedForwardNetwork import *#from .FeedForwardNetApps.FeedForwardNetworkUI import FeedForwardNetworkUI
from matplotlib import colors

from Model.FeedForwardNetApps.AutoEncoder import AutoEncoder
from Model.FeedForwardNetwork import utils


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
if (0):
    np.random.seed(1)
    xor_err = test_xor()
    print('xor error = ', xor_err)

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
if (0):
    np.random.seed(1)
    add_error = test_addition()
    print('add error = ', add_error)


def test_sine(verb=0):
    NN = FeedForwardNetworkUI([1, 200, 1], trans_fcns="tanh", reg_const=1e-5)
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
    encoding_vals = encoder.get_encoding_vals()
    for _ in range(10):
        encoder.train(10)
        if verb > 0:
            encoding_vals = encoder.get_encoding_vals()
            err1 = np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,0])[0,1]) + \
                   np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,1])[0,1])
            err2 = np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,0])[0,1]) + \
                   np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,1])[0,1])
            print("correlation between true hidden and encoders: ", np.max([err1, err2])/2)
    reconstruction = encoder.predict()
    encoding_vals = encoder.get_encoding_vals()
    plt.scatter(encoding_vals[:,0], encoding_vals[:,1])
    plt.show()
    return np.mean(np.square(reconstruction - X))
if (0):
    np.random.seed(1)
    encoding_categorical_error = test_encoding_categorical(1)
    print('autoencoding regression error = ', encoding_categorical_error)

def test_encoding_categorical_3d(verb=0):
    num_x = 300
    X1h = np.random.randint(0,2,num_x)
    X2h = np.random.randint(0,2,num_x)
    X3h = np.random.randint(0,2,num_x)
    size_encoding = 13
    X = np.zeros([num_x, size_encoding])
    rgb = np.zeros([num_x, 3])
    for idx in range(num_x):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X3 = X3h[idx]
        X[idx,:] = [X1, X2,X1 + X2, X1 - X2, X2 - X1, X1*X2,
                    X3, X2-X1, X3-X1, X3+ X2, X3 + X1, X3*X2, X3*X1]
        rgb[idx,:] = [X1, X2, X3]
    X = X/4 + np.random.rand(num_x, size_encoding)/4
    encoder = AutoEncoder(X, hidden_dim = 3)
    encoding_vals = encoder.get_encoding_vals()
    for _ in range(10):
        encoder.train(20)
        if verb > 0:
            encoding_vals = encoder.get_encoding_vals()
            #err1 = np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,0])[0,1]) + \
            #       np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,1])[0,1])
            #err2 = np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,0])[0,1]) + \
            #       np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,1])[0,1])
            #print("correlation between true hidden and encoders: ", np.max([err1, err2])/2)
    reconstruction = encoder.predict()
    encoding_vals = encoder.get_encoding_vals()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis = 0))
    ax.scatter(xs = encoding_vals[:,0], ys = encoding_vals[:,1], zs = encoding_vals[:,2], c = rgb)
    plt.show()
    return np.mean(np.square(reconstruction - X))
if (0):
    np.random.seed(1)
    encoding_categorical_error_3d = test_encoding_categorical_3d(1)
    print('autoencoding regression error = ', encoding_categorical_error_3d)


def test_encoding_5_vars(verb=0):
    num_x = 200
    X1h = np.random.randint(0, 2, num_x)
    X2h = np.random.randint(0, 2, num_x)
    X3h = np.random.randint(0, 2, num_x)
    X4h = np.random.randint(0, 2, num_x)
    X5h = np.random.randint(0, 2, num_x)
    X6h = np.random.randint(0, 2, num_x)
    size_encoding = 16*4
    X = np.zeros([num_x, size_encoding])
    rgb = ['0']*num_x
    color_list = list(six.iteritems(colors.cnames))
    for idx in range(num_x):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X3 = X3h[idx]
        X4 = X4h[idx]
        X5 = X5h[idx]
        X6 = X6h[idx]
        X[idx, :] = np.array([[xi+xj, xi-xj, xj-xi, xi*xj]
                     for xi in [X1, X2, X3, X4]
                     for xj in [X1, X2, X3, X4]]).flatten()
        rgb[idx] = color_list[2*(X1+X2*2+X3*2**2+X4*2**3)][0]
    X = X + np.random.rand(num_x, size_encoding) / 2
    X = X / np.max(X) / 1.8
    encoder = AutoEncoder(X, hidden_dim=3)
    encoding_vals = encoder.get_encoding_vals()
    for _ in range(10):
        encoder.train(10)
        if verb > 0:
            encoding_vals = encoder.get_encoding_vals()
            # err1 = np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,0])[0,1]) + \
            #       np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,1])[0,1])
            # err2 = np.abs(np.corrcoef(x=X2h, y=encoding_vals[:,0])[0,1]) + \
            #       np.abs(np.corrcoef(x=X1h, y=encoding_vals[:,1])[0,1])
            # print("correlation between true hidden and encoders: ", np.max([err1, err2])/2)
    reconstruction = encoder.predict()
    encoding_vals = encoder.get_encoding_vals()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis=0))
    ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1], zs=encoding_vals[:, 2], c=rgb)
    plt.show()
    return np.mean(np.square(reconstruction - X))


if (1):
    np.random.seed(1)
    err_5 = test_encoding_5_vars(1)
    print('autoencoding regression error 5 vars = ', err_5)
