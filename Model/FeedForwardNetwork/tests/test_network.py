import copy
import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork import *
from Model.FeedForwardNetwork.NetworkLayers import *

class TestNetwork(unittest.TestCase):

    def test_network_function(self):

        sigfcn = trans_fcns['sigmoid']
        self.assertTrue(sigfcn.forward_fcn is sigmoid)
        self.assertTrue(sigfcn.derivative_fcn is sigmoid_p)
        self.assertEqual(sigfcn.forward_fcn(0), 0.5)
        self.assertEqual(sigfcn.derivative_fcn(0), 0.25)

        tanhfcn = trans_fcns['tanh']
        self.assertTrue(tanhfcn.forward_fcn is tanh)
        self.assertTrue(tanhfcn.derivative_fcn is tanh_p)
        self.assertEqual(tanhfcn.forward_fcn(0), 0)
        self.assertEqual(tanhfcn.derivative_fcn(0), 1)

        purelinfcn = trans_fcns['purelin']
        self.assertTrue(purelinfcn.forward_fcn is purelin)
        self.assertTrue(purelinfcn.derivative_fcn is purelin_p)
        self.assertEqual(purelinfcn.forward_fcn(2), 2)
        self.assertEqual(purelinfcn.derivative_fcn(2), -1)

    def test_network_constructor(self):

        network = Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-3)
        self.assertEqual(network.layers[0].FullyConnectedLayer.weights.shape, (3, 3))
        self.assertEqual(network.layers[1].FullyConnectedLayer.weights.shape, (4, 1))
        self.assertEqual(network.layers[1].ActivationLayer.trans_fcn, sigmoid)
        self.assertEqual(network.layers[1].ActivationLayer.derivative_fcn, sigmoid_p)
        self.assertEqual(network.loss_fcn.forward_fcn, mse)
        self.assertEqual(network.reg_const, 1e-3)

        network = Network([2, 3, 1], trans_fcns=['tanh', 'purelin'], loss_fcn='mse', reg_const=1e-3)
        self.assertEqual(network.layers[0].ActivationLayer.trans_fcn, tanh)
        self.assertEqual(network.layers[0].ActivationLayer.derivative_fcn, tanh_p)
        self.assertEqual(network.layers[1].ActivationLayer.trans_fcn, purelin)
        self.assertEqual(network.layers[1].ActivationLayer.derivative_fcn, purelin_p)

        Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=np.float(1.1))
        Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=np.int(1))
        Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=1.1)
        Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=0)

    def test_network_errors(self):
        with self.assertRaises(KeyError):
            Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn=12, reg_const=1e-4)
        with self.assertRaises(ValueError):
            Network([2, 3, 1], trans_fcns=[], loss_fcn='mse', reg_const=1e-4)
        with self.assertRaises(ValueError):
            Network([2, -1, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-4)
        with self.assertRaises(ValueError):
            Network([], trans_fcns='sigmoid', loss_fcn='mse', reg_const=1e-4)
        with self.assertRaises(ValueError):
            Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const='number')
        with self.assertRaises(ValueError):
            Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=-1)
        with self.assertRaises(ValueError):
            Network([2, 3, 1], trans_fcns='sigmoid', loss_fcn='mse', reg_const=[1, 2])
        with self.assertRaises(TypeError):
            Network()

    def test_network_learner_constructor(self):
        pass