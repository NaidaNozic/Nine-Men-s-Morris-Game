from NineMensMorrisGame.Game import NineMensMorrisGame
from NineMensMorrisGame.utils import GamePhase, printBoard

if __name__ == "__main__":
    print("Welcome to the Nine Men's Morris Game")
    game = NineMensMorrisGame()
    printBoard(game.get_board())
    winner = None
    while(winner is None):

        # Player 1
        if game.get_current_phase(1) == GamePhase.PLACING:
            position1 = -1
            while True:
                try:
                    position1 = int(input("\nPLAYER 1: Choose position where to place your piece: "))
                    game.place_piece(1,position1)
                    printBoard(game.get_board())
                    break
                except Exception as e:
                    print(str(e))

            if game.is_mill_formed(1,position1):
                if game.are_all_mills() == 2:
                    winner = 2
                    break

                while True:
                    try:
                        to_be_removed = int(input("\nPLAYER 1: Choose piece of Player 2 you would like to remove: "))
                        game.remove_piece(1,to_be_removed)
                        printBoard(game.get_board())
                        break
                    except Exception as e:
                        print(str(e))

        elif game.get_current_phase(1) == GamePhase.MOVING or game.get_current_phase(1) == GamePhase.FLYING:
            while True:
                try:
                    start = int(input("\nPLAYER 1: Choose position of piece you want to move: "))
                    target = int(input("\nPLAYER 1: Choose target position to which you want to move your piece"))
                    game.move_piece(1,start,target)
                    printBoard(game.get_board())
                    break
                except Exception as e:
                    print(str(e))

            if game.is_mill_formed(1,target):
                if game.are_all_mills() == 2:
                    winner = 2
                    break
                while True:
                    try:
                        to_be_removed = int(input("\nPLAYER 1: Choose piece of Player 2 you would like to remove: "))
                        game.remove_piece(1,to_be_removed)
                        printBoard(game.get_board())
                        break
                    except Exception as e:
                        print(str(e))
        
        # Player 2
        if game.get_current_phase(2) == GamePhase.PLACING:
            placed = None
            position2 = -1
            while True:
                try:
                    position2 = int(input("\nPLAYER 2: Choose position where to place your piece: "))
                    game.place_piece(2,position2)
                    printBoard(game.get_board())
                    break
                except Exception as e:
                    print(str(e))
           
            if game.is_mill_formed(2,position2):
                if game.are_all_mills() == 1:
                    winner = 1
                    break
                while True:
                    try:
                        to_be_removed = int(input("\nPLAYER 2: Choose piece of Player 1 you would like to remove: "))
                        game.remove_piece(2,to_be_removed)
                        printBoard(game.get_board())
                        break
                    except Exception as e:
                        print(str(e))

        elif game.get_current_phase(2) == GamePhase.MOVING or game.get_current_phase(2) == GamePhase.FLYING:
            while True:
                try:
                    start = int(input("\nPLAYER 2: Choose position of piece you want to move: "))
                    target = int(input("\nPLAYER 2: Choose target position to which you want to move your piece"))
                    game.move_piece(2,start,target)
                    printBoard(game.get_board())
                    break
                except Exception as e:
                    print(str(e))

            if game.is_mill_formed(2,target):
                if game.are_all_mills() == 1:
                    winner = 1
                    break
                while True:
                    try:
                        to_be_removed = int(input("\nPLAYER 2: Choose piece of Player 1 you would like to remove: "))
                        game.remove_piece(2,to_be_removed)
                        printBoard(game.get_board())
                        break
                    except Exception as e:
                        print(str(e))

        winner = game.is_winner()

    print("THE GAME HAS ENDED")
    print("THE WINNER IS THE PLAYER "+str(winner))