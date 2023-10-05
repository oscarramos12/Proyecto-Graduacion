import os
import glob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from nltk.corpus import stopwords

import nltk
#nltk.download('stopwords')
#nltk.download('punkt')

def generate_term_matrix(folder_path):
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))

    term_frequencies = Counter()

    spanish_stop_words = set(stopwords.words('spanish'))

    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as file:
            content = file.read()
            words = content.lower().split()

            words = [word for word in words if word not in spanish_stop_words]

            term_frequencies.update(words)

    top_terms = dict(term_frequencies.most_common(15))

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top_terms)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    wordcloud.to_file(os.path.join(folder_path, "wordcloud.png"))

# Example usage
folder_path = "C:\\Users\\Oscar\\Desktop\\LIBROS\\txt_clean\\"
generate_term_matrix(folder_path)
