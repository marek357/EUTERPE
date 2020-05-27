from default import *

class PieceJazz(Piece):
    def __init__(this, metrum, skala, tempo, gatunek):
        Piece.__init__(this, metrum, skala, tempo, 8, [1, 2, 3, 8, 27, 33, 34, 43, 44, 46, 57, 58], [35, 51, 55, 57, 59])