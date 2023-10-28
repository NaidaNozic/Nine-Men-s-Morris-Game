from NineMensMorrisGame.Player import Player
from NineMensMorrisGame.utils import adjacentPositions, mills
from NineMensMorrisGame.utils import GamePhase

class NineMensMorrisGame:
    board: list[str]
    players: list[Player]

    def __init__(self):
        self.board = ['x' for _ in range(24)]
        self.players = []
        self.players.append(Player(1))
        self.players.append(Player(2))

    def get_status(self):
        return self.status

    def get_board(self):
        return self.board
    
    def get_players(self):
        return self.players

    def place_piece(self, player_id, position):
        if self.players[player_id-1].phase != GamePhase.PLACING:
            print("Player is not in the placing phase")
            return None
        if  self.board[position] == 'x':
            self.board[position] = str(player_id)
            self.players[player_id-1].num_of_pieces -= 1 
            # Switching to Moving phase
            if self.players[player_id-1].num_of_pieces == 0:
                self.players[player_id-1].switch_phase()
            return 1
        else:
            print("Position is already taken")
            return None
    
    def move_piece(self, player_id, start, target):
        if self.players[player_id-1].phase == GamePhase.PLACING:
            print("Player is not in the moving phase")
            return None
        if self.board[target] != 'x':
            print("Position is already taken")
            return None
        if self.board[start] != str(player_id):
            print("Player "+str(player_id)+" is not located on the starting position")
            return None

        if self.players[player_id-1].phase == GamePhase.FLYING or target in adjacentPositions(start):
            self.board[start] = 'x'
            self.board[target] = str(player_id)
            return 1
        else:
            print("Choosen target position is not adjacent")
            return None

    def is_mill_formed(self, player_id, position):
        for mill in mills:
            if position in mill and all(self.board[pos] == str(player_id) for pos in mill):
                return True

        return False
    
    def remove_piece(self, player_id, position):
        opponent_id = 2 if player_id == 1 else 1

        if (self.board[position] == str(opponent_id) and not self.is_mill_formed(opponent_id, position) or
            self.is_mill_formed(opponent_id,position) and self.players[opponent_id-1].num_of_removed_pieces == 6):
            self.board[position] = 'x'
            self.players[opponent_id-1].num_of_removed_pieces += 1
            # Switching to Flying phase
            if self.players[opponent_id-1].num_of_removed_pieces == 6 and self.players[opponent_id-1].num_of_pieces == 0:
                self.players[opponent_id-1].switch_phase()
            return 1        
        else:
            print("Unable to remove piece due to invalid index")
            return None

    def get_current_phase(self, player_id):
        return self.players[player_id-1].phase
    
    def is_winner(self):
        if self.players[0].num_of_removed_pieces > 6:
            return 2
        elif self.players[1].num_of_removed_pieces > 6:
            return 1
        else:
            return None
    
    def are_all_mills(self):
        # if one player has all mills and more that 3 pieces on the board (no more moves for the opponent so potential WIN)
        if(all([self.is_mill_formed(element, index) for index, element in enumerate(self.board) if element == '1']) and
             self.players[0].num_of_removed_pieces < 6):
            return 1
        elif (all([self.is_mill_formed(element, index) for index, element in enumerate(self.board) if element == '2']) and
              self.players[1].num_of_removed_pieces < 6):
            return 2
        return None