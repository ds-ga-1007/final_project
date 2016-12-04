
import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork import *


class TestUI(unittest.TestCase):

    def test_autoencoder_constructor(self):

        def get_shape(x):
            return x.FullyConnectedLayer.weights.shape

        X = np.ones((5, 5))
        for hidden_rep in range(1, 4):
            auto = AutoEncoder(X, hidden_dim=hidden_rep)
            layers = auto.neuralnetworklearner.network.layers
            transfer_size = (5 + hidden_rep)//2
            self.assertEqual(get_shape(layers[0]), (6, transfer_size))
            self.assertEqual(get_shape(layers[1]), (transfer_size+1, hidden_rep))
            self.assertEqual(get_shape(layers[2]), (hidden_rep+1, transfer_size))
            self.assertEqual(get_shape(layers[3]), (transfer_size+1, 5))

    def test_autoencoder_errors(self):

        X = np.ones((5, 5))
        with self.assertRaises(ValueError):
            AutoEncoder(X, hidden_dim=0)
        with self.assertRaises(ValueError):
            AutoEncoder(X, hidden_dim=-1)
        with self.assertRaises(ValueError):
            AutoEncoder([], hidden_dim=3)
        with self.assertRaises(ValueError):
            AutoEncoder('data', hidden_dim=3)
        with self.assertRaises(ValueError):
            AutoEncoder([1, 2], hidden_dim=3)

    def test_networkUI_constructor(self):

        UI = FeedForwardNetworkUI([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-3)
        self.assertEqual(UI.network.layers[0].FullyConnectedLayer.weights.shape, (3, 3))
        self.assertEqual(UI.network.layers[1].FullyConnectedLayer.weights.shape, (4, 1))
        self.assertEqual(UI.network.layers[1].ActivationLayer.trans_fcn, sigmoid)
        self.assertEqual(UI.network.layers[1].ActivationLayer.derivative_fcn, sigmoid_p)
        self.assertEqual(UI.network.loss_fcn.forward_fcn, mse)
        self.assertEqual(UI.network.reg_const, 1e-3)

        UI = FeedForwardNetworkUI([2, 3, 1], trans_fcns=['tanh', 'purelin'], loss_fcn='mse', reg_const=1e-3)
        self.assertEqual(UI.network.layers[0].ActivationLayer.trans_fcn, tanh)
        self.assertEqual(UI.network.layers[0].ActivationLayer.derivative_fcn, tanh_p)
        self.assertEqual(UI.network.layers[1].ActivationLayer.trans_fcn, purelin)
        self.assertEqual(UI.network.layers[1].ActivationLayer.derivative_fcn, purelin_p)

        FeedForwardNetworkUI([1, 3, 1])

    def test_networkUI_errors(self):
        with self.assertRaises(KeyError):
            FeedForwardNetworkUI([2, 3, 1], trans_fcns='sigmoid', loss_fcn=12, reg_const=1e-4)
        with self.assertRaises(ValueError):
            FeedForwardNetworkUI([2, 3, 1], trans_fcns=[], loss_fcn='mse', reg_const=1e-4)
        with self.assertRaises(ValueError):
            FeedForwardNetworkUI([2, -1, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-4)
        with self.assertRaises(ValueError):
            FeedForwardNetworkUI([], trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-4)
        with self.assertRaises(ValueError):
            FeedForwardNetworkUI([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=[1, 2])
        with self.assertRaises(TypeError):
            FeedForwardNetworkUI()

