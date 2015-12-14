"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'


import numpy as np
def get_sampling_distribution(c, pow=3/4.0):
    # Typecast to a numpy array if it is not already an array or a pandas series
    if not isinstance(c, (np.ndarray, pd.Series)):
        c = np.array(c)

    p = c**pow           # Raise unigram counts to the 3/4
    return  p/p.sum()    # Normalize to make values add up to 1
