from default import *

class PieceElectronic(Piece):
    def __init__(this, metrum, skala, tempo, gatunek):
        Piece.__init__(this, metrum, skala, tempo, 10, [5, 6, 39, 40, 45, 51, 52, 55, 63, 64, 81, 82], [39, 40, 45, 47])