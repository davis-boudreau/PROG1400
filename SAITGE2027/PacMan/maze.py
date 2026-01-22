
"""
Student: Walker Gould
Student ID: W0403704
Instructor: Davis Boudreau
Course: PROG1400
Assignment: Final Project: Pac-Man Enhanced
Date: April 18th, 2025 - Friday
Term: 2nd Semester - Winter of 2025.

"""

"""Maze.py class/module"""
import pygame
"""Using some settings from settings.py for increased functionality of this module """
from settings import WHITE, screen

##### This is the actual maze walls that are drawed and made during the game
##### this code will be called by game.py and other classes as needed to encapsulate the code.

"""# Maze List with gaps
# pygame.Rect(x, y, width, height): This function creates a rectangle with the specified position (x, y) and dimensions (width, height).
"""

"""The list of maze walls as a pygame rect for proper pygame rect collisions"""
maze_walls = [
    pygame.Rect(50, 50, 200, 10),  # numbers are width, height, x, y postions sort of thing.
    pygame.Rect(50, 50, 10, 200),
    pygame.Rect(50, 350, 10, 200),
    pygame.Rect(50, 540, 200, 10),
    pygame.Rect(150, 150, 200, 10),
    pygame.Rect(150, 150, 10, 200),
    pygame.Rect(150, 440, 200, 10),
    pygame.Rect(350, 50, 200, 10),
    pygame.Rect(350, 540, 200, 10),
    pygame.Rect(440, 150, 10, 200),
    pygame.Rect(540, 50, 10, 200),
    pygame.Rect(540, 350, 10, 200)
]

""" Function to call from the list of pygame rects from maze_walls above
it iterates through the list of the maze_walls rects and then draws the mazes/list according to the parameters set
onto the screen, colored as white"""
def draw_maze():
    """Iterates through the list of maze_walls objects/rects"""
    for wall in maze_walls:
        """Draws the maze_walls rects, onto the screen colored as white as the list is iterated through."""
        pygame.draw.rect(screen, WHITE, wall)
  
