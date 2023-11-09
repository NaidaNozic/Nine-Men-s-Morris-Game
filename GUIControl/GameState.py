from abc import abstractmethod

class GameState:

    @abstractmethod
    def handle_events(self, game, state, index):
        pass