from topicModelingFunctions import *
import pandas as pd
import re
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from gensim.models import CoherenceModel
from gensim.models import TfidfModel
import spacy
from nltk.corpus import stopwords
# nltk.download('stopwords')
# import en_core_web_sm

df = pd.read_csv(DATAPATH, usecols=['score', 'body'])  
conditions = [ (df['score'] < 1), (df['score'] >= 1) & (df['score'] <= 13), (df['score'] > 13) ] 
values = ['bad', 'okay', 'good']
df['flag'] = np.select(conditions, values)  # Bin our scores into categories under the column name 'flag'

stop_words = stopwords.words('english')
stop_words.extend(['thisIsAnExampleOfExtendingTheStopwordsList'])
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])  # Won't be using NER nor the parser

df['cComment'] = df.apply(text_preproc, axis=1)
df = df[~df.cComment.apply(lambda x: len(x.split()) == 0)]  # Remove the now empty strings after cleaning
df.reset_index(inplace=True)  # Reset index after removal of rows

sents = df.cComment.values.tolist()
data_words = list(comment_to_words(sents))

bigrams = gensim.models.Phrases(data_words, min_count=5000)   # Large min_count  as we'll have huge amount of data
bigram_mod = gensim.models.phrases.Phraser(bigrams)

data_bigrams = make_bigrams(data_words)
data_lemmatized = lemmatizePOS(data_bigrams)

# Remove words if they are just 1 or 2 characters long
#### Can definitely make this faster than it is now
frequency = defaultdict(int)

for text in data_lemmatized:
    for token in text:
        frequency[token] += 1
        
texts = [
    [token for token in text if len(token) > 2]
    for text in data_lemmatized
]

# TF-IDF Removal
id2word = corpora.Dictionary(texts)  
id2word.filter_extremes(no_below=20, no_above=0.5)  # Filter words that occur in less than 20 documents or more than 50% of documents
corpus = [id2word.doc2bow(comment) for comment in texts]  # Make our bag of words
tfidf = TfidfModel(corpus, id2word=id2word)

low_value = 0.05
for i in range(0, len(corpus)):
    bow = corpus[i]
    low_value_words = [] 
    tfidf_ids = [id for id, value in tfidf[bow]]
    bow_ids = [id for id, value in bow]
    low_value_words = [id for id, value in tfidf[bow] if value < low_value]
    words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids] 

    new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]  
     
corpus[i] = new_bow

model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=data_lemmatized, start=2, limit=30, step=5)

res = sorted(zip(model_list, coherence_values), key = lambda x: x[1])  # Sort by coherence values ASC
best_model = res[-1][0]  # Select the best model by cv

best_model.save(f"{MODELPATH}/LDAmodel_{MODELNAME}.model")