
import matplotlib.pyplot as plt
import six
from matplotlib import colors

import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork.NetworkLayers import *



from dataprep.loader import *
from dataprep.transformer import *

def process_arrhythmia():

    csvloader = CSVLoader()

    dataset = csvloader.load_from_path('dataset/arrhythmia.data')

    nv = NullValueTransformer('?')

    ni = NullIndicatorTransformer()

    mi = NumericImputationTransformer('mean')

    ohe = OneHotEncoderTransformer()

    pipeline = PipelineTransformer(nv, ni, mi, ohe)

    processed_data = pipeline.transform(dataset)

    return processed_data



def test_encode_n_vars_d_dims(visualize=1):

    X = process_arrhythmia()

    num_x = X.shape[0]

    rgb = ['0'] * num_x
    color_list = list(six.iteritems(colors.cnames))
    for idx in range(num_x):
        X[idx, :] = np.array([[xi + xj, xi - xj, xj - xi, xi * xj]
                              for xi in Xhidden[idx,:]
                              for xj in Xhidden[idx,:]]).flatten()
        rgb[idx] = color_list[np.sum([Xhidden[idx, i] * (2 ** i)
                                      for i in range(num_hidden_dim)])][0]
    X = X + np.random.rand(num_x, size_encoding)
    X = X - np.mean(X)
    X = X / np.abs(np.max(X)) / 3
    encoder = AutoEncoder(X, hidden_dim=d)
    for _ in range(10):
        encoder.train(10)
    reconstruction = encoder.predict()
    if visualize > 0:
        if d > 3 or d < 2:
            raise(ValueError('d must be 2 or 3 for visualization'))
        encoding_vals = encoder.get_encoding_vals()
        encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis=0))
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
    return np.mean(np.square(reconstruction - X))


class TestAutoEncoding(unittest.TestCase):
    """
    unit tests for functions relating to the interval class
    These should be run by enterring the command "python -m unittest discover"
    from the root directory of this project
    """

    def test_autoencode_3d(self):
        np.random.seed(1)
        encoding_error = test_arrhythmia_3d()
        self.assertLess(encoding_error, .1)
