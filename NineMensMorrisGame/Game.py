from NineMensMorrisGame.Player import Player
from NineMensMorrisGame.utils import adjacentPositions, mills
from NineMensMorrisGame.utils import GamePhase

class NineMensMorrisGame:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(NineMensMorrisGame, cls).__new__(cls)
        return cls.__instance
    
    def __init__(self):
        self.__board = ['x' for _ in range(24)]
        self.__players = []
        self.__players.append(Player(1))
        self.__players.append(Player(2))

    def get_board(self):
        return self.__board
    
    def get_players(self):
        return self.__players

    def place_piece(self, player_id, position):
        if self.__players[player_id-1].phase != GamePhase.PLACING:
            raise Exception("Player is not in the placing phase")
        if  self.__board[position] == 'x':
            self.__board[position] = str(player_id)
            self.__players[player_id-1].num_of_pieces -= 1 
            # Switching to Moving phase
            if self.__players[player_id-1].num_of_pieces == 0:
                self.__players[player_id-1].switch_phase()
        else:
            raise Exception("Position is already taken")
    
    def move_piece(self, player_id, start, target):
        if self.__players[player_id-1].phase == GamePhase.PLACING:
            raise Exception("Player is not in the moving phase")
        if self.__board[target] != 'x':
            raise Exception("Position is already taken")
        if self.__board[start] != str(player_id):
            raise Exception("Player "+str(player_id)+" is not located on the starting position")

        if self.__players[player_id-1].phase == GamePhase.FLYING or target in adjacentPositions(start):
            self.__board[start] = 'x'
            self.__board[target] = str(player_id)
        else:
            raise Exception("Choosen target position is not adjacent")

    def is_mill_formed(self, player_id, position):
        if position == -1:
            return False
        for mill in mills:
            if position in mill and all(self.__board[pos] == str(player_id) for pos in mill):
                return True

        return False
    
    def remove_piece(self, player_id, position):
        opponent_id = 2 if player_id == 1 else 1

        if (self.__board[position] == str(opponent_id) and not self.is_mill_formed(opponent_id, position) or
            self.__board[position] == str(opponent_id) and opponent_id in self.are_all_mills()):
            self.__board[position] = 'x'
            self.__players[opponent_id-1].num_of_removed_pieces += 1
            # Switching to Flying phase
            if self.__players[opponent_id-1].num_of_removed_pieces == 6 and self.__players[opponent_id-1].num_of_pieces == 0:
                self.__players[opponent_id-1].switch_phase()   
        else:
            raise Exception("Unable to remove piece due to invalid index")

    def get_current_phase(self, player_id):
        return self.__players[player_id-1].phase
    
    def is_winner(self):
        if self.__players[0].num_of_removed_pieces > 6:
            return 2
        elif self.__players[1].num_of_removed_pieces > 6:
            return 1
        else:
            return None
    
    def are_all_mills(self):
        result = []
        if(all([self.is_mill_formed(element, index) for index, element in enumerate(self.__board) if element == '1'])):
            result.append(1)
        if (all([self.is_mill_formed(element, index) for index, element in enumerate(self.__board) if element == '2'])):
            result.append(2)
        return result