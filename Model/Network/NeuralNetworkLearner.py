import numpy as np
import copy

class NeuralNetworkLearner(object):
    def __init__(self, network, learning_rate):
        self.network = network
        self.learning_rate = learning_rate

    def run_epochs(self, X, Y, epochs = 10):
        for _ in range(epochs):
            self._run_one_epoch(X, Y)

    def _run_one_epoch(self, X, Y):
        self.network.train_one_epoch(X, Y)
        self.network.update_weights()
        error = self.network.evaluate_error(X, Y)
        if error > self.best_network['error']:
            pass

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

    #Should I code it this way? I would rather use evaluate error, but that has hidden
    #effects, or whatever the professor called it.


