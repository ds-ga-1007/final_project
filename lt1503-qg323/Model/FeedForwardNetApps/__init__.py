'''
Applications of Neural Networks.
The two main user-accessible applications of neural networks are
Autoencoders and Feed Forward Networks.

Autoencoders attempt to create a low dimensional projection of data
that contains most of the dimensionality of the true data.

Feed Forward Neural Networks learn mappings from visible features to
class labels or regression values.

Autoencoders just need input data, whereas Feed Forward Networks
need input data as well as known output values to learn from
'''

from .AutoEncoder import *
from .FeedForwardNetworkUI import *