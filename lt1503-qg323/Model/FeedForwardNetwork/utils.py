
import numpy as np
from Model.FeedForwardNetwork.NetworkFunction import NetworkFunction

GRADIENT_DESCENT = 0
MOMENTUM_BP = 1

TRAINING_ALGORITHMS = {GRADIENT_DESCENT,
                       MOMENTUM_BP}

MOMENTUM_DECAY = 0.99

STOP_TRAIN = -1

def vect_with_bias(nparr):
    return np.concatenate([nparr, [1]])

def get_weight_error(input_activation, output_gradient):
    return np.atleast_2d(input_activation) * np.atleast_2d(output_gradient).T

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(np.clip(-x, -50, 50)))


def sigmoid_p(x):
    return sigmoid(x) * (1.0 - sigmoid(x))


def tanh(x):
    return np.tanh(x)


def tanh_p(x):
    return 1.0 - x ** 2


def purelin(x):
    return x


def purelin_p(x):
    return -1


def mse(Y, a):
    return np.sum(np.square(Y - a))


def mse_p(Y, a):
    return (Y - a)

trans_fcns = {
              'sigmoid': NetworkFunction(sigmoid, sigmoid_p),
              'tanh': NetworkFunction(tanh, tanh_p),
              'purelin': NetworkFunction(purelin, purelin_p)
             }

loss_fcns = {
              'mse': NetworkFunction(mse, mse_p),
            }

def print_y(y_predict, Y, dec=2):

    if y_predict.ndim > 1:
        y_predict = y_predict.flatten()
    print(np.around(y_predict, dec))


def get_one_trans(trans):

    if trans in trans_fcns:
        return trans_fcns[trans]

    else:
        raise ValueError("Error: " + str(trans) + " not known in tran_fcns")


def get_trans_list(trans):
    return [get_one_trans(fcn) for fcn in trans]

def get_trans(trans_fcns, num_layers):

    if isinstance(trans_fcns, str):
        return [get_one_trans(trans_fcns)] * num_layers

    elif isinstance(trans_fcns, list):

        if num_layers != len(trans_fcns):
            raise ValueError("wrong number of trans fcns")

        return get_trans_list(trans_fcns)
    else:
        raise ValueError("transfer function must be string or list of strings")

def get_loss(loss_fcn):
    return loss_fcns[loss_fcn]
