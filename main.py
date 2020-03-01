# import numpy as np
import pandas as pd
from pprint import pprint
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import Dropout
# from keras.layers import LSTM
# from keras.callbacks import ModelCheckpoint
# from keras.utils import np_utils

def load_lyrics():
    lyrics_df = pd.read_csv('res/lyrics.csv')
    genre_set = {}
    for genre in lyrics_df['genre']:
        if genre in genre_set:
            genre_set[genre] += 1
        else:
            genre_set[genre] = 1
    pprint(genre_set)

if __name__=='__main__':
    load_lyrics()