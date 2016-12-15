import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork import *
from Model.FeedForwardNetwork.NetworkLayers import *

class TestNetworkFunction(unittest.TestCase):
    """
    Tests for functionality of the NetworkFunction class
    """

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

    def test_network_function_errors(self):

        purelinfcn = trans_fcns['purelin']
        sigfcn = trans_fcns['sigmoid']

        with self.assertRaises(TypeError):
            NetworkFunction(purelinfcn, sigfcn)
        with self.assertRaises(TypeError):
            NetworkFunction(2, sigfcn.derivative_fcn)
        with self.assertRaises(TypeError):
            NetworkFunction(purelinfcn.forward_fcn, sigfcn)
        with self.assertRaises(TypeError):
            NetworkFunction(purelinfcn.forward_fcn, [])
