import pygame
import sys
from result_of_game import show_winner

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 5
SQUARE_SIZE = WIDTH // 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)

board = [" " for _ in range(9)]

def draw_lines(screen):
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_symbols(screen):
    for i in range(9):
        row, col = i // 3, i % 3
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        if board[i] == "X":
            pygame.draw.line(screen, X_COLOR, (x - 40, y - 40), (x + 40, y + 40), 6)
            pygame.draw.line(screen, X_COLOR, (x + 40, y - 40), (x - 40, y + 40), 6)
        elif board[i] == "O":
            pygame.draw.circle(screen, O_COLOR, (x, y), 40, 6)

def check_winner(player):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any(board[a] == board[b] == board[c] == player for a,b,c in wins)

def is_draw():
    return " " not in board

def get_cell_from_pos(pos):
    x, y = pos
    return (y // SQUARE_SIZE) * 3 + (x // SQUARE_SIZE)

def play_game():
    global board
    board = [" " for _ in range(9)]
    current_player = "X"
    running = True

    screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Now initialized at runtime
    font = pygame.font.SysFont(None, 40)                # Safe now

    screen.fill(WHITE)
    draw_lines(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                index = get_cell_from_pos(pygame.mouse.get_pos())
                if board[index] == " ":
                    board[index] = current_player
                    if check_winner(current_player):
                        draw_symbols(screen)
                        pygame.display.update()
                        show_winner(screen, font, f"Player {1 if current_player == 'X' else 2} Wins!", play_game)
                        return
                    elif is_draw():
                        draw_symbols(screen)
                        pygame.display.update()
                        show_winner(screen, font, "It's a Draw!", play_game)
                        return
                    else:
                        current_player = "O" if current_player == "X" else "X"

        screen.fill(WHITE)
        draw_lines(screen)
        draw_symbols(screen)
        pygame.display.update()
