
import unittest
from utils import *
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

def autoencode_abalone(visualize=0):

    X, Y = process_abalone()
    return autoencode_2d_3d_data(X, Y, visualize)


def autoencode_iris(visualize=0):

    X, Y = process_iris()
    return autoencode_2d_3d_data(X, Y, visualize)

class TestAutoEncodingData(unittest.TestCase):
    """
    Tests that the autoencoder can process and reconstruct the initial X vector
    even though the data is passed through a narrow layer.
    For user inspection, visualize can be set to 1 to understand how this
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
