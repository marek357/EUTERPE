from midiutil import MIDIFile
import random
import copy

#oznaczenia rodzajów dźwięków w programie
C=0
Cis=1
D=2
Dis=3
E=4
F=5
Fis=6
G=7
Gis=8
A=9
B=10
H=11

#oznaczenia rodzajów skal
Dur=1
Mol=2
Blues=3

#oznaczenia gatunków
Other = 1
Not_Available = 2
Metal = 3
Country = 4
R_B = 5
Folk = 6
Rock = 7
Jazz = 8
Indie = 9
Electronic = 10
Pop = 11
Hip_Hop = 12

#funkcje generujące skale

def generateMajorScale(key):
    curr = key
    scale = list()
    for i in range(7):
        scale.append(curr)
        if i == 2 or i == 6:
            curr = curr + 1
        else:
            curr = curr + 2
        curr = curr % (H + 1)
    return tuple(scale)

#harmoniczna skala molowa
def generateMinorScale(key):
    curr = key
    scale = list()
    for i in range(7):
        scale.append(curr)
        if i == 1 or i == 4 or i == 6:
            curr = curr + 1
        else:
            curr = curr + 2
        curr = curr % (H + 1)
    return tuple(scale)

def generateBluesScale(key):
    scale = list(generateMajorScale(key))
    scale[2] = (scale[2] + H) % (H + 1)
    scale[4] = (scale[4] + H) % (H + 1)
    scale[6] = (scale[6] + H) % (H + 1)
    return tuple(scale)

def generateScale(key, type):
    key = key % (H + 1)
    if type == Dur:
        return generateMajorScale(key)
    elif type == Mol:
        return generateMinorScale(key)
    elif type == Blues:
        return generateBluesScale(key)

#klasa zawierając dźwięki gamy
class Skala:
    def __init__(this, key, type):
        this.key = key
        this.type = type
        this.gama = generateScale(key, type)

#dostępne gatunki jako listy instrumentów

OtherInstrumenty = list(range(1, 112+1))
Not_AvailableInstrumenty = list(range(1, 112+1))
MetalInstrumenty = [31, 32, 34, 35]
CountryInstrumenty = [4, 21, 26, 41, 42, 106]
R_BInstrumenty = [8, 33, 34, 84, 89]
FolkInstrumenty = [4, 13, 16, 22, 23, 41, 42, 46, 48, 76, 78, 107, 108, 109, 110, 112]
RockInstrumenty = [19, 26, 28, 29, 30, 34, 35, 87]
JazzInstrumenty = [1, 2, 3, 8, 27, 33, 34, 43, 44, 46, 57, 58]
IndieInstrumenty = [3, 8, 12, 14, 26, 33, 38, 54, 79]
ElectronicInstrumenty = [5, 6, 39, 40, 45, 51, 52, 55, 63, 64, 81, 82]
PopInstrumenty = [5, 6, 26, 28, 29, 33, 49, 50, 81, 87, 89, 90, 96, 97]
Hip_HopInstrumenty = [33, 34, 84, 98]


OtherPerkusja = list(range(35, 81+1))
Not_AvailablePerkusja = list(range(35, 81+1))
MetalPerkusja = [37, 38, 40, 43, 44, 45, 46, 47, 49, 51, 57]
CountryPerkusja = [35, 54, 58, 69]
R_BPerkusja = [35, 36, 39, 60, 73]
FolkPerkusja = [41, 48, 50, 53, 54, 56, 58, 60, 61, 69, 70, 73, 80]
RockPerkusja = [35, 36, 37, 38, 40, 43, 44, 45, 46, 47, 49, 51, 53, 56, 57]
JazzPerkusja = [35, 51, 55, 57, 59]
IndiePerkusja = [35, 36, 41, 48, 53, 56, 73, 80]
IndiePerkusja = [35, 36, 41, 48, 53, 56, 73, 80]
ElectronicPerkusja = [39, 40, 45, 47]
PopPerkusja = [35, 36, 41, 48, 53, 56]
Hip_HopPerkusja = [35, 36, 39]

#konwersja slowa oznaczającego tonację na int
def keyToInt(key):
    res = C
    if key == 'C':
        res = C
    if key == 'Cis':
        res = Cis
    if key == 'D':
        res = D
    if key == 'Dis':
        res = Dis
    if key == 'E':
        res = E
    if key == 'F':
        res = F
    if key == 'Fis':
        res = Fis
    if key == 'G':
        res = G
    if key == 'Gis':
        res = Gis
    if key == 'A':
        res = A
    if key == 'B':
        res = B
    if key == 'H':
        res = H
    return res

#konwersja slowa oznaczającego skalę na int
def scaleToInt(scale):
    res = Dur
    if scale == 'Dur':
        res = Dur
    if scale == 'Mol':
        res = Mol
    if scale == 'Blues':
        res = Blues
    return res

