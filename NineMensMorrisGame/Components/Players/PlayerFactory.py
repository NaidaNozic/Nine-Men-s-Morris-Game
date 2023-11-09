from abc import abstractmethod

class PlayerFactory:
    
    @abstractmethod
    def create_player(self, player_id):
        pass