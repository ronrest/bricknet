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


# ==============================================================================
#                                                                           TANH
# ==============================================================================
def tanh_prime(z, as_int=True):
    """
    :param z: {numpy array}

        the array representing the pre-activation values vector.

    :param as_int: {boolean}

        returns an array of integers (3.88 times faster than returning array of
        floats). Since the gradients will always be 0 or 1 for the tanh
        function, then there is no loss of information.

        default = True

        If False, return array of floats.

    :return:

        Gradient of the tanh activation function evaluated at the values in z.
    """
    # ==========================================================================
    return (z > 0).astype(int) if as_int else (z > 0).astype(float)

