from nltk.corpus import reuters, brown
from nltk import bigrams, trigrams, ngrams
from collections import Counter, defaultdict
from random import randint
from pprint import pprint

"""
Plik generujący ngramy
"""


def ngram_gen(input_dict):
    model = defaultdict(lambda: defaultdict(lambda: 0))
    for sentence in input_dict:
        for a, b in bigrams(sentence.split(' '), pad_right=True, pad_left=True):
            model[a][b] += 1
    for a in model:
        count = float(sum(model[a].values()))
        for b in model[a]:
            model[a][b] /= count
    return model


def random_weigths(d):
    weight_list = []
    for (key, value) in d.items():
        weight_list += [key] * int(value * 200.)
    if not weight_list:
        return ""
    return weight_list[randint(0, len(weight_list) - 1)]


def predict_next_words(word, model):
    sList = []
    prev2 = word
    # pprint(model)
    for _ in range(100):
        d = dict(model[prev2])
        out = random_weigths(d)
        sList.append(prev2)
        prev2 = out
        if out == "":
            # print("Break")
            break
    sList.append(prev2)
    return " ".join(filter(lambda x: x is not None, sList))
