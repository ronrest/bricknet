__author__ = 'ronny'


# ==============================================================================
#                                                                           TANH
# ==============================================================================
def tanh(z):
    """
    :param z: {array-like}

        the array representing the pre-activation values vector.

    :return:

        Post activation values using the tanh activation function.
    """
    # ==========================================================================
    return (z > 0) * z

