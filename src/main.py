# import numpy as np
import pandas as pd
from pprint import pprint
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import Dropout
# from keras.layers import LSTM
# from keras.callbacks import ModelCheckpoint
# from keras.utils import np_utils


def load_lyrics(genre):
    """
    Funkcja laduje z dolaczonego pliku csv odpowiednie teksty
    zgodne z gatunkiem.

    Parameters:
        genre (string): Gatunek muzyki.
    
    Returns:
        genre_set (list): Lista tekstow utworow.
    """

    lyrics_df = pd.read_csv('../res/lyrics.csv')
    genre_set = []
    for text, genre_value in zip(lyrics_df['lyrics'], lyrics_df['genre']):
        if genre_value == genre:
            genre_set.append(str(text).lower())
    return genre_set

if __name__=='__main__':
    lista_utworow = load_lyrics('Country')