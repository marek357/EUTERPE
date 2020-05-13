from default import *

class PieceCountry(Piece):
    def __init__(this, metrum, skala, tempo):
        Piece.__init__(this, metrum, skala, tempo, [4, 21, 26, 41, 42, 106], [35, 54, 58, 69])