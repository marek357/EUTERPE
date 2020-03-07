from src.dataHelper import load_lyrics, encode_data, convert_to_numpy
from src.dataHelper import save_data, load_data
from src.modelHelper import character_model
from src.generator import generate

if __name__ == '__main__':
    """
    Workflow do trenowania sieci:
    * - opcjonalne
    
    1) load_lyrics
    2) encode_data
    3*) save_data - zrobienie checkpointu, zeby 
    nie encodowac znowu przy kolejnym uruchamianiu
    4) convert_to_numpy
    """
    LOAD_DATA = True
    if LOAD_DATA:
        lyrics_list, char_to_int, int_to_char = load_lyrics('Folk')
        print('done1')
        x_list, y_list = encode_data(lyrics_list, char_to_int)
        print('done2')
        save_data(x_list, y_list, char_to_int, '/Users/marekmasiak/Desktop/')
        print('done3')
        x, y = convert_to_numpy(x_list, y_list, 100, float(len(char_to_int)))
        print('done4')
        # character_model(x, y)
        generate(x, y, int_to_char, x_list[0])
        print('done5')
    else:
        x, y, char_to_int = load_data('/Users/marekmasiak/Desktop/')
        x, y = convert_to_numpy(x, y, 100, float(char_to_int))
        character_model(x, y)
    print('done4')

