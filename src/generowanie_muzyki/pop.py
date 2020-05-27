from default import *

class PiecePop(Piece):
    def __init__(this, metrum, skala, tempo, gatunek):
        Piece.__init__(this, metrum, skala, tempo, 11, [5, 6, 26, 28, 29, 33, 49, 50, 81, 87, 89, 90, 96, 97], [35, 36, 41, 48, 53, 56])