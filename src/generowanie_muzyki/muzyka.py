from midiutil import MIDIFile
import random

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


#losowanie długości dźwięku
def noteLength():
    los=random.randint(1,100)
    #jedna szesnasta
    if los <= 10:
        return 0.25
    #jedna ósma
    if los <= 41:
        return 0.5
    #ćwierć nuta
    if los <= 81:
        return 1
    #ćwierć nuta z kropką
    if los <= 88:
        return 1.5
    #pół nuta
    if los <= 97:
        return 2
    #cała nuta
    return 4


#klasa trzyma dźwięk jako rodzaj będący nazwą dźwięku oraz numer oktawy w jakiej się dany dźwięk znajduje
class Dzwiek:
    #jeśli trzeci argument nie jest podany drugi jest traktowany jako numer midi
    def __init__(this, dzwiek, oktawa=None):
        if oktawa==None:
            this.rodzaj=dzwiek%12
            this.oktawa=dzwiek//12
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
                return this.next(7)
            return this.prev(7)
        #kwarta
        elif los <= 27:
            if random.random() < 0.5:
                return this.next(5)
            return this.prev(5)
        #tercja (wielka lub mała w zależności od skali)
        elif los <= 75:
            if random.random() < 0.5:
                return this.noteUp(skala).noteUp(skala)
            return this.noteDown(skala).noteDown(skala)
        #seksta (wielka lub mała w zależności od skali)
        else:
            if random.random() < 0.5:
               for i in range(5):
                  this.noteUp(skala)
            else:
                for i in range(5):
                    this.noteDown(skala)
        return this

    #zwiększanie danego dźwięku o jeden w górę lub w dół po gamie
    def __step(this, skala):
        if random.random() < 0.5:
            #dźwięk do góry
            return this.noteUp(skala)
        else:
            #dźwięk w dół
            return this.noteDown(skala)

    ####publiczne metody####

    #zamienia dźwięk na numer midi
    def toMidi(this):
        return 12*(this.oktawa+1)+this.rodzaj

    #jeśli dźwięk jest poza skalą dopasowuje go do najbliższego dźwięku ze skali do góry
    def fitScaleUp(this, skala):
        for x in skala.gama:
            if this.rodzaj <= x:
                this.rodzaj=x
                return this
        this.rodzaj=skala.gama[0]
        this.oktawa+=1
        return this

    #jeśli dźwięk jest poza skalą dopasowuje go do najbliższego dźwięku ze skali do góry
    def fitScaleDown(this, skala):
        for x in reversed(skala.gama):
            if this.rodzaj >= x:
                this.rodzaj=x
                return this
        this.rodzaj=skala.gama[-1]
        this.oktawa-=1
        return this

    #podwyższa dźwięk o jeden do góry po skali
    def noteUp(this, skala):
        for x in skala.gama:
            if this.rodzaj==x:
                if skala.gama.index(x)==len(skala.gama)-1:
                    this.rodzaj=skala.gama[0]
                    this.oktawa+=1
                else:
                    this.rodzaj=skala.gama[skala.gama.index(x)+1]
                return this
        #pierwotny dźwięk był poza skalą
        raise Exception

    #obniża dźwięk o jeden w dół po skali
    def noteDown(this, skala):
        for x in reversed(skala.gama):
            if this.rodzaj==x:
                if skala.gama.index(x)==0:
                    this.rodzaj=skala.gama[-1]
                    this.oktawa-=1
                else:
                    this.rodzaj=skala.gama[skala.gama.index(x)-1]
                return this
        #pierwotny dźwięk był poza skalą
        raise Exception   

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
            return this
        #oktawa
        elif los <= 27:
            if random.random() < 0.5:
                this.oktawa-=1
            this.oktawa+=1
        #krok o 1
        elif los <= 75:
            return this.__step(skala)
        #skip
        else:
            return this.__skip(skala)
        return this

#klasa zawierając dźwięki gamy
class Skala:
    def __init__(this, d1, d2, d3, d4, d5, d6, d7):
        this.gama = (d1,d2,d3,d4,d5,d6,d7)



#losowanie głównych parametrów utworu, TODO: sprawdzić sensowność zakresów losowania

#tempo
tempo=random.randint(60, 160)
#ilość taktów w piosence
liczbaTaktow=random.randint(30,100);
#metrum, podstawą jest zawsze ćwierćnuta (np. po wylosowaniu 3 metrum to 3/4)
metrum=random.randint(2,6);


track    = 0
channel  = 0
time     = 0   # In beats
duration = 1   # In beats
volume   = 100 # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
MyMIDI.addTempo(track,time, tempo)

note=Dzwiek(C,4) #pierwszym dźwiękiem jest C4 arbitralnie wybranym
skala=Skala(C,D,E,F,G,A,H) #skala C-dur

#generacja piosenki
while time < liczbaTaktow*metrum:
    duration=noteLength()
    note.nextNote(skala)
    print(note.rodzaj, note.oktawa)
    #na początku każdego nowego taktu powinien być nowy dźwięk
    if (metrum - time % metrum) < duration:
        duration = metrum - time % metrum
    #uwydatnianie akcentów głośnością
    if (time % metrum) == 0:
        volume = 120
    else:
        volume = 80

    MyMIDI.addNote(track, channel, note.toMidi(), time, duration, volume)
    time = time + duration

with open("muzyka.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)


