################################################################################
#                                                            WORD 2 VEC SKIPGRAM
################################################################################
__author__ = 'ronny'


#TODO: maybe have pandas load from root module.
import pandas as pd
np = pd.np
#from .. import np


# ==============================================================================
#                                                             GRAD_INPUT_VECTORS
# ==============================================================================
def grad_input_vectors(in_word, out_word, in_df, out_df):
    """
    calculates the dderivative of the log probabilities of the for the word pair
    relative to the input word.

    :param in_word: {string}
    :param out_word:{string}
    :param in_df:
        dataframe of the input words
    :param out_df:
        dataframe of the output word
    :return:
    """

    # in_vec = in_df.loc[in_word]
    # out_vec = out_df.loc[out_word]
    # vocab_size = out_df.shape[0]
    #
    # # all the probabilities of all out words, with the with in_word.
    # all_out_combinations = most_likely_output_words(in_word, in_df, out_df, n=vocab_size)
    # #TODO: somehow times that with U_j for each word j.
    #
    # out_vec - sum_out_combinations*
    #
    # numerator = np.exp(out_vec.dot(in_vec))
    # denominator = (np.exp(out_df.dot(in_vec))).sum()

    # Naive unoptimised version
    in_vec = in_df.loc[in_word]
    out_vec = out_df.loc[out_word]
    vocab_size = out_df.shape[0]

    sum_probs = 0       # stores the cumulative sum SUM(p(j|c) * U_j)
    for j in range(vocab_size):
        jth_output_word = out_df.index[j]
        jth_output_vector = out_df.iloc[j]
        sum_probs += prob_word_pair(in_word, jth_output_word, in_df, out_df) * jth_output_vector

    return out_vec - sum_probs


# ==============================================================================
#                                                            GRAD_OUTPUT_VECTORS
# ==============================================================================
def grad_output_vectors(in_word, out_word, in_df, out_df):
    """
    calculates the dderivative of the log probabilities of the for the word pair
    relative to the input word.

    :param in_word: {string}
    :param out_word:{string}
    :param in_df:
        dataframe of the input words
    :param out_df:
        dataframe of the output word
    :return:
    """
    # in_vec = in_df.loc[in_word]
    # out_vec = out_df.loc[out_word]
    # vocab_size = out_df.shape[0]
    #
    # # all the probabilities of all out words, with the with in_word.
    # all_out_combinations = most_likely_output_words(in_word, in_df, out_df, n=vocab_size)
    # #TODO: somehow times that with U_j for each word j.
    #
    # out_vec - sum_out_combinations*
    #
    # numerator = np.exp(out_vec.dot(in_vec))
    # denominator = (np.exp(out_df.dot(in_vec))).sum()

    # Naive unoptimised version
    in_vec = in_df.loc[in_word]
    out_vec = out_df.loc[out_word]
    vocab_size = out_df.shape[0]

    sum_probs = 0  # stores the cumulative sum SUM(p(j|c) * v_c)
    for j in range(vocab_size):
        jth_output_word = out_df.index[j]
        sum_probs += prob_word_pair(in_word, jth_output_word, in_df,
                                    out_df) * in_vec

    return in_vec - sum_probs


#                                                                 PROB_WORD_PAIR
# ==============================================================================
def prob_word_pair(in_word, out_word, in_df, out_df):
    """

    Using softmax probabilities

    The dataframe of word vectors should be organised as follows:
        rows: each row represents a single word
        cols: each column is one of the dimensions of the word vector.

    in_word = string
    out_word = string

    in_df = dataframe of the input word
    out_df = dataframe of the output word
    """
    in_vec = in_df.loc[in_word]
    out_vec = out_df.loc[out_word]

    numerator = np.exp(out_vec.dot(in_vec))
    denominator = (np.exp(out_df.dot(in_vec))).sum()

    return numerator / denominator


# ==============================================================================
#                                                       MOST_LIKELY_OUTPUT_WORDS
# ==============================================================================
def most_likely_output_words(in_word, in_df, out_df, n=10):
    """
    Given some input word, what are the top-n most likely set of output words.

    in_word = string
    in_df = dataframe of the input word
    out_df = dataframe of the output word
    """
    in_vec = in_df.loc[in_word]
    dot_products = np.exp(out_df.dot(in_vec))
    out_probabilities = dot_products / dot_products.sum()
    out_probabilities.sort(ascending=False)
    out_probabilities.head(n)


# ==============================================================================
#                                                                         DELTAS
# ==============================================================================
def deltas(sentence, c, in_df, out_df):
    """
    sentence = string of just one single sentence.
    c = number of words to either side of center word to use for window context.

    """
    sum_grads_U = 0     # Sum of gradients for the output vectors
    sum_grads_V = 0     # Sum of gradients for the input vectors

    words = sentence.split()
    num_words = len(words)

    # Add Start and end of sentence tokens
    words = c*["START"] + words + ["END"]* c

    # for each word in the sentence, (skipping start of sentence tokens).
    for w in range(c, num_words+c):
        window_indexes = range(w-c, w) + range(w+1, w+c+1)
        center_word = words[w]
        #print center_word

        for out_index in window_indexes:
            out_word = words[out_index]
            #print "     "+ out_word
            sum_grads_U += grad_output_vectors(center_word, out_word, in_df, out_df)
            sum_grads_V += grad_input_vectors(center_word, out_word, in_df, out_df)

    return [sum_grads_V/num_words , sum_grads_U/num_words ]

# ==============================================================================
#                                                          GET_VOCAB_FROM_STRING
# ==============================================================================
def get_vocab_from_string(s):
    """
    Creates a set of words from a string as the corpus.

    :param s: {string}

        The string to use as a corpus.

    :return: {set}

        A set of all the unique words in the corpus string.

    """
    # TODO: use a real word tokenisation function.
    words = set(s.split())

    # Clean up words
    words = {word.replace(".", "") for word in words}       # remove full stops
    words = {word.replace(",", "") for word in words}       # remove commas
    words = {word.replace("?", "") for word in words}       # remove q marks
    words = {word.replace("!", "") for word in words}       # remove exclamations
    words = {word.replace(";", "") for word in words}       # remove semicolons
    words = {word.lower() for word in words}                # to lower case

    return words


# ==============================================================================
#                                                                 WORD_VECTOR_DF
# ==============================================================================
def word_vector_df(vocab, vec_size = 20):
    """
    Creates a dataframe of word vectors from a list or set of words as the vocab.

    :param vocab: {set, or list}

        A list of all the unique words.

    :param vec_size: {int}

        The size of the vector to use as the word vectors.

    :return: {datagrame}

    """
    # initialise the word vectors to random values
    df = np.random.rand(len(vocab), vec_size)
    df = pd.DataFrame(df, index=vocab)
    return df
