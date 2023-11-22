from NineMensMorrisGame.Components.Players.Player import Player
from NineMensMorrisGame.utils import adjacentPositions, mills
from NineMensMorrisGame.utils import GamePhase
from NineMensMorrisGame.memory import MemoryMeta, Memory


class Game:
    board: list[str]
    players: list[Player]
    memory: Memory()

    def __init__(self, player1, player2):
        self.board = ['x' for _ in range(24)]
        self.players = [player1, player2]
        self.memory = Memory()

    def place_piece(self, player_id, position):
        player = self.players[player_id - 1]
        if player.phase != GamePhase.PLACING:
            raise Exception("Player is not in placing phase")
        if self.board[position] == 'x':
            self.board[position] = str(player_id)
            player.num_of_pieces -= 1
            old_phase = player.phase
            if player.num_of_pieces == 0:
                player.switch_phase()
            write = str("Placement," + str(player_id) + "," + str(position) + "," +
                        str(int(old_phase.value)) + "," + str(int(player.phase.value)))
            self.memory.write_move(write)
        else:
            raise Exception("Position is already taken")

    def move_piece(self, player_id, start, target):
        try:
            self.validate_start_target(player_id, start, target)
            if target is None:
                return False
            self.board[start] = 'x'
            self.board[target] = str(player_id)
            write = str("Movement," + str(player_id) + "," + str(start) + "," + str(target))
            self.memory.write_move(write)
            return True
        except Exception as e:
            raise

    def validate_start_target(self, player_id, start, target):
        if self.players[player_id - 1].phase == GamePhase.PLACING:
            raise Exception("Player is not in moving phase")
        if self.board[start] != str(player_id):
            raise Exception("Player " + str(player_id) + " is not on the starting position")
        if target is not None:
            if self.board[target] != 'x':
                raise Exception("Position is already taken")
            if not (self.players[player_id - 1].phase == GamePhase.FLYING or target in adjacentPositions(start)):
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
            self.players[opponent_id - 1].num_of_removed_pieces += 1
            old_phase = self.players[opponent_id - 1].phase
            if self.players[opponent_id - 1].num_of_removed_pieces == 6 and self.players[
                opponent_id - 1].num_of_pieces == 0:
                self.players[opponent_id - 1].switch_phase()
            write = str("Removal," + str(opponent_id) + "," + str(position) + "," +
                        str(int(old_phase.value)) + "," + str(int(self.players[opponent_id - 1].phase.value)))
            self.memory.write_move(write)
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
        if (all([self.is_mill_formed(element, index) for index, element in enumerate(self.board) if element == '1'])):
            result.append(1)
        if (all([self.is_mill_formed(element, index) for index, element in enumerate(self.board) if element == '2'])):
            result.append(2)
        return result

    def undo(self):
        index = self.memory.undo()
        if index >= -1:
            self.set_up_board(index)

    def redo(self):
        index = self.memory.redo()
        if index >= 0:
            self.set_up_board(index)

    def save(self):
        self.memory.save_game()


    def load(self):
        index = self.memory.load_game()
        if index >= 0:
            self.set_up_board(index)

        move = self.memory.get_moves()[index].split(",")
        active_player = int(move[1])
        if move[0] != 'Removal':
            active_player = 2 if int(move[1]) == 1 else 1
        return active_player

    def set_up_board(self, index: int):
        self.board = ['x' for _ in range(24)]
        for player in self.players:
            player.reset()
        moves = self.memory.get_moves()
        i = 0
        while i <= index:
            move = moves[i].split(",")
            match move[0]:
                case "Placement":
                    player = self.players[int(move[1])-1]
                    self.board[int(move[2])] = move[1]
                    player.num_of_pieces -= 1
                    if player.num_of_pieces == 0:
                        player.switch_phase()
                case "Movement":
                    self.board[int(move[2])] = 'x'
                    self.board[int(move[3])] = move[1]
                case "Removal":
                    self.board[int(move[2])] = 'x'
                    self.players[int(move[1]) - 1].num_of_removed_pieces += 1
                    if self.players[int(move[1]) - 1].num_of_removed_pieces == 6 and self.players[
                        int(move[1]) - 1].num_of_pieces == 0:
                        self.players[move[1] - 1].switch_phase()
                case _:
                    pass
            i += 1

