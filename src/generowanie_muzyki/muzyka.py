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

#losowanie długości dźwięku
def noteLength(sixteenth=10,eight=31,quarter=40,quarterExtended=7,half=9):
    los=random.randint(1,100)
    #jedna szesnasta
    if los <= sixteenth:
        return 0.25
    #jedna ósma
    if los <= sixteenth+eight:
        return 0.5
    #ćwierć nuta
    if los <= sixteenth+eight+quarter:
        return 1
    #ćwierć nuta z kropką
    if los <= sixteenth+eight+quarter+quarterExtended:
        return 1.5
    #pół nuta
    if los <= sixteenth+eight+quarter+quarterExtended+half:
        return 2
    #cała nuta
    return 4


#klasa trzyma dźwięk jako rodzaj będący nazwą dźwięku oraz numer oktawy w jakiej się dany dźwięk znajduje
class Dzwiek:
    #jeśli trzeci argument nie jest podany drugi jest traktowany jako numer midi
    def __init__(this, dzwiek, oktawa=None):
        if oktawa==None:
            this.rodzaj=dzwiek%12
            this.oktawa=dzwiek/12
        else:
            this.rodzaj=dzwiek
            this.oktawa=oktawa

    ####prywatne metody pomocnicze####

    #implementacja skipa z tabelki prawdopodobieństw
    def __skip(this, skala):
        los = random.randint(1,100)
        #kwinta
        if los <= 25:
            if random.random() < 0.5:
                for i in range(4):
                    this.noteUp(skala)
            else:
                for i in range(4):
                    this.noteDown(skala)
        #kwarta
        elif los <= 27:
            if random.random() < 0.5:
                for i in range(3):
                    this.noteUp(skala)
            else:
                for i in range(3):
                    this.noteDown(skala)
        #tercja (wielka lub mała w zależności od skali)
        elif los <= 75:
            if random.random() < 0.5:
                for i in range(2):
                    this.noteUp(skala)
            else:
                for i in range(2):
                    this.noteDown(skala)
        #seksta (wielka lub mała w zależności od skali)
        else:
            if random.random() < 0.5:
               for i in range(5):
                  this.noteUp(skala)
            else:
                for i in range(5):
                  this.noteDown(skala)

    #zwiększanie danego dźwięku o jeden w górę lub w dół po gamie
    def __step(this, skala):
        if random.random() < 0.5:
            #dźwięk do góry
            this.noteUp(skala)
        else:
            #dźwięk w dół
            this.noteDown(skala)

    ####publiczne metody####

    #tworzy kopię obiektu
    def copy(this):
        nowy=Dzwiek(this.rodzaj,this.oktawa)
        return nowy

    #zamienia dźwięk na numer midi
    def toMidi(this):
        return 12*(this.oktawa+1)+this.rodzaj

    #podwyższa dźwięk o jeden do góry po skali
    def noteUp(this, skala):
        idx = skala.gama.index(this.rodzaj)
        if idx == len(skala.gama) - 1:
            this.oktawa += 1
            this.rodzaj = skala.gama[0]
        else:
            this.rodzaj = skala.gama[idx+1]
        return this

    #obniża dźwięk o jeden w dół po skali
    def noteDown(this, skala):
        idx = skala.gama.index(this.rodzaj)
        if idx == 0:
            this.oktawa -= 1
            this.rodzaj = skala.gama[len(skala.gama) - 1]
        else:
            this.rodzaj = skala.gama[idx - 1]
        return this

    #podwyższa wysokość dźwięku o [ile] półtonów
    def next(this, ile=1):
        temp=this.rodzaj
        this.rodzaj+=ile%12
        this.rodzaj%=12
        this.oktawa+=ile//12 + 1 if this.rodzaj<temp else 0
        return this

    #obniża wysokość dźwięku o [ile] półtonów
    def prev(this, ile=1):
        temp=this.rodzaj
        this.rodzaj-=ile%12
        this.rodzaj%=12
        this.oktawa-=ile//12 + 1 if this.rodzaj>temp else 0
        return this

    #zmiana na kolejny dźwięk na podstawie obecnego
    def nextNote(this, skala):
        los = random.randint(1,100)

        #unison
        if los <= 25:
            this.oktawa = this.oktawa
        #oktawa
        elif los <= 27:
            if random.random() < 0.5:
                this.oktawa-=1
            else:
                this.oktawa+=1
        #krok o 1
        elif los <= 75:
            this.__step(skala)
        #skip
        else:
            this.__skip(skala)

        return this

    #kontrola zbyt wysokich/niskich dzwiekow
    def normalize(self):
        if self.oktawa <= 2:
            self.oktawa = 2
        if self.oktawa >= 6:
            self.oktawa = 6

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


