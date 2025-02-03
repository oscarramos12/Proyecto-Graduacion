import spacy
from sklearn.metrics.pairwise import cosine_similarity
import os
import spacy
from fuzzywuzzy import fuzz

def format(name):
    name = name.lower()
    name = name.replace("-", " ")
    name = name.replace('_', ' ')
    name = name.split('.')[0]
    return name


def check_dups():


    nlp = spacy.load("es_core_news_sm")

    file_name_1 = "emma by jane austen"
    file_name_2 = "emma by jane austen: el regreso"

    tokens_1 = [token.text.lower() for token in nlp(file_name_1)]
    tokens_2 = [token.text.lower() for token in nlp(file_name_2)]
    

    intersection = len(set(tokens_1).intersection(tokens_2))
    union = len(set(tokens_1).union(tokens_2))
    jaccard_similarity = intersection / union if union > 0 else 0.0

    levenshtein_distance = fuzz.ratio(file_name_1, file_name_2) / 100.0  # Normalize to [0, 1]

    threshold = 0.4 

    overall_similarity = (jaccard_similarity + levenshtein_distance) / 2.0

    print(overall_similarity)
    if overall_similarity >= threshold:
        print("File names are similar and can be discarded.")
    else:
        print("File names are dissimilar and should be kept.")

check_dups()
