from nltk.corpus import reuters, brown
from nltk import bigrams, trigrams, ngrams
from collections import Counter, defaultdict
from random import randint
from pprint import pprint

"""
Plik generujący ngramy
"""


def ngram_gen(input_dict):
    """
    Wprowadzam model bigramu i obliczam odpowiednie wagi początkowe
    """
    model = defaultdict(lambda: defaultdict(lambda: 0))
    for sentence in input_dict:
        for a, b in bigrams(sentence.split(' '), pad_right=True, pad_left=True):
            model[a][b] += 1
    for a in model:
        count = float(sum(model[a].values()))
        for b in model[a]:
            model[a][b] /= count
    return model


def random_weigths(model):
    """
    Funkcja do generowania losych wag
    """
    weight_list = []
    for (key, value) in model.items():
        weight_list += [key] * int(value * 300.)
    if not weight_list:
        return ""
    return weight_list[randint(0, len(weight_list) - 1)]


def predict_next_words(word, model):
    """
    Funkcja do generowania zdań z bigramów
    """
    sentence = []
    previous_outcome = word
    for _ in range(100):
        weights = dict(model[previous_outcome])
        out = random_weigths(weights)
        sentence.append(previous_outcome)
        previous_outcome = out
        if out == "":
            break
    sentence.append(previous_outcome)
    return " ".join(filter(lambda x: x is not None, sentence))
