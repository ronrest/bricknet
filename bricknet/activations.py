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


def sigmoid_prime(self, z):
    """
    derivative of Sigmoid Function
    return np.exp(-z) / ((1 + np.exp(-z)) ** 2)

    :param z:
    :return:
    """
    # More computationally efficient version.
    sig = NN.sigmoid(z)
    return sig * (1 - sig)
