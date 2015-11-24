"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'

import numpy as np

def sigmoid(z):
    """
    Sigmoid function on input

    :param z: {numeric value, or array-like object}
    :return:
    """
    return 1.0 / (1 + np.exp(-z))


def sigmoid_prime(z):
    """
    derivative of Sigmoid Function
    return np.exp(-z) / ((1 + np.exp(-z)) ** 2)

    :param z:
    :return:
    """
    # More computationally efficient version.
    sig = sigmoid(z)
    return sig * (1 - sig)


def softmax(z):
    """
    Returns the softmax probabulities fot the elements of z.

    :param z: {array-like}

        An array of values

    :return: {array}

        An  array of the softmax probabilities of the input values.
    """
    exponent_vals = np.exp(z)
    return exponent_vals / exponent_vals.sum()


def softmax_prime(z, selected_output):
    """
    Returns the the values of the derivative of the softmax function for the
    selected output element, WRT the input values.

    :param z: {array-like}

        An array of values

    :param selected_output: {array-like}

        A one hot vector specifying the element that is selected from the output
        of the softmax function.

    :return: {array}

        Gradients of the sofmtax function curve at the input values.
    """
    # TODO: Check that this is even working properly.
    h_y_is_c = softmax(z*selected_output)
    hc = softmax(z)
    hy = hc * selected_output

    return h_y_is_c  - hy*hc
