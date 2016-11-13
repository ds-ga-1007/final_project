from Model.Network.ActivationLayer import ActivationLayer
from Model.Network.FullyConnectedLayer import FullyConnectedLayer
from Model.Network.Layer import Layer

import sys

class ConnectionActivationLayer(Layer):
    '''
    ConnectionActivation Layers are used to represent a Layer that consists
    of a FullyConnectedLayer and then an ActivationLayer.
    Each ConnectionActivationLayer is just an abstraction of these two layers
    because, from a feed forward neural networks point of view,
    the connection between any two layers is often a fully connected layer
    that outputs a transfer function of the matrix multiplication of the
    previous layer and it's edge weights.
    Also, for other types of neural networks such as convolutional neural
    networks, the network may have other layer types but ConnectionActivationLayers
    are a core, commonly used layer type.
    '''

    def __init__(self, fcn, fcn_p, num_in, num_out):
        Layer.__init__(self, num_in)
        self.FullyConnectedLayer = FullyConnectedLayer(
            num_in = num_in, num_out = num_out)

        self.ActivationLayer = ActivationLayer(
            fcn = fcn, derivative= fcn_p, num_in= num_out)

        self.act_vals = [0]*num_out
        self.num_out = num_out

    def propogate_forward(self, X):
        if X.shape[0] != self.num_in:
            print("error. Input X shape 1 is not self.num_in. Replace this error message")
            sys.exit(0)
        edge_output = self.FullyConnectedLayer.propogate_forward(X)
        self.act_vals = self.ActivationLayer.apply_trans_fcn(edge_output)

    @property
    def num_in(self):
        return self._num_in

    @num_in.setter
    def num_in(self, num_in):
        self._num_in = num_in

    @property
    def num_out(self):
        return self._num_out

    @num_out.setter
    def num_out(self, num_out):
        self._num_out = num_out

    @property
    def act_vals(self):
        return self._act_vals

    @act_vals.setter
    def act_vals(self, act_vals):
        self._act_vals = act_vals

    @property
    def FullyConnectedLayer(self):
        return self._FullyConnectedLayer

    @FullyConnectedLayer.setter
    def FullyConnectedLayer(self, FullyConnectedLayer):
        self._FullyConnectedLayer = FullyConnectedLayer

    @property
    def ActivationLayer(self):
        return self._ActivationLayer

    @ActivationLayer.setter
    def ActivationLayer(self, ActivationLayer):
        self._ActivationLayer = ActivationLayer

