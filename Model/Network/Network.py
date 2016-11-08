import numpy as np
from Model.Network.ConnectionActivationLayer import ConnectionActivationLayer
from Model import utils

class Network(object):
    def __init__(self, layer_sizes, trans_fcns, loss_fcn):
        trans_fcns = utils.get_trans(trans_fcns = trans_fcns, num_layers = len(layer_sizes) - 1)
        self.loss_fcn = utils.get_loss(loss_fcn)
        self._set_layers(trans_fcns, layer_sizes)

    def _set_layers(self, trans_fcns, layer_sizes):
        self.layers = []
        self.layer_sizes = layer_sizes
        self.trans_fcns = trans_fcns
        self.num_layers = len(layer_sizes)
        self.deltas = []
        self._init_layers()

    def _init_layers(self):
        for layer_idx in range(self.num_layers - 1):
            self._add_one_layer(layer_idx)

    def _add_one_layer(self, layer_idx):
        #The connection input size is the previous layer size plus one for the bias term
        num_in = self.layer_sizes[layer_idx] + 1
        num_out = self.layer_sizes[layer_idx+1]
        fcn = self._get_one_trans_fcn(layer_idx)
        self.add_one_layer_and_associated_delta(fcn, num_in, num_out)

    def _get_one_layer_size(self, idx):
        return self.layer_sizes[idx]

    def _get_one_trans_fcn(self, idx):
        return self.trans_fcns[idx]

    def add_one_layer_and_associated_delta(self, fcn, num_in, num_out):
        layer = ConnectionActivationLayer(fcn = fcn.trans_fcn, fcn_p = fcn.trans_fcn_p,
                            num_in = num_in, num_out = num_out)
        self._layers.append(layer)
        delta_placeholder = np.zeros(num_out)
        self._deltas.append(delta_placeholder)

    def feed_forward(self, X):
        act_vals = X
        for layer in self.layers:
            layer.propogate_forward(utils.vect_with_bias(act_vals))
            act_vals = layer.act_vals

    def _compute_layer_derivative(self, idx):

        fullyconnectedlayer = self.layers[idx - 1].FullyConnectedLayer
        weight_vals = fullyconnectedlayer.get_weights_except_bias()

        act_layer = self.layers[idx - 1].ActivationLayer
        trans_prime = act_layer.trans_fcn_p
        act_values_previous_layer = self.layers[idx-1].act_vals
        derivative_of_previous_activations = trans_prime(act_values_previous_layer)

        return weight_vals.T * derivative_of_previous_activations

    def prop_back_one_layer(self, delta_idx):
        error_mat = np.dot(self.deltas[delta_idx],
                        self._compute_layer_derivative(delta_idx - 1))
        error =  np.sum(error_mat)
        self.deltas[delta_idx - 1] = error

    def backpropagate(self, error):
        self.deltas[-1] = error
        for delta_idx in range(len(self.deltas) - 1, 0, -1):
            self.prop_back_one_layer(delta_idx)

    def predict(self, X):
        self.feed_forward(X)
        return self.layers[-1].act_vals

    def train_one_epoch(self, X, Y):
        for xi, yi in zip(X, Y):
            self.feed_forward(xi)
            yhat = self.layers[-1].act_vals
            error = self.loss_fcn.trans_fcn(yhat, yi)
            self.backpropagate(error)

    def evaluate_error(self, X, Y):
        self.feed_forward(X)
        yhat = self.layers[-1].act_vals
        error = self.loss_fcn.trans_fcn(yhat, Y)
        return error

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
    def layer_sizes(self):
        return self._layer_sizes

    @layer_sizes.setter
    def layer_sizes(self, layer_sizes):
        self._layer_sizes = layer_sizes

    @property
    def trans_fcns(self):
        return self._trans_fcns

    @trans_fcns.setter
    def trans_fcns(self, trans_fcns):
        self._trans_fcns = trans_fcns

    @property
    def deltas(self):
        return self._deltas

    @deltas.setter
    def deltas(self, deltas):
        self._deltas = deltas

    @property
    def loss_fcn(self):
        return self._loss_fcn

    @loss_fcn.setter
    def loss_fcn(self, loss_fcn):
        self._loss_fcn = loss_fcn
