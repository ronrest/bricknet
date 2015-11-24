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
