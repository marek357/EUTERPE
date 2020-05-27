import random
import json


def load_ngram(name):
    """
    Funkcja zaciągająca model ngramu z pliku

    Parameters:
        name (str): nazwa pliku z modelem

    Returns:
        model (defaultdict): model ngramu
    """
    with open("./"+name+".json") as json_file:
        model = json.load(json_file)
    return model

def generate_text(model, dlugosc_lancucha):
    """
    Funkcja wypisująca tekst o podanej długoci według danego modelu

    Parameters:
        model (defaultdict): model ngramu
        dlugosc_lancucha (int): liczba słów w tekscie

    Returns:
        lancuch (str): Gotowy tekst
    """

    lancuch = [random.choice(list(model.keys()))]
    for i in range(dlugosc_lancucha):
        try:
            lancuch.append(random.choices(
                population = list(model[lancuch[-1]].keys()),
                weights = list(model[lancuch[-1]].values()),
                k = 1
            )[0])
        except:
            pass
    return ' '.join(lancuch)
def dressing(genre, liczba_zwrotek = 4, liczba_wersow_zwrotki = 5, liczba_wersow_ref = 4, powtorzenia_refrenu = 1, avr_slow_w_wersie = 6):
    """
    Funkcja komponująca piosenkę o zadanych parametrach

    Parameters:
        genre (str): Gatunek
        liczba_zwrotek (int):  liczba zwrotek w piosence
        liczba_wersow_zwrotki (int): liczba wersow każdej zwrotki
        liczba_wersow_ref (int): liczba wersow refrenu
        avr_slow_w_wersie (int): srednia liczba slow w kazdym wersie
    Returns:
        song (str): Gotowa piosenka
    """
    model = load_ngram(genre)

    def zwrotka(liczba_wersow, avr_slow_w_wersie):        
        text_rar = generate_text(model,liczba_wersow*(avr_slow_w_wersie + 2))
        text = ""
        i=0 # iterator slow w wersie
        j=0 # iterator wersow
        k=0 #iterator po wszystkich slowach
        while j < liczba_wersow:
            word = text_rar.split()[k]
            text = text + word+ ' '
            i+=1
            if i >= avr_slow_w_wersie-1 and len(word) > 3:
                j+=1
                i=0
                text = text + '\n'
            k+=1
        text[0].upper()
        
        return text
    
    song = ""
    ref = zwrotka(liczba_wersow_ref, avr_slow_w_wersie)
    for i in range(liczba_zwrotek):
        zwroteczka = zwrotka(liczba_wersow_zwrotki, avr_slow_w_wersie)
        song = song + zwroteczka + '\n'
        for i in range(powtorzenia_refrenu):
            song = song + ref + '\n'
    return song

def save(song, name):
    text_file = open(name+".txt", "w")
    text_file.write(song)
    text_file.close()
def read(name):
    text_file = open(name+".txt", "r")
    song = text_file.read()
    text_file.close()
    return song
    
if __name__ == '__main__':

    Genres = ['Metal', 'Soul', 'Punk', 'Folk','Rap', 'Hip_Hop', 'Pop','Rock', 'Indie', 'Country', 'Blues']
 
    gatunek = int(input())
    gatunek = Genres[gatunek-3]
    
    liczbaZwrotek = int(input())
    powtorzeniaRefrenu = int(input())
    liczbaWersowZwrotki = int(input())
    liczbaWersowRefrenu = int(input())

#    model = load_ngram('Rap')
#    print(generate_text(model,500))
    song = dressing('Country', liczbaZwrotek, liczbaWersowZwrotki, liczbaWersowRefrenu, powtorzeniaRefrenu, avr_slow_w_wersie = 4)
    print(song)
    save(song,'xd')
#    song = read('xd')
#    print(song)
