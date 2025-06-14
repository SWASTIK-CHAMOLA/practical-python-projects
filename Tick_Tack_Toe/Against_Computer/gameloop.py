# game_loop.py
import pygame
import sys
import random

def play_game(screen, font, show_winner):
    WIDTH, HEIGHT = 600, 600
    SQUARE_SIZE = WIDTH // 3
    WHITE = (255, 255, 255)
    LINE_COLOR = (50, 50, 50)
    X_COLOR = (200, 0, 0)
    O_COLOR = (0, 0, 200)

    board = [" " for _ in range(9)]

    def draw_lines():
        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), 5)
            pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), 5)

    def draw_symbols():
        for i in range(9):
            row = i // 3
            col = i % 3
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            if board[i] == "X":
                pygame.draw.line(screen, X_COLOR, (x - 25, y - 25), (x + 25, y + 25), 4)
                pygame.draw.line(screen, X_COLOR, (x + 25, y - 25), (x - 25, y + 25), 4)
            elif board[i] == "O":
                pygame.draw.circle(screen, O_COLOR, (x, y), 30, 4)

    def check_winner(player):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(board[a] == board[b] == board[c] == player for a,b,c in wins)

    def is_draw():
        return " " not in board

    def computer_move():
        empty = [i for i in range(9) if board[i] == " "]
        if empty:
            board[random.choice(empty)] = "O"

    def get_cell(pos):
        x, y = pos
        return (y // SQUARE_SIZE) * 3 + (x // SQUARE_SIZE)

    running = True
    player_turn = True
    screen.fill(WHITE)
    draw_lines()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if player_turn and event.type == pygame.MOUSEBUTTONDOWN:
                index = get_cell(pygame.mouse.get_pos())
                if board[index] == " ":
                    board[index] = "X"
                    if check_winner("X"):
                        draw_symbols()
                        pygame.display.update()
                        show_winner(screen, font, "You Win!")
                        running = False
                    elif is_draw():
                        draw_symbols()
                        pygame.display.update()
                        show_winner(screen, font, "It's a Draw!")
                        running = False
                    else:
                        player_turn = False

        if not player_turn and running:
            pygame.time.delay(500)
            computer_move()
            if check_winner("O"):
                draw_symbols()
                pygame.display.update()
                show_winner(screen, font, "Computer Wins!")
                running = False
            elif is_draw():
                draw_symbols()
                pygame.display.update()
                show_winner(screen, font, "It's a Draw!")
                running = False
            else:
                player_turn = True

        screen.fill(WHITE)
        draw_lines()
        draw_symbols()
        pygame.display.update()
