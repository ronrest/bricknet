"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'

import numpy as np

################################################################################
#                                                                    LAYER CLASS
################################################################################
class Layer(object):
    """
    A template for layer objects

    Note you will need to implement your own methods.

    TODO: take into account Bias weights
    TODO: Consider having a saturation warning if activated values are too high
          for a given activation function.
    """
    # ==========================================================================
    #                                                                   __INIT__
    # ==========================================================================
    def __init__(self, in_size=3, out_size=3, weights=None):
        """

        :param in_size: {int}{optional}(default = 3)

            The number of inputs that this layer takes

            NOTE: This value is ignored if you enter pre-baked weights

        :param out_size: {int}{optional}(default = 3)

            The number of outputs from this layer.

            NOTE: This value is ignored if you enter pre-baked weights

        :param weights:  {numpy array}{optional} (default = 3)

            You can use pre-baked weights if you like.
        """
        # ======================================================================
        if weights is None:
            # Initialise Layer Dimensions to values in arguments
            self.in_size = in_size
            self.out_size = out_size

            # Initialise Weights to random values between 0 and 1
            self.weights = np.random.rand(out_size, in_size)
        else:
            # Initialise Layer Dimensions based on pre-baked weights
            self.in_size = weights.shape[1]
            self.out_size = weights.shape[0]

            # Initialise Weights to the pre-baked values that have been entered
            self.weights = weights

        # Initialise Activations to zeroes
        self.activated_vals = np.zeros(out_size)

    # ==========================================================================
    #                                                                    FORWARD
    # ==========================================================================
    def forward(self, input, return_val=True):
        """
        Performs forward propagation
        :param input: {array like object}

            The values to use as inputs to this layer.

        :param return_val: {Boolean}

            Should it return the output values? If False, then it updates the
            values silently.

        :return:{array}
            The Output value (only if return_val = True)
        """
        # ======================================================================
        agg = self.aggregate(input)
        self.activated_vals = self.activate(agg)

        if return_val:
            return self.activated_vals


    def aggregate(self, input):
        """
        A function for aggregating the raw input values.

        :param input:
        :return:
        """
        return self.weights.dot(input)

    def activate(self, agg):
        """
        A function for handling how the aggregated values are then dealt with.

        :param agg: {array-like}
            the raw aggregated values.

        :return:{array}

            The activated values
        """
        return agg
