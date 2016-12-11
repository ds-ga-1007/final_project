
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import six
from matplotlib import colors

import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork.NetworkLayers import *


from dataprep.loader import *
from dataprep.transformer import *


def process_arrhythmia_supervised():

    csvloader = CSVLoader(target=[-1])
    datasetX, datasetY = csvloader.load_from_path('dataset/arrhythmia.data')
    tsX = TabularSchemaTransformer\
            (
            [
                "numeric",          # Age
                "categorical",      # Sex
                "numeric",          # Height
                "numeric",          # Weight
                "numeric",          # QRS duration
                "numeric",          # P-R interval
                "numeric",          # Q-T interval
                "numeric",          # T interval
                "numeric",          # P interval
            ] +
            ["numeric"] * 12 +      # 10-21
            ["categorical"] * 6 +   # 22-27
            ["numeric"] * 252       # 28-279
            )
    tsY = TabularSchemaTransformer(["categorical"])

    # Normalize all numeric columns into [-1, 1] first.
    norm = ColumnNormalizer('negpos')
    # Replace all string values equal to '?' to NaN
    # Note that the '?''s in numeric fields are already replaced by NaNs
    # in TabularSchemaTransformer
    nv = NullValueTransformer('?')
    # Add a 'missing indicator' for each column with missing values
    ni = NullIndicatorTransformer()
    # Impute the NaN's in numeric fields by mean value
    mi = NumericImputationTransformer('mean')
    # One-hot categorical encoder.  PD.get_dummies() does all the magic
    ohe = OneHotEncoderTransformer()

    # A pipeline which does transformation one-by-one
    pipelineX = PipelineTransformer(tsX, norm, nv, ni, mi, ohe)
    # For labels we don't need to normalize them
    pipelineY = PipelineTransformer(tsY, nv, ni, mi, ohe)

    # Transform dataset
    processedX = pipelineX.transform(datasetX)
    processedY = pipelineY.transform(datasetY)
    return processedX, processedY

def process_abalone():

    csvloader = CSVLoader(target=[-1])
    datasetX, datasetY = csvloader.load_from_path('dataset/abalone.data')


    # Normalize all numeric columns into [-1, 1] first.
    norm = ColumnNormalizer('negpos')
    # Replace all string values equal to '?' to NaN
    # Note that the '?''s in numeric fields are already replaced by NaNs
    # in TabularSchemaTransformer

    # Add a 'missing indicator' for each column with missing values
    ni = NullIndicatorTransformer()
    # Impute the NaN's in numeric fields by mean value
    mi = NumericImputationTransformer('mean')
    # One-hot categorical encoder.  PD.get_dummies() does all the magic
    ohe = OneHotEncoderTransformer()

    # A pipeline which does transformation one-by-one
    pipelineX = PipelineTransformer(norm, ni, mi, ohe)
    # For labels we don't need to normalize them
    pipelineY = PipelineTransformer(ni, mi, ohe)

    # Transform dataset
    processedX = pipelineX.transform(datasetX)
    processedY = pipelineY.transform(datasetY)
    return processedX, processedY

def process_iris():

    csvloader = CSVLoader(target=[-1])
    datasetX, datasetY = csvloader.load_from_path('dataset/iris.data')

    # Normalize all numeric columns into [-1, 1] first.
    norm = ColumnNormalizer('negpos')
    # Replace all string values equal to '?' to NaN
    # Note that the '?''s in numeric fields are already replaced by NaNs
    # in TabularSchemaTransformer

    # Add a 'missing indicator' for each column with missing values
    ni = NullIndicatorTransformer()
    # Impute the NaN's in numeric fields by mean value
    mi = NumericImputationTransformer('mean')
    # One-hot categorical encoder.  PD.get_dummies() does all the magic
    ohe = OneHotEncoderTransformer()

    # A pipeline which does transformation one-by-one
    pipelineX = PipelineTransformer(norm, ni, mi, ohe)
    # For labels we don't need to normalize them
    pipelineY = PipelineTransformer(ni, mi, ohe)

    # Transform dataset
    processedX = pipelineX.transform(datasetX)
    processedY = pipelineY.transform(datasetY)
    return processedX, processedY

def prepare_autoencoding_data(X, Y, visualize):

    X /= 2
    color_list = list(six.iteritems(colors.cnames))

    if Y.ndim == 1:
        rgb = [color_list[y * 2 + 1][0] for y in Y]
    elif Y.ndim == 2:
        rgb = [color_list[4 * np.sum(
            [yi * (2 ** idx) for idx, yi in enumerate(y)])][0] for y in Y]
    else:
        visualize = 0

    return X, visualize, rgb

def visualize_autoencoding_data(encoder, d, rgb, fig):

    encoding_vals = encoder.get_encoding_vals()

    if d == 2:
        fig.add_subplot(120 + d - 1)
        plt.scatter(encoding_vals[:, 0], encoding_vals[:, 1], color=rgb)
    if d == 3:
        ax = fig.add_subplot(120 + d - 1, projection='3d')
        ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1],
                   zs=encoding_vals[:, 2], c=rgb)

    plt.title('real data visualized with graphed in ' + str(d) + 'D')

def process_autoencoding(X, visualize, rgb):

    err = np.empty(2)

    if visualize:
        fig = plt.figure()

    for d in [2, 3]:

        encoder = AutoEncoder(X, hidden_dim=d)
        encoder.train(10)
        reconstruction = encoder.predict()

        if visualize:
            visualize_autoencoding_data(encoder, d, rgb, fig)

        err[d-2] = np.mean(np.square(reconstruction - X))

    if visualize:
        plt.show()

    return err

def autoencode_2d_3d(X, Y, visualize = 0):

    X, visualize, rgb = prepare_autoencoding_data(X, Y, visualize)

    err = process_autoencoding(X, visualize, rgb)

    return err[0], err[1]

def autoencode_abalone(visualize=0):

    X, Y = process_abalone()
    return autoencode_2d_3d(X, Y, visualize)


def autoencode_iris(visualize=0):

    X, Y = process_iris()
    return autoencode_2d_3d(X, Y, visualize)

class TestAutoEncodingData(unittest.TestCase):
    """
    Tests that the autoencoder can process and reconstruct the initial X vector
    even though the data is passed through a narrow layer.
    For user inspection, visualize can be set to true to understand how this
    narrow layer encodes such high dimensional information in 2D and 3D, but that is not enabled
    as a default for unit testing.
    """

    def test_autoencode_iris(self):
        np.random.seed(1)
        err_2d, err_3d = autoencode_iris()
        self.assertLess(err_2d, .1)
        self.assertLess(err_3d, .1)

    def test_autoencode_abalone(self):
        np.random.seed(1)
        err_2d, err_3d = autoencode_abalone()
        self.assertLess(err_2d, .1)
        self.assertLess(err_3d, .1)
