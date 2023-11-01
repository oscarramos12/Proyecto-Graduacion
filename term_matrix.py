import os
import re
from collections import Counter
from nltk import ngrams as nltk_ngrams
from sklearn.feature_extraction.text import CountVectorizer
import reports

#hacer un reporte sucio y limpio para comparar
#columnas: nombre, tipo de ngrama, top, bottom


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\sáéíóúüñ]', '', text)
    return text

def generate_ngrams(text, n):
    words = text.split()
    ngrams_list = list(nltk_ngrams(words, n))
    return [' '.join(ngram) for ngram in ngrams_list]

def create_term_matrix(folder_path, n,top,bot,report_file):
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

        sorted_ngrams = sorted(ngram_freq.items(), key=lambda x: x[1], reverse=True)

        top_ngrams = dict(sorted_ngrams[:top])
        top_ngram_list = list(top_ngrams.keys())
        report_top = ''
        print("TOP:")
        for ngram in top_ngram_list:
            report_top += '[' + ngram + ']' + ' aparece: ' + str(ngram_freq[ngram]) + ' veces.\n'
            print(f"{ngram}: {ngram_freq[ngram]} times")

        bottom_ngrams = dict(sorted_ngrams[-bot:])
        bottom_ngram_list = list(bottom_ngrams.keys())
        report_bot = ''
        print("BOT:")
        for ngram in bottom_ngram_list:
            report_bot += '[' + ngram + ']' + ' aparece: ' + str(ngram_freq[ngram]) + ' veces.\n'
            print(f"{ngram}: {ngram_freq[ngram]} times")

        for i in range(bot+top):
            if((i < top) and (i < bot)):
                reports.write_report('file_reports',report_file,'N-Gramas',[filename,n,top_ngram_list[i],ngram_freq[top_ngram_list[i]],bottom_ngram_list[i],ngram_freq[bottom_ngram_list[i]]])
            elif((i < top) and (i >= bot)):
                reports.write_report('file_reports',report_file,'N-Gramas',[filename,n,top_ngram_list[i],ngram_freq[top_ngram_list[i]],'',''])
            elif((i >= top) and (i < bot)):
                reports.write_report('file_reports',report_file,'N-Gramas',[filename,n,'','',bottom_ngram_list[i],ngram_freq[bottom_ngram_list[i]]])

    #vectorizer = CountVectorizer(vocabulary=top_ngram_list + bottom_ngram_list)
    #term_matrix = vectorizer.fit_transform(flattened_ngrams)
    #feature_names = vectorizer.get_feature_names_out()
    #return term_matrix, feature_names

folder_path = "C:\\Users\\Oscar\\Desktop\\LIBROS\\txt_clean"
n = 3  
top = 20
bot = 20
create_term_matrix(folder_path, n,top,bot,'clean_files_reports')
'''
print("Top 20 N-grams and Frequencies:")
for ngram, freq in sorted(top_ngrams.items(), key=lambda x: x[1], reverse=True):
    print(f"{ngram}: {freq}")

print("\nBottom 5 N-grams and Frequencies:")
for ngram, freq in sorted(bottom_ngrams.items(), key=lambda x: x[1]):
    print(f"{ngram}: {freq}")
print("\nTerm Matrix:")
print(term_matrix.toarray())
cum = term_matrix.toarray()
result = ""
for line in cum:
     result += str(line)
with open('matriz.txt', 'w', encoding='utf-8') as file:
            file.write(result)
print("Feature Names:", feature_names)
'''
