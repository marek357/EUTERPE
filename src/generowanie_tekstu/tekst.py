import sys
sys.path.append('..')
from dataHelper import load_lyrics_words
from collections import defaultdict
from nltk import ngrams
import random


def generate_ngram(genre, dlugosc_lancucha):
    lista = load_lyrics_words(genre)
    polaczenia = defaultdict(lambda: defaultdict(int))
    for zdanie in lista:
        for slowo1, slowo2 in ngrams(zdanie, 2):
            polaczenia[slowo1][slowo2] += 1
    for slowo1 in polaczenia:
        ilosc_wystapien = float(sum(polaczenia[slowo1].values()))
        for slowo in polaczenia[slowo1]:
            polaczenia[slowo1][slowo] /= ilosc_wystapien 
    lancuch = [random.choice(list(polaczenia.keys()))]
    for i in range(dlugosc_lancucha):
        try:
            lancuch.append(random.choices(
                population = list(polaczenia[lancuch[-1]].keys()),
                weights = list(polaczenia[lancuch[-1]].values()),
                k = 1
            )[0])
        except:
            pass
    return ' '.join(lancuch)


if __name__ == '__main__':
    print(generate_ngram(sys.argv[1], int(sys.argv[2])))
