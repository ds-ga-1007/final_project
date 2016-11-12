import numpy as np
from Model.Network.ConnectionActivationLayer import ConnectionActivationLayer
from Model import utils

class Network(object):
    def __init__(self, layer_sizes, trans_fcns='sigmoid', loss_fcn='mse', reg_const = 1e-3,
                 learn_alg = utils.MOMENTUM_BP, learning_rate = 0.01):
        self.learning_rate = learning_rate
        self.reg_const = reg_const
        trans_fcns = utils.get_trans(trans_fcns = trans_fcns, num_layers = len(layer_sizes) - 1)
        self.loss_fcn = utils.get_loss(loss_fcn)
        self._init_layers_and_deltas(trans_fcns, layer_sizes)
        self.learn_alg = learn_alg

    def _init_layers_and_deltas(self, trans_fcns, layer_sizes):
        self.layers = []
        self.layer_sizes = layer_sizes
        self.trans_fcns = trans_fcns
        self.num_layers = len(layer_sizes)
        self.layer_deltas = []
        self.weight_deltas = []
        self.weight_velocity = []
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

    def add_one_layer_and_associated_delta(self, fcn, num_in, num_out):
        layer = ConnectionActivationLayer(fcn = fcn.forward_fcn, fcn_p = fcn.derivative_fcn,
                                          num_in = num_in, num_out = num_out)
        self._layers.append(layer)
        layer_delta_placeholder = np.zeros(num_out)
        weight_delta_placeholder = np.zeros([num_in, num_out])
        weight_velocity_placeholder = np.zeros([num_in, num_out])
        self._layer_deltas.append(layer_delta_placeholder)
        self._weight_deltas.append(weight_delta_placeholder)
        self.weight_velocity.append(weight_velocity_placeholder)

    def feed_forward(self, X):
        act_vals = X
        for layer in self.layers:
            layer.propogate_forward(utils.vect_with_bias(act_vals))
            act_vals = layer.act_vals

    def _layer_derivative(self, idx):

        fullyconnectedlayer = self.layers[idx].FullyConnectedLayer
        weight_vals = fullyconnectedlayer.get_weights_except_bias()

        prev_layer = self.layers[idx-1]
        trans_prime = prev_layer.ActivationLayer.derivative_fcn
        act_values_previous_layer = prev_layer.act_vals
        derivative_of_previous_activations = trans_prime(act_values_previous_layer)

        error_matrix_for_layer_nodes = weight_vals.T * derivative_of_previous_activations
        return np.sum(error_matrix_for_layer_nodes, 0)

    def prop_back_one_layer(self, delta_idx):
        fullyconnectedlayer = self.layers[delta_idx].FullyConnectedLayer
        edge_weights = fullyconnectedlayer.get_weights_except_bias()
        forward_error = self.layer_deltas[delta_idx]
        edge_error = edge_weights * forward_error
        self.layer_deltas[delta_idx - 1] = np.sum(edge_error, 1)

    def backpropagate(self, error):
        self.layer_deltas[-1] = error
        for delta_idx in range(len(self.layer_deltas) - 1, 0, -1):
            self.prop_back_one_layer(delta_idx)


    def predict(self, X):
        self.feed_forward(X)
        return self.layers[-1].act_vals

    def evaluate_error(self, X, Y):
        self.feed_forward(X)
        yhat = self.layers[-1].act_vals
        error = self.loss_fcn.forward_fcn(yhat, Y)
        return error


    def _get_one_layer_size(self, idx):
        return self.layer_sizes[idx]

    def _get_one_trans_fcn(self, idx):
        return self.trans_fcns[idx]

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
    def layer_deltas(self):
        return self._layer_deltas

    @layer_deltas.setter
    def layer_deltas(self, layer_deltas):
        self._layer_deltas = layer_deltas

    @property
    def weight_deltas(self):
        return self._weight_deltas

    @weight_deltas.setter
    def weight_deltas(self, weight_deltas):
        self._weight_deltas = weight_deltas

    @property
    def weight_velocity(self):
        return self._weight_velocity

    @weight_velocity.setter
    def weight_velocity(self, weight_velocity):
        self._weight_velocity = weight_velocity

    @property
    def loss_fcn(self):
        return self._loss_fcn

    @loss_fcn.setter
    def loss_fcn(self, loss_fcn):
        self._loss_fcn = loss_fcn

    @property
    def reg_const(self):
        return self._reg_const

    @reg_const.setter
    def reg_const(self, reg_const):
        self._reg_const = reg_const

    @property
    def learn_alg(self):
        return self._learn_alg

    @learn_alg.setter
    def learn_alg(self, learn_alg):
        self._learn_alg = learn_alg


    @property
    def learning_rate(self):
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, learning_rate):
        self._learning_rate = learning_rate
