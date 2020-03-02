from typing import Tuple, List, Dict
import re
import pandas as pd


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
                        r"[^0-9a-z.,' ]+",
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
            X (list of list): Ciagi znakow do ktorych y jest uzupelnieniem.
            y (list): Przewidywania.
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
    def save_data(x_list: List[List[int]], y_list: List[int], path: str) -> None:
        with open(path + 'x_list.json') as file:
            file.write(str(x_list))
        with open(path + 'y_list.json') as file:
            file.write(str(y_list))
