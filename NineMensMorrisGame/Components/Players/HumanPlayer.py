from NineMensMorrisGame.Components.Players.Player import Player
from NineMensMorrisGame.utils import GamePhase

class HumanPlayer(Player):
    
    def __init__(self, player_id):
        super().__init__(player_id)

    def switch_phase(self):
        if self.phase == GamePhase.PLACING:
            self.phase = GamePhase.MOVING
        elif self.phase == GamePhase.MOVING:
            self.phase = GamePhase.FLYING