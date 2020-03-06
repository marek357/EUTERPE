from src.dataHelper import load_lyrics, encode_data, convert_to_numpy
from src.dataHelper import save_data, load_data
from src.modelHelper import character_model
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import LSTM, Dense, GRU, Embedding
from keras.callbacks import EarlyStopping, ModelCheckpoint

if __name__ == '__main__':
    """
    Workflow do trenowania sieci:
    * - opcjonalne
    
    1) load_lyrics
    2) encode_data
    3*) save_data - zrobienie checkpointu, zeby 
    nie encodowac znowu przy kolejnym uruchamianiu
    4) convert_to_numpy
    """
    LOAD_DATA = True
    if LOAD_DATA:
        lyrics_list, char_to_int = load_lyrics('Country')
        print('done1')
        x_list, y_list = encode_data(lyrics_list, char_to_int)
        print('done2')
        save_data(x_list, y_list, char_to_int, '/Users/marekmasiak/Desktop/')
        print('done3')
        x, y = convert_to_numpy(x_list, y_list, 100, float(len(char_to_int)))
        print('done4')
        character_model(x, y, len(char_to_int))
        print('done5')
    else:
        data, length = load_data('/Users/marekmasiak/Desktop/')
        character_model(data, length)
    print('done4')

    # save_data(x_list, y_list, '/Users/marekmasiak/Desktop/')
    # x_list, y_list = load_data('/Users/marekmasiak/Desktop/')
    # x, y = convert_to_numpy(x_list, y_list, 100, float(len(char_to_int)))
