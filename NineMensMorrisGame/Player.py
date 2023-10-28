from NineMensMorrisGame.utils import GamePhase

class Player:
    player_id: int
    num_of_pieces: int
    num_of_removed_pieces: int
    phase: GamePhase

    def __init__(self, player_id):
        self.player_id = player_id
        self.num_of_pieces = 9
        self.num_of_removed_pieces = 0
        self.phase = GamePhase.PLACING

    def switch_phase(self):
        if self.phase == GamePhase.PLACING:
            self.phase = GamePhase.MOVING
        elif self.phase == GamePhase.MOVING:
            self.phase = GamePhase.FLYING
