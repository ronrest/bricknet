################################################################################
#                                                            WORD 2 VEC SKIPGRAM
################################################################################
__author__ = 'ronny'


#TODO: maybe have pandas load from root module.
import pandas as pd
np = pd.np
#from .. import np


# ==============================================================================
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
def deltas(sentence, c):
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
        print center_word

        for out_index in window_indexes:
            out_word = words[out_index]
            sum_grads_U += grad_output_vectors()
            sum_grads_V += grad_input_vectors()

