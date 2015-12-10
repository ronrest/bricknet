"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'





# ==============================================================================
#                                                                 WORD_VECTOR_DF
# ==============================================================================
def word_vector_df(vocab, vec_size = 20, orientation="cols"):
    """
    Creates a dataframe of word vectors from a list or set of words as the vocab.

    :param vocab: {set, or list}

        A list of all the unique words.

    :param vec_size: {int}

        The size of the vector to use as the word vectors.

    "param orientation: {str}

        "cols" = Each word vector is a column in the dataframe

        "rows" = Each word vector is a row in the dataframe

    :return: {dataframe}

    """
    # TODO: check the datatype of vocab, typecaset to set to be safe.
    # initialise the word vectors to random values

    if orientation == "rows":
        df = np.random.rand(len(vocab), vec_size)
        return pd.DataFrame(df, index=vocab)
    elif orientation == "cols":
        df = np.random.rand(vec_size, len(vocab))
        return pd.DataFrame(df, columns=vocab)
    else:
        # TODO: throw an exception, error message for incorrect value entered.
        return None
