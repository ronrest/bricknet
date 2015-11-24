"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'

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

    def activate(selg, agg):
        """
        Sigmoid Activation function

        :param selg:
        :param agg:
        :return:
        """
        return activations.sigmoid(agg)