#konwersja slowa oznaczającego gatunek na int
def genreToInt(genre):
    res = Other
    if genre == 'Other':
        res = Other
    if genre == 'Metal':
        res = Metal
    if genre == 'Country':
        res = Country
    if genre == 'R&B':
        res = R_B
    if genre == 'Folk':
        res = Folk
    if genre == 'Rock':
        res = Rock
    if genre == 'Jazz':
        res = Jazz
    if genre == 'Indie':
        res = Indie
    if genre == 'Electronic':
        res = Electronic
    if genre == 'Pop':
        res = Pop
    if genre == 'Hip-Hop':
        res = Hip_Hop
    return res




def getInstrumentsForGenre(gatunek):
    if gatunek == Other:
        return OtherInstrumenty
    if gatunek == Not_Available:
        return Not_AvailableInstrumenty
    if gatunek == Metal:
        return MetalInstrumenty
    if gatunek == Country:
        return CountryInstrumenty
    if gatunek == R_B:
        return R_BInstrumenty
    if gatunek == Folk:
        return FolkInstrumenty
    if gatunek == Rock:
        return RockInstrumenty
    if gatunek == Jazz:
        return JazzInstrumenty
    if gatunek == Indie:
        return IndieInstrumenty
    if gatunek == Electronic:
        return ElectronicInstrumenty
    if gatunek == Pop:
        return PopInstrumenty
    if gatunek == Hip_Hop:
        return Hip_HopInstrumenty

def getDrumsForGenre(gatunek):
    if gatunek == Other:
        return OtherPerkusja
    if gatunek == Not_Available:
        return Not_AvailablePerkusja
    if gatunek == Metal:
        return MetalPerkusja
    if gatunek == Country:
        return CountryPerkusja
    if gatunek == R_B:
        return R_BPerkusja
    if gatunek == Folk:
        return FolkPerkusja
    if gatunek == Rock:
        return RockPerkusja
    if gatunek == Jazz:
        return JazzPerkusja
    if gatunek == Indie:
        return IndiePerkusja
    if gatunek == Electronic:
        return ElectronicPerkusja
    if gatunek == Pop:
        return PopPerkusja
    if gatunek == Hip_Hop:
        return Hip_HopPerkusja

if __name__=="__main__":
    #losowanie głównych parametrów utworu
    parametry = input('Czy chcesz wybrać parametry utworu (T/N)')
    #tempo
    if parametry == 'T':
        tempo = input('Wprowadź tempo od 70 do 120 lub R (domyślne losowanie)')
        if tempo != 'R':
            tempo = int(tempo)
    if parametry == 'N' or tempo == 'R':
        tempo=random.randint(70, 120)
    #metrum, podstawą jest zawsze ćwierćnuta (np. po wylosowaniu 3 metrum to 3/4)
    if parametry == 'T':
        metrum = input('Wprowadź metrum od 2 do 4 (2/4 - 4/4) lub R (domyślne losowanie)')
        if metrum != 'R':
            metrum = int(tempo)
    if parametry == 'N' or metrum == 'R':
        metrum = random.randint(2, 4);
    #skala
    if parametry == 'T':
        tonacja = input('Wprowadź tonację (np. Gis) lub R (domyślne losowanie)')
        tonacja = keyToInt(tonacja)
    if parametry == 'N' or tonacja == 'R':
        tonacja = random.randint(0, 11);
    if parametry == 'T':
        rodzajSkali = input('Wproadź rodzaj skali (dostępne Dur, Mol, Blues) lub R (domyślne losowanie)')
    if parametry == 'N' or rodzajSkali == 'R':
        rodzajSkali = random.choice([Dur, Mol, Blues]);

    rodzajSkali = scaleToInt(rodzajSkali)
    skala = Skala(tonacja, rodzajSkali)
    #gatunek
    if parametry == 'T':
        gatunek = input('Wprowadź gatunek (dostępne Metal, Country, R&B, Folk, Rock, Jazz, Indie, Electronic, Pop, Hip-Hop lub R (domyślne losowanie)')
        gatunek=genreToInt(gatunek)
    if parametry == 'N' or gatunek == 'R':
        gatunek = random.randint(3, 12)
    if parametry == 'T':
        if gatunek==Metal:
            from metal import PieceMetal as Piece
        elif gatunek==Country:
            from country import PieceCountry as Piece
        elif gatunek==R_B:
            from R_B import PieceRB as Piece
        elif gatunek==Folk:
            from folk import PieceFolk as Piece
        elif gatunek==Rock:
            from rock import PieceRock as Piece
        elif gatunek==Jazz:
            from jazz import PieceJazz as Piece
        elif gatunek==Indie:
            from indie import PieceIndie as Piece
        elif gatunek==Electronic:
            from eletronic import PieceElectronic as Piece
        elif gatunek==Pop:
            from pop import PiecePop as Piece
        elif gatunek==Hip_Hop:
            from hip_hop import PieceHipHop as Piece
    else:
        from default import Piece

    muzyka=Piece(metrum,skala,tempo)
    muzyka.generatePiece()
