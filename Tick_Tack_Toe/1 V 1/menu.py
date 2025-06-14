import pygame
import sys

def show_menu():
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Tic-Tac-Toe Menu")
    font = pygame.font.SysFont(None, 40)

    screen.fill((93,164, 205))  # custom background color WHITE
    menu_text = font.render("Press R to Start, Q to Quit", True, (240, 240, 240))
    rect = menu_text.get_rect(center=(300, 300))
    screen.blit(menu_text, rect)
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
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
