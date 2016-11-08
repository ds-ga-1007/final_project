class Layer(object):
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
        self._num_in = num_in
