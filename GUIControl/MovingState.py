
from GUIControl.GameState import GameState

class MovingState(GameState):

    def handle_events(self, game, state, index):
        try:
            if state.start is None and state.target is None:
                state.start = index
            elif state.start is not None and state.target is None:
                state.target = index
                game.move_piece(state.global_player,state.start,state.target)
                state.placed = True
                state.mill_tested = False
                state.placed_index = state.target
                state.start = None
                state.target = None
        except Exception as e:
            state.text_command = str(e)
            state.start = None
            state.target = None