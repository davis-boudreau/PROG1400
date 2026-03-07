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

#Using settings.py, in particular the screen variable to access the screen to draw on, etc.

from settings import screen




"""Making a iterable list of pygame rect objects as pellets, this is the locations of the pellets in game on the screen
"""
pellet_locations = [
    pygame.Rect(100, 100, 5, 5),  # Pellet 1, there's x, y positions, e.g 100, 100 and then the size of the pellets, 5 by 5 pixels
    pygame.Rect(200, 200, 5, 5),  # Pellet 2
    pygame.Rect(250, 250, 5, 5),  # Pellet 3
    pygame.Rect(100, 100, 5, 5),  # Pellet 4
    pygame.Rect(275, 275, 5, 5),  # Pellet 5
    pygame.Rect(420, 420, 5, 5),  # Pellet 6
    pygame.Rect(450, 450, 5, 5)   # Pellet 7
]

  ##Creating a food class for pellets
class Pellets: #Declaring the pellets class
    def __init__(self, x, y, color): #Initializing the pellet class
        self.x = x # self.x, self.y and self.color as some properties.
        self.y = y
        self.color = color
        """Setting the self locations of the pellets as the list of pellets defined earlier in the code, directly 
        referring to it as 'self.locations = pellet_locations. The location of the pellets are now this list that was made
        earlier."""
        self.locations = pellet_locations
        """Loading an image from the graphics folder as the pellet image used for pellets in game"""
        self.image = pygame.image.load("graphics/pellet.png")

        """Function for drawing pellets onto the screen in-game, with pixel image size of 30.
        this isn't used but was used for developmental purposes while constructioning the other code."""
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 30)
        
        """Function to be able to get the position of the pellets if needed"""
    def get_position(self):
        return self.x, self.y
    
    """Loads self onto the game screen and 'draws' it using the self.image png file as defined earlier in this class"""
    def load(self):
        """sets self.image as the image defined in self.image above, e.g from the graphics folder
        and then using the pygame.transform.scale to draw it onto the screen, initalize it and set the pixel size, 30, 30
        for the pellet."""
        self.image = pygame.transform.scale(self.image, (30, 30)) 
        """For the pellet locations, it is iterated through, and as it is iterated through
        the image for the pellet is drawn"""
        for p in pellet_locations:
            """drawing the image defined in self.image as the image for each particular pellet location defined earlier
            in the pellet_locations, etc."""
            screen.blit(self.image, p)

        

