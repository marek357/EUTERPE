from default import *

class PieceRock(Piece):
    def __init__(this, metrum, skala, tempo):
        Piece.__init__(this, metrum, skala, tempo, [19, 26, 28, 29, 30, 34, 35, 87], [35, 36, 37, 38, 40, 43, 44, 45, 46, 47, 49, 51, 53, 56, 57])