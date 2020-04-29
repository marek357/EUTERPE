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

def generateIntro(nOfMeasures, note, metrum, skala):
    piece = list()
    relative_time = 0
    while relative_time < nOfMeasures * metrum:
        new_sound = list()
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
                        new_sound.append([2, x.toMidi(), metrum, 70])
            # uuwydatnianie akcentu głośnością
            volume = 100
        else:
            volume = 60

        new_sound.append([1, note.toMidi(), duration, volume])
        relative_time = relative_time + duration
        piece.append(new_sound)
    return piece

def generateVerse(nOfMeasures, note, metrum, skala):
    piece = list()
    relative_time = 0
    while relative_time < nOfMeasures * metrum:
        new_sound = list()
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
                new_sound.append([2, x.toMidi(), metrum, 70])
            # uwydatnianie akcentu głośnością
            volume = 120
        else:
            volume = 80

        new_sound.append([1, note.toMidi(), duration, volume])
        relative_time = relative_time + duration
        piece.append(new_sound)
    return piece

def generateChorus(nOfMeasures, note, metrum, skala):
    piece = list()
    relative_time = 0
    while relative_time < nOfMeasures * metrum:
        new_sound = list()
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
                new_sound.append([2, x.toMidi(), metrum, 90])
            # uwydatnianie akcentu głośnością
            volume = 140
        else:
            volume = 100

        new_sound.append([1, note.toMidi(), duration, volume])
        relative_time = relative_time + duration
        piece.append(new_sound)
    return piece

def generateOutro(nOfMeasures, note, metrum, skala):
    piece = list()
    relative_time = 0
    while relative_time < nOfMeasures * metrum:
        new_sound = list()
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
                new_sound.append([2, x.toMidi(), metrum, 70])
            # uwydatnianie akcentu głośnością
            volume = 100
        else:
            volume = 60

        new_sound.append([1, note.toMidi(), duration, volume])
        relative_time = relative_time + duration
        piece.append(new_sound)
    return piece

def generateSolo(nOfMeasures, note, metrum, skala):
    piece = list()
    relative_time = 0
    while relative_time < nOfMeasures * metrum:
        new_sound = list()
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
                    new_sound.append([2, x.toMidi(), 2*metrum, 70])
            # uwydatnianie akcentu głośnością
            volume = 120
        else:
            volume = 80

        new_sound.append([1, note.toMidi(), duration, volume])
        relative_time = relative_time + duration
        piece.append(new_sound)
    return piece


def appendToMidi(piece):
    global MyMIDI
    global time
    for sound in piece:
        for elem in sound:
            MyMIDI.addNote(0, elem[0], elem[1], time, elem[2], elem[3])
            if elem[0] == 1:
                time += elem[2]
    # MyMIDI.addNote(track, channel, note.toMidi(), time, duration, volume)

def generatePiece():
    skala = Skala(C, Dur)  # skala C-Dur
    note = Dzwiek(list(skala.gama)[random.randint(0, 6)], random.randint(3, 5)) # losujemy początek ze skali

    liczbaZwrotek = random.randint(1, 3)
    powtorzeniaRefrenu = random.randint(1, 2)
    zwrotkaSolo = random.randint(-1, liczbaZwrotek-1)

    intro = generateIntro(random.randint(4, 6), note, metrum, skala)
    zwrotka = generateVerse(random.randint(8, 16), note, metrum, skala)
    refren = generateChorus(random.randint(6, 12), note, metrum, skala)
    solo = generateSolo(random.randint(8, 16), note, metrum, skala)
    outro = generateOutro(random.randint(4, 8), note, metrum, skala)

    #debug
    print("Liczba zwrotek " + str(liczbaZwrotek))
    print("Powtórzenia refrenu " + str(powtorzeniaRefrenu))
    print("Zwrotka po której następuje solo " + str(zwrotkaSolo + 1))
    
    appendToMidi(intro)
    for i in range(liczbaZwrotek):
        appendToMidi(zwrotka)
        for j in range(powtorzeniaRefrenu):
            appendToMidi(refren)
        if zwrotkaSolo == i:
            appendToMidi(solo)
    appendToMidi(outro)

#losowanie głównych parametrów utworu

#tempo
tempo=random.randint(70, 120)
#metrum, podstawą jest zawsze ćwierćnuta (np. po wylosowaniu 3 metrum to 3/4)
metrum=random.randint(2,4);

track    = 0
channel  = 0
time     = 0   # In beats
duration = 1   # In beats
volume   = 100 # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)

MyMIDI.addTempo(track, time, tempo)

generatePiece()

with open("muzyka.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
