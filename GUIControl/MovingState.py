
from GUIControl.GameState import GameState

class MovingState(GameState):

    def handle_events(self, game, event, clickables, state):
        try:
            game.move_piece(state.global_player,state.start,state.target)
            state.placed = True
            state.mill_tested = False
            state.placed_index = state.target
        except Exception as e:
            state.text_command = str(e)
            state.start = None
            state.target = None