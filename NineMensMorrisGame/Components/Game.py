from NineMensMorrisGame.Components.Players.Player import Player
from NineMensMorrisGame.utils import adjacentPositions, mills
from NineMensMorrisGame.utils import GamePhase

class Game:
    board: list[str]
    players: list[Player]
    
    def __init__(self, player1, player2):
        self.board = ['x' for _ in range(24)]
        self.players = [player1, player2]

    def place_piece(self, player_id, position):
        player = self.players[player_id-1]
        if player.phase != GamePhase.PLACING:
            raise Exception("Player is not in placing phase")
        if  self.board[position] == 'x':
            self.board[position] = str(player_id)
            player.num_of_pieces -= 1 
            if player.num_of_pieces == 0:
                player.switch_phase()
        else:
            raise Exception("Position is already taken")
    
    def move_piece(self, player_id, start, target):
        try:
            self.validate_start_target(player_id, start, target)
            if target is None:
                return False
            self.board[start] = 'x'
            self.board[target] = str(player_id)
            return True
        except Exception as e:
            raise
        
    def validate_start_target(self, player_id, start, target):
        if self.players[player_id-1].phase == GamePhase.PLACING:
            raise Exception("Player is not in moving phase")
        if self.board[start] != str(player_id):
            raise Exception("Player "+str(player_id)+" is not on the starting position")
        if target is not None:
            if self.board[target] != 'x':
                raise Exception("Position is already taken")
            if not (self.players[player_id-1].phase == GamePhase.FLYING or target in adjacentPositions(start)):
                raise Exception("Choosen target is not adjacent")

    def is_mill_formed(self, player_id, position):
        if position == -1:
            return False
        for mill in mills:
            if position in mill and all(self.board[pos] == str(player_id) for pos in mill):
                return True

        return False
    
    def remove_piece(self, player_id, position):
        opponent_id = 2 if player_id == 1 else 1

        if (self.board[position] == str(opponent_id) and not self.is_mill_formed(opponent_id, position) or
            self.board[position] == str(opponent_id) and opponent_id in self.are_all_mills()):
            self.board[position] = 'x'
            self.players[opponent_id-1].num_of_removed_pieces += 1
            if self.players[opponent_id-1].num_of_removed_pieces == 6 and self.players[opponent_id-1].num_of_pieces == 0:
                self.players[opponent_id-1].switch_phase()   
        else:
            raise Exception("Invalid index")
    
    def is_winner(self):
        if self.players[0].num_of_removed_pieces > 6:
            return 2
        elif self.players[1].num_of_removed_pieces > 6:
            return 1
        else:
            return None
    
    def are_all_mills(self):
        result = []
        if(all([self.is_mill_formed(element, index) for index, element in enumerate(self.board) if element == '1'])):
            result.append(1)
        if (all([self.is_mill_formed(element, index) for index, element in enumerate(self.board) if element == '2'])):
            result.append(2)
        return result