# import numpy as np
import pandas as pd
from pprint import pprint
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import Dropout
# from keras.layers import LSTM
# from keras.callbacks import ModelCheckpoint
# from keras.utils import np_utils
from src.dataHelper import DataHelper

if __name__ == '__main__':
    lista_utworow = DataHelper.load_lyrics('Country')
