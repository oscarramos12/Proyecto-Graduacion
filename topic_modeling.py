from bertopic import BERTopic
import json
import pandas as pd
import os
import codecs
from nltk.corpus import stopwords
import reports

folder_path = 'C:\\Users\\Oscar\\Desktop\\LIBROS\\topic_model\\'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    if filename.endswith('.txt'):
        with codecs.open(file_path, 'r', 'utf-8') as file:
            text = file.read()
    sentences = text.split('.')
    spanish_stopwords = set(stopwords.words('spanish'))

    sentences_without_stopwords = []

    for sentence in sentences:
        words = sentence.split(' ')

        filtered_words = [word for word in words if word.lower() not in spanish_stopwords]

        modified_sentence = ' '.join(filtered_words)

        sentences_without_stopwords.append(modified_sentence)

    sentences_without_stopwords = [item for item in sentences_without_stopwords if item != '']
    topic_model = BERTopic(embedding_model="all-MiniLM-L6-v2")
    topics, probs = topic_model.fit_transform(sentences_without_stopwords)
    results = topic_model.get_topic(topic=0)

    for result in results:
        word = result[0]
        value = result[1]
        reports.write_report('file_reports','clean_files_reports','Modelacion Temas',[filename,word,value])
    print(f'DONE: {filename}')


                    