import numpy as np

from Model.FeedForwardNetwork import utils


class NeuralNetworkLearner(object):
    '''
    A neural network learner is the trainer for a neural network. It forward and backward
    propagates errors within its FeedForwardNetwork, and updates the network layer weights according
    to the error derivatives in accordance with the learners learning algorithm.

    '''
    def __init__(self, network, learning_rate = 0.01, learn_alg = utils.MOMENTUM_BP, loss_fcn='mse'):
        self.network = network
        self.learning_rate = learning_rate
        self.learn_alg = learn_alg
        self.loss_fcn = utils.get_loss(loss_fcn)

        self.layer_sizes = network.layer_sizes
        self.num_layers = network.num_layers

        self._init_delta_layers()


    def _init_delta_layers(self):
        self.weight_deltas = []
        self.weight_velocity = []

        for layer_index in range(self.num_layers - 1):
            num_in, num_out = self.get_delta_layer_size(layer_index)
            self._add_one_delta_layer(num_in, num_out)

    def get_delta_layer_size(self, layer_index):
        #The connection input size is the previous layer size plus one for the bias term
        num_in = self.layer_sizes[layer_index] + 1
        num_out = self.layer_sizes[layer_index+1]
        return (num_in, num_out)

    def _add_one_delta_layer(self, num_in, num_out):
        weight_delta_placeholder = np.zeros([num_in, num_out])
        weight_velocity_placeholder = np.zeros([num_in, num_out])
        self._weight_deltas.append(weight_delta_placeholder)
        self.weight_velocity.append(weight_velocity_placeholder)


    def run_epochs(self, X, Y, epochs = 10):
        for _ in range(epochs):
            self._run_one_epoch(X, Y)

    def _run_one_epoch(self, X, Y):
        self.train_one_epoch(X, Y)
        #error = self.network.evaluate_error(X, Y)
        #if error > self.best_network['error']:
        #    pass




    def get_weight_deltas_for_active_algorithm(self, old_weights, backprop_error):
        if self.learn_alg == utils.GRADIENT_DESCENT:
            return backprop_error

        if self.learn_alg == utils.MOMENTUM_BP:
            return old_weights * utils.MOMENTUM_DECAY + backprop_error

    def _update_deltas_active_algorithm(self, layer_index, old_weights, backprop_error):

        if self.learn_alg == utils.GRADIENT_DESCENT:

            updated_weight_deltas = self.get_weight_deltas_for_active_algorithm(
                                        old_weights = old_weights,
                                        backprop_error = backprop_error)
            self.weight_deltas[layer_index] = updated_weight_deltas

        if self.learn_alg == utils.MOMENTUM_BP:

            past_velocity = self.weight_velocity[layer_index]
            force_on_weights = backprop_error
            new_velocity = past_velocity * utils.MOMENTUM_DECAY + force_on_weights
            self.weight_velocity[layer_index] = new_velocity
            self.weight_deltas[layer_index] = self.weight_velocity[layer_index]

    def _get_weight_error_with_reg(self, layer_index, layer_activation_with_bias):

            output_gradient = self.layer_deltas[layer_index]
            current_edge_weight_values = self.layers[layer_index].FullyConnectedLayer.weights
            weight_error = utils.get_weight_error(
                            input_activation = layer_activation_with_bias,
                            output_gradient = output_gradient)
            return weight_error + self.reg_const * current_edge_weight_values.T

    def _calc_edge_deltas(self, X):

        layer_activation_with_bias = utils.vect_with_bias(X)
        for layer_index in range(self.num_layers - 1):

            weight_error_with_reg = self._get_weight_error_with_reg(
                                            layer_index, layer_activation_with_bias)

            self._update_deltas_active_algorithm(
                                        layer_index = layer_index,
                                        old_weights = self.weight_deltas[layer_index],
                                        backprop_error = weight_error_with_reg.T)

            updated_weight_deltas = self.get_weight_deltas_for_active_algorithm(
                                        old_weights = self.weight_deltas[layer_index],
                                        backprop_error = weight_error_with_reg.T)

            self.weight_deltas[layer_index] = updated_weight_deltas


            layer_activation = self.layers[layer_index].act_vals
            layer_activation_with_bias = utils.vect_with_bias(layer_activation)

    def _update_weights_current_algorithm(self):
        for idx in range(len(self.layers)):
            fullyconnectedlayer = self.layers[idx].FullyConnectedLayer
            weights = fullyconnectedlayer.weights
            delta_update = self.weight_deltas[idx]
            fullyconnectedlayer.weights = weights - delta_update * self.learning_rate

    def _update_weights(self, X):
        self._calc_edge_deltas(X)
        self._update_weights_current_algorithm()

    def train_one_epoch(self, X, Y):
        for xi, yi in zip(X, Y):
            self.network.feed_forward(xi)
            yhat = self.layers[-1].act_vals
            error_derivative = self.loss_fcn.derivative_fcn(yhat, yi)
            self.network.backpropagate(error_derivative)
            self._update_weights(xi)








    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    @property
    def learning_rate(self):
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, learning_rate):
        self._learning_rate = learning_rate

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
    def layers(self):
        return self.network.layers

    @property
    def reg_const(self):
        return self.network.reg_const

    @property
    def layer_deltas(self):
        return self.network.layer_deltas

    #Should I code it this way? I would rather use evaluate error, but that has hidden
    #effects, or whatever the professor called it.


