class Layer(object):
    '''
    A layer is a parent class for the different layer types
    of a Neural FeedForwardNetwork
    '''
    def __init__(self, num_in, has_bias = False):
        self.num_in = num_in
        self.has_bias = has_bias


    @property
    def has_bias(self):
        return self._has_bias

    @has_bias.setter
    def has_bias(self, has_bias):
        self._has_bias = has_bias

    @property
    def num_in(self):
        return self._num_in

    @num_in.setter
    def num_in(self, num_in):
        if num_in < 1:
            raise ValueError("Layers need positive number of inputs")
        self._num_in = num_in