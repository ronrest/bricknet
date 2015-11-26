import matplotlib.pyplot as plt
from numpy import array
import numpy as np
import activations
import layers
import classifiers
import eval

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
        # TODO: maybe include a gradient checking method build in
        self.Weights = [np.random.rand(self.layerSizes[i], \
                                       self.layerSizes[i+1]) \
                        for i in range(self.numlayers - 1)]