#klara obsługuje operacje na akordach
class Akord:
    #tworzy akord z podanym dźwiękiem jako bazą, dostosowuje tercje tak aby należała do podanej skali
    def __init__(this, dzwiek, skala):
        d=dzwiek.copy()
        this.chord=[d.copy(),d.copy().noteUp(skala).noteUp(skala),d.copy().noteUp(skala).noteUp(skala).noteUp(skala).noteUp(skala)]
        this.podstawa=dzwiek.rodzaj
    
    #tworzy kopię obiektu
    def copy(this):
        return copy.deepcopy(this)

    #tworzy kolejne przewroty akordu n razy, TODO: dla n>1 można zrobić optymalniej, dodać obsługę n<0
    def transpose(this, n=1):
        for i in range(n):
            d=this.chord.pop(0)
            d.oktawa+=1
            this.chord.append(d)
        return this
    
    #podnosi cały akord n oktaw do góry
    def octaveDown(this, n=1):
        for x in this.chord:
            x.oktawa-=n
        return this

    #podnosi cały akord n oktaw w dół
    def octaveUp(this,n=1):
        for x in this.chord:
            x.oktawa+=n
        return this
    
    #modyfikuje losowo akord, TODO: trzeba by sprawdzić jakie procenty będą sensowne i dorobić więcej możliwości zmian
    def variate(this):
        this.transpose(random.randint(0,2))
        this.octaveDown(random.randint(0,1))
        return this

"""
Klasa pozwalająca zarządzać używanymi w piosence instrumentami

Kody dostępnych intrumentów są następujące:
Piano:
1 Acoustic Grand Piano
2 Bright Acoustic Piano
3 Electric Grand Piano
4 Honky-tonk Piano
5 Electric Piano 1
6 Electric Piano 2
7 Harpsichord
8 Clavinet

Chromatic Percussion:
9 Celesta
10 Glockenspiel
11 Music Box
12 Vibraphone
13 Marimba
14 Xylophone
15 Tubular Bells
16 Dulcimer

Organ:
17 Drawbar Organ
18 Percussive Organ
19 Rock Organ
20 Church Organ
21 Reed Organ
22 Accordion
23 Harmonica
24 Tango Accordion

Guitar:
25 Acoustic Guitar (nylon)
26 Acoustic Guitar (steel)
27 Electric Guitar (jazz)
28 Electric Guitar (clean)
29 Electric Guitar (muted)
30 Overdriven Guitar
31 Distortion Guitar
32 Guitar harmonics

Bass:
33 Acoustic Bass
34 Electric Bass (finger)
35 Electric Bass (pick)
36 Fretless Bass
37 Slap Bass 1
38 Slap Bass 2
39 Synth Bass 1
40 Synth Bass 2

Strings:
41 Violin
42 Viola
43 Cello
44 Contrabass
45 Tremolo Strings
46 Pizzicato Strings
47 Orchestral Harp
48 Timpani

Strings (continued):
49 String Ensemble 1
50 String Ensemble 2
51 Synth Strings 1
52 Synth Strings 2
53 Choir Aahs
54 Voice Oohs
55 Synth Voice
56 Orchestra Hit

Brass:
57 Trumpet
58 Trombone
59 Tuba
60 Muted Trumpet
61 French Horn
62 Brass Section
63 Synth Brass 1
64 Synth Brass 2

Reed:
65 Soprano Sax
66 Alto Sax
67 Tenor Sax
68 Baritone Sax
69 Oboe
70 English Horn
71 Bassoon
72 Clarinet

Pipe:
73 Piccolo
74 Flute
75 Recorder
76 Pan Flute
77 Blown Bottle
78 Shakuhachi
79 Whistle
80 Ocarina

Synth Lead:
81 Lead 1 (square)
82 Lead 2 (sawtooth)
83 Lead 3 (calliope)
84 Lead 4 (chiff)
85 Lead 5 (charang)
86 Lead 6 (voice)
87 Lead 7 (fifths)
88 Lead 8 (bass + lead)

Synth Pad:
89 Pad 1 (new age)
90 Pad 2 (warm)
91 Pad 3 (polysynth)
92 Pad 4 (choir)
93 Pad 5 (bowed)
94 Pad 6 (metallic)
95 Pad 7 (halo)
96 Pad 8 (sweep)

Synth Effects:
97 FX 1 (rain)
98 FX 2 (soundtrack)
99 FX 3 (crystal)
100 FX 4 (atmosphere)
101 FX 5 (brightness)
102 FX 6 (goblins)
103 FX 7 (echoes)
104 FX 8 (sci-fi)

Ethnic:
105 Sitar
106 Banjo
107 Shamisen
108 Koto
109 Kalimba
110 Bag pipe
111 Fiddle
112 Shanai

Percussive:
113 Tinkle Bell
114 Agogo
115 Steel Drums
116 Woodblock
117 Taiko Drum
118 Melodic Tom
119 Synth Drum

Sound effects:
120 Reverse Cymbal
121 Guitar Fret Noise
122 Breath Noise
123 Seashore
124 Bird Tweet
125 Telephone Ring
126 Helicopter
127 Applause
128 Gunshot
"""
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

