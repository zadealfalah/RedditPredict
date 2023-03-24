def lemmatizePOS(comments, allowed_pos=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """
    Takes in comments and lemmatizes them while simultaniously filtering by the allowed POS

    Args:
        comments (list): list of comments to lemmatize
        allowed_pos (list, optional): _description_. Defaults to ['NOUN', 'ADJ', 'VERB', 'ADV'].

    Returns:
        _type_: _description_
    """
    texts_out = []
    for sent in comments:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_pos])
    return texts_out

def make_bigrams(comments):
    return [bigram_mod[doc] for doc in comments]


def comment_to_words(comments):
    """
    Takes in the comments as a list and returns a list of tokens via gensim.  
    This lowercases, tokenizes, and de-accents the comments as well
    
    Args:
        comments (list): list of comments to preprocess with gensim
    """
    for comment in comments:
        yield(gensim.utils.simple_preprocess(str(comment), deacc=True))  # Text may contain accent marks as it's comment data, may not be english
        
        
        
def text_preproc(row):
    """
    Used with a pandas dataframe via .apply() to clean the 'body' (comment) data
    Args:
        row (str): str representing a comment in a row of a dataframe
    """
    text = str(row['body']) 
    text = text.encode('ascii', errors = 'ignore').decode()  # Remove non-ascii characters
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = text.lower()  # Set to lowercase
    text = text.strip()  # Remove whitespace
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)  # Remove URLs
    text = re.sub(r'[:"#$%&\*+,-/:;<=>@\\^_`{|}~.\'!?]+','',text)  # Remove punctuation
    text = re.sub(r'[()]', '', text)  # Remove parens specifically
    text = re.sub(r'[\[\]]', '', text)  # Remove brackets specifically
    text = " ".join([word for word in text.split() if (word not in stop_words) and len(word) > 1])  # Make the sentence into a list of words if it's not a stopword and longer than 1 character
    
    return text



def compute_coherence_values(dictionary, corpus, texts, limit, start=5, step=3):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values