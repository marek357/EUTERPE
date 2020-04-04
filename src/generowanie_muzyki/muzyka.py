from midiutil import MIDIFile
import random

#generowanie losowej melodii składającej się z 50 dźwięków, metrum 4/4, stała głośność, jeden instrument

#niektóre dźwięki w midi
A0=21
B0=23
C1=24
D1=26
E1=28
F1=29
C4=60


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

#implementacja skipa z tabelki prawdopodobieństw
def skip(note):
    los = random.randint(1,100)
    #kwinta
    if los <= 25:
        if random.random() < 0.5:
            return note + 7
        return note - 7
    #kwarta
    if los <= 27:
        if random.random() < 0.5:
            return note + 5
        return note - 5
    #tercja wielka (TODO: na razie wszystko jest w dur)
    if los <= 75:
        if random.random() < 0.5:
            return note + 4
        return note - 4
    #seksta wielka (TODO: tutaj podobnie jak dla tercji)
    if random.random() < 0.5:
       return note + 9
    return note - 9


#zwiększanie danego dźwięku o jeden w górę lub w dół po gamie
def step(note):
    if random.random() < 0.5:
        #dźwięk do góry
        i = 0
        #przebiega po wszystkich dostępnych dźwiękach dla midi szukając dźwięków B lub E
        while i < 9:
            if (note == B0 + 12 * i) or (note == E1 + 12 * i):
                return note + 1
            i+=1
        return note + 2
    else:
        #dźwięk w dół
        i = 0
        while i < 9:
            if (note == C1 + 12 * i) or (note == F1 + 12 * i):
                return note - 1
            i+=1
        return note - 2

#losowanie kolejnego dźwięku na podstawie poprzedniego
def nextNote(note):
    los = random.randint(1,100)

    #unison
    if los <= 25:
        return note
    #oktawa
    if los <= 27:
        if random.random() < 0.5:
            return note + 12
        return note - 12
    #krok o 1
    if los <= 75:
        return step(note)
    #skip
    return skip(note)


track    = 0
channel  = 0
time     = 0   # In beats
duration = 1   # In beats
tempo    = 80  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
MyMIDI.addTempo(track,time, tempo)

note=60 #pierwszym dźwiękiem jest C4 arbitralnie wybranym

#generuje 30 losowych dźwięków według procentów z tabelki
for i in range(30):
    duration=noteLength()
    note=nextNote(note)
    MyMIDI.addNote(track, channel, note, time, duration, volume)
    time = time + duration

with open("muzyka.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)


