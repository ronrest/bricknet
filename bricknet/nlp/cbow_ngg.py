"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'


import pandas as pd
np = pd.np
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


# ==============================================================================
#                                                             GET_UNIGRAM_COUNTS
# ==============================================================================
def get_unigram_counts(sentences):
    """
    Takes an iterable of iterables containing individual words, and returns a
    pandas Series contianing the words as indices, and the number of times
    those words appeared in the corpus as the element values.

    :param sentences: {iterable of iterables of strings}

        Can be something like an outer list encapsulating all sentences. Each
        sentence is a list of strings representing each word.

    :return: {pandas.Series}

        returns a pandas Series of the unigram word counts.
    """
    # ==========================================================================
    unigram = {}        # Tallies the unigram counts of words in corpus

    for sentence in sentences:
        for word in sentence:
            # create a tally of the words. If word does not already exist in the
            # dictionary, then create a new element, and assign it the value of 1.
            unigram[word] = unigram.get(word, 0) + 1

    return pd.Series(unigram)


def create_vocab_df(sentences, p_power=(3/4.0)):
    u = get_unigram_counts(s)
    p = get_sampling_distribution(u)
    vocab = pd.DataFrame({"counts":u, "p":p, "i":range(len(u))})
    vocab["words"] = vocab.index  # technically redundant, but intuitively more
                                  # sensical to retreive the words using
                                  # vocab.words (or vocab["words"] than using
                                  # vocab.index
    return vocab
