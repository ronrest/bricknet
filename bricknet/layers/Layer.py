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

    ISSUE: The current implementation stores the post activated values in memory.
           THis might potentially cause memory efficiency issues.
           - COnsider maybe only storing these during the training phase, and
             not storing them during normal usage.

           - Run some tests to see which is more computationally expensive to
             compute, the post activations, or the aggregated values (z). Store
             which ever one involves the most computational time.

           - Or maybe consider having this as a setting. Letting the user decide
            if they want to store these values (for gains in speed, but at the
            expense of memory useage) or if they want to not store (for minimal
            memory useage, but slower to compute)
              -  This could be a speed setting:
                 1. Fastest. Stores both z, and a.
                 2. medium. Stores one of z or a
                 3. Slowest. Stores nothing?

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

        # Initialise Preactivations and Activations to zeroes
        self.activated_vals = np.zeros(out_size)
        self.preactivated_vals = np.zeros(out_size)

        # Initialise Errors Gradients of post-activation to zeroes
        #self.errors = np.zeros(out_size)


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

    def back(self, input_vals, update_weights=True):
        """
        Back propagate the errors

        :param input_vals:
        :param update_weights:
        :return:
        """
        return np.zeros(self.in_size)
