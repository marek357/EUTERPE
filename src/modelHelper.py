from sklearn.model_selection import train_test_split
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import ModelCheckpoint


"""
Plik obslugujacy funkcje zwiazane z modelem,
ktory uczy sie tekstu
"""


def character_model(x: np.ndarray, y: np.ndarray) -> None:
    """
    Funkcja majaca za zadanie utworzenie i trenowanie
    modelu na danych podanych jako argumenty.
    Ponadto funkcja tworzy checkpointy, do którch można
    pozniej wrocic (nie zaczynajac od zera obliczenia).

    Parameters:
        x (np.ndarray): NumPy'owa tablica
            z zaencodowanymi danymi
        y (np.ndarray): NumPy'owa tablica
            z zaencodowanymi danymi

    Returns:
        None
    """

    print(x.shape)
    print('-----')
    print(y.shape)
    print('-----')

    model = Sequential()
    model.add(LSTM(256, input_shape=(x.shape[1], x.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    model.fit(x, y, epochs=50, batch_size=64, callbacks=[checkpoint])
    return

