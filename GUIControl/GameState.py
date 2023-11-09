from abc import abstractmethod

class GameState:

    @abstractmethod
    def handle_events(self, game, event, clickables, state):
        pass