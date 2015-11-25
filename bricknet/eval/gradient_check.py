from .. import np

# ==============================================================================
#                                                                 GRADIENT CHECK
# ==============================================================================
def gradient_check(net, y, epsilon=0.01, verbose=True, x=None):
    """
    Perform gradient checking of a neural network, (or just an output layer
    object)

    You feed it the neural net object (or output layer object), an array of
    input values, the correct outputs, and it compares the gradients using the
    built in built in methods with manually calculated gradients and returns
    the differences between both calculations.

    If the built in gradient methods is implemented properly, then the returned
    values should be very close to zeros.

    Manual Gradients Calculated as:

        (cost(x+epsilon) - cost(x-epsilon)) / (x+epsilon - x-epsilon)

    :param net:{neural net object, or output layer object}

        The neural net (or output layer object) you want to test for correctness
        of the gradient calculation method.


    :param y:{array}

        The correct output values

    :param epsilon: {float}

        How much of a change in the input elements should be used to manually
        calculate the gradients?


    :param verbose:{boolean}{optional}(default=True)

        Should it print out detailed info about costs and gradients?

    :param x:{array}(optional) (default=None)

        By default, this function uses random values between 0 and 1 as input
        values to the neural net to test the gradients. But you can specify your
        own input values if you like.

    :return:
    """
    # ==========================================================================
    # Calculate the gradients using the built in function we are testing
    # --------------------------------------------------------------------------
    if x is None:
        x = np.random.ranf(net.in_size)

    net.forward(x)
    builtin_gradients = net.back(x, y, update_weights=False)
    if verbose:
      print("=======================================")
      print("Cost using x: {}".format(net.cost(y)[0]))
      print("=======================================")

    # --------------------------------------------------------------------------
    # Calculate The gradients manually WRT each each input in turn
    # --------------------------------------------------------------------------
    manual_gradients = np.ones(len(x)) #Stores the manually calculated gradients

    for i in range(len(x)):
        # ----------------------------------------------------------------------
        # Cost when we move input for element i by a tiny bit to the left
        # ----------------------------------------------------------------------
        x1 = x.copy()
        x1[i] = x1[i] - epsilon
        net.forward(x1)
        cost_x1 = net.cost(y)

        # ----------------------------------------------------------------------
        # Cost when we move input for element i by a tiny bit to the right
        # ----------------------------------------------------------------------
        x2 = x.copy()
        x2[i] = x2[i]+epsilon
        net.forward(x2)
        cost_x2 =net.cost(y)

        # ----------------------------------------------------------------------
        # Calculate gradient for the element i
        # ----------------------------------------------------------------------
        dy = (cost_x2- cost_x1)
        manual_gradients[i] = dy/(2*epsilon)

        # ----------------------------------------------------------------------
        # Print the change in cost due to the element i
        # ----------------------------------------------------------------------
        if verbose:
            print("DJ by changing x[{0}]: {1:+0.10f}".format(i, dy[0]))


    # The differences between builtin and manually calculated gradients
    diff = builtin_gradients - manual_gradients

    # --------------------------------------------------------------------------
    # Print a table of the builtin gradients vs manually calculated gradients
    # --------------------------------------------------------------------------
    if verbose:
        print("------------------------------------------------------------")
        print("Builtin Gradients || Manual Gradients || Diff")
        print("------------------------------------------------------------")
        for i in range(len(x)):
            print("{0:+17.6f} || {1:+16.6f} || {2:+0.6f}".format(
                manual_gradients[i],
                builtin_gradients[i],
                diff[i]))

    # --------------------------------------------------------------------------
    # Return the differences between builtin and manually calculated gradients
    # --------------------------------------------------------------------------
    return diff

