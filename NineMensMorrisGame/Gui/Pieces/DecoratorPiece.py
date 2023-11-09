from NineMensMorrisGame.Gui.Pieces.Piece import Piece

class DecoratorPiece(Piece):
    def __init__(self, piece):
        self.piece = piece

    def draw(self):
        self.piece.draw()