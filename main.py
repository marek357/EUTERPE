from src.dataHelper import DataHelper
from pprint import pprint

if __name__ == '__main__':
    lista_utworow, char_to_int = DataHelper.load_lyrics('Country')
    x, y = DataHelper.encode_data(lista_utworow, char_to_int)
    pprint(x)
    pprint(y)
