from sklearn.model_selection import train_test_split
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import ModelCheckpoint


"""
Plik obslugujacy model generujacy tekst
"""


def generate(x, y, int_to_char, pattern):
    model = Sequential()
    model.add(LSTM(256, input_shape=(x.shape[1], x.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))
    print(x.shape)
    print('-----')
    print(y.shape)
    print('-----')

    for char in pattern:
        print(int_to_char[char], end=' ')
    filename = "res/weights-improvement-01-2.7803-bigger.hdf5"
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    print(pattern)
    # pattern = 'rise and fall, like the tidemy hand goes with your cheststeady now, moon will pulla slow and even br'
    for i in range(3000):
        x_test = np.reshape(pattern, (1, len(pattern), 1))
        x_test = x_test / float(len(int_to_char))
        prediction = model.predict(x_test, verbose=0)
        index = np.argmax(prediction)
        result = int_to_char[index]
        print(result, end='')
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
