import os
import re
from collections import Counter
from nltk import ngrams as nltk_ngrams
from sklearn.feature_extraction.text import CountVectorizer

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\sáéíóúüñ]', '', text)
    return text

def generate_ngrams(text, n):
    words = text.split()
    ngrams_list = list(nltk_ngrams(words, n))
    return [' '.join(ngram) for ngram in ngrams_list]

def create_term_matrix(folder_path, n):
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                preprocessed_text = preprocess_text(text)
                documents.append(preprocessed_text)

    ngrams_per_document = [generate_ngrams(doc, n) for doc in documents]

    flattened_ngrams = [ngram for sublist in ngrams_per_document for ngram in sublist]

    ngram_freq = Counter(flattened_ngrams)

    top_ngrams = dict(sorted(ngram_freq.items(), key=lambda x: x[1], reverse=True)[:20])
    top_ngram_list = list(top_ngrams.keys())

    vectorizer = CountVectorizer(vocabulary=top_ngram_list)
    term_matrix = vectorizer.fit_transform(flattened_ngrams)
    return term_matrix, vectorizer.get_feature_names_out()

folder_path = "C:\\Users\\Oscar\\Desktop\\LIBROS\\temp"
n = 3  
term_matrix, feature_names = create_term_matrix(folder_path, n)

print("Term Matrix:")
print(term_matrix.toarray())
print("Feature Names:", feature_names)
