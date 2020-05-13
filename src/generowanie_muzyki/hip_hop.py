from default import *

class PieceHipHop(Piece):
    def __init__(this, metrum, skala, tempo):
        Piece.__init__(this, metrum, skala, tempo, [33, 34, 84, 98], [35, 36, 39])