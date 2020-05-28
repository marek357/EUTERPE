import os.path
from os import path
from default import *

#sprawdzanie czy generowane kolejno dźwięki melodii leżą na skali
class TestDzwiek:
    def test_czy_w_skali_Dur(this):
        for i in range(C,H):
            skala = Skala(i, Dur)
            note = Dzwiek(skala.gama[0], 4)
            for j in range(1000):
                note = note.nextNote(skala)
            assert note.rodzaj in skala.gama
    def test_czy_w_skali_Mol(this):
        for i in range(C,H):
            skala = Skala(i, Mol)
            note = Dzwiek(skala.gama[0], 4)
            for j in range(1000):
                note = note.nextNote(skala)
                assert note.rodzaj in skala.gama
    def test_czy_w_skali_Blues(this):
        for i in range(C,H):
            skala = Skala(i, Blues)
            note = Dzwiek(skala.gama[0], 4)
            for j in range(1000):
                note = note.nextNote(skala)
                assert note.rodzaj in skala.gama

    def test_wysokosc(this):
        for i in range(C,H):
            skala = Skala(i, Dur)
            note = Dzwiek(skala.gama[0], 4)
            for j in range(1000):
                note = note.nextNote(skala)
                note.normalize()
                assert note.oktawa >= 2 and note.oktawa <= 7

#sprawdzanie czy po generacji akordu wszystkie jego dźwięki należą do użytej skali
class TestAkord:
    def test_czy_w_skali_Dur(this):
        for i in range(C,H):
            skala = Skala(i, Dur)
            for j in skala.gama:
                note = Dzwiek(j,4)
                akord = Akord(note,skala)
                for k in akord.chord:
                    assert k.rodzaj in skala.gama
    def test_czy_w_skali_Mol(this):
        for i in range(C,H):
            skala = Skala(i, Mol)
            for j in skala.gama:
                note = Dzwiek(j,4)
                akord = Akord(note,skala)
                for k in akord.chord:
                    assert k.rodzaj in skala.gama
    def test_czy_w_skali_Blues(this):
        for i in range(C,H):
            skala = Skala(i, Blues)
            for j in skala.gama:
                note = Dzwiek(j,4)
                akord = Akord(note,skala)
                for k in akord.chord:
                    assert k.rodzaj in skala.gama

#sprawdzanie istnienia pliku po dokonaniu generacji muzyki
class TestPlik:
    def test_czy_plik_istnieje(this):
        for _ in range(1000):
            metrum = random.randint(2, 4)
            tempo = random.randint(70, 120)
            tonacja = random.randint(0, 11)
            rodzajSkali = random.choice([Dur, Mol, Blues])
            skala = Skala(tonacja, rodzajSkali)
            muzyka = Piece(metrum, skala, tempo)
            muzyka.generatePiece()
            assert path.exists('muzyka.mid')
            os.remove('muzyka.mid')
