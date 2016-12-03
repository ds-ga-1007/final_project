import types
from Model.FeedForwardNetwork.NetworkLayers.Layer import Layer
from Model.FeedForwardNetwork import NetworkFunction
import numpy as np

class ActivationLayer(Layer):
    '''
    Activation Layers are used to represent a Layer that applies
    an activation function. Each Activation Layer therefore needs
    a transfer function trans_fcn and a function derivative derivative_fcn.
    '''
    
    def __init__(self, fcn, derivative, num_in):
        Layer.__init__(self, num_in, has_bias=True)
        self.trans_fcn = fcn
        self.derivative_fcn = derivative
        self.num_in = num_in

    def apply_trans_fcn(self, vect):
        if len(vect) != self.num_in or not isinstance(vect[0], np.float):
            raise ValueError("Activation Layer is not a num_in vector")
        return self.trans_fcn(vect)

    def apply_derivative_fcn(self, vect):
        if len(vect) != self.num_in or not isinstance(vect[0], np.float):
            raise ValueError("Activation Layer is not a num_in vector")
        return self.derivative_fcn(vect)

    @property
    def trans_fcn(self):
        return self._trans_fcn

    @trans_fcn.setter
    def trans_fcn(self, fcn):
        if not isinstance(fcn, types.FunctionType):
            raise TypeError("transfer functions of activation layers must be a function")
        self._trans_fcn = fcn

    @property
    def derivative_fcn(self):
        return self._derivative_fcn

    @derivative_fcn.setter
    def derivative_fcn(self, derivative_fcn):
        if not isinstance(derivative_fcn, types.FunctionType):
            raise TypeError("deritive functions of activation layers must be a function")

        self._derivative_fcn = derivative_fcn
