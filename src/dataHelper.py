from typing import Tuple, List, Dict

import pandas as pd


class DataHelper:
    """
    Klasa z funkcjami do obslugi plikow, danych
    """

    def __init__(self):
        pass

    @staticmethod
    def load_lyrics(genre: str) -> Tuple[List[str], Dict[set, int]]:
        """
        Funkcja laduje z dolaczonego pliku csv odpowiednie teksty
        zgodne z gatunkiem oraz zwraca slownik przekonwertowanych
        znakow na liczby.

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
        char_set = set()
        for text, genre_value in zip(lyrics_df['lyrics'], lyrics_df['genre']):
            if genre_value == genre:
                lyrics_list.append(str(text).lower())
                char_set.update(set(str(text)))
        for index, elem in enumerate(sorted(list(char_set))):
            char_to_int[elem] = index
        return lyrics_list, char_to_int
