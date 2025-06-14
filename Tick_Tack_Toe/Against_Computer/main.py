# age_calculator.py
import pygame
import sys
from menu import show_menu
from result_of_game import show_winner
from gameloop import play_game

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Fonts
font = pygame.font.SysFont(None, 40)

# Start game
show_menu(screen, font)
play_game(screen, font, show_winner)
