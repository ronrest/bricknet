import matplotlib.pyplot as plt
from numpy import array
import numpy as np



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
    """
    def __init__(self, size=3, next_size=3, weights=None):
        """

        :param size: {int} (default = 3)

            Size of this layer

        :param next_size: {int} (default = 3)

            Size of the next layer

        :param weights:  {matrix} (default = 3)

            You can use pre-baked weights if you like.

        :return:
        """
        # Layer Dinensions
        self.size = size
        self.next_size = next_size

        # Initialise Activations to zeroes
        self.activated_vals = np.zeros(size)

        # Initialise Weights to random values between 0 and 1, unless prebaked
        # values have been entered as an argument.
        if weights == None:
            self.weights = np.random.rand(next_size, size)
        else:
            self.weights = weights

