import pygame
from NineMensMorrisGame.Gui.Pieces.Piece import Piece


class DefaultPiece(Piece):

    def __init__(self, screen, color, position, radius):
        super().__init__(screen, color, position, radius)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.radius)