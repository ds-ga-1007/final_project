
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


def test_encoding_regression(verb=0):
    num_x = 100
    X1h = np.random.rand(num_x)
    X2h = np.random.rand(num_x)
    size_encoding = 6
    X = np.zeros([num_x, size_encoding])
    for idx in range(num_x):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X[idx, :] = [X1, X2, X1 + X2, X1 - X2, X2 - X1, X1 * X2]
    X = X / 4 + np.random.rand(num_x, size_encoding) / 100
    encoder = AutoEncoder(X)
    for _ in range(10):
        encoder.train(10)
        if verb > 0:
            encoding_vals = encoder.get_encoding_vals()
            err1 = np.abs(np.corrcoef(x=X1h, y=encoding_vals[:, 0])[0, 1]) + \
                   np.abs(np.corrcoef(x=X2h, y=encoding_vals[:, 1])[0, 1])
            err2 = np.abs(np.corrcoef(x=X2h, y=encoding_vals[:, 0])[0, 1]) + \
                   np.abs(np.corrcoef(x=X1h, y=encoding_vals[:, 1])[0, 1])
            print(err1, err2)
        reconstruction = encoder.predict()
    return np.mean(np.square(reconstruction - X))


def test_encoding_categorical_2D(verb=0):
    num_x = 100
    X1h = np.random.randint(0, 2, num_x)
    X2h = np.random.randint(0, 2, num_x)
    size_encoding = 6
    X = np.zeros([num_x, size_encoding])
    for idx in range(num_x):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X[idx, :] = [X1, X2, X1 + X2, X1 - X2, X2 - X1, X1 * X2]
    X = X / 4 + np.random.rand(num_x, size_encoding) / 100
    encoder = AutoEncoder(X)
    encoding_vals = encoder.get_encoding_vals()
    for _ in range(10):
        encoder.train(10)
        if verb > 0:
            encoding_vals = encoder.get_encoding_vals()
            err1 = np.abs(np.corrcoef(x=X1h, y=encoding_vals[:, 0])[0, 1]) + \
                   np.abs(np.corrcoef(x=X2h, y=encoding_vals[:, 1])[0, 1])
            err2 = np.abs(np.corrcoef(x=X2h, y=encoding_vals[:, 0])[0, 1]) + \
                   np.abs(np.corrcoef(x=X1h, y=encoding_vals[:, 1])[0, 1])
            print("correlation between true hidden and encoders: ", np.max([err1, err2]) / 2)
    reconstruction = encoder.predict()
    if verb > 0:
        encoding_vals = encoder.get_encoding_vals()
        plt.scatter(encoding_vals[:, 0], encoding_vals[:, 1])
        plt.show()
    return np.mean(np.square(reconstruction - X))


def test_encoding_categorical_3d(verb=0):
    num_x = 300
    X1h = np.random.randint(0, 2, num_x)
    X2h = np.random.randint(0, 2, num_x)
    X3h = np.random.randint(0, 2, num_x)
    size_encoding = 13
    X = np.zeros([num_x, size_encoding])
    rgb = np.zeros([num_x, 3])
    for idx in range(num_x):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X3 = X3h[idx]
        X[idx, :] = [X1, X2, X1 + X2, X1 - X2, X2 - X1, X1 * X2,
                     X3, X2 - X1, X3 - X1, X3 + X2, X3 + X1, X3 * X2, X3 * X1]
        rgb[idx, :] = [X1, X2, X3]
    X = X / 4 + np.random.rand(num_x, size_encoding) / 4
    encoder = AutoEncoder(X, hidden_dim=3)
    for _ in range(10):
        encoder.train(20)
    reconstruction = encoder.predict()
    if verb > 0:
        encoding_vals = encoder.get_encoding_vals()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis=0))
        ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1], zs=encoding_vals[:, 2], c=rgb)
        plt.show()
    return np.mean(np.square(reconstruction - X))


