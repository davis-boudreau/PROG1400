"""
Student: Walker Gould
Student ID: W0403704
Instructor: Davis Boudreau
Course: PROG1400
Assignment: Final Project: Pac-Man Enhanced
Date: April 18th, 2025 - Friday
Term: 2nd Semester - Winter of 2025.

"""


"""Check_collision.py class, used for checking collisions between pacman and ghost
kept here to keep the code more organized and cleaner"""

"""Defining the check collision function for pacman and *ghosts, which is simply multiple arguments
for ghost, it means that you can put more than one argument into the *ghosts part of the code
essentially meaning that you can enter multiple types of ghosts from the ghost class in ghost.py
into this code, so it doesn't only work for one type of ghost, it can work for all of them
typically by iterating through the list of ghost types, e.g pinky or clyde, etc."""\

def check_collision(pacman, *ghosts):
    """Iterates through the list of ghosts."""
    for ghost in ghosts:
        """Calculating the distance between a ghost and pacman using their x and y cords.
        and declaring the distance calculated as variable 'distance' """
        distance = ((pacman.x - ghost.x) ** 2 + (pacman.y - ghost.y) ** 2) ** 0.5
        """if the distance between pacman and a ghost is less than 20 pixels, then it counts as a collision
        between the ghost and pacman."""
        if distance < 20:  # Collision threshold
            """Returns the collision as true, so a collision is made."""
            return True  # Return True if a collision is detected
        """returns collision as false, so no collision is made."""
    return False  # Return False if no collision is detected
    

