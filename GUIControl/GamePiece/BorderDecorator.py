import pygame
from GUIControl.GamePiece.DecoratorPiece import DecoratorPiece

class BorderDecorator(DecoratorPiece):

    def __init__(self, piece, border_color, border_radius):
        super().__init__(piece)
        self.border_color = border_color
        self.border_radius = border_radius

    def draw(self):
        pygame.draw.circle(self.piece.screen, self.border_color, self.piece.position, self.border_radius)
        super().draw()