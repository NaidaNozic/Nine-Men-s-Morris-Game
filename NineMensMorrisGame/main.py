import pygame
from NineMensMorrisGame.Components.Game import Game
from NineMensMorrisGame.Components.Players.HumanPlayerFactory import HumanPlayerFactory
from NineMensMorrisGame.Gui.Config import Config
from NineMensMorrisGame.Gui.Global import Global
from NineMensMorrisGame.Gui.Pieces.BorderDecorator import BorderDecorator
from NineMensMorrisGame.Gui.Pieces.DefaultPiece import DefaultPiece
from NineMensMorrisGame.Gui.States.MovingState import MovingState
from NineMensMorrisGame.Gui.States.PlacingState import PlacingState
from NineMensMorrisGame.Gui.States.RemovingState import RemovingState
from NineMensMorrisGame.memory import Memory
from NineMensMorrisGame.utils import GamePhase
from NineMensMorrisGame.utils import coords

pygame.init()
pygame.display.set_caption("Nine Men's Morris")
icon = pygame.image.load('static/GameLogo.png')
game_board = pygame.image.load('static/GameBoard.png')
screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
pygame.display.set_icon(icon)

font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 26)
text_surface = font.render("Nine Men's Morris", True, Config.BLACK)

text_undo = font.render("UNDO", True, Config.BLACK)
text_redo = font.render("REDO", True, Config.BLACK)
text_save = font.render("SAVE", True, Config.BLACK)
text_load = font.render("LOAD", True, Config.BLACK)

scaling_factor = 500 / 843
clickables = [pygame.Rect(scaling_factor * c[0], scaling_factor * c[1], 60, 60) for c in coords.values()]
clock = pygame.time.Clock()
pieces = [(int(area.x + area.width / 2), int(area.y + area.height / 2)) for area in clickables]

placing_state = PlacingState()
removing_state = RemovingState()
moving_state = MovingState()
current_state = None

human_player1 = HumanPlayerFactory().create_player(1)
human_player2 = HumanPlayerFactory().create_player(2)
game = Game(human_player1, human_player2)
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


def undo():
    return game.undo()


def redo():
    return game.redo()


def save():
    game.save()


def load():
    next_player = game.load()
    return next_player

def main():
    running = True
    winner = None

    while running:
        screen.fill((255, 255, 255))
        screen.blit(game_board, (50, 110))
        screen.blit(text_surface, (50, 20))
        screen.blit(font_small.render(state.text_command, True, Config.BLACK), (50, 60))
        screen.blit(font_small.render(state.error_message, True, Config.BLACK), (50, 535))

        pygame.draw.rect(screen, (150, 150, 150), [550, 200, 140, 40])
        pygame.draw.rect(screen, (150, 150, 150), [550, 250, 140, 40])

        pygame.draw.rect(screen, (100, 100, 170), [550, 300, 140, 40])
        pygame.draw.rect(screen, (100, 100, 170), [550, 350, 140, 40])

        screen.blit(text_undo, (585, 208))
        screen.blit(text_redo, (585, 258))
        screen.blit(text_save, (585, 308))
        screen.blit(text_load, (585, 358))

        drawBoard(game.board)

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 550 <= mouse[0] <= 690 and 200 <= mouse[1] <= 240:
                    if undo() >= 0:
                        state.global_player = 2 if state.global_player == 1 else 1

                elif 550 <= mouse[0] <= 690 and 250 <= mouse[1] <= 290:
                    if redo() >= 0:
                        state.global_player = 2 if state.global_player == 1 else 1

                elif 550 <= mouse[0] <= 690 and 300 <= mouse[1] <= 340:
                    save()

                elif 550 <= mouse[0] <= 690 and 350 <= mouse[1] <= 390:
                    next_player = load()
                    state.global_player = next_player

            if winner is None:
                if not state.mill_tested and state.placed:
                    if game.is_mill_formed(state.global_player, state.placed_index):
                        state.text_command = f"PLAYER {state.global_player}: Choose piece of opponent you would like to remove: "
                        current_state = removing_state
                    else:
                        state.global_player = 2 if state.global_player == 1 else 1
                        state.placed = False
                        state.placed_index = None
                        state.mill_tested = True
                else:
                    current_phase = game.players[state.global_player - 1].phase
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
            drawBoard(game.board)
            clock.tick(Config.FPS)

        if winner is None:
            winner = game.is_winner()
            if winner is not None:
                state.text_command = f"The winner is Player: {winner}"

    pygame.quit()
