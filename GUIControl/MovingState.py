from GUIControl.GameState import GameState

class MovingState(GameState):

    def handle_events(self, game, state, index):
        try:
            state.target = index if state.start is not None and state.target is None else None
            state.start = index if state.start is None else state.start
            moved = game.move_piece(state.global_player,state.start,state.target)
            state.error_message = str()
            if moved is True:
                state.placed = True
                state.mill_tested = False
                state.placed_index = state.target
                state.start = None
                state.target = None
        except Exception as e:
            state.error_message = str(e)
            state.start = None
            state.target = None