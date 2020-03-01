import pandas as pd


class DataHelper:
    """
    Klasa z funkcjami do obslugi plikow, danych
    """

    def __init__(self):
        pass

    @staticmethod
    def load_lyrics(genre):
        """
        Funkcja laduje z dolaczonego pliku csv odpowiednie teksty
        zgodne z gatunkiem.

        Parameters:
            genre (string): Gatunek muzyki.

        Returns:
            lyrics_list (list): Lista tekstow utworow.
        """

        lyrics_df = pd.read_csv('../res/lyrics.csv')
        lyrics_list = []
        for text, genre_value in zip(lyrics_df['lyrics'], lyrics_df['genre']):
            if genre_value == genre:
                lyrics_list.append(str(text).lower())
        return lyrics_list
