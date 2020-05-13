from default import *

class PieceIndie(Piece):
    def __init__(this, metrum, skala, tempo):
        Piece.__init__(this, metrum, skala, tempo, [3, 8, 12, 14, 26, 33, 38, 54, 79], [35, 36, 41, 48, 53, 56, 73, 80])