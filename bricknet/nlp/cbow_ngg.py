"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'


import numpy as np
# ==============================================================================
#                                                      GET_SAMPLING_DISTRIBUTION
# ==============================================================================
def get_sampling_distribution(c, power=3/4.0):
    """
    Takes an array of unigram counts for each word in the vocabulary, and
    returns an array representing a distribution for each of those words for
    sampling purposes.

    The type of distribution returned can be controlled by setting the value of
    the `power` argument.
    
    :param c: {array-like}

        An array-like object of values representing the unigram counts for the
        words in the vocabulary (in the same order as the words in the
        vocabulary)

    :param power: {float}

        power to raise the unigram counts by.

        By default it uses (3/4.0) as in Mikolov et al 2013, due to its
        empirical usefulness in negative sampling.

        if power = 1, then this returns the unigram distribution.

        if power = 0, then this returns a uniform distribution.

    :return:

        An array, containing a sampling distribution calculated as:

            c**power  then normalised to make the values add to 1.

    :references:

        - Mikolov, T., Sutskever, I., Chen, K., Corrado, G. S., and Dean, J.
          (2013b). Distributed representations of words and phrases and their
          compositionality. In Advances in Neural Information Processing
          Systems, pages 3111-3119

    """
    # ==========================================================================

    # Typecast to a numpy array if it is not already an array or a pandas series
    if not isinstance(c, (np.ndarray, pd.Series)):
        c = np.array(c)

    p = c**float(power)  # Raise unigram counts to the 3/4
    return  p/p.sum()    # Normalize to make values add up to 1
