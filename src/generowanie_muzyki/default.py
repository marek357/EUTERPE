import random
import copy
from midiutil import MIDIFile
from muzyka import Skala

#oznaczenia rodzajów dźwięków w programie
C = 0
Cis = 1
D = 2
Dis = 3
E = 4
F = 5
Fis = 6
G = 7
Gis = 8
A = 9
B = 10
H = 11

#oznaczenia rodzajów skal
Dur = 1
Mol = 2
Blues = 3

#losowanie długości dźwięku
def noteLength(sixteenth=10,eight=31,quarter=40,quarterExtended=7,half=9):
    los = random.randint(1,100)
    #jedna szesnasta
    if los <= sixteenth:
        return 0.25
    #jedna ósma
    if los <= sixteenth + eight:
        return 0.5
    #ćwierć nuta
    if los <= sixteenth + eight + quarter:
        return 1
    #ćwierć nuta z kropką
    if los <= sixteenth + eight + quarter + quarterExtended:
        return 1.5
    #pół nuta
    if los <= sixteenth + eight + quarter + quarterExtended + half:
        return 2
    #cała nuta
    return 4

#klasa trzyma dźwięk jako rodzaj będący nazwą dźwięku oraz numer oktawy w
#jakiej się dany dźwięk znajduje
class Dzwiek:
    #jeśli trzeci argument nie jest podany drugi jest traktowany jako numer
    #midi
    def __init__(this, dzwiek, oktawa=None):
        if oktawa == None:
            this.rodzaj = dzwiek % 12
            this.oktawa = dzwiek / 12
        else:
            this.rodzaj = dzwiek
            this.oktawa = oktawa

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
        nowy = Dzwiek(this.rodzaj,this.oktawa)
        return nowy

    #zamienia dźwięk na numer midi
    def toMidi(this):
        return 12 * (this.oktawa + 1) + this.rodzaj

    #podwyższa dźwięk o jeden do góry po skali
    def noteUp(this, skala):
        idx = skala.gama.index(this.rodzaj)
        if idx == len(skala.gama) - 1:
            this.oktawa += 1
            this.rodzaj = skala.gama[0]
        else:
            this.rodzaj = skala.gama[idx + 1]
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
        temp = this.rodzaj
        this.rodzaj+=ile % 12
        this.rodzaj%=12
        this.oktawa+=ile // 12 + 1 if this.rodzaj < temp else 0
        return this

    #obniża wysokość dźwięku o [ile] półtonów
    def prev(this, ile=1):
        temp = this.rodzaj
        this.rodzaj-=ile % 12
        this.rodzaj%=12
        this.oktawa-=ile // 12 + 1 if this.rodzaj > temp else 0
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




#klara obsługuje operacje na akordach
class Akord:
    #tworzy akord z podanym dźwiękiem jako bazą, dostosowuje tercje tak aby
    #należała do podanej skali
    def __init__(this, dzwiek, skala):
        d = dzwiek.copy()
        this.chord = [d.copy(),d.copy().noteUp(skala).noteUp(skala),d.copy().noteUp(skala).noteUp(skala).noteUp(skala).noteUp(skala)]
        this.podstawa = dzwiek.rodzaj
    
    #tworzy kopię obiektu
    def copy(this):
        return copy.deepcopy(this)

    #tworzy kolejne przewroty akordu n razy, TODO: dla n>1 można zrobić
    #optymalniej, dodać obsługę n<0
    def transpose(this, n=1):
        for i in range(n):
            d = this.chord.pop(0)
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
    
    #modyfikuje losowo akord, TODO: trzeba by sprawdzić jakie procenty będą
    #sensowne i dorobić więcej możliwości zmian
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
class Instrumenty:
    #losuje dowolne instrumenty i przypisuje im kanały w utworze
    def __init__(this, midiFile, instrumenty, track=0):
        this.main = random.choice(instrumenty) - 1
        this.accompaniment = random.choice(instrumenty) - 1
        this.second = random.choice(instrumenty) - 1
        this.solo = random.choice(instrumenty) - 1
        this.mainChan = 0
        this.accompanimentChan = 1
        this.secondChan = 2
        this.soloChan = 3
        this.midi = midiFile
        midiFile.addProgramChange(track, this.mainChan, 0, this.main)
        midiFile.addProgramChange(track, this.accompanimentChan, 0, this.accompaniment)
        midiFile.addProgramChange(track, this.secondChan, 0, this.second)
        midiFile.addProgramChange(track, this.soloChan, 0, this.solo)
    #ustawia główny instrument
    def setMain(this, instrument, time=0, track=0):
        this.main = instrument - 1
        this.midi.addProgramChange(track, this.mainChan, time, this.main)
    #ustawia instrument używany w akompaniamencie
    def setAccompaniment(this, instrument, time=0, track=0):
        this.accompaniment = instrument - 1
        this.midi.addProgramChange(track, this.accompanimentChan, time, this.accompaniment)
    #ustawia dodatkowy instrument
    def setSecond(this, instrument, time=0, track=0):
        this.second = instrument - 1
        this.midi.addProgramChange(track, this.secondChan, time, this.second)
    #ustawia instrument solowy
    def setsolo(this, instrument, time=0, track=0):
        this.solo = instrument - 1
        this.midi.addProgramChange(track, this.soloChan, time, this.solo)
    #ustawia dowolny instrumnt na wybranym kanale
    def setInstrument(this, instrument, channel, time=0, track=0):
        this.midi.addProgramChange(track, channel, time, instrument - 1)

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
    def getSoundEffect(this):
        return random.randint(120,128)
    def getGuitar(this):
        return random.randint(25,32)

