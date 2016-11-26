
from dataprep.loader import *
from dataprep.transformer import *

csvloader = CSVLoader()
dataset = csvloader.load_from_path('dataset/arrhythmia.data')
# testset = csvloader.load_from_path('dataset/test.data')

# Convert the data types according to the schema given
ts = TabularSchemaTransformer(
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
        ["numeric"] * 252 +     # 28-279
        ["categorical"]         # class label
        )
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
pipeline = PipelineTransformer(ts, nv, ni, mi, ohe)

# Transform one dataset
train = pipeline.transform(dataset)
# Transform two datasets at once so that the encodings are preserved
# train, test = pipeline.transform(dataset, testset)
NP.save('dataset/arrhythmia.npy', train)
