

class NetworkFunction(object):
    def __init__(self, trans, trans_p):
        self.trans_fcn = trans
        self.trans_fcn_p = trans_p

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
