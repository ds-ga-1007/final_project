
class NetworkFunction(object):
    '''
    FeedForwardNetwork functions are used to represent transfer functions
    and performance functions. Each NetworkFunction requires
    a forward activation function and a derivative function.
    '''
    def __init__(self, forward, derivative):

        self.forward_fcn = forward
        self.derivative_fcn = derivative

    @property
    def forward_fcn(self):
        return self._forward_fcn

    @forward_fcn.setter
    def forward_fcn(self, fcn):

        if not callable(fcn):
            raise TypeError("Network Function forward functions must be callable")

        self._forward_fcn = fcn

    @property
    def derivative_fcn(self):
        return self._derivative_fcn

    @derivative_fcn.setter
    def derivative_fcn(self, derivative_fcn):

        if not callable(derivative_fcn):
            raise TypeError("Network Function derivative functions must be callable")

        self._derivative_fcn = derivative_fcn
