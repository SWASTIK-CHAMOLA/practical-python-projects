# age_calculator.py
import pygame
import sys
from menu import show_menu
from game_logic import play_game

pygame.init()  # Initialize pygame BEFORE using anything from pygame

if __name__ == "__main__":
    while True:
        show_menu()   # Show the menu screen
        play_game()   # Start the game after menu
