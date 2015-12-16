"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'


import pandas as pd
np = pd.np


# ==============================================================================
#                                                              PAD_SENTENCE_LIST
# ==============================================================================
def pad_sentence_list(s, c_left, c_right, start="START", end="END"):
    """
    Pad the left and right of a sentence with Start of sentence and end of
    sentence tokens.

    :param s: {list of strings}

        The list of strings representing a sentence.

    :param c_left: {int}

        The number of context words to the left

    :param c_right: {int}

        The number of context words to the left

    :param start: {string}

        default = "START"

    :param end:  {string}

        default = "END"

    :return: {list}

        same list, but with start and end of sentence padded words.
    """
    # ==========================================================================
    return c_left * [start] + s + [end] * c_right


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
def get_unigram_counts(sentences, window=8):
    """
    Takes an iterable of iterables containing individual words, and returns a
    pandas Series contianing the words as indices, and the number of times
    those words appeared in the corpus as the element values.

    :param sentences: {iterable of iterables of strings}

        Can be something like an outer list encapsulating all sentences. Each
        sentence is a list of strings representing each word.

    :param window {list, or int}

        window size to use for context. must be either an integer, for a
        symetrical window, or, for an asymentrical window, you use a list of
        two integer elements.  The first element is for the number of words to
        the left, and the second element is for the number of words to the right
        to use as the context window.

        default = 8

    :return: {pandas.Series}

        returns a pandas Series of the unigram word counts.
    """
    # ==========================================================================
    unigram = {}        # Tallies the unigram counts of words in corpus

    # --------------------------------------------------------------------------
    #                                                         handle window size
    # --------------------------------------------------------------------------
    if isinstance(window, (int, long)):
        c_left  = window / 2
        c_right = c_left
    elif (isinstance(window, list)
    and (len(window) > 1)
    and isinstance(window[0], (int, long))
    and isinstance(window[1], (int, long))):
        c_left  = window[0]
        c_right = window[1]
    else:
        msg = "\n  get_unigram_counts() expects the `window` argument to be an"\
              "\n  integer, or a list of two integers."
        raise ValueError(msg)

    # --------------------------------------------------------------------------
    #                                                     Loop through sentences
    # --------------------------------------------------------------------------
    for sentence in sentences:
        sentence = pad_sentence_list(sentence, c_left, c_right)
        for word in sentence:
            # create a tally of the words. If word does not already exist in the
            # dictionary, then create a new element, and assign it the value of 1.
            unigram[word] = unigram.get(word, 0) + 1

    return pd.Series(unigram)


# ==============================================================================
#                                                                CREATE_VOCAB_DF
# ==============================================================================
def create_vocab_df(sentences, window=8, p_power=(3/4.0)):
    """

    :param sentences: {iterable of iterables of strings}

        Can be something like an outer list encapsulating all sentences. Each
        sentence is a list of strings representing each word.

    :param window: {int or list of two ints}

        number of words to use as the window context.

        can be asymetrical by using a list of two values.

    :param p_power: {float}

        power to use for creating the sampling distribution, see the
        power argument in get_sampling_distribution() function.

        default value is (3/4.0)


    :return: {pandas.DataFrame}

        returns a dataframe with the following columns:

            counts : the number of times the word occured in the corpus.

            i      : the index of of this word in the word matrices.

            p      : the sampling propability distribution for the words.

                     - Used for negative sampling.

            words  : An intuitive way to retreive the words in the vocabulary.
    """
    # ==========================================================================
    u = get_unigram_counts(sentences, window=window)
    p = get_sampling_distribution(u)
    vocab = pd.DataFrame({"counts":u, "p":p, "i":range(len(u))})
    vocab["words"] = vocab.index  # technically redundant, but intuitively more
                                  # sensical to retreive the words using
                                  # vocab.words (or vocab["words"] than using
                                  # vocab.index
    return vocab


# ==============================================================================
#                                                             GET_SAMPLE_INDICES
# ==============================================================================
def get_sample_indices(vocab, k):
    """
    Takes a vocabulary dataframe and returns the indices of k randomly sampled
    words.

    :param vocab:
    :param k:
    :return:
    """
    # ==========================================================================
    return np.random.choice(vocab.i, size=k, p=vocab.p, replace=False)


# ==============================================================================
#                                                                 GET_WORD_INDEX
# ==============================================================================
def get_word_indices(vocab, words):
    """
    takes a word string, or a list of strings,  and returns the index(es) of the
    word(s).

    :param vocab: {DataFrame}

        Vacabulary dataframe

    :param words: {string, or list of strings}

        the word(s) you want to get the index for.

    :return:
    """
    # ==========================================================================
    if isinstance(words, str):
        words = [words]
    return vocab["i"][words]


