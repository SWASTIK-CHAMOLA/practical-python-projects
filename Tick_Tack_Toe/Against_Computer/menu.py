# menu.py
import pygame
import sys

def show_menu(screen, font):
    WHITE = (255, 255, 255)
    screen.fill(WHITE)
    label = font.render("Press R to Start, Q to Quit", True, (0, 0, 0))
    screen.blit(label, (screen.get_width() // 2 - label.get_width() // 2, screen.get_height() // 2 - label.get_height() // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
