from default import *

class PieceMetal(Piece):
    def __init__(this, metrum, skala, tempo, gatunek):
        Piece.__init__(this, metrum, skala, tempo, 3, [31, 32, 34, 35], [37, 38, 40, 43, 44, 45, 46, 47, 49, 51, 57])