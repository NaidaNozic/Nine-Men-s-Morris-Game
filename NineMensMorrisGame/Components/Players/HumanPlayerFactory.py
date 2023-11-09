from NineMensMorrisGame.Components.Players.HumanPlayer import HumanPlayer
from NineMensMorrisGame.Components.Players.PlayerFactory import PlayerFactory

class HumanPlayerFactory(PlayerFactory):
    
    def create_player(self, player_id):
        return HumanPlayer(player_id)
