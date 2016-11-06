
class ActivationLayer():
    
    def __init__(self, fcn, width):
        self.trans_fcn = fcn
        self.width = width

    @property
    def trans_fcn(self):
        return self._trans_fcn

    @trans_fcn.setter
    def trans_fcn(self, fcn):
        self._trans_fcn = fcn

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    def apply_trans_fcn(self, vect):
        return self.trans_fcn(vect)

    def calc_act_vals(self, input):
        return

    def propogate_forward(self, X):
        return self.trans_fcn(X)
