import pygame
from NineMensMorrisGame.Game import NineMensMorrisGame

from NineMensMorrisGame.utils import BLACK, WHITE, GamePhase

pygame.init()
pygame.display.set_caption("Nine Men's Morris")

icon = pygame.image.load('static/GameLogo.png')
game_board = pygame.image.load('static/GameBoard.png')

pygame.display.set_icon(icon)

font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 26)
text_surface = font.render("Nine Men's Morris", True, BLACK)

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
fps = 20
clock = pygame.time.Clock()
pieces = [(int(area.x + area.width / 2), int(area.y + area.height / 2)) for area in clickables]

#STATE VARIABLES
global global_player, placed, mill_tested, game, text_command
global placed_index, start, target
global_player = 1
placed = False
mill_tested = False
placed_index = -1
start = None
target = None
game = NineMensMorrisGame()
text_command = "PLAYER 1: Choose position where to place your piece: "

def drawBoard(board: list[str]):
    for i, (x, y) in enumerate(pieces):
        if board[i] == '2':
            pygame.draw.circle(screen, BLACK, pieces[i], 15)
        elif board[i] == '1':
            pygame.draw.circle(screen, BLACK, pieces[i], 16)
            pygame.draw.circle(screen, WHITE, pieces[i], 15)

def handle_placing(player, event):
    global placed, mill_tested, game, text_command
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for i, area in enumerate(clickables):
            if area.collidepoint(event.pos):
                try:
                    game.place_piece(player, i)
                    placed = True
                    mill_tested = False
                    return i
                except Exception as e:
                    text_command = str(e)

def handle_removing(player, event):
    global placed, global_player, mill_tested, placed_index, game, text_command
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for i, area in enumerate(clickables):
            if area.collidepoint(event.pos):
                try:
                    game.remove_piece(player,i)
                    global_player = 2 if global_player == 1 else 1
                    placed = False
                    mill_tested = True
                    placed_index = -1
                except Exception as e:
                    text_command = str(e)

def handle_start_target(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for i, area in enumerate(clickables):
            if area.collidepoint(event.pos):
                    return i

def handle_moving():
    global start, target, text_command, placed, global_player, mill_tested, placed_index, game, placed_index
    try:
        game.move_piece(global_player,start,target)
        placed = True
        mill_tested = False
        placed_index = target
    except Exception as e:
        text_command = str(e)
        start = None
        target = None

screen = pygame.display.set_mode((900,560))
running = True
winner = None

while running:
    screen.fill((255, 255, 255))
    screen.blit(game_board, (50, 110))
    screen.blit(text_surface, (50, 20))
    text = font_small.render(text_command, True, BLACK)
    screen.blit(text, (50, 60))
    drawBoard(game.get_board())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if winner is None:
            if not mill_tested and placed:
                if game.is_mill_formed(global_player,placed_index):
                    if ((game.are_all_mills() == 1 and global_player == 2) or
                        (game.are_all_mills() == 2 and global_player == 1)):
                        winner = game.are_all_mills()
                        text_command ="The winner is Player: "+str(winner)
                        pygame.display.update()
                        break

                    text_command = "PLAYER "+str(global_player)+": Choose piece of opponent you would like to remove: "
                    handle_removing(global_player, event)
                else:
                    global_player = 2 if global_player == 1 else 1
                    placed = False
                    placed_index = -1
                    mill_tested = True
            else:
                if game.get_current_phase(global_player) == GamePhase.PLACING and not placed:
                    text_command = "PLAYER "+str(global_player)+": Choose position where to place your piece: "
                    placed_index = handle_placing(global_player, event)
                    
                elif game.get_current_phase(global_player) == GamePhase.MOVING or game.get_current_phase(global_player) == GamePhase.FLYING and not placed:
                    if start is None and target is None:
                        text_command = "PLAYER "+ str(global_player) +": Choose position of piece you want to move: "
                        start = handle_start_target(event)
                    elif start is not None and target is None:
                        text_command = "PLAYER " + str(global_player) + ": Choose target position to which you want to move your piece"
                        target = handle_start_target(event)
                    else:
                        handle_moving()
                    
        pygame.display.update()
        drawBoard(game.get_board())
        clock.tick(fps)

    if winner is None:
        winner = game.is_winner()
        if winner is not None:
            text_command ="The winner is Player: "+str(winner)