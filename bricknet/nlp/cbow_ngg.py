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
    # Typecast to a numpy array if it is not already an array or a pandas series
    if not isinstance(c, (np.ndarray, pd.Series)):
        c = np.array(c)

    p = c**float(power)  # Raise unigram counts to the 3/4
    return  p/p.sum()    # Normalize to make values add up to 1