def test_encoding_4_variables(verb=0):
    num_x = 200
    X1h = np.random.randint(0, 2, num_x)
    X2h = np.random.randint(0, 2, num_x)
    X3h = np.random.randint(0, 2, num_x)
    X4h = np.random.randint(0, 2, num_x)
    size_encoding = 16 * 4
    X = np.zeros([num_x, size_encoding])
    rgb = ['0'] * num_x
    color_list = list(six.iteritems(colors.cnames))
    for idx in range(num_x):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X3 = X3h[idx]
        X4 = X4h[idx]
        X[idx, :] = np.array([[xi + xj, xi - xj, xj - xi, xi * xj]
                              for xi in [X1, X2, X3, X4]
                              for xj in [X1, X2, X3, X4]]).flatten()
        rgb[idx] = color_list[2 * (X1 + X2 * 2 + X3 * 2 ** 2 + X4 * 2 ** 3)][0]
    X = X + np.random.rand(num_x, size_encoding) / 2
    X = X / np.max(X) / 1.8
    encoder = AutoEncoder(X, hidden_dim=3)
    for _ in range(10):
        encoder.train(10)
    reconstruction = encoder.predict()
    if verb > 0:
        encoding_vals = encoder.get_encoding_vals()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis=0))
        ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1], zs=encoding_vals[:, 2], c=rgb)
        plt.show()
    return np.mean(np.square(reconstruction - X))

def test_encoding_5_variables(verb=0):
    num_x = 1000
    X1h = np.random.randint(0, 2, num_x)
    X2h = np.random.randint(0, 2, num_x)
    X3h = np.random.randint(0, 2, num_x)
    X4h = np.random.randint(0, 2, num_x)
    X5h = np.random.randint(0, 2, num_x)
    size_encoding = 25 * 4
    X = np.zeros([num_x, size_encoding])
    rgb = ['0'] * num_x
    color_list = list(six.iteritems(colors.cnames))
    for idx in range(num_x):
        X1 = X1h[idx]
        X2 = X2h[idx]
        X3 = X3h[idx]
        X4 = X4h[idx]
        X5 = X5h[idx]
        X[idx, :] = np.array([[xi + xj, xi - xj, xj - xi, xi * xj]
                              for xi in [X1, X2, X3, X4, X5]
                              for xj in [X1, X2, X3, X4, X5]]).flatten()
        rgb[idx] = color_list[2 * (X1 + X2 * 2 + X3 * 2 ** 2 + X4 * 2 ** 3 + X5 * 2 ** 4)][0]
    X = X + np.random.rand(num_x, size_encoding) / 2
    X = X - np.mean(X)
    X = X / np.abs(np.max(X)) / 3
    encoder = AutoEncoder(X, hidden_dim=3)
    for _ in range(5):
        encoder.train(10)
    reconstruction = encoder.predict()
    if verb > 0:
        encoding_vals = encoder.get_encoding_vals()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis=0))
        ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1], zs=encoding_vals[:, 2], c=rgb)
        plt.show()
    return np.mean(np.square(reconstruction - X))

def test_encoding_n_variables_3d(n, verb=0):
    num_x = (n**2) * 20
    size_encoding = (n**2) * 4
    Xhidden = np.random.randint(0, 2, [num_x, n])
    print (Xhidden.shape)
    X = np.zeros([num_x, size_encoding])
    rgb = ['0'] * num_x
    color_list = list(six.iteritems(colors.cnames))
    for idx in range(num_x):
        X[idx, :] = np.array([[xi + xj, xi - xj, xj - xi, xi * xj]
                              for xi in Xhidden[idx,:]
                              for xj in Xhidden[idx,:]]).flatten()
        rgb[idx] = color_list[np.sum([Xhidden[idx, i] * (2 ** i) for i in range(n)])][0]
    X = X + np.random.rand(num_x, size_encoding) / 2
    X = X - np.mean(X)
    X = X / np.abs(np.max(X)) / 3
    encoder = AutoEncoder(X, hidden_dim=3)
    for _ in range(5):
        encoder.train(10)
    reconstruction = encoder.predict()
    if verb > 0:
        encoding_vals = encoder.get_encoding_vals()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis=0))
        ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1], zs=encoding_vals[:, 2], c=rgb)
        plt.title(str(2**n * 4) + ' Visible Variables \n With ' +
                  str(n) + ' Hidden Dimensions. Graphed in  3D')
        plt.show()
    return np.mean(np.square(reconstruction - X))

