from typing import Tuple, List, Dict
import re
import pandas as pd
import numpy as np
import json
from keras.utils import np_utils


class DataHelper:
    """
    Klasa z funkcjami do obslugi plikow, danych
    """

    def __init__(self):
        pass

    @staticmethod
    def load_lyrics(genre: str) -> Tuple[List[str], Dict[str, int]]:
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
        """

        lyrics_df = pd.read_csv('res/lyrics.csv')
        lyrics_list = []
        char_to_int = {}
        dlugosc = 0
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
                dlugosc += len(lyrics_list[-1])
                char_set.update(set(str(text)))
        for index, elem in enumerate(sorted(list(char_set))):
            char_to_int[elem] = index
        return lyrics_list, char_to_int

    @staticmethod
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

    @staticmethod
    def convert_to_numpy(x_list: List[List[int]], y_list: List[int],
                         dlugosc: int, char_to_int_len: int) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Funkcja konwertujaca Pythonowe listy do NumPy'owych arrayow
        ktore mozna bedzie feedowac do LSTMu

        Parameters:
            x_list (list of list): Ciagi znakow
            do ktorych y jest uzupelnieniem.
            y_list (list): Przewidywania.
            dlugosc (int): dlugosc wzorca
            char_to_int_len (int): ilosc roznych
            znakow w tekstach utworow

        Returns:
            x (np.ndarray): przekonwertowane x_list
            y (np.ndarray): przekonwertowane y_list
        """

        x = np.reshape(x_list, (len(x_list), dlugosc, 1))
        x /= float(char_to_int_len)
        y = np_utils.to_categorical(y_list)
        return x, y

    @staticmethod
    def save_data(x_list: List[List[int]], y_list: List[int],
                  path: str) -> None:
        """
        Funkcja zachowujaca listy do plikow, zeby na wypadek
        ponownego trenowania modelu nie trzeba bylo ponownie
        encodowac tekstow piosenek.

        Parameters:
            x_list (list of list): lista x
            y_list (list): lista y
            path (str): sciezka do zapisu

        Returns:
            None
        """

        with open(path + 'x_list.json', 'w+') as file:
            file.write(str(x_list))
        with open(path + 'y_list.json', 'w+') as file:
            file.write(str(y_list))
        return

    @staticmethod
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
