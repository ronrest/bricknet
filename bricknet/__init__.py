import matplotlib.pyplot as plt
from numpy import array
import numpy as np
from bricknet import activations


################################################################################
#                                                           NEURAL_NETWORK CLASS
################################################################################
class Neural_Network(object):
    """
    An object to build a neural network in a modular way. You will be able to
    specify the size of each layer individual, the activation function for
    each one of them.

    Each layer will be an object that inherits from the Layer object.

    You can specify each layer in the neural network to be a different Layer
    object, with potentially very different activation  functions, and
    different ways of propagating forward and backwards.

    """
    def __init__(self, layers=[2,3,1]):
        """

        :param layers: {list of ints} (default=[2,3,1])

            A list containing the size of each layer (including input and
            output layers)
        """
        # Layers
        self.layerSizes = layers
        self.numlayers = len(self.layerSizes)

        # Initialised Weights as random values between 0 and 1
        # TODO: add Layer objects instead. 
        self.Weights = [np.random.rand(self.layerSizes[i], \
                                       self.layerSizes[i+1]) \
                        for i in range(self.numlayers - 1)]



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

