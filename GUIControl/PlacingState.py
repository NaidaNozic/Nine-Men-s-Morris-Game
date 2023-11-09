import pygame
from GUIControl.GameState import GameState

False
class PlacingState(GameState):
    
    def handle_events(self, game, event, clickables, state):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, area in enumerate(clickables):
                if area.collidepoint(event.pos):
                    try:
                        game.place_piece(state.global_player, i)
                        state.placed = True
                        state.mill_tested = False
                        state.placed_index = i
                        break
                    except Exception as e:
                        state.text_command = str(e)
            