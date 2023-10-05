from bertopic import BERTopic
import pandas as pd
import os
import codecs
from nltk.corpus import stopwords

folder_path = "C:\\Users\\Oscar\\Desktop\\LIBROS\\txt_clean\\"

file_contents = []
stop_words = stopwords.words('spanish')
for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Filter for text files
            file_path = os.path.join(folder_path, filename)
            with codecs.open(file_path, 'r', 'utf-8') as file:
                content = file.readlines()
                for line in content:
                     words = line.split(' ')
                     line_no_stopwords = ''
                     for word in words:
                        if(word not in stop_words):
                             line_no_stopwords += word + ' '
            file_contents.append(line_no_stopwords)
                            
print(len(file_contents))

topic_model = BERTopic(embedding_model="all-MiniLM-L6-v2")
topics, probs = topic_model.fit_transform(file_contents)


print(topic_model.get_topic_info())

print(topic_model.get_topic(topic=0))







