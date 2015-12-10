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
# ==============================================================================
#                                                              CALC_HIDDEN_LAYER
# ==============================================================================
def calc_hidden_layer(words):
    """

    :param words: The context words
    :return:
    """
    # aggregate the inputs
    num_input_words = len(words)
    in_vecs = in_df[words]  # Input word vectors
    return in_vecs.sum(axis=1) / num_input_words       # Hidden layer.


# ==============================================================================
#                                               CALC_PREACTIVATIONS_OUTPUT_LAYER
# ==============================================================================
def calc_preactivations_output_layer(a):
    """

    :param a: the hidden layer node values
    :return:
    """
    return out_df.dot(a)


# ==============================================================================
#                                                                CALC_HYPOTHESES
# ==============================================================================
def calc_hypotheses(z):
    """

    :param z: the preactivations of the output layer
    :return:
    """
    exp_z = np.exp(z)
    return exp_z / exp_z.sum()


# ==============================================================================
#                                                             TRAIN_ONE_EXAMPLE
# ==============================================================================
def train_one_example(context, output, alpha=0.01):
    words = context
    correct_output = output

    # FOrward propagation
    a = calc_hidden_layer(words)
    z = calc_preactivations_output_layer(a)
    h = calc_hypotheses(z)

    # Back propagation
    G_z = h.copy()
    G_z[correct_output]  -= 1
    G_a = out_df.transpose().dot(G_z)
    G_W_out = np.outer(G_z, a)


    # update the out word matrix
    out_df += -alpha * G_W_out

    # Update teh input word matrix
    inputs_update = -(1.0/len(words)) * alpha * G_a
    in_df[words] = in_df[words].add(inputs_update, axis="rows")
