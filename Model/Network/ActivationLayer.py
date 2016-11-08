from Model.Network.Layer import Layer

class ActivationLayer(Layer):
    
    def __init__(self, fcn, fcn_p, num_in):
        Layer.__init__(self, num_in, has_bias=True)
        self.trans_fcn = fcn
        self.trans_fcn_p = fcn_p
        self.num_in = num_in

    def apply_trans_fcn(self, vect):
        return self.trans_fcn(vect)

    def apply_trans_fcn_p(self, vect):
        return self.trans_fcn_p(vect)

    @property
    def trans_fcn(self):
        return self._trans_fcn

    @trans_fcn.setter
    def trans_fcn(self, fcn):
        self._trans_fcn = fcn

    @property
    def trans_fcn_p(self):
        return self._trans_fcn_p

    @trans_fcn_p.setter
    def trans_fcn_p(self, trans_fcn_p):
        self._trans_fcn_p = trans_fcn_p

    @property
    def num_in(self):
        return self._num_in

    @num_in.setter
    def num_in(self, num_in):
        self._num_in = num_in

