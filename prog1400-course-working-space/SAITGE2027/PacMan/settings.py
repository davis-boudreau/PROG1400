"""
Student: Walker Gould
Student ID: W0403704
Instructor: Davis Boudreau
Course: PROG1400
Assignment: Final Project: Pac-Man Enhanced
Date: April 18th, 2025 - Friday
Term: 2nd Semester - Winter of 2025.

"""

"""Settings that are used and referenced too by other classes, such as game.py, pacman.py, etc as needed
These are some common settings, such as colors, width and height of the, clock, display, screen, etc.
It helps to keep the code cleaner and more organized and makes changing code easier
for example instead of defining a color every time you need a color, using the RGB numbers
you can simply reference this settings.py file with the color that you want, such as 'from settings import RED, BLACK' or 
whatever color that you need in your current class, such as pacman.py class, this also allows for ease of changes, for examples
for the width or height of the screen you don't need to manually change each number referencing the screen, or color or whatever it is
you can simply change the width, height or color parameters as an example for more consistency across your code."""

# imports pygame module functionality for making games.
import pygame
# settings.py


#The screen width and height values in pixels set as a fixed value.
WIDTH, HEIGHT = 600, 600

# Tuples for Colors for use by any class.
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)

"""Here's an example of using the settings, in this case it actually works and is functional
I don't have to manually put in 600, 600 for the set_mode as the number of pixels, I simply plug in the
width and height settings into it and it will work."""
screen = pygame.display.set_mode((WIDTH, HEIGHT))
"""Pacman terminal display name."""
display = pygame.display.set_caption("Pac-Man Interactive by Walker Gould.")
"""clock rate for clock."""
clock = pygame.time.Clock()