def test_encoding_n_variables_2d(n, verb=0):
    num_x = (n**2) * 20
    size_encoding = (n**2) * 4
    Xhidden = np.random.randint(0, 2, [num_x, n])
    print (Xhidden.shape)
    X = np.zeros([num_x, size_encoding])
    rgb = ['0'] * num_x
    color_list = list(six.iteritems(colors.cnames))
    for idx in range(num_x):
        X[idx, :] = np.array([[xi + xj, xi - xj, xj - xi, xi * xj]
                              for xi in Xhidden[idx,:]
                              for xj in Xhidden[idx,:]]).flatten()
        rgb[idx] = color_list[np.sum([Xhidden[idx, i] * (2 ** i) for i in range(n)])][0]
    X = X + np.random.rand(num_x, size_encoding) / 2
    X = X - np.mean(X)
    X = X / np.abs(np.max(X)) / 3
    encoder = AutoEncoder(X, hidden_dim=2)
    for _ in range(5):
        encoder.train(10)
    reconstruction = encoder.predict()
    if verb > 0:
        encoding_vals = encoder.get_encoding_vals()
        plt.scatter(encoding_vals[:, 0], encoding_vals[:, 1], color=rgb)
        plt.title(str(2**n * 4) + ' Visible Variables \n With ' + str(n) + ' Hidden Dimensions. Graphed in  2D')
        plt.show()
    return np.mean(np.square(reconstruction - X))


class TestAutoEncoding(unittest.TestCase):
    """unit tests for functions relating to the interval class
    These should be run by enterring the command "python -m unittest discover"
    from the root directory of this project
    """

    def test_learnability(self):


        np.random.seed(1)
        encoding_regression_error = test_encoding_regression()
        print('autoencoding regression error = ', encoding_regression_error)
        self.assertLess(encoding_regression_error, 0.01)

        np.random.seed(1)
        encoding_categorical_error = test_encoding_n_variables_2d(n = 2, verb = 1)
        print('autoencoding categorical error 2d 2 vars= ', encoding_categorical_error)
        self.assertLess(encoding_categorical_error, 0.1)

        np.random.seed(1)
        encoding_categorical_error_3d = test_encoding_n_variables_3d(n = 3, verb = 1)
        print('autoencoding regression error 3d 3 vars= ', encoding_categorical_error_3d)
        self.assertLess(encoding_categorical_error_3d, 0.1)

        np.random.seed(1)
        err_4 = test_encoding_n_variables_3d(n = 4, verb = 1)
        print('autoencoding error 3d 4 vars = ', err_4)
        self.assertLess(err_4, 0.1)

        np.random.seed(1)
        err_5 = test_encoding_n_variables_3d(n = 5, verb = 1)
        print('autoencoding error 3d 5 vars = ', err_5)
        self.assertLess(err_5, 0.1)

        np.random.seed(1)
        err_3_2d = test_encoding_n_variables_2d(n = 3, verb = 1)
        print('autoencoding error 2d 3 vars = ', err_3_2d)
        self.assertLess(err_3_2d, 0.1)

        np.random.seed(1)
        err_4_2d = test_encoding_n_variables_2d(n = 4, verb = 1)
        print('autoencoding error 2d 4 vars = ', err_4_2d)
        self.assertLess(err_4_2d, 0.1)

        np.random.seed(1)
        err_5_2d = test_encoding_n_variables_2d(n = 5, verb = 1)
        print('autoencoding error 2d 5 vars = ', err_5_2d)
        self.assertLess(err_5_2d, 0.1)