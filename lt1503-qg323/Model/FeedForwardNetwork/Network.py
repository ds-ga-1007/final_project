import numpy as np
import numbers

from Model.FeedForwardNetwork import utils
from Model.FeedForwardNetwork.NetworkFunction import NetworkFunction
from Model.FeedForwardNetwork.NetworkLayers.ConnectionActivationLayer import ConnectionActivationLayer


class Network(object):
    '''
    A network object represents an Artifical Neural FeedForwardNetwork. It is able to
    forward propogate inputs to calculate outputs, evaluate the error of those outputs,
     and can backward propogate known errors to compute error derivatives
    with respect to every layer.
    '''

    def __init__(self, layer_sizes, trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-3):
        """
        Feed Forward Neural Network constructor
        :param layer_sizes: list of integers. Represents the layer sizes of the network structure
        :param trans_fcns: String or list of strings. If a list, must be same legnth as layer_sizes
        :param loss_fcn: String representation of a loss function
        :param reg_const: Numeric value used to regularize the network during training.
            Must be non-negative. 0 corresponds to no regularization.
        """
        self.reg_const = reg_const
        trans_fcns = utils.get_trans(trans_fcns = trans_fcns, num_layers =len(layer_sizes) - 1)
        self.loss_fcn = utils.get_loss(loss_fcn)
        self._init_layers_and_deltas(trans_fcns, layer_sizes)

    def _init_layers_and_deltas(self, trans_fcns, layer_sizes):
        """
        Initialize layers and corresponding deltas for a network
        :param trans_fcns: list of NetworkFunctions for forward and backward propoagation
        :param layer_sizes: width of layers of the network
        :return: None
        """
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
        """
        For initialization, initializes the layer_idx layer within the network
        :param layer_idx: int-like, represents the layer
        :return: None
        """
        try:
            layer_idx = int(layer_idx)
        except ValueError:
            raise ValueError('network._add_one_layer(layer_idx) only accepts integer layer indexes')

        #The connection input size is the previous layer size plus one for the bias term
        num_in = self.layer_sizes[layer_idx] + 1
        num_out = self.layer_sizes[layer_idx+1]
        if num_in < 1 or num_out < 1:
            raise ValueError("layers must have strictly positive nodes at each layer")
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

    def _feed_forward(self, xi):

        act_vals = xi
        for layer in self.layers:
            layer.propogate_forward(utils.vect_with_bias(act_vals))
            act_vals = layer.act_vals

    def _layer_derivative(self, idx):
        """
        Calculate the derivitive of the idx layer of the network, from the
        activation values of the previous layer and the weight values.
        :param idx:
        :return: numpy.ndarray of the np.float values, length of the idx layer of the network,
        """

        fullyconnectedlayer = self.layers[idx].FullyConnectedLayer
        weight_vals = fullyconnectedlayer.get_weights_except_bias()

        prev_layer = self.layers[idx-1]
        trans_prime = prev_layer.ActivationLayer.derivative_fcn
        act_values_previous_layer = prev_layer.act_vals
        derivative_of_previous_activations = trans_prime(act_values_previous_layer)

        error_matrix_for_layer_nodes = weight_vals.T * derivative_of_previous_activations
        return np.sum(error_matrix_for_layer_nodes, 0)

    def _prop_back_one_layer(self, delta_idx):
        """
        Backpropogate the error one layer, from the delta_idx layer to the previous layer.
        :param delta_idx: int-like. Represents the index in the network
            of which layer to backpropogate error from
        :return: None
        """
        fullyconnectedlayer = self.layers[delta_idx].FullyConnectedLayer
        edge_weights = fullyconnectedlayer.get_weights_except_bias()
        forward_error = self.layer_deltas[delta_idx]
        edge_error = edge_weights * forward_error
        self.layer_deltas[delta_idx - 1] = np.sum(edge_error, 1)

    def _backpropagate(self, error):

        self.layer_deltas[-1] = error
        for delta_idx in range(len(self.layer_deltas) - 1, 0, -1):
            self._prop_back_one_layer(delta_idx)


    def predict(self, xi):
        """
        Predict output based on input xi
        :param X: numpy.ndarray of input activations
        :return: np.ndarray of activations of the last layer
            corresponding to input xi
        """

        self._feed_forward(xi)
        return self.layers[-1].act_vals

    def evaluate_error(self, X, Y):
        """
        self evaluate the error of the current network
        by evaluate the learner's loss function of the predicted yhat
        and the true Y values
        :param X: numpy.ndarray of input activations
        :param Y: np.ndarray of true output values
        :return: numeric loss function evaluated between the predicted
            and correct output activation valuess
        """

        self._feed_forward(X)
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

        if num_layers < 1:
            raise ValueError("Neural Networks must have at least one layer")

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

        if not isinstance(loss_fcn, NetworkFunction):
            raise ValueError("loss function must be a NetworkFunction")

        self._loss_fcn = loss_fcn

    @property
    def reg_const(self):
        return self._reg_const

    @reg_const.setter
    def reg_const(self, reg_const):

        if not isinstance(reg_const, numbers.Number):
            raise ValueError("regularization constant must be a number")

        if reg_const < 0:
            raise ValueError("regularization constant must be non-negative")

        self._reg_const = reg_const
