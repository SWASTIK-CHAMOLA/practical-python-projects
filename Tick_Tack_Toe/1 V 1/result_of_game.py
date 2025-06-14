import pygame
import sys

def show_winner(screen, font, text, restart_callback):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    screen.fill(WHITE)
    label = font.render(text, True, BLACK)
    info = font.render("Press R to Restart or Q to Quit", True, (100, 100, 100))
    screen.blit(label, (600 // 2 - label.get_width() // 2, 600 // 2 - 30))
    screen.blit(info, (600 // 2 - info.get_width() // 2, 600 // 2 + 10))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    restart_callback()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
