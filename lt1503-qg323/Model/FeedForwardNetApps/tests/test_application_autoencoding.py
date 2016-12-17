from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import six
from matplotlib import colors
import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork.NetworkLayers import *
"""
Test the applications ability to autoencode and reconstruct simulated data
Contains functionality to visualize 2d and 3d encodings that are not
included in unit tests.
"""
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
    encoder.train(20)
    reconstruction = encoder.predict()

    return np.mean(np.square(reconstruction - X))

def prepare_data_autoencoding(num_hidden_dim):

    num_x = (num_hidden_dim ** 2) * 20
    size_encoding = (num_hidden_dim ** 2) * 4
    Xhidden = np.random.randint(0, 2, [num_x, num_hidden_dim])
    X = np.zeros([num_x, size_encoding])
    rgb = ['0'] * num_x
    color_list = list(six.iteritems(colors.cnames))

    for idx in range(num_x):
        X[idx, :] = np.array([[xi + xj, xi - xj, xj - xi, xi * xj]
                              for xi in Xhidden[idx, :]
                              for xj in Xhidden[idx, :]]).flatten()
        rgb[idx] = color_list[np.sum([Xhidden[idx, i] * (2 ** i)
                                      for i in range(num_hidden_dim)])][0]

    X += (np.random.rand(num_x, size_encoding) / 5)
    X -= - np.mean(X)
    X /= (np.abs(np.max(X)) * 3)
    return X, rgb, Xhidden, num_x

def get_trained_autoencoder(X, d):

    encoder = AutoEncoder(X, hidden_dim=d)
    encoder.train(5)

    return encoder

def visualize_autoencoding(encoding_vals, d, rgb, num_hidden_dim):

    if d > 3 or d < 2:
        raise (ValueError('d must be 2 or 3 for visualization'))

    if d == 2:
        plt.scatter(encoding_vals[:, 0], encoding_vals[:, 1], color=rgb)

    if d == 3:

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1],
                   zs=encoding_vals[:, 2], c=rgb)

    plt.title(str(2 ** num_hidden_dim * 4) + ' Visible Variables \n With ' +
              str(num_hidden_dim) + ' Hidden Dimensions. Graphed in ' + str(d) + 'D')

    plt.show()

def test_encode_n_vars_d_dims(num_hidden_dim, d, visualize=0):

    if not isinstance(d, int):
        raise(ValueError("hidden dimensions must be an integer"))

    X, rgb, Xhidden, num_x = prepare_data_autoencoding(num_hidden_dim)

    encoder = get_trained_autoencoder(X, d)

    reconstruction = encoder.predict()

    encoding_vals = encoder.get_encoding_vals()
    encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis=0))

    if visualize > 0:
        visualize_autoencoding(encoding_vals, d, rgb, num_hidden_dim)

    return np.mean(np.square(reconstruction - X)), encoding_vals, Xhidden


class TestSystemAutoEncoding(unittest.TestCase):
    """
    Tests that the autoencoder can reconstruct the initial X vector
    even though the data is passed through a narrow layer.
    For user inspection, visualize can be set to true to understand how this
    narrow layer encodes such high dimensional information in 2D and 3D, but that is not enabled
    as a default for unit testing.
    """

    def test_autoencode_regression(self):

        np.random.seed(1)
        encoding_regression_error = test_encoding_regression()
        self.assertLess(encoding_regression_error, 1e-2)

    def test_autoencode_3d(self):

        for num_hidden_dim in range(3, 5):
            np.random.seed(1)
            encoding_error, _, _ = test_encode_n_vars_d_dims(num_hidden_dim = num_hidden_dim, d = 3)
            self.assertLess(encoding_error, .1)

    def test_autoencode_2d(self):

        for num_hidden_dim in range(2, 5):
            np.random.seed(1)
            encoding_error, _, _ = test_encode_n_vars_d_dims(num_hidden_dim = num_hidden_dim, d = 2)
            self.assertLess(encoding_error, .1)
