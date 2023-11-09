import pygame
from NineMensMorrisGame.Components.Game import Game
from NineMensMorrisGame.Gui.Config import Config
from NineMensMorrisGame.Gui.Global import Global
from NineMensMorrisGame.Gui.Pieces.BorderDecorator import BorderDecorator
from NineMensMorrisGame.Gui.Pieces.DefaultPiece import DefaultPiece
from NineMensMorrisGame.Gui.States.MovingState import MovingState
from NineMensMorrisGame.Gui.States.PlacingState import PlacingState
from NineMensMorrisGame.Gui.States.RemovingState import RemovingState
from NineMensMorrisGame.utils import GamePhase

pygame.init()
pygame.display.set_caption("Nine Men's Morris")
icon = pygame.image.load('static/GameLogo.png')
game_board = pygame.image.load('static/GameBoard.png')
screen = pygame.display.set_mode((Config.SCREEN_WIDTH,Config.SCREEN_HEIGHT))
pygame.display.set_icon(icon)

font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 26)
text_surface = font.render("Nine Men's Morris", True, Config.BLACK)

coords = {
    0: (45, 140, 95, 190),
    1: (373, 140, 423, 190),
    2: (701, 140, 751, 190),
    3: (45, 468, 95, 518),
    4: (701, 468, 751, 518),
    5: (45, 796, 95, 846),
    6: (373, 796, 423, 846),
    7: (701, 796, 751, 846),
    8: (148, 246, 198, 296),
    9: (373, 246, 423, 296),
    10: (600, 246, 650, 296),
    11: (148, 468, 198, 518),
    12: (600, 468, 650, 518),
    13: (148, 695, 198, 745),
    14: (373, 695, 423, 745),
    15: (600, 695, 650, 745),
    16: (235, 337, 285, 387),
    17: (373, 337, 423, 387),
    18: (511, 337, 561, 387),
    19: (235, 468, 285, 518),
    20: (511, 468, 561, 518),
    21: (235, 610, 285, 660),
    22: (373, 610, 423, 660),
    23: (511, 610, 561, 660)
}
scaling_factor = 500/843
clickables = [pygame.Rect(scaling_factor*c[0], scaling_factor*c[1], 60, 60) for c in coords.values()]
clock = pygame.time.Clock()
pieces = [(int(area.x + area.width / 2), int(area.y + area.height / 2)) for area in clickables]

placing_state = PlacingState() 
removing_state = RemovingState()
moving_state = MovingState()
current_state = None

game = Game()
state = Global()
config = Config()

def drawBoard(board: list[str]):
    for i in range(len(pieces)):
        if board[i] == '2':
            DefaultPiece(screen, Config.BLACK, pieces[i], 15).draw()
        elif board[i] == '1':
            white_piece = DefaultPiece(screen, Config.WHITE, pieces[i], 15)
            BorderDecorator(white_piece, Config.BLACK, 16).draw()

def detect_button_click(event) -> int | None:
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for i, area in enumerate(clickables):
            if area.collidepoint(event.pos):
                return i
    return None

def main():
    running = True
    winner = None

    while running:
        screen.fill((255, 255, 255))
        screen.blit(game_board, (50, 110))
        screen.blit(text_surface, (50, 20))
        screen.blit(font_small.render(state.text_command, True, Config.BLACK), (50, 60))
        screen.blit(font_small.render(state.error_message, True, Config.BLACK), (50, 535))
        drawBoard(game.get_board())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if winner is None:
                if not state.mill_tested and state.placed:
                    if game.is_mill_formed(state.global_player,state.placed_index):
                        state.text_command = f"PLAYER {state.global_player}: Choose piece of opponent you would like to remove: "
                        current_state = removing_state
                    else:
                        state.global_player = 2 if state.global_player == 1 else 1
                        state.placed = False
                        state.placed_index = None
                        state.mill_tested = True
                else:
                    current_phase = game.get_current_phase(state.global_player)
                    if current_phase == GamePhase.PLACING and not state.placed:
                        state.text_command = f"PLAYER {state.global_player}: Choose position where to place your piece: "
                        current_state = placing_state
                        
                    elif current_phase == GamePhase.MOVING or current_phase == GamePhase.FLYING and not state.placed:
                        if state.start is None and state.target is None:
                            state.text_command = f"PLAYER {state.global_player}: Choose position of piece you want to move: "
                        elif state.start is not None and state.target is None:
                            state.text_command = f"PLAYER {state.global_player}: Choose target position to which you want to move your piece"
                        current_state = moving_state

                colidepoint_index = detect_button_click(event)
                if colidepoint_index is not None and current_state is not None:
                    current_state.handle_events(game, state, colidepoint_index)
                    current_state = None
                        
            pygame.display.update()
            drawBoard(game.get_board())
            clock.tick(Config.FPS)

        if winner is None:
            winner = game.is_winner()
            if winner is not None:
                state.text_command =f"The winner is Player: {winner}"

    pygame.quit()