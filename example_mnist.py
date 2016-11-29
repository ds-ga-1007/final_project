
from dataprep.loader import *
from dataprep.transformer import *

hdfloader_inputs = HDFArrayFlattenLoader('train/inputs')
x = hdfloader_inputs.load_from_path('dataset/mnist.h5')
hdfloader_targets = HDFArrayFlattenLoader('train/targets')
y = hdfloader_targets.load_from_path('dataset/mnist.h5')

norm = GlobalLinearNormalizer(vmin=0, vmax=255, nmin=0, nmax=1)
NP.save('mnist_flatten_x.npy', norm.transform(x))
NP.save('mnist_y.npy', NP.array(y))
