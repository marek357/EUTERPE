from default import *

class PieceHipHop(Piece):
    def __init__(this, metrum, skala, tempo, gatunek):
        Piece.__init__(this, metrum, skala, tempo, 12, [33, 34, 84, 98], [35, 36, 39])