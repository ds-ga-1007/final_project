from Model.Network.ActivationLayer import ActivationLayer
from Model.Network.FullyConnectedLayer import FullyConnectionLayer
import sys

class ConnectionActivationLayer(object):

    def __init__(self, fcn, num_in, num_out):
        self.FullyConnectedLayer = FullyConnectionLayer(
            num_in = num_in, num_out = num_out)

        self.ActivationLayer = ActivationLayer(
            fcn = fcn, num_out = num_out)

        self.act_vals = [0]*num_out

        self.num_in = num_in
        self.num_out = num_out

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

    def propogate_forward(self, X):
        if X.shape[1] != self.num_in:
            print("error. Input X shape 1 is not self.num_in. Replace this error message")
            sys.exit(0)
        self.act_vals = self.ActivationLayer.propogate_forward(
            self.FullyConnectedLayer.propogate_forward(X))
