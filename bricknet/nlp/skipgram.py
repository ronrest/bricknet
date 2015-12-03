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

