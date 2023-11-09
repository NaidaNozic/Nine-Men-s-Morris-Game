import pygame
from GUIControl.GameState import GameState

class RemovingState(GameState):
    
    def handle_events(self, game, event, clickables, state):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, area in enumerate(clickables):
                if area.collidepoint(event.pos):
                    try:
                        game.remove_piece(state.global_player,i)
                        state.global_player = 2 if state.global_player == 1 else 1
                        state.placed = False
                        state.mill_tested = True
                        state.placed_index = -1
                    except Exception as e:
                        state.text_command = str(e)