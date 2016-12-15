import unittest
from Model.FeedForwardNetwork import *

class TestLayers(unittest.TestCase):
    """Tests for Layer classes"""

    def test_Act_layer_constructor(self):

        actlayer = ActivationLayer(sigmoid, sigmoid_p, 3)
        self.assertEqual(actlayer.trans_fcn, sigmoid)
        self.assertEqual(actlayer.derivative_fcn, sigmoid_p)
        self.assertEqual(actlayer.num_in, 3)

    def test_connected_layer_constructor(self):

        fullyconnectedlayer = FullyConnectedLayer(num_in= 2, num_out = 2)
        shape_sans_bias = fullyconnectedlayer.get_weights_except_bias().shape
        self.assertEqual(shape_sans_bias, (1, 2))
        self.assertEqual(fullyconnectedlayer.weights.shape, (2, 2))


    def test_ConnAct_layer_constructor(self):

        conn_act_layer = ConnectionActivationLayer(tanh, tanh_p, 2, 2)
        self.assertEqual(conn_act_layer.ActivationLayer.trans_fcn, tanh)
        self.assertEqual(conn_act_layer.ActivationLayer.derivative_fcn, tanh_p)
        self.assertEqual(conn_act_layer.ActivationLayer.num_in, 2)

        conn_act_FC_layer = conn_act_layer.FullyConnectedLayer
        shape_sans_bias = conn_act_FC_layer.get_weights_except_bias().shape
        self.assertEqual(shape_sans_bias, (1, 2))
        self.assertEqual(conn_act_layer.FullyConnectedLayer.weights.shape, (2, 2))


    def test_Act_layer_functionality(self):

        actlayer = ActivationLayer(sigmoid, sigmoid_p, 3)
        output = actlayer.apply_trans_fcn(np.ones(3))
        self.assertTrue(output.ndim == 1)
        self.assertTrue(output.shape[0] == 3)

        derivative = actlayer.apply_derivative_fcn(np.ones(3))
        self.assertTrue(derivative.ndim == 1)
        self.assertTrue(derivative.shape[0] == 3)

    def test_connected_layer_functionality(self):

        fullyconnectedlayer = FullyConnectedLayer(num_in= 2, num_out = 2)
        fullyconnectedlayer.weights = np.array([[1, 0], [0, -1]])
        output = fullyconnectedlayer.propogate_forward(np.ones(2))
        self.assertTrue(output.shape[0] == 2)
        self.assertTrue(output.ndim == 1)
        self.assertEqual(output[0], 1)
        self.assertEqual(output[1], -1)


    def test_ConnAct_layer_functionality(self):

        conn_act_layer = ConnectionActivationLayer(tanh, tanh_p, 2, 2)
        conn_act_layer.FullyConnectedLayer.weights = np.ones((2,2))
        conn_act_layer.propogate_forward(np.ones(2))
        conn_act_output = conn_act_layer.act_vals

        fullyconnectedlayer = FullyConnectedLayer(num_in= 2, num_out = 2)
        fullyconnectedlayer.weights = np.ones((2, 2))
        actlayer = ActivationLayer(tanh, tanh_p, 2)

        fc_output = fullyconnectedlayer.propogate_forward(np.ones(2))
        act_output = actlayer.apply_trans_fcn(fc_output)

        self.assertEqual(conn_act_output[0], act_output[0])
        self.assertEqual(conn_act_output[1], act_output[1])

    def test_negative_node_errors(self):

        with self.assertRaises(ValueError):
            FullyConnectedLayer(num_in=2, num_out=-3)
        with self.assertRaises(ValueError):
            FullyConnectedLayer(num_in=-2, num_out=3)
        with self.assertRaises(ValueError):
            ActivationLayer(sigmoid, sigmoid_p, -2)
        with self.assertRaises(ValueError):
            ConnectionActivationLayer(tanh, tanh_p, 2, -2)
        with self.assertRaises(ValueError):
            ConnectionActivationLayer(tanh, tanh_p, -2, 2)

    def test_non_NetworkFunction_errors(self):

        with self.assertRaises(TypeError):
            ActivationLayer(sigmoid, 10, 2)
        with self.assertRaises(TypeError):
            ActivationLayer([], sigmoid_p, 2)
        with self.assertRaises(TypeError):
            ActivationLayer('sigmoid', sigmoid_p, 2)
        with self.assertRaises(TypeError):
            ConnectionActivationLayer(sigmoid, 10, 2)
        with self.assertRaises(TypeError):
            ConnectionActivationLayer([], sigmoid_p, 2)
        with self.assertRaises(TypeError):
            ConnectionActivationLayer('tanh', sigmoid_p, 2)

    def test_FC_layer_error(self):

        fullyconnectedlayer = FullyConnectedLayer(num_in= 2, num_out = 3)
        with self.assertRaises(ValueError):
            fullyconnectedlayer.propogate_forward(np.ones(3))
        with self.assertRaises(ValueError):
            fullyconnectedlayer.propogate_forward(np.ones((2, 3)))
        with self.assertRaises(ValueError):
            fullyconnectedlayer.propogate_forward([])

    def test_act_layer_error(self):

        activationLayer = ActivationLayer(sigmoid, sigmoid_p, 2)
        with self.assertRaises(ValueError):
            activationLayer.apply_trans_fcn(np.ones(4))
        with self.assertRaises(ValueError):
            activationLayer.apply_trans_fcn(np.ones((2, 3)))
        with self.assertRaises(ValueError):
            activationLayer.apply_trans_fcn([])
        with self.assertRaises(ValueError):
            activationLayer.apply_derivative_fcn(np.ones(3))
        with self.assertRaises(ValueError):
            activationLayer.apply_derivative_fcn(np.ones((2, 3)))
        with self.assertRaises(ValueError):
            activationLayer.apply_derivative_fcn([])

    def test_conn_act_layer_error(self):

        conn_act_layer = ConnectionActivationLayer(purelin, purelin_p, 2, 2)
        with self.assertRaises(ValueError):
            conn_act_layer.propogate_forward(np.ones(3))
        with self.assertRaises(ValueError):
            conn_act_layer.propogate_forward(np.ones((2, 3)))
        with self.assertRaises(ValueError):
            conn_act_layer.propogate_forward([])

