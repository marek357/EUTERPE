from default import *

class PieceFolk(Piece):
    def __init__(this, metrum, skala, tempo, gatunek):
        Piece.__init__(this, metrum, skala, tempo, 6, [4, 13, 16, 22, 23, 41, 42, 46, 48, 76, 78, 107, 108, 109, 110, 112], [41, 48, 50, 53, 54, 56, 58, 60, 61, 69, 70, 73, 80])