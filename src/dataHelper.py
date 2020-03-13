from typing import Tuple, List, Dict
import re
import pandas as pd
import numpy as np
import json
from keras.utils import np_utils

"""
Plik z funkcjami do obslugi plikow, danych
"""


def load_lyrics(genre: str) -> Tuple[List[str], Dict[str, int], Dict[int, str]]:
    """
    Funkcja laduje z dolaczonego pliku csv odpowiednie teksty
    zgodne z gatunkiem oraz zwraca slownik przekonwertowanych
    znakow na liczby. Z tekstow usuwane sa wszelkie znaki nie
    bedace alfanumerycznymi, albo diakrytycznymi

    Parameters:
        genre (string): Gatunek muzyki.

    Returns:
        lyrics_list (list): Lista tekstow utworow.
        char_to_int (dict of char: int): Slownik znakow
        i odpowiadajacych im liczb
        int_to_char (dict of int: char): char_to_int^-1
    """

    lyrics_df = pd.read_csv('res/lyrics.csv')
    lyrics_list = []
    char_to_int = {}
    int_to_char = {}
    char_set = set()
    for text, genre_value in zip(lyrics_df['lyrics'], lyrics_df['genre']):
        if genre_value == genre:
            lyrics_list.append(
                re.sub(
                    r'[^0-9a-z.,\' ]+',
                    '',
                    str(text).lower()
                )
            )
            char_set.update(set(str(text)))
    for index, elem in enumerate(sorted(list(char_set))):
        char_to_int[elem] = index
        int_to_char[index] = elem
    return lyrics_list, char_to_int, int_to_char


def encode_data(lyrics_list: List[str], char_to_int: Dict[str, int]
                ) -> Tuple[List[List[int]], List[int]]:
    """
    Funkcja iteruje sie po tekscie kazdej piosenki i tworzy
    tablice X,y, posiadające wzorce do feedowania do LSTMu

    TODO zmienic - na razie mamy ciagi ustalonej dlugosci
    (jak w tutorialu), ale możemy zrobic tokenizacje i
    zdaniami feedowac. Nie mam pojecia czy to cokolwiek
    ulepszy, ale mozemy sprobowac.

    Parameters:
        lyrics_list (list): Lista tekstow utworow.
        char_to_int (dict of char: int): Slownik znakow
        i odpowiadajacych im liczb

    Returns:
        x_list (list of list): Ciagi znakow do ktorych y jest uzupelnieniem.
        y_list (list): Przewidywania.
    """

    dlugosc_wzorca = 100
    x_list = []
    y_list = []
    continuous_lyric = ' '.join(lyrics_list)
    for i in range(len(continuous_lyric) - dlugosc_wzorca):
        y_list.append(char_to_int[continuous_lyric[i + dlugosc_wzorca]])
        temp_x = []
        for elem in continuous_lyric[i: i + dlugosc_wzorca]:
            temp_x.append(char_to_int[elem])
        x_list.append(temp_x)
    return x_list, y_list


def convert_to_numpy(x_list: List[List[int]], y_list: List[int],
                     length: int, char_to_int_len: float) \
        -> Tuple[np.ndarray, np.ndarray]:
    """
    Funkcja konwertujaca Pythonowe listy do NumPy'owych arrayow
    ktore mozna bedzie feedowac do LSTMu

    Parameters:
        x_list (list of list): Ciagi znakow
        do ktorych y jest uzupelnieniem.
        y_list (list): Przewidywania.
        length (int): dlugosc wzorca
        char_to_int_len (int): ilosc roznych
        znakow w tekstach utworow

    Returns:
        x (np.ndarray): przekonwertowane x_list
        y (np.ndarray): przekonwertowane y_list
    """

    x = np.reshape(x_list, (len(x_list), length, 1))
    x = x / float(char_to_int_len)
    y = np_utils.to_categorical(y_list)
    return x, y


def save_data(x_list: List[List[int]], y_list: List[int],
              char_to_int: dict, path: str) -> None:
    """
    Funkcja zachowujaca listy do plikow, zeby na wypadek
    ponownego trenowania modelu nie trzeba bylo ponownie
    encodowac tekstow piosenek.

    Parameters:
        x_list (list of list): lista x
        y_list (list): lista y
        char_to_int (dict): slownik do encodowania
        path (str): sciezka do zapisu

    Returns:
        None
    """

    with open(path + 'x_list.json', 'w+') as x_file:
        x_file.write(str(x_list))
    with open(path + 'y_list.json', 'w+') as y_file:
        y_file.write(str(y_list))
    with open(path + 'char_to_int.json', 'w+') as y_file:
        y_file.write(str(char_to_int))
    return


def load_data(path: str) -> Tuple[List[List[int]], List[int]]:
    """
    Funkcja ladujaca listy z plikow, zeby na wypadek
    ponownego trenowania modelu nie trzeba bylo ponownie
    encodowac tekstow piosenek.

    Parameters:
        path (str): sciezka do plikow

    Returns:
        x_list (list of list): lista x
        y_list (list): lista y
    """

    with open(path + 'x_list.json', 'r') as x_file:
        x_list = json.loads(x_file.read())
    with open(path + 'y_list.json', 'r') as y_file:
        y_list = json.loads(y_file.read())
    return x_list, y_list
