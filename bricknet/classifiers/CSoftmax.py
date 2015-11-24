"""====================================================
    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'

import numpy as np
from .. import activations
from ..layers import Layer


class CSoftmax(Layer):
    def __init__(self, in_size=3, out_size=3, weights=None):
        """

        :param in_size:
        :param out_size:
        :param weights:
        :return:
        """
        Layer.__init__(self, in_size, out_size, weights)
        self.classification = np.zeros(out_size)

    # ==========================================================================
    # FORWARD
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
        # TODO: currently using arrray.max() method may result in occasionally
        #       one hot vectors that are NOT "one hot" in cases where there are
        #       ties. Find a better solution to avoid this.

        # ======================================================================
        self.preactivated_vals = self.aggregate(input)
        agg = self.preactivated_vals
        self.activated_vals = self.activate(agg)
        # One hot vector of the class with the highest probability
        self.classification = self.activated_vals == self.activated_vals.max()

        if return_val:
            return self.classification


    def activate(selg, agg):
        """
        Sigmoid Activation function

        :param selg:
        :param agg:
        :return:
        """
        return activations.softmax(agg)

    def back(self, out_errors, input_vals, y, update_weights=True):
        """
        Back propagate the errors

        :param out_errors: {arrray like}

            error gradients at the post activation of the layer.
        :param input_vals:
        :param y:{array-like object of Boolean elements}
            An array of booleans, representing a one hot vector of the correct
            class y.
        :param update_weights:
        :return:
        """

        # Gradient of errors WRT the preactivation of the layer.
        # z = self.aggregate(input_vals)
        z = self.preactivated_vals

        #

        # Gradient of Softmax for the correct class WRT preactivations
        h_y_is_c = self.activated_vals[y]
        hc = self.acivated_vals
        hy_only = np.ones(len(hc)) * h_y_is_c
        errors_preactivation = h_y_is_c - hy_only * hc


        errors_input = self.weights.transpose().dot(errors_preactivation)
        errors_weights = np.outer(errors_preactivation, input_vals)

        if update_weights:
            self.weights = self.weights + errors_input

        return errors_input




