
import matplotlib.pyplot as plt
import six
from matplotlib import colors

import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork.NetworkLayers import *


from dataprep.loader import *
from dataprep.transformer import *

def process_arrhythmia():

    csvloader = CSVLoader(target=[-1])
    datasetX, datasetY = csvloader.load_from_path('dataset/arrhythmia.data')

    tsX = TabularSchemaTransformer(
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
    norm = Normalizer('negpos')
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


def test_arrhythmia(d = 3, visualize=1):

    X, Y = process_arrhythmia()
    print(Y)

    num_x = X.shape[0]
    print(X.shape)
    color_list = list(six.iteritems(colors.cnames))
    print(Y[:,0])
    rgb = [color_list[np.sum([yi*2 for yi in y])][0] for y in Y]
    encoder = AutoEncoder(X, hidden_dim=3)
    print(np.mean(X, 0))
    return
    for _ in range(10):
        encoder.train(1)
        reconstruction = encoder.predict()
        print(reconstruction)
    reconstruction = encoder.predict()
    if visualize > 0:
        encoding_vals = encoder.get_encoding_vals()
        encoding_vals = encoding_vals / np.abs(np.mean(encoding_vals, axis=0))
        if d == 2:
            plt.scatter(encoding_vals[:, 0], encoding_vals[:, 1], color=rgb)
        if d == 3:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1],
                       zs=encoding_vals[:, 2], c=rgb)
        plt.title(str(2 ** 0 * 4) + ' Visible Variables \n With ' +
                  str(0) + ' Hidden Dimensions. Graphed in ' + str(d) + 'D')
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
        encoding_error = test_arrhythmia(d = 3)
        self.assertLess(encoding_error, .1)
