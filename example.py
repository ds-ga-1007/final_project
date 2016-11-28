
from dataprep.loader import *
from dataprep.transformer import *

csvloader = CSVLoader(target=[-1])
datasetX, datasetY = csvloader.load_from_path('dataset/arrhythmia.data')
# testset = csvloader.load_from_path('dataset/test.data')

# Convert the data types according to the schema given
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
norm = ColumnNormalizer('normal')
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
trainX = pipelineX.transform(datasetX)
trainY = pipelineY.transform(datasetY)
# Transform two datasets at once so that the encodings are preserved
# train, test = pipeline.transform(dataset, testset)
NP.save('dataset/arrhythmiaX.npy', trainX)
NP.save('dataset/arrhythmiaY.npy', trainY)
