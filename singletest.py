import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
from gensim import corpora, models
import gensim
import spacy
from gensim.models import CoherenceModel
import glob

import pyLDAvis
import pyLDAvis.gensim

# Download NLTK data
#nltk.download('punkt')
#nltk.download('stopwords')


#

def main():
    
    folder_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\topic_model\\*.txt'  # Update with your folder path and file extension
    read_file = ""
    for file_path in glob.glob(folder_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            read_file = file.read()

    def sent_to_words(sentences):
        yield(gensim.utils.simple_preprocess(str(sentences), deacc=True, min_len=4))  # deacc=True removes punctuations

    read_file = ' '.join(read_file.split())

    data_words = list(sent_to_words(read_file))
    nlp = spacy.load('es_core_news_sm', disable=['parser', 'ner'])
    nlp.max_length = 30000000 
    stop_words = stopwords.words('spanish')
    stop_words.append(['decir','habio','hacer'])

    #ahi veo que pedo
    bigram = gensim.models.Phrases(data_words, min_count=2, threshold=100)

    bigram_mod = gensim.models.phrases.Phraser(bigram)

    def remove_stopwords(texts):
        return [[word for word in gensim.utils.simple_preprocess(str(texts)) if word not in stop_words]]

    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]

    def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'ADV']):#, 'VERB'
        texts_out = []
        for sent in texts:
            doc = nlp(" ".join(sent)) 
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        return texts_out

    data_words_nostops = remove_stopwords(data_words)

    data_words_bigrams = make_bigrams(data_words_nostops)

    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    id2word = corpora.Dictionary(data_lemmatized)

    texts = data_lemmatized

    corpus = [id2word.doc2bow(text) for text in texts]

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                            id2word=id2word,
                                            num_topics=5, 
                                            random_state=100,
                                            update_every=1,
                                            chunksize=500,
                                            passes=10,
                                            alpha='auto',
                                            per_word_topics=True)
    for topic in lda_model.print_topics():
    
        print(topic)

    print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

    #coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
    #coherence_lda = coherence_model_lda.get_coherence()
    #print('\nCoherence Score: ', coherence_lda)

    #vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    #pyLDAvis.display(vis)

if __name__ == "__main__":
    main()