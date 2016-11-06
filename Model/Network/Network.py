from Model.Network.ConnectionActivationLayer import ConnectionActivationLayer

class network(object):
    def __init__(self, trans_fcns, layer_sizes):
        self._set_layers(trans_fcns, layer_sizes)

    def _set_layers(self, trans_fcns, layer_sizes):
        self.layers = []
        self.layers_sizes = layer_sizes
        self.trans_fcns = trans_fcns
        self.num_layers = layer_sizes.shape[1]
        self._init_layers()

    def _init_layers(self):
        for layer_idx in range(self._get_num_layers() - 1):
            self._add_one_layer(layer_idx)

    def _add_one_layer(self, layer_idx):
        num_in = self._get_one_layer_size(layer_idx)
        num_out = self._get_one_layer_size(layer_idx+1)
        fcn = self._get_one_trans_fcn(layer_idx)
        self.add_one_layer(fcn, num_in, num_out)

    def _get_one_layer_size(self, idx):
        return self._layer_sizes[idx]

    def _get_one_trans_fcn(self, idx):
        return self._get_trans_fcns()[idx]

    def add_one_layer(self, fcn, num_in, num_out):
        self.layers.append(ConnectionActivationLayer(fcn = fcn, num_in = num_in, num_out = num_out)

    def feed_forward(self, X):
        act_vals = X
        for layer in self.layers:
            layer.propogate_forward(act_vals)
            act_vals = layer.act_vals

    def feed_forward_one_layer(self, layer, act_vals):

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, layers):
        self._layers = layers

    @property
    def num_layers(self):
        return self._num_layers

    @num_layers.setter
    def num_layers(self, num_layers):
        self._num_layers = num_layers

    @property
    def layers_sizes(self):
        return self._layers_sizes

    @layers_sizes.setter
    def layers_sizes(self, layers_sizes):
        self._layers_sizes = layers_sizes

    @property
    def trans_fcns(self):
        return self._trans_fcns

    @trans_fcns.setter
    def trans_fcns(self, trans_fcns):
        self._trans_fcns = trans_fcns
