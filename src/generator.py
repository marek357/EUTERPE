from sklearn.model_selection import train_test_split
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import ModelCheckpoint


"""
Plik obslugujacy model generujacy tekst
"""


def generate(x, y, int_to_char):
    model = Sequential()
    model.add(LSTM(256, input_shape=(x.shape[1], x.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    # model.add(LSTM(256))
    # model.add(Dropout(0.2))
    print(x.shape)
    print('-----')
    print(y.shape)
    print('-----')

    model.add(Dense(y.shape[1], activation='softmax'))
    filename = "res/weights-improvement-50-1.7895-bigger.hdf5"
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    pattern = 'rise and fall, like the tidemy hand goes with' \
              ' your cheststeady now, moon will pulla slow and even br'
    for i in range(1000):
        x = np.reshape(pattern, (1, len(pattern), 1))
        x = x / float(len(int_to_char))
        prediction = model.predict(x, verbose=0)
        index = np.argmax(prediction)
        result = int_to_char[index]
        print(result)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