#klasa pozwalająca tworzyć dźwięki do późniejszego dołączenia do głównej części
#utworu
class Sound:
    def __init__(this, relTime, channel, note, duration, volume):
        this.relTime = relTime
        this.channel = channel
        this.note = note
        this.duration = duration
        this.volume = volume

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
    def __init__(this, metrum, instrumenty=list(range(35, 81 + 1))):
        this.metrum = metrum
        this.first = random.choice(instrumenty)
        this.second = random.choice(instrumenty)
        this.third = random.choice(instrumenty)
        this.bit = list()
        this.bit.append(Sound(0,9,this.first,1,120))
        if random.random() < 0.9:
            for i in range(metrum):
                this.bit.append(Sound(i,9,this.second,1,100))
        if random.random() < 0.8:
            if(metrum == 3):
                this.bit.append(Sound(1,9,this.third,1,100))
                this.bit.append(Sound(2,9,this.third,1,100))
            if(metrum == 2):
                this.bit.append(Sound(1,9,this.third,1,100))
            if(metrum == 4):
                this.bit.append(Sound(2,9,this.third,1,100))

class Piece:
    def __init__(this, metrum, skala, tempo, instruments=list(range(1,112 + 1)), drums=list(range(35, 81 + 1))):
        this.track = 0
        this.time = 0   # In beats
        this.skala = skala
        this.tempo = tempo
        this.metrum = metrum
        this.MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                             # automatically created)
        #tworzenie zestawu instrumentów używanych w piosence
        this.instruments = Instrumenty(this.MyMIDI, instruments)
        #70% szans na pojawienie się perkusji w utworze
        if random.random() < 0.7:
            this.perkusja = Drums(metrum, drums)
        else:
            this.perkusja = None
        this.MyMIDI.addTempo(this.track, this.time, tempo)
    #generuje piosenkę z parametrami ustawionymi podczas tworzenie obiektu i zapisuje ją w pliku muzyka.mid
    def generatePiece(this):
        # losujemy początek ze skali
        note = Dzwiek(list(this.skala.gama)[random.randint(0, 6)], random.randint(3, 5))

        liczbaZwrotek = random.randint(1, 3)
        powtorzeniaRefrenu = random.randint(1, 2)
        zwrotkaSolo = random.randint(-1, liczbaZwrotek - 1)

        dlugoscIntro = random.randint(4, 6)
        dlugoscZwrotka = random.randint(8, 16)
        dlugoscRefren = random.randint(6, 12)
        dlugoscSolo = random.randint(8, 16)
        dlugoscOutro = random.randint(4, 8)
        intro = this.generateIntro(dlugoscIntro, note, this.metrum, this.skala, this.instruments, this.perkusja)
        zwrotka = this.generateVerse(dlugoscZwrotka, note, this.metrum, this.skala, this.instruments, this.perkusja)
        refren = this.generateChorus(dlugoscRefren, note, this.metrum, this.skala, this.instruments, this.perkusja)
        solo = this.generateSolo(dlugoscSolo, note, this.metrum, this.skala, this.instruments, this.perkusja)
        outro = this.generateOutro(dlugoscOutro, note, this.metrum, this.skala, this.instruments, this.perkusja)

        #debug
        print()
        print("metrum "+str(this.metrum))
        print("tempo "+str(this.tempo))
        print("liczba taktów "+str(dlugoscIntro+
            liczbaZwrotek*(dlugoscZwrotka+powtorzeniaRefrenu*dlugoscRefren)+(dlugoscSolo if zwrotkaSolo!=-1 else 0)+dlugoscOutro))
        print("\nLiczba zwrotek " + str(liczbaZwrotek))
        print("Powtórzenia refrenu " + str(powtorzeniaRefrenu))
        print("Zwrotka po której następuje solo " + str(zwrotkaSolo + 1))
        print("\nInstrumenty:")
        print("main " + str(this.instruments.main))
        print("accompaniment " + str(this.instruments.accompaniment))
        print("second " + str(this.instruments.second))
        print("solo " + str(this.instruments.solo))
        print("\nPerkusja:")
        if this.perkusja is None:
            print("brak")
        else:
            print("first " + str(this.perkusja.first))
            print("second " + str(this.perkusja.second))
            print("third " + str(this.perkusja.third))
    
        this._appendToMidi(intro, dlugoscIntro * this.metrum)
        for i in range(liczbaZwrotek):
            this._appendToMidi(zwrotka, dlugoscZwrotka * this.metrum)
            for j in range(powtorzeniaRefrenu):
                this._appendToMidi(refren, dlugoscRefren * this.metrum)
            if zwrotkaSolo == i:
                this._appendToMidi(solo, dlugoscSolo * this.metrum)
        this._appendToMidi(outro, dlugoscOutro * this.metrum)
        #zapisywanie wygenerowanej muzyki
        with open("muzyka.mid", "wb") as output_file:
            this.MyMIDI.writeFile(output_file)

    #dołącza dźwięki wchodzące w skład podanego fragmentu utworu jako kolejną sekscję w obiekcie midi
    def _appendToMidi(this, piece, pieceDuration):
        for sound in piece:
            this.MyMIDI.addNote(0,sound.channel, sound.note, sound.relTime + this.time, sound.duration, sound.volume)
        this.time+=pieceDuration
    #generuje intro do utworu
    def generateIntro(this, nOfMeasures, note, metrum, skala, instruments, perkusja):
        piece = list()
        relative_time = 0

        #generacja dźwięków perkusji
        if perkusja is not None:
            for i in range(nOfMeasures):
                for j in perkusja.bit:
                    if j.note == perkusja.first:
                        piece.append(Sound(j.relTime + i * metrum,j.channel,j.note,j.duration,j.volume))

        while relative_time < nOfMeasures * metrum:
            duration = noteLength(2,25)
            note = note.nextNote(skala)
            note.normalize()
            # na początku każdego nowego taktu powinien być nowy dźwięk
            if (metrum - relative_time % metrum) < duration:
                duration = metrum - relative_time % metrum
            # akcenty i akompaniament
            if (relative_time % metrum) == 0:
                if (relative_time == 0 or relative_time == metrum):
                    #na początku utworu początkowe akordy mogą zostać pominięte
                    if(random.random() < 0.3):
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
    #generuje zwrotkę utworu
    def generateVerse(this, nOfMeasures, note, metrum, skala, instruments, perkusja):
        piece = list()
        relative_time = 0

        #generacja dźwięków perkusji
        if perkusja is not None:
            for i in range(nOfMeasures):
                for j in perkusja.bit:
                    piece.append(Sound(j.relTime + i * metrum,j.channel,j.note,j.duration,j.volume))

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
    #generuje refren utworu
    def generateChorus(this, nOfMeasures, note, metrum, skala, instruments, perkusja):
        piece = list()
        relative_time = 0

        #generacja dźwięków perkusji
        if perkusja is not None:
            for i in range(nOfMeasures):
                for j in perkusja.bit:
                    piece.append(Sound(j.relTime + i * metrum, j.channel, j.note, j.duration, j.volume))

        #w refrenie do grania melodii może być wybrany instrument pomocniczy
        if random.random() < 0.4:
            instrument = instruments.getMain()
        else:
            instrument = instruments.getSecond()
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
    #generuje zakończenie utworu
    def generateOutro(this, nOfMeasures, note, metrum, skala, instruments, perkusja):
        piece = list()
        relative_time = 0

        #generacja dźwięków perkusji
        if perkusja is not None:
            for i in range(nOfMeasures):
                for j in perkusja.bit:
                    if j.note == perkusja.first:
                        piece.append(Sound(j.relTime + i * metrum, j.channel, j.note, j.duration, j.volume))

        while relative_time < nOfMeasures * metrum:
            duration = noteLength(2,10,15,20,30)
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

    #generuje fragment w utworze przeznaczony na solo
    def generateSolo(this, nOfMeasures, note, metrum, skala, instruments, perkusja):
        piece = list()
        relative_time = 0

        #generacja dźwięków perkusji
        if perkusja is not None:
            for i in range(nOfMeasures):
                for j in perkusja.bit:
                    if j.note == perkusja.first or j.note == perkusja.third:
                        piece.append(Sound(j.relTime + i * metrum, j.channel, j.note, j.duration, j.volume))

        if random.random() < 0.8:
            instrument = instruments.getSolo()
        else:
            instrument = instruments.getMain()

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
                if (relative_time == 0):
                    akord = Akord(note, skala)
                    for x in akord.chord:
                        piece.append(Sound(relative_time, instruments.getAccompaniment(), x.toMidi(), 2 * metrum, 70))
                # uwydatnianie akcentu głośnością
                volume = 120
            else:
                volume = 80

            piece.append(Sound(relative_time, instrument, note.toMidi(), duration, volume))
            relative_time = relative_time + duration
        return piece