# ==============================================================================
#                                                                   WORDS_MATRIX
# ==============================================================================
def words_matrix(vocab_size, vec_size = 20, orientation="cols", scale=1):
    """
    Creates a matrix (array) for the word vectors.

    :param vocab_size: {int, or long}

        number of words in the vocabulary.

    :param vec_size: {int}

        The size of the word vectors. Good values are somewhere between 20-300.

    :param orientation: {str}

        "cols" = Each word vector is a column in the dataframe

        "rows" = Each word vector is a row in the dataframe

    :param scale: {number}

        by default it returns weights as random values between 0 and 1. You
        can scale it to be random numbers between 0 and another number.


    :return: {array}

    """
    # ==========================================================================
    if orientation == "rows":
        return (np.random.rand(vocab_size, vec_size)-0.5) * scale
        #return pd.DataFrame(df, index=vocab)
    elif orientation == "cols":
        return  (np.random.rand(vec_size, vocab_size) - 0.5) * scale
        #return pd.DataFrame(df, columns=vocab)
    else:
        msg = '\n  words_matrix() expects `orientation` argument to '\
              '\n  be either "cols" or "rows"'
        raise ValueError(msg)


# ==============================================================================
#                                                                        SIGMOID
# ==============================================================================
def sigmoid(x):
    """
    Calculates the sigmoid value of x.

    :param x: {number}
    :return: {float}
    """
    # ==========================================================================
    #TODO: Check out http://stackoverflow.com/a/25164452 for potential
    #      optimisation of the sigmoid function.
    return 1 / (1 + np.exp(-x))


# ==============================================================================
#                                                               TRAIN_ONE_WINDOW
# ==============================================================================
def train_one_window(input_words, y, k=5, alpha=0.01):
    """

    :param input_words: {list, or array-like of strings}

        list of words to use as input words context.

    :param y: {string}

        The correct output word

    :param k: {int}

        The number of negative samples to use.

    :param alpha: {float}

        learning rate.

    :return:
    """
    global W_in, W_out, vocab
    correct_word = y

    # ==========================================================================
    #                                                        Forward Propagation
    # ==========================================================================
    # TODO: try see what happens when words to not exist in vocab.

    # --------------------------------------------------------------------------
    #                                                     Calculate Hidden layer
    # --------------------------------------------------------------------------
    num_input_words = len(input_words)
    input_word_indices = get_word_indices(vocab, words=input_words)
    input_word_vectors = W_in[:,input_word_indices]
    a = input_word_vectors.sum(axis=1) / num_input_words

    # --------------------------------------------------------------------------
    #                                         Calculate Subset of Weights to Use
    # --------------------------------------------------------------------------
    # The correct word will be the word in row 0, and all others will be the
    # negative samples.
    neg_sample_indices = get_sample_indices(vocab, k=k)
    pos_sample_index = get_word_indices(vocab, correct_word)
    sample_indices = np.concatenate([pos_sample_index, neg_sample_indices])
    output_word_vectors = W_out[sample_indices, :]

    # --------------------------------------------------------------------------
    #                                                     Calculate Output layer
    # --------------------------------------------------------------------------
    z = output_word_vectors.dot(a)

    # --------------------------------------------------------------------------
    #                                                             Calculate Cost
    # --------------------------------------------------------------------------
    # TODO: optimise this by vetcorising and caching sigmoid(z) and taking
    #       advantage of the property sigmoid(-z) = 1 - sigmoid(z)
    J = -np.log(sigmoid(z[0])) - np.log(sigmoid(-z[1:])).sum()

    # --------------------------------------------------------------------------
    #                                                                  Gradients
    # --------------------------------------------------------------------------
    G_z = sigmoid(z)    # Gradient at the output layer
    G_z[0] += -1        # Update gradient for correct word

    G_W_out = np.outer(G_z, a)                     # Gradient of output word vectors
    G_a = output_word_vectors.transpose().dot(G_z) # Gradient of hidden layer a

    # --------------------------------------------------------------------------
    #                                                          Update Parameters
    # --------------------------------------------------------------------------

    # ------------------------------------------------- Update Input Word Matrix
    # Make G_a thicker to update multiple words in one go.
    G_a = np.repeat([G_a], num_input_words, axis=0).transpose()
    W_in[:,input_word_indices] += -(alpha/num_input_words) * G_a

    # ----------------------------------------------- Update Output  Word Matrix
    W_out[sample_indices, :] += (-alpha) * G_W_out

    return J

