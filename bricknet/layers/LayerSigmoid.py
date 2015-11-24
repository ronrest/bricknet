"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'
import numpy as np
from bricknet import activations
from bricknet.layers import Layer

class LayerSigmoid(Layer):
    def __init__(self, in_size=3, out_size=3, weights=None):
        """

        :param in_size:
        :param out_size:
        :param weights:
        :return:
        """
        Layer.__init__(self, in_size, out_size, weights)

    def activate(self, agg):
        """
        Sigmoid Activation function

        :param selg:
        :param agg:
        :return:
        """
        return activations.sigmoid(agg)

    def back(self, out_errors, input_vals, update_weights=True):
        """
        Back propagate the errors

        :param out_errors: {arrray like}

            error gradients at the post activation of the layer.
        :param input_vals:
        :param update_weights:
        :return:
        """

        # Gradient of errors WRT the preactivation of the layer.
        #z = self.aggregate(input_vals)
        z = self.preactivated_vals
        errors_preactivation = out_errors * activations.sigmoid_prime(z)

        errors_input = self.weights.transpose().dot(errors_preactivation)
        errors_weights = np.outer(errors_preactivation,input_vals)

        if update_weights:
            self.weights = self.weights + errors_input

        return errors_input


