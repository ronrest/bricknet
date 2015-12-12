"""====================================================
                    DESCRIPTION

=======================================================
"""
__author__ = 'ronny'





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
    words =

    # Clean up words
    words = {word.replace(".", "") for word in words}       # remove full stops

    # words = {word.replace(",", "") for word in words}       # remove commas
    # words = {word.replace("?", "") for word in words}       # remove q marks
    # words = {word.replace("!", "") for word in words}       # remove exclamations
    # words = {word.replace(";", "") for word in words}       # remove semicolons
    # words = {word.lower() for word in words}                # to lower case

    return words


# ==============================================================================
#                                                  GET_VOCAB_FROM_SENTENCES_LIST
# ==============================================================================
def get_vocab_from_sentences_list(sl):
    """
    Creates a set of words from a string as the corpus.

    :param sl: {iterable of iterables of strings}

        List containing sentences. Each sentences being a list of strings.

    :return: {set}

        A set of all the unique words in the corpus.

    """

    # TODO: use a real word tokenisation function.

    vocab = set()
    for sentence in sentences:
        vocab = vocab.union([word for word in sentence])

    return vocab

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
    """

    :param context: {list of strings}
    :param output: {string}
    :param alpha: {float}
    :return:
    """
    global out_df
    global in_df
    words = context
    correct_output = output

    # FOrward propagation
    a = calc_hidden_layer(words)
    z = calc_preactivations_output_layer(a)
    h = calc_hypotheses(z)

    cost = -np.log(h[correct_output])

    # Back propagation
    G_z = h.copy()
    G_z[correct_output]  -= 1
    G_a = out_df.transpose().dot(G_z)
    G_W_out = np.outer(G_z, a)


    # update the out word matrix
    out_df += -alpha * G_W_out

    # Update teh input word matrix
    # TODO: find out what happens when you have the same word twice in a
    #       context.
    inputs_update = -(1.0/len(words)) * alpha * G_a
    in_df[words] = in_df[words].add(inputs_update, axis="rows")

    return cost



def trainCBOW(iterations, alpha=0.01):
    cost = [666]*iterations     # initialise the cost over time
    window_dims = [4,4]  # Number of words on either side of the center word
    c_left  = window_dims[0]    # Number of context words to the left of center word
    c_right = window_dims[1]    # Number of context words to the right of center word

    #sentence = "the one and the only jones the magnificent"
    # list of indices of sampled sentences
    sample_indices = np.random.randint(low=0, high=len(sentences), size=iterations)

    for i in range(iterations):
        sentence_list = sentences[sample_indices[i]]

        # Skips empty sentences
        if sentence_list == []:
            cost[i] = 333
            continue

        # Add Start and end of sentence tokens
        sentence_list = c_left * ["START"] + sentence_list + ["END"] * c_right

        # Select a random word in the sentence to be the center word
        center_word_index = np.random.randint(low=c_left,
                                              high=len(sentence_list) - c_right,
                                              size=1)

        #center_word_index = 5
        center_word = sentence_list[center_word_index]
        context = sentence_list[center_word_index - c_left: center_word_index]
        context += sentence_list[center_word_index +1 : center_word_index + c_right +1]

        # TODO: this is a hack at the moment to stop dupicate words.
        #       because i dont know what duplicate words do. Need to test if it
        #       will behave properly with duplicates.
        window_words = list(set(context))

        cost[i] = train_one_example(window_words, center_word, alpha)

    print "DOne training word vectors"
    return cost





def trainCBOW2(alpha=0.01):
    cost = [666]*iterations     # initialise the cost over time
    window_dims = [4,4]  # Number of words on either side of the center word
    c_left  = window_dims[0]    # Number of context words to the left of center word
    c_right = window_dims[1]    # Number of context words to the right of center word

    num_sentences = len(sentences)

    # A dictionary to keep track of percentage completed printout
    # keys are the sentence number
    # values are the percentage completed by that point
    progress = np.linspace(0, num_sentences, num=101)
    progress = {progress[i]: i for i in range(101)}
    progress_keys = progress.keys()

    for i in range(num_sentences):
        # print progress
        if i in progress_keys:
            print "   {} % complete".format(progress[i])

        sentence_list = sentences[i]

        # Skips empty sentences
        if sentence_list == []:
            cost[i] = 333
            continue

        # Add Start and end of sentence tokens
        sentence_list = c_left * ["START"] + sentence_list + ["END"] * c_right



        for center_word_index in range(c_left, len(sentence_list) - c_right):
            center_word = sentence_list[center_word_index]
            context = sentence_list[center_word_index - c_left: center_word_index]
            context += sentence_list[center_word_index +1 : center_word_index + c_right +1]

            # TODO: this is a hack at the moment to stop dupicate words.
            #       because i dont know what duplicate words do. Need to test if it
            #       will behave properly with duplicates.
            window_words = list(set(context))

            # TODO: cost calculation is wrong. It is just giving the last
            #       center word for the sentence. Should average the
            #       cost for each sentence. 
            cost[i] = train_one_example(window_words, center_word, alpha)

    print "DOne training word vectors"
    return cost




# ##############################################################################
#                                                                          SETUP
# ##############################################################################
file = "/tmp/corpus"

with open(file, "r") as textFile:
    corpus = textFile.read()


# ------------------------------------------------------------------------------
#                                                                 Clean up words
# ------------------------------------------------------------------------------
corpus = corpus.lower()  # lowercase
corpus = corpus.replace(",", "")  # remove commas
corpus = corpus.replace("!", "")  # remove exclamation
corpus = corpus.replace("?", "")  # remove qmark
corpus = corpus.replace(";", "")  # remove semi colon
corpus = corpus.replace(":", "")  # remove colon
corpus = corpus.replace(")", "")  # remove
corpus = corpus.replace("(", "")  # remove
corpus = corpus.replace("]", "")  # remove
corpus = corpus.replace("[", "")  # remove
corpus = corpus.replace("{", "")  # remove
corpus = corpus.replace("}", "")  # remove
corpus = corpus.replace("`", "")  # remove
corpus = corpus.replace("?", " QUESTION ")  # remove
corpus = corpus.replace("!", " EXCALMATION ")  # remove

corpus = corpus.replace('"', " DOUBLE-QUOTE ")  # replace double quotes
corpus = corpus.replace("'", " QUOTE ")  # replace single quotes
print "Done cleaning up corpus"



# ------------------------------------------------------------------------------
#                                                          Sentence Segmentation
# ------------------------------------------------------------------------------
# Crude sentence segmentation.
# TODO: use nltk to do a better job
sentences = corpus.split(".")
sentences = [sentence.split() for sentence in sentences]
sentences  = [s for s in sentences if s != ""] # remove empty sentences

print "done creating sentences list"


