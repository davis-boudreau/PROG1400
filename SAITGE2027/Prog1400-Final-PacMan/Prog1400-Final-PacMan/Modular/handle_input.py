"""
Student: Walker Gould
Student ID: W0403704
Instructor: Davis Boudreau
Course: PROG1400
Assignment: Final Project: Pac-Man Enhanced
Date: April 18th, 2025 - Friday
Term: 2nd Semester - Winter of 2025.

"""

import pygame

# Handles the keyboard input for pacman, the player.
# this is called by game.py.

def handle_input(pacman): # calls pacman for handle input
    
    """Handle user input for movement"""
    keys = pygame.key.get_pressed() #detects when a button is pressed on the keyboard

    if keys[pygame.K_UP]: pacman.move("UP") # if the keypad button K_UP is pressed, it will move pacman up on the game screen.

    if keys[pygame.K_DOWN]: pacman.move("DOWN") # if the keypad button K_DOWN is pressed, it will move pacman down on the game screen.

    if keys[pygame.K_LEFT]: pacman.move("LEFT") # if the keypad button K_LEFT is pressed, it will move pacman left on the game screen.

    if keys[pygame.K_RIGHT]: pacman.move("RIGHT")   # if the keypad button K_RIGHT is pressed, it will move pacman right on the game screen.
