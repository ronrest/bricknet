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


def tanh_prime(z, as_int=True):
    return (z > 0).astype(int) if as_int else (z > 0).astype(float)
