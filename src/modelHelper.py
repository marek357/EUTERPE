import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint


class ModelHelper:
    """
    Klasa obslugujaca funkcje zwiazane z modelem,
    ktory uczy sie tekstu
    """

    def __init__(self):
        pass

    @staticmethod
    def character_model(X: np.ndarray, y: np.ndarray) -> None:
        """
        Funkcja majaca za zadanie utworzenie i trenowanie
        modelu na danych podanych jako argumenty.
        Ponadto funkcja tworzy checkpointy, do którch można
        pozniej wrocic (nie zaczynajac od zera obliczenia).

        Parameters:
            X (np.ndarray):
            y (np.ndarray):

        Returns:
            None
        """
        model: Sequential = Sequential()
        model.add(
            LSTM(
                256,
                input_shape=(X.shape[1], X.shape[2]),
                return_sequences=True
            )
        )
        model.add(Dropout(0.2))
        model.add(LSTM(256))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1], activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
        checkpoint = ModelCheckpoint(
            filepath,
            monitor='loss',
            verbose=1,
            save_best_only=True,
            mode='min'
        )
        callbacks_list = [checkpoint]
        model.fit(X, y, epochs=500, batch_size=64, callbacks=callbacks_list)
        return

