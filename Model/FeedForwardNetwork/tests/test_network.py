import copy
import unittest
from Model.FeedForwardNetApps import *
from Model.FeedForwardNetwork import *
from Model.FeedForwardNetwork.NetworkLayers import *

trans_fcns = {
              'sigmoid': NetworkFunction(sigmoid, sigmoid_p),
              'tanh': NetworkFunction(tanh, tanh_p),
              'purelin': NetworkFunction(purelin, purelin_p)
              }

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
        pass

    def test_network_learner_constructor(self):
        pass