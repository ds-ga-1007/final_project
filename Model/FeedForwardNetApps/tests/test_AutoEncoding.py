
import matplotlib.pyplot as plt
import six
from matplotlib import colors
from sklearn.cluster import KMeans
import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork.NetworkLayers import *

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


def test_encode_n_vars_d_dims(num_hidden_dim, d, visualize=0):
    if not isinstance(d, int):
        raise(ValueError("hidden dimensions must be an integer"))
    num_x = (num_hidden_dim ** 2) * 20
    size_encoding = (num_hidden_dim ** 2) * 4
    Xhidden = np.random.randint(0, 2, [num_x, num_hidden_dim])
    X = np.zeros([num_x, size_encoding])
    rgb = ['0'] * num_x
    color_list = list(six.iteritems(colors.cnames))
    for idx in range(num_x):
        X[idx, :] = np.array([[xi + xj, xi - xj, xj - xi, xi * xj]
                              for xi in Xhidden[idx,:]
                              for xj in Xhidden[idx,:]]).flatten()
        rgb[idx] = color_list[np.sum([Xhidden[idx, i] * (2 ** i)
                                      for i in range(num_hidden_dim)])][0]
    X = X + np.random.rand(num_x, size_encoding) / 3
    X = X - np.mean(X)
    X = X / np.abs(np.max(X)) / 3
    encoder = AutoEncoder(X, hidden_dim=d)
    for _ in range(10):
        encoder.train(10)
    reconstruction = encoder.predict()
    encoding_vals = encoder.get_encoding_vals()
    encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis=0))
    if visualize > 0:
        if d > 3 or d < 2:
            raise(ValueError('d must be 2 or 3 for visualization'))
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
    return np.mean(np.square(reconstruction - X)), encoding_vals, Xhidden


class TestAutoEncoding(unittest.TestCase):
    """
    unit tests for functions relating to the interval class
    These should be run by enterring the command "python -m unittest discover"
    from the root directory of this project
    """

    def test_autoencode_cluster_3d(self):

        for num_hidden_dim in range(3, 7):
            np.random.seed(1)
            _, encoding_vals, Xhidden = \
                test_encode_n_vars_d_dims(
                    num_hidden_dim = num_hidden_dim, d = 3)
            num_hidden = 2**num_hidden_dim
            kmeans_classes = KMeans(
                n_clusters=num_hidden).fit_predict(
                    encoding_vals
            )
            true_classes = [np.sum([xi*(2**idx) for idx, xi in enumerate(x)])
                            for x in Xhidden]
            min_total_divergence = 0
            for kmean_class in range(np.max(kmeans_classes)+1):
                a = np.array([c == kmean_class for c in kmeans_classes])
                min_divergence = np.inf
                for true_class in range(np.max(true_classes)+1):
                    b = np.array([c == true_class
                                  for c in true_classes])
                    difference = np.logical_xor(a, b)
                    divergence = np.sum(difference)
                    min_divergence = np.min((min_divergence, divergence))
                min_total_divergence += min_divergence
            min_total_divergence /= len(true_classes)
            print(min_total_divergence)
            self.assertLess(min_total_divergence, .1)
"""
    def test_autoencode_regression(self):

        np.random.seed(1)
        encoding_regression_error = test_encoding_regression()
        self.assertLess(encoding_regression_error, 1e-2)

    def test_autoencode_3d(self):

        for num_hidden_dim in range(3, 6):
            np.random.seed(1)
            encoding_error = test_encode_n_vars_d_dims(num_hidden_dim = num_hidden_dim, d = 3)
            self.assertLess(encoding_error, .1)

    def test_autoencode_2d(self):

        for num_hidden_dim in range(2, 6):
            np.random.seed(1)
            encoding_error = test_encode_n_vars_d_dims(num_hidden_dim = num_hidden_dim, d = 2)
            self.assertLess(encoding_error, .1)
"""