class Instrumenty:
    #losuje dowolne instrumenty i przypisuje im kanały w utworze
    def __init__(this, midiFile, gatunek=1, track=0):
        instrumenty = getInstrumentsForGenre(gatunek)
        this.main= random.choice(instrumenty)
        this.accompaniment=random.choice(instrumenty)
        this.second=random.choice(instrumenty)
        this.solo=random.choice(instrumenty)
        this.mainChan=0
        this.accompanimentChan=1
        this.secondChan=2
        this.soloChan=3
        this.midi=midiFile
        midiFile.addProgramChange(track, this.mainChan, 0, this.main-1)
        midiFile.addProgramChange(track, this.accompanimentChan, time, this.accompaniment-1)
        midiFile.addProgramChange(track, this.secondChan, 0, this.second-1)
        midiFile.addProgramChange(track, this.soloChan, 0, this.solo-1)
    #ustawia główny instrument
    def setMain(this, instrument, time=0):
        this.main=instrument-1
        midi.addProgramChange(track, mainChan, time, main)
    #ustawia instrument używany w akompaniamencie
    def setAccompaniment(this, instrument, time=0, track=0):
        this.accompaniment=instrument-1
        midi.addProgramChange(track, accompanimentChan, time, accompaniment)
    #ustawia dodatkowy instrument
    def setSecond(this, instrument, time=0, track=0):
        this.second=instrument-1
        this.midi.addProgramChange(track, secondChan, time, second)
    #ustawia instrument solowy
    def setsolo(this, instrument, time=0, track=0):
        this.solo=instrument-1
        this.midi.addProgramChange(track, soloChan, time, solo)
    #ustawia dowolny instrumnt na wybranym kanale
    def setInstrument(this, instrument, channel, time=0, track=0):
        this.midi.addProgramChange(track, channel, time, instrument-1)

    #metody zwracające numery kanałów odpowiednich instrumentów
    def getMain(this):
        return this.mainChan
    def getAccompaniment(this):
        return this.accompanimentChan    
    def getSecond(this):
        return this.secondChan
    def getSolo(this):
        return this.soloChan

    #metody zwracające numery instrumentów z różnych grup
    def getSoundEffect():
        return random.randint(120,128)
    def getGuitar():
        return random.randint(25,32)

#klasa pozwalająca tworzyć dźwięki do późniejszego dołączenia do głównej części utworu
class Sound:
    def __init__(this, relTime, channel, note, duration, volume):
        this.relTime=relTime
        this.channel=channel
        this.note=note
        this.duration=duration
        this.volume=volume

"""
Klasa tworząca losowy bit perkusyjny wykorzysywany w utworze. 
W parametrze bit trzymane są wszystkie dźwięki dla pojedynczego taktu.

Dostępne instrumenty perkusyjne:
35 Acoustic Bass Drum
36 Bass Drum 1
37 Side Stick/Rimshot
38 Acoustic Snare
39 Hand Clap
40 Electric Snare
41 Low Floor Tom
42 Closed Hi-hat
43 High Floor Tom
44 Pedal Hi-hat
45 Low Tom
46 Open Hi-hat
47 Low-Mid Tom
48 Hi-Mid Tom
49 Crash Cymbal 1
50 High Tom
51 Ride Cymbal 1
52 Chinese Cymbal
53 Ride Bell
54 Tambourine
55 Splash Cymbal
56 Cowbell
57 Crash Cymbal 2
58 Vibra Slap
59 Ride Cymbal 2
60 High Bongo
61 Low Bongo
62 Mute High Conga
63 Open High Conga
64 Low Conga
65 High Timbale
66 Low Timbale
67 High Agogô
68 Low Agogô
69 Cabasa
70 Maracas
71 Short Whistle
72 Long Whistle
73 Short Güiro
74 Long Güiro
75 Claves
76 High Wood Block
77 Low Wood Block
78 Mute Cuíca
79 Open Cuíca
80 Mute Triangle
81 Open Triangle
"""
class Drums:
    def __init__(this, metrum, gatunek):
        instrumenty = getDrumsForGenre(gatunek)
        this.metrum=metrum
        this.first=random.choice(instrumenty)
        this.second=random.choice(instrumenty)
        this.third=random.choice(instrumenty)
        this.bit=list()
        this.bit.append(Sound(0,9,this.first,1,120))
        if random.random()<0.9:
            for i in range(metrum):
                this.bit.append(Sound(i,9,this.second,1,100))
        if random.random()<0.8:
            if(metrum==3):
                this.bit.append(Sound(1,9,this.third,1,100))
                this.bit.append(Sound(2,9,this.third,1,100))
            if(metrum==2):
                this.bit.append(Sound(1,9,this.third,1,100))
            if(metrum==4):
                this.bit.append(Sound(2,9,this.third,1,100))

def generateIntro(nOfMeasures, note, metrum, skala, instruments, perkusja):
    piece = list()
    relative_time = 0

    #generacja dźwięków perkusji
    if perkusja is not None:
        for i in range(nOfMeasures):
            for j in perkusja.bit:
                if j.note==perkusja.first:
                    piece.append(Sound(j.relTime+i*metrum,j.channel,j.note,j.duration,j.volume))

    while relative_time < nOfMeasures * metrum:
        duration = noteLength(2,25)
        note = note.nextNote(skala)
        note.normalize()
        # na początku każdego nowego taktu powinien być nowy dźwięk
        if (metrum - relative_time % metrum) < duration:
            duration = metrum - relative_time % metrum
        # akcenty i akompaniament
        if (relative_time % metrum) == 0:
            if (relative_time==0 or relative_time==metrum):
                #na początku utworu początkowe akordy mogą zostać pominięte
                if(random.random()<0.3):
                    # tworzy akord z aktualnie granego dźwięku
                    akord = Akord(note, skala)
                    for x in akord.chord:
                        piece.append(Sound(relative_time, instruments.getAccompaniment(), x.toMidi(), metrum, 70))
            # uuwydatnianie akcentu głośnością
            volume = 100
        else:
            volume = 60

        piece.append(Sound(relative_time, instruments.getMain(), note.toMidi(), duration, volume))
        relative_time = relative_time + duration
    return piece

def generateVerse(nOfMeasures, note, metrum, skala, instruments, perkusja):
    piece = list()
    relative_time = 0

    #generacja dźwięków perkusji
    if perkusja is not None:
        for i in range(nOfMeasures):
            for j in perkusja.bit:
                piece.append(Sound(j.relTime+i*metrum,j.channel,j.note,j.duration,j.volume))

    while relative_time < nOfMeasures * metrum:
        duration = noteLength()
        note = note.nextNote(skala)
        note.normalize()
        # na początku każdego nowego taktu powinien być nowy dźwięk
        if (metrum - relative_time % metrum) < duration:
            duration = metrum - relative_time % metrum
        # akcenty i akompaniament
        if (relative_time % metrum) == 0:
            akord = Akord(note, skala)
            for x in akord.chord:
                piece.append(Sound(relative_time, instruments.getAccompaniment(), x.toMidi(), metrum, 70))
            # uwydatnianie akcentu głośnością
            volume = 120
        else:
            volume = 80

        piece.append(Sound(relative_time, instruments.getMain(), note.toMidi(), duration, volume))
        relative_time = relative_time + duration
    return piece

def generateChorus(nOfMeasures, note, metrum, skala, instruments, perkusja):
    piece = list()
    relative_time = 0

    #generacja dźwięków perkusji
    if perkusja is not None:
        for i in range(nOfMeasures):
            for j in perkusja.bit:
                piece.append(Sound(j.relTime+i*metrum,j.channel,j.note,j.duration,j.volume))

    #w refrenie do grania melodii może być wybrany instrument pomocniczy
    if random.random()<0.4:
        instrument=instruments.getMain()
    else:
        instrument=instruments.getSecond()
    while relative_time < nOfMeasures * metrum:
        duration = noteLength()
        note = note.nextNote(skala)
        note.normalize()
        # na początku każdego nowego taktu powinien być nowy dźwięk
        if (metrum - relative_time % metrum) < duration:
            duration = metrum - relative_time % metrum
        # akcenty i akompaniament
        if (relative_time % metrum) == 0:
            # tworzy akord z aktualnie granego dźwięku
            akord = Akord(note, skala)
            for x in akord.chord:
                piece.append(Sound(relative_time, instruments.getAccompaniment(), x.toMidi(), metrum, 90))
            # uwydatnianie akcentu głośnością
            volume = 140
        else:
            volume = 100

        piece.append(Sound(relative_time, instrument, note.toMidi(), duration, volume))
        relative_time = relative_time + duration
    return piece

def generateOutro(nOfMeasures, note, metrum, skala, instruments, perkusja):
    piece = list()
    relative_time = 0

    #generacja dźwięków perkusji
    if perkusja is not None:
        for i in range(nOfMeasures):
            for j in perkusja.bit:
                if j.note==perkusja.first:
                    piece.append(Sound(j.relTime+i*metrum,j.channel,j.note,j.duration,j.volume))

    while relative_time < nOfMeasures * metrum:
        duration = noteLength(2,20)
        note = note.nextNote(skala)
        note.normalize()
        # na początku każdego nowego taktu powinien być nowy dźwięk
        if (metrum - relative_time % metrum) < duration:
            duration = metrum - relative_time % metrum
        # akcenty i akompaniament
        if (relative_time % metrum) == 0:
            # tworzy akord z aktualnie granego dźwięku
            akord = Akord(note, skala)
            for x in akord.chord:
                piece.append(Sound(relative_time, instruments.getAccompaniment(), x.toMidi(), metrum, 70))
            # uwydatnianie akcentu głośnością
            volume = 100
        else:
            volume = 60

        piece.append(Sound(relative_time, instruments.getMain(), note.toMidi(), duration, volume))
        relative_time = relative_time + duration
    return piece

def generateSolo(nOfMeasures, note, metrum, skala, instruments, perkusja):
    piece = list()
    relative_time = 0

    #generacja dźwięków perkusji
    if perkusja is not None:
        for i in range(nOfMeasures):
            for j in perkusja.bit:
                if j.note==perkusja.first or j.note==perkusja.third:
                    piece.append(Sound(j.relTime+i*metrum,j.channel,j.note,j.duration,j.volume))

    if random.random()<0.8:
        instrument=instruments.getSolo()
    else:
        instrument=instruments.getMain()

    while relative_time < nOfMeasures * metrum:
        duration = noteLength(40,35,15,7,3)
        note = note.nextNote(skala)
        note.normalize()
        # na początku każdego nowego taktu powinien być nowy dźwięk
        if (metrum - relative_time % metrum) < duration:
            duration = metrum - relative_time % metrum
        # akcenty i akompaniament
        if (relative_time % metrum) == 0:
            # tworzy akord z aktualnie granego dźwięku
            if (relative_time==0):
                akord = Akord(note, skala)
                for x in akord.chord:
                    piece.append(Sound(relative_time, instruments.getAccompaniment(), x.toMidi(), 2*metrum, 70))
            # uwydatnianie akcentu głośnością
            volume = 120
        else:
            volume = 80

        piece.append(Sound(relative_time, instrument, note.toMidi(), duration, volume))
        relative_time = relative_time + duration
    return piece


def appendToMidi(piece, pieceDuration):
    global MyMIDI
    global time
    global instruments
    for sound in piece:
        MyMIDI.addNote(0,sound.channel, sound.note, sound.relTime+time, sound.duration, sound.volume)
    time+=pieceDuration

def generatePiece(instruments, gatunek, metrum, skala):
    note = Dzwiek(list(skala.gama)[random.randint(0, 6)], random.randint(3, 5)) # losujemy początek ze skali
    #60% szans na pojawienie się perkusji w utworze
    if random.random()<0.7:
        perkusja= Drums(metrum, gatunek)
    else:
        perkusja=None


    liczbaZwrotek = random.randint(1, 3)
    powtorzeniaRefrenu = random.randint(1, 2)
    zwrotkaSolo = random.randint(-1, liczbaZwrotek-1)

    dlugoscIntro=random.randint(4, 6)
    dlugoscZwrotka=random.randint(8, 16)
    dlugoscRefren=random.randint(6, 12)
    dlugoscSolo=random.randint(8, 16)
    dlugoscOutro=random.randint(4, 8)
    intro = generateIntro(dlugoscIntro, note, metrum, skala, instruments, perkusja)
    zwrotka = generateVerse(dlugoscZwrotka, note, metrum, skala, instruments, perkusja)
    refren = generateChorus(dlugoscRefren, note, metrum, skala, instruments, perkusja)
    solo = generateSolo(dlugoscSolo, note, metrum, skala, instruments, perkusja)
    outro = generateOutro(dlugoscOutro, note, metrum, skala, instruments, perkusja)

    #debug
    print()
    print("Liczba zwrotek " + str(liczbaZwrotek))
    print("Powtórzenia refrenu " + str(powtorzeniaRefrenu))
    print("Zwrotka po której następuje solo " + str(zwrotkaSolo + 1))
    print("\nInstrumenty:")
    print("main "+str(instruments.main))
    print("accompaniment "+str(instruments.accompaniment))
    print("second "+str(instruments.second))
    print("solo "+str(instruments.solo))
    print("\nPerkusja:")
    if perkusja is None:
        print("brak")
    else:
        print("first "+str(perkusja.first))
        print("second "+str(perkusja.second))
        print("third "+str(perkusja.third))
    
    appendToMidi(intro, dlugoscIntro*metrum)
    for i in range(liczbaZwrotek):
        appendToMidi(zwrotka, dlugoscZwrotka*metrum)
        for j in range(powtorzeniaRefrenu):
            appendToMidi(refren, dlugoscRefren*metrum)
        if zwrotkaSolo == i:
            appendToMidi(solo, dlugoscSolo*metrum)
    appendToMidi(outro, dlugoscOutro*metrum)


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
    gatunek = input('Wprowadź gatunek (dostępne Metal, Country, R&B, Folk, Rock, Jazz, Indie, Electronic, Pop, Hip-Hop, Other lub R (domyślne losowanie)')
    gatunek = genreToInt(gatunek)
if parametry == 'N' or gatunek == 'R':
    gatunek = random.randint(1, 12)

track    = 0
time     = 0   # In beats

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)

#tworzenie zestawu instrumentów używanych w piosence
instruments=Instrumenty(MyMIDI, gatunek)

MyMIDI.addTempo(track, time, tempo)

generatePiece(instruments, gatunek, metrum, skala)

with open("muzyka.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)