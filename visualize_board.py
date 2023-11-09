from NineMensMorrisGame.Components.Game import Game
from NineMensMorrisGame.Components.Players.HumanPlayerFactory import HumanPlayerFactory
from NineMensMorrisGame.utils import printBoard

if __name__ == "__main__":
    print("Here is a visualization of the game board")
    human_player1 = HumanPlayerFactory().create_player(1)
    human_player2 = HumanPlayerFactory().create_player(2)
    game = Game(human_player1, human_player2)
    printBoard(game.board)