import numpy as np

class NeuralNetworkLearner(object):
    def __init__(self, network, loss_fcn, learning_rate):
        self.network = network
        self.loss_fcn = loss_fcn
        self.learning_rate = learning_rate

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    @property
    def loss_fcn(self):
        return self._loss_fcn

    @loss_fcn.setter
    def loss_fcn(self, loss_fcn):
        self._loss_fcn = loss_fcn

    @property
    def learning_rate(self):
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, learning_rate):
        self._learning_rate = learning_rate

    def train_one_epoch(self, X, Y):
        self.network.feed_forward(X)
