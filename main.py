from NineMensMorrisGame.Game import NineMensMorrisGame
from NineMensMorrisGame.utils import GamePhase, printBoard

if __name__ == "__main__":
    print("Welcome to the Nine Men's Morris Game")
    game = NineMensMorrisGame()
    printBoard(game.get_board())
    res = 1
    winner = None
    while(res and winner is None):

        # Player 1
        if game.get_current_phase(1) == GamePhase.PLACING:
            placed = None
            position1 = -1
            while(placed is None):
                position1 = int(input("\nPLAYER 1: Choose position where to place your piece: "))
                placed = game.place_piece(1,position1)
            res = placed
            if res:
                printBoard(game.get_board())
            if game.is_mill_formed(1,position1):
                if game.are_all_mills() == 2:
                    winner = 2
                    break
                removed = None
                while(removed is None):
                    to_be_removed = int(input("\nPLAYER 1: Choose piece of Player 2 you would like to remove: "))
                    removed = game.remove_piece(1,to_be_removed)
                printBoard(game.get_board())

        elif game.get_current_phase(1) == GamePhase.MOVING or game.get_current_phase(1) == GamePhase.FLYING:
            moved = None
            while(moved is None):
                start = int(input("\nPLAYER 1: Choose position of piece you want to move: "))
                target = int(input("\nPLAYER 1: Choose target position to which you want to move your piece"))
                moved = game.move_piece(1,start,target)

            res = moved
            printBoard(game.get_board())
            if game.is_mill_formed(1,target):
                if game.are_all_mills() == 2:
                    winner = 2
                    break
                removed = None
                while(removed is None):
                    to_be_removed = int(input("\nPLAYER 1: Choose piece of Player 2 you would like to remove: "))
                    removed = game.remove_piece(1,to_be_removed)
                printBoard(game.get_board())
        
        # Player 2
        if game.get_current_phase(2) == GamePhase.PLACING:
            placed = None
            position2 = -1
            while(placed is None):
                position2 = int(input("\nPLAYER 2: Choose position where to place your piece: "))
                placed = game.place_piece(2,position2)
            res = placed
            if res:
                printBoard(game.get_board())
            if game.is_mill_formed(2,position2):
                if game.are_all_mills() == 1:
                    winner = 1
                    break
                removed = None
                while(removed is None):
                    to_be_removed = int(input("\nPLAYER 2: Choose piece of Player 1 you would like to remove: "))
                    removed = game.remove_piece(2,to_be_removed)
                printBoard(game.get_board())


        elif game.get_current_phase(2) == GamePhase.MOVING or game.get_current_phase(2) == GamePhase.FLYING:
            moved = None
            while(moved is None):
                start = int(input("\nPLAYER 2: Choose position of piece you want to move: "))
                target = int(input("\nPLAYER 2: Choose target position to which you want to move your piece"))
                moved = game.move_piece(2,start,target)

            res = moved
            printBoard(game.get_board())

            if game.is_mill_formed(2,target):
                if game.are_all_mills() == 1:
                    winner = 1
                    break
                removed = None
                while(removed is None):
                    to_be_removed = int(input("\nPLAYER 2: Choose piece of Player 1 you would like to remove: "))
                    removed = game.remove_piece(2,to_be_removed)
            printBoard(game.get_board())

        winner = game.is_winner()

    print("THE GAME HAS ENDED")
    print("THE WINNER IS THE PLAYER "+str(winner))