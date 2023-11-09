import pygame
from GUIControl.GameState import GameState

False
class PlacingState(GameState):
    
    def handle_events(self, game, state, index):
        try:
            game.place_piece(state.global_player, index)
            state.placed = True
            state.mill_tested = False
            state.placed_index = index
        except Exception as e:
            state.text_command = str(e)
            