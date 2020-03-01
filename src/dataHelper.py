import pandas as pd


class DataHelper:
    """
    Klasa z funkcjami do obslugi plikow, danych
    """

    @staticmethod
    def load_lyrics(genre):
        """
        Funkcja laduje z dolaczonego pliku csv odpowiednie teksty
        zgodne z gatunkiem.

        Parameters:
            genre (string): Gatunek muzyki.

        Returns:
            genre_set (list): Lista tekstow utworow.
        """

        lyrics_df = pd.read_csv('../res/lyrics.csv')
        genre_set = []
        for text, genre_value in zip(lyrics_df['lyrics'], lyrics_df['genre']):
            if genre_value == genre:
                genre_set.append(str(text).lower())
        return genre_set
