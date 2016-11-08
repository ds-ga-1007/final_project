
class ActivationLayer():
    
    def __init__(self, fcn, fcn_p, width):
        self.trans_fcn = fcn
        self.trans_fcn_p = fcn_p
        self.width = width

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
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

