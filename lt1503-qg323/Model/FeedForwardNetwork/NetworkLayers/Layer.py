class Layer(object):
    '''
    Parent class for all Layers.

    Parameters
    ----------
    num_in : integer representing the number of nodes into a layer instance
    has_bias : boolean representing if the layer contains a bias term
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
