"""====================================================
    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'

import numpy as np
from .. import activations
from ..layers.Layer import Layer


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
    def forward(self, input, return_val=True, return_cost=False):
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
            if return_cost:
                pass
            else:
                return self.classification
        elif return_cost:
            pass

    def cost(self, y):
        """
        Returns the cost function of the hypothesised value as:

        -log(hypothesised_probability_for_the_correct_class)

        :param y: {array of booleans}

            one-hot vector of the correct class with elements as booleans

        :return:
        """
        return -np.log(self.activated_vals[y])


    def activate(selg, agg):
        """
        Sigmoid Activation function

        :param selg:
        :param agg:
        :return:
        """
        return activations.softmax(agg)

    def back(self, input_vals, y, update_weights=True):
        """
        Back propagate the errors using the negative Log Likelihood Cost Function

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

        # Gradient of Softmax for the correct class WRT preactivations
        errors_preactivation = self.activated_vals - y

        errors_input = self.weights.transpose().dot(errors_preactivation)
        errors_weights = np.outer(errors_preactivation, input_vals)

        if update_weights:
            self.weights = self.weights + errors_input

        return errors_input




