import sys
sys.path.append('..')
from collections import defaultdict
from nltk import ngrams
from typing import List
import json
import re


def load_lyrics_words(genre: str) -> List[str]:
    """
    Funkcja ladujaca z datasetu piosenki odpowiedniego 
    gatunku i zwracajaca liste slow, dla modelu ngramu.

    Parameters:
        genre (str): gatunek muzyki

    Returns:
        word_list (list): lista slow
    """
    text = open("teksty/"+genre+'.txt','r').read()
    text = text.replace('\n',' ')
    
    pattern = re.compile('[^\t\n]+|[\t\n]+')    
    lyrics = [val for values in map(pattern.findall, text.split(' ')) for val in values]
    lyrics_list = []
    lyrics_list.append(lyrics)
    return lyrics_list
    


def generate_ngram(genre):
    """
    Funkcja tworząca model ngramu z zaciągniętej listy słów danego gatunku

    Parameters:
        genre (str): gatunek muzyki

    Returns:
        model (defaultdict): model ngramu
    """
    lista = load_lyrics_words(genre)
    model = defaultdict(lambda: defaultdict(int))
    for zdanie in lista:
        for slowo1, slowo2 in ngrams(zdanie, 2):
            model[slowo1][slowo2] += 1
    for slowo1 in model:
        
        ilosc_wystapien = float(sum(model[slowo1].values()))
        for slowo in model[slowo1]:
            model[slowo1][slowo] /= ilosc_wystapien 
    return model

def save_ngram(name, model):
    """
    Zapisanie modelu do pliku w formacie JSON

    Parameters:
        name (str): nazwa pliku
        model (defaultdict): model ngramu

    Returns:        
    """
    js = json.dumps(model)
    f = open(name+".json","w")
    f.write(js)
    f.close()

def generate_all_ngrams():
    """
    Funkcja generująca modele dla wszystkich dostępnych
    getunków muzycznych. Modele są zapisywane w plikach 
    o nazwach odpowiadjacych gatunkom

    Parameters:

    Returns:        
    """

    Genres = ['Metal', 'Soul', 'Punk', 'Folk','Rap', 'Hip_Hop', 'Pop','Rock', 'Indie', 'Country', 'Blues']
    for i,gen in enumerate(Genres):
        print(f'{i+1}/{len(Genres)}')
        model = generate_ngram(gen)
        save_ngram(gen, model)
        
        
if __name__ == '__main__':
    generate_all_ngrams()
