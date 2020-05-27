from default import *

class PieceRB(Piece):
    def __init__(this, metrum, skala, tempo, gatunek):
        Piece.__init__(this, metrum, skala, tempo, 5,  [8, 33, 34, 84, 89], [35, 36, 39, 60, 73])