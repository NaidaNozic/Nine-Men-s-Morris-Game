import pygame
from GUIControl.States.GameState import GameState

False
class PlacingState(GameState):
    
    def handle_events(self, game, state, index):
        try:
            game.place_piece(state.global_player, index)
            state.placed = True
            state.mill_tested = False
            state.placed_index = index
            state.error_message = str()
        except Exception as e:
            state.error_message = str(e)
            