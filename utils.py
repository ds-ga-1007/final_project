
from Model import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import six
from matplotlib import colors

def prepare_autoencoding_data(X, Y, visualize):

    X /= 2
    color_list = list(six.iteritems(colors.cnames))

    if Y.ndim == 1:
        rgb = [color_list[y * 2 + 1][0] for y in Y]
    elif Y.ndim == 2:
        rgb = [color_list[4 * np.sum(
            [yi * (2 ** idx) for idx, yi in enumerate(y)])][0] for y in Y]
    else:
        visualize = 0

    return X, visualize, rgb

def visualize_autoencoding_data(encoder, d, rgb, fig):

    encoding_vals = encoder.get_encoding_vals()

    if d == 2:
        fig.add_subplot(120 + d - 1)
        plt.scatter(encoding_vals[:, 0], encoding_vals[:, 1], color=rgb)
    if d == 3:
        ax = fig.add_subplot(120 + d - 1, projection='3d')
        ax.scatter(xs=encoding_vals[:, 0], ys=encoding_vals[:, 1],
                   zs=encoding_vals[:, 2], c=rgb)

    plt.title('real data visualized with graphed in ' + str(d) + 'D')

def process_autoencoding_data(X, visualize, rgb):

    err = np.empty(2)

    if visualize:
        fig = plt.figure()

    for d in [2, 3]:

        encoder = AutoEncoder(X, hidden_dim=d)
        encoder.train(10)
        reconstruction = encoder.predict()

        if visualize:
            visualize_autoencoding_data(encoder, d, rgb, fig)

        err[d-2] = np.mean(np.square(reconstruction - X))

    if visualize:
        plt.show()

    return err

def autoencode_2d_3d_data(X, Y, visualize = 0):

    X, visualize, rgb = prepare_autoencoding_data(X, Y, visualize)

    err = process_autoencoding_data(X, visualize, rgb)

    return err[0], err[1]