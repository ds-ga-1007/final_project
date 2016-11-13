
from Model.Network.Layer import Layer

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
        return self.trans_fcn(vect)

    def apply_derivative_fcn(self, vect):
        return self.derivative_fcn(vect)

    @property
    def trans_fcn(self):
        return self._trans_fcn

    @trans_fcn.setter
    def trans_fcn(self, fcn):
        self._trans_fcn = fcn

    @property
    def derivative_fcn(self):
        return self._derivative_fcn

    @derivative_fcn.setter
    def derivative_fcn(self, derivative_fcn):
        self._derivative_fcn = derivative_fcn

    @property
    def num_in(self):
        return self._num_in

    @num_in.setter
    def num_in(self, num_in):
        self._num_in = num_in

