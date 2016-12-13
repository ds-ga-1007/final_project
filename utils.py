
from Model import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import six
from matplotlib import colors

def prepare_autoencoding_data(X, Y):
    """
    prepare data to be autoencoded
    :param X: numpy.ndarray 2D array of independent high dimensional variables to be autoencoded
    :param Y: numpy.ndarray 1D array of response variables for coloring purposes
    :return: X = numpy.ndarray of processed input array, data_color_labels = list of color labels.
    """

    color_list = list(six.iteritems(colors.cnames))

    Y_uni = np.unique(Y)

    Y_map = dict(zip(Y_uni,range(len(Y_uni))))

    if Y is None:
        data_color_labels = [color_list[0][0] for x in X]

    elif Y.ndim == 1:
        data_color_labels = [color_list[Y_map[y] * 2 + 1][0] for y in Y]

    elif Y.ndim == 2:
        data_color_labels = [color_list[4 * np.sum(
            [Y_map[yi] * (2 ** idx) for idx, yi in enumerate(y)])][0] for y in Y]

    else:
        raise ValueError("response variables must be 1 or 2 dimensional")

    return X, data_color_labels

def visualize_autoencoding_data(encoder, d, data_color_labels, fig):
    """
    Visualize the autoencoding
    :param encoder: AutoEncoder to visualize
    :param d: dimension of data to be AutoEncoded
    :param data_color_labels: Array of color names for the autoencoding visualizations points
    :param fig: matplotlib.figure.Figure to draw the visualization
    :return: None
    """

    encoding_vals = encoder.get_encoding_vals()

    if d == 2:
        fig.add_subplot(120 + d - 1)
        plt.scatter(encoding_vals[:, 0], encoding_vals[:, 1], color=data_color_labels)
    if d == 3:
        ax = fig.add_subplot(120 + d - 1, projection='3d')
        ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1],
                   zs=encoding_vals[:, 2], c=data_color_labels)

    plt.title('real data visualized with graphed in ' + str(d) + 'D')

def process_autoencoding_data(X, visualize, data_color_labels):
    """
    Perform autoencoding of data. Optionally visualize data using color tags from data_color_labels.
    :param X: numpy.ndarray 2D array of independent high dimensional variables to be autoencoded.
    :param visualize: Boolean-like. If evaluates to True, display visualizations.
    :param data_color_labels: Array of color names for the autoencoding visualizations points.
    :return: array of reconstruction errors for an embedding dimension of width 2 or 3.
    """

    err_2d_3d = np.empty(2)

    if visualize:
        fig = plt.figure(figsize=(20, 15))

    for d in [2, 3]:

        encoder = AutoEncoder(X, hidden_dim=d)

        # Not neccessary for functionality,
        # but the following makes many dataset visualization look prettier
        encoder.reg_const = .00001

        encoder.train(10)
        reconstruction = encoder.predict()

        if visualize:
            visualize_autoencoding_data(encoder, d, data_color_labels, fig)

        err_2d_3d[d-2] = np.mean(np.square(reconstruction - X))

    if visualize:
        plt.show()

    return err_2d_3d

def autoencode_2d_3d_data(X, Y, visualize = 0):
    """
    Autoencode data into 2 dimensions and 3 dimensions, report the error to the user
    Optionally, also visualize the 2D and 3D embedding dimensions
    :param X: numpy.ndarray 2D array of independent high dimensional variables to be autoencoded
    :param Y: numpy.ndarray 1D array of response variables for coloring purposes
    :param visualize: Boolean-like. If evaluates to True, display visualizations.
    :return: array of reconstruction errors for an embedding dimension of width 2 or 3.
    """

    X, data_color_labels = prepare_autoencoding_data(X, Y)

    err_2d_3d = process_autoencoding_data(X, visualize, data_color_labels)

    return err_2d_3d[0], err_2d_3d[1]
