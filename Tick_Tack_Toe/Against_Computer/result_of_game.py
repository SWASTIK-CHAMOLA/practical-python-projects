# end_result_screen.py
import pygame

def show_winner(screen, font, text):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    screen.fill(WHITE)
    label = font.render(text, True, BLACK)
    screen.blit(label, (screen.get_width() // 2 - label.get_width() // 2, screen.get_height() // 2 - label.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)
