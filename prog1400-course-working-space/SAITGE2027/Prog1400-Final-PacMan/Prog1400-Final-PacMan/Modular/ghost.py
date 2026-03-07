"""
Student: Walker Gould
Student ID: W0403704
Instructor: Davis Boudreau
Course: PROG1400
Assignment: Final Project: Pac-Man Enhanced
Date: April 18th, 2025 - Friday
Term: 2nd Semester - Winter of 2025.

"""


# Importing essential modules, used in this class, such as pygame, random, math, time and threading.
import pygame
import random
import math
import time
import threading

#importing maze walls so that ghost classes and functions can reference it, especially for collision detection, etc.
from maze import maze_walls

#importing the screen from settings.py so that classes and functions can be written to the game screen.
from settings import screen





# Defining the main ghost class that all subclasses of ghost will inherit from for basic common functionality.
class Ghost: #Ghost class name
    def __init__(self, x, y, color): # initalizing class ghost as an object with class attributes.
        self.x = x
        self.y = y
        self.color = color #default color set to color variable
        self.speed = 3 # default ghost speed is set to 3.
        """# Random direction movement choice set as a list of left, right, up, down as a random choice
        using the random module imported earlier."""
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        """default self.image for the ghost set as ghost.png from graphics folder
        unless overridden by subclasses"""
        self.image = pygame.image.load("graphics/ghost.png")
        """self position calling method to get cords"""
        self.position = (x, y)
        """movement history list to append too if needed"""
        self.history = []
        """common ghost name is 'Ghost' if name ever wanted to be referenced or printed by future code"""
        self.name = "Ghost"
        """The ghost is set to not dead, as default, ironically."""
        self.dead = False
        """Setting the location of which the ghost will scatter or run too, if in scatter mode
        in this case, the scatter_target is the ghost or subclass ghost original spawn point location of itself
        in any further code."""
        self.scatter_target = (100, 100)  # Example corner (can be customized)
        """The default mode for a ghost is 'chase' which means to chase pac man."""
        self.mode = "chase"


    """defining the default scatter behavior for ghost and subclasses of ghost as a function unless overridden explicitly.
    Therefore unless overridden, will apply to all ghost and all ghost subclasses"""
    def scatter(self, pacman, maze_walls):

        """Chase Pac-Man and avoid maze walls"""
        for wall in maze_walls[:]:  # Iterate over a copy of the list of maze_walls, accessing locations.
            #add location history, see pellets for example, and pac-man
            #with the goal of avoiding collisions to walls.

            """ # settings the new_y and new_x the same as self.y and self.x
            this is setting the rect or collision part of the program the same as the ghost self location."""
            new_x, new_y = self.x, self.y
            """defining the collison area of the ghost"""
            new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)

            """if ghost or collision area, e.g new_rect collides with a wall
            as defined in maze_walls for wall"""
            if new_rect.colliderect(wall):
                """if mindlessly colliding with a wall, this should make the ghost follow a wall instead of being stuck."""
                self.follow_wall()

        """Some scatter logic I made myself, so that ghost will move to their scatter target location as defined previously
        but they will also run away from pacman, directly, e.g if pacman moves towards them, they will move away instead
        e.g ghost will actively move in any direction away from pacman depending on pacman's location from the
        ghost's current position."""
        ###I wrote this algorithm myself

        """ Initiating that a rect or collision object is the same as the ghosts position
        this allows the game or program to detect if something collides with a ghost."""
        new_x, new_y = self.x, self.y
        """initating the collision area of the ghost."""

        new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
        """If there's no collision with the walls for the ghost, this code will execute."""
        if not any(new_rect.colliderect(wall) for wall in maze_walls):
            """calculating the distance from the ghost collision area to pacman's position"""
            distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5
            """initating the collision area of the ghost - might be unnecessary, but no time to correct."""
            self.x, self.y = new_x, new_y
            """appending movement history to the self.history list defined earlier"""
            self.history.append((self.x, self.y))
            """
                I MADE THIS ALGORITHM MYSELF or most of it.

            If there's no collisions detected this is how the scatter mode should operate for the ghost."""
            if self.x < self.scatter_target[0]:
                self.x += self.speed
                new_x += self.speed
            elif self.x > self.scatter_target[0]:
                self.x -= self.speed
                new_x -= self.speed
            if self.y < self.scatter_target[1]:
                self.y += self.speed
                new_y += self.speed
            elif self.y > self.scatter_target[1]:
                self.y -= self.speed
                new_y -= self.speed 
            """if there's a collision detected in this loop for the ghost and wall, this will be executed"""
            if new_rect.colliderect(wall):
                                # First condition: between (170, 170) and (200, 200)
                if 170 <= self.x <= 200 and 170 <= self.y <= 200:
                    self.x += 25
                    self.y += 25

                # Second condition: between (515, 65) and (530, 80)
                elif 515 <= self.x <= 530 and 65 <= self.y <= 80:
                    self.x -= 25
                    self.y += 25

                # Second condition: between (515, 65) and (530, 80)
                elif 515 <= self.x <= 530 and 515 <= self.y <= 530:
                    self.x -= 25
                    self.y -= 25

                elif 68 <= self.x <= 95 and 515 <= self.y <= 540:
                    self.x += 25
                    self.y -= 25

                elif 68 <= self.x <= 95 and 68 <= self.y <= 95:
                    self.x += 25
                    self.y += 25
                """Ghost will follow wall instead of getting stuck."""
                self.follow_wall()
                """defining the collision area again"""
                new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
            """defining the collision area again slightly outside of loop."""
            new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
            """if there's no collision detected for wall and ghost, calculate the distance between
            pacman and ghost again."""
            if not any(new_rect.colliderect(wall) for wall in maze_walls):
                distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5


        """setting variable distance as ghost distance to pacman, calculated as of above code.."""
        distance = self.distance_to(pacman)

        """If the calculated distance from ghost and pacman is less than 200 pixels, this code will execute.
            I MADE THIS ALGORITHM MYSELF"""
        if distance < 200:  # Change 100 to whatever distance you feel is appropriate
            """If the distance calculated is less than 200 pixels and pacman.eatghost equals true
            then the ghost will stay in self.mode 'scared' or scatter mode as defined previously"""
            if pacman.eatghost == True:
                self.mode = "scared"
                self.speed = 10 # If the pacman.ghost is true, the ghost will get a speed boost for scared or scatter mode to run away faster.
            """
                I MADE THIS ALGORITHM MYSELF
                If the distance calculated is less than 200 pixels and pacman.eatghost equals false
            then the ghost will switch to self.mode 'chase' mode to chase pacman instead"""
            if pacman.eatghost == False:
                self.mode = "chase"
                self.speed = 3 # supposed to reset self speed of ghost back to normal but this doesnt work but is corrected in future code.

        """initating the collision area of the ghost."""
        new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)

        """If there's no collision with the walls for the ghost, this code will execute.""" 
        if not any(new_rect.colliderect(wall) for wall in maze_walls):
                """calculates the distance between ghost collison area and pacman and sets it as distance."""
                distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5
                """sets the collision area position the same as ghost x and y cords"""
                self.x, self.y = new_x, new_y
                """appends the ghost positions to self history, if there's no collisions, to sort of make a better movement path
                if wanted"""
                self.history.append((self.x, self.y))
                """     I MADE THIS ALGORITHM MYSELF
                If the calculated distance between ghost and pacman is less than 200 pixels then
                the code below if distance < 200: will execute."""
                if distance < 200:
                    """if the distance is less than 200 pixels and the ghost mode self.mode scared is active
                    then the below code will execute."""
                    if self.mode == "scared":
                        """     I MADE THIS ALGORITHM MYSELF
                        This logic actively moves the ghost away from pacman from any position
                        if the ghost mode is set to scared. """
                        if self.x < (pacman.x):
                            self.x -= self.speed
                            new_x -= self.speed
                        elif self.x > (pacman.x): 
                            self.x += self.speed
                            new_x += self.speed
                        if self.y < (pacman.y): 
                            self.y -= self.speed
                            new_y -= self.speed
                        elif self.y > (pacman.y): 
                            self.y += self.speed   
                            new_y += self.speed

                        """
                            I MADE THIS ALGORITHM MYSELF
                        If the above if distance statement is true
                        and there's a collsion between the ghost and a wall, the ghost will follow the wall instead
                        of getting stuck"""
                        if new_rect.colliderect(wall):
                            self.follow_wall()
                            """If the distance is greater than > 200 and there isn't any collision between
                            the ghost and wall, the code below will execute."""
                    elif distance > 200 and not any(new_rect.colliderect(wall) for wall in maze_walls):

                        """     I MADE THIS ALGORITHM MYSELF
                        if distance is greater than 200 and there's no wall and ghost collisions this
                        code below will execute."""
                        if pacman.eatghost == True: # if pacman.eatghost is true, ghost are scared and faster than normal
                            self.mode = "scatter"
                            self.speed = 10
                        if pacman.eatghost == False: # if pacman.ghost is false, ghost are normal speed and chase pacman
                            self.mode = "chase"
                            self.speed = 3
                    if pacman.eatghost == False: # if pacman.ghost is false, ghost are normal speed and chase pacman
                        self.mode = "chase"
                        self.speed = 3
                
            # Check for collisions with maze walls
                new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
                
                if not any(new_rect.colliderect(wall) for wall in maze_walls):
                        distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5 # distance between pacman and ghost


    """
        I MADE THIS ALGORITHM MYSELF
    Function scat is setting ghost speed to 0, so that it freezes
    this is used for when ghost are died when pacman eats them, when pacman can eat them"""
    def scat(self):
        self.speed = 0
        
    """function, sort of default behavior of moving ghost towards pacman, e.g the 'chase' function 
    as previously mentioned."""
    def move_towards(self, pacman):
        """Chase Pac-Man and avoid maze walls"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        best_direction = None # no best direction set yet.
        min_distance = float('inf') # logic to detect minimum distance from ghost to pacman and to move towards it.

        #Defining the behavior of ghost movement directions in pygame directions.
        # Moves at self.speed or ghost speed when chasing.
        for direction in directions:
            new_x, new_y = self.x, self.y
            if direction == "UP":
                new_y -= self.speed

            elif direction == "DOWN":
                new_y += self.speed
            elif direction == "LEFT":
                new_x -= self.speed
            elif direction == "RIGHT":
                new_x += self.speed

            
            # Check for collisions with maze walls
            new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
            if not any(new_rect.colliderect(wall) for wall in maze_walls):
                # Calculates distance between ghost and pacman.
                distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5
                #ghost movement behavior to chase pacman.
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction


        # defining the best direction to move or chase pacman.
        if best_direction:
            if best_direction == "UP":
                self.y -= self.speed
            elif best_direction == "DOWN":
                self.y += self.speed
            elif best_direction == "LEFT":
                self.x -= self.speed
            elif best_direction == "RIGHT":
                self.x += self.speed
        else:
            # If no best direction found, follow the wall
            self.follow_wall()
        
    """A switch between scatter mode (scared) or chasing pacman, called as needed, intended or wanted."""
    def update(self, pacman):
        self.switch_mode(pacman)  # Switch between chase and scatter mode
        if self.mode == "chase": # if mode is 'self.mode chase' then ghost will move towards 
            #pacman using the move_towards function.
            self.move_towards(pacman)
        elif self.mode == "scatter": # if self.mode scatter is set, then ghost will run away or 'scatter' away from pacman
            # using the scatter function. Maze walls is in the function to detect collisions with walls
            # and to prevent ghost moving through walls.
            self.scatter(pacman, maze_walls)
            
    """### function using math module to calculate distance between ghost and pacman, can be used for further game development and 
    # ghost behaviors"""
    def distance_to(self, pacman):
        return math.sqrt((self.x - pacman.x)**2 + (self.y - pacman.y)**2)
    
    """A variant of update(self,pacman) function defined earlier but uses distance to pacman
    as a switching mechanism instead of just directly updating ghost chase modes like function update(self, pacman) defined
    above."""
    def switch_mode(self, pacman):
        # Switch to scatter mode if close to Pac-Man
        distance = self.distance_to(pacman) # calculates distance using distance_to(pacman) as defined earlier
        """if this method of ghost switch mdoe behavior is called, which is based on distance instead of absolutes
        then the ghost will switch into this mode depending on it's distance to pacman
        so in this case, the ghost will switch into scatter mode (scared mode) if the distance is less than
         100 pixels to pacman, and if it's more than 100, the ghost will move towards to 'chase' mode
          or moves towards pacman, this is essentially a clyde like behavior function
           that can be changed even further. """
        if distance < 100:  # Change 100 to whatever distance you feel is appropriate #if 
            self.mode = "scatter"
        else:
            self.mode = "chase"

### Function for defining ghost when they start colliding with maze walls and getting stuck.
    def follow_wall(self):
        """Follow the wall to avoid getting stuck"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        random.shuffle(directions)  # Randomize direction order to avoid getting stuck
        # Accessing the parameters of which directions are available for the ghost to move with, using collision
        # rect factors new_x, new_y
        for direction in directions:
            new_x, new_y = self.x, self.y
            if direction == "UP":
                new_y -= self.speed
            elif direction == "DOWN":
                new_y += self.speed
            elif direction == "LEFT":
                new_x -= self.speed
            elif direction == "RIGHT":
                new_x += self.speed
            
            # Check for collisions with maze walls # if there's no collisions, it will move in this direction.
            new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
            if not any(new_rect.colliderect(wall) for wall in maze_walls):
                self.x, self.y = new_x, new_y
                break # breaks the loop so it doesnt continue indefinitely.

    """Creating a load function to load custom images as self.image for ghost. Their basic default images."""
    def load(self):
        self.image = pygame.transform.scale(self.image, (50, 50)) # loads image, scales it and sets it to 50, 50 pixels
        #sets image the same location of their actual position in-game
        img_rect = self.image.get_rect(center=(self.x, self.y))

        screen.blit(self.image, img_rect) # draws the ghost image on screen

    # Draws the ghost on the screen as a circle if called.
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)

    """
        I MADE THIS ALGORITHM MYSELF for the most part.

    # Defines the ghost died function if a ghost dies, if they are eaten by pacman.
    The ghost will die once this is called, the speed is set to 0 so it can't move
    the self.dead property is set to true to indicate to the game that it is actually dead
    and then will reset the ghosts position to their default position
    and then there's a timer set, to revive the ghost after the timer ends so they can
    resume their normal behavior and interact again."""
    def died(self):
        self.speed = 0
        self.dead = True
        self.resetcords()
        timer_thread = threading.Thread(target=self.revive)
        timer_thread.start()

    """
        I MADE THIS ALGORITHM MYSELF
        
        function to reset the ghosts position if needed, such as when a ghost is eaten by pacman or when a ghost
    eats pacman and the game resets."""
    def resetcords(self, x=100, y=100):
        self.x = x
        self.y = y

        
    """
    I MADE THIS ALGORITHM MYSELF for the most part, e.g didnt make the time.sleep part.

    Timer function as mentioned in the died function, this revives a ghost after a timer countdown when it is eaten
    by pacman. It does some basic stuff such as calling scat to set ghost speed to 0 so it freezes
    the timer sleeps for 10 seconds as initiated by died function and after the timer ends
    the self.dead property of the ghost is set to false, so it's alive again and then the speed of the ghost is set back to 3, or 'normal
    and then it prints that the ghost is revived"""
    def revive(self):
        self.scat()
        self.speed = 0
        time.sleep(10)  # wait for 10 seconds
        self.dead = False # ghost is back!
        self.speed = 3
        print(f"[DEBUG] Ghost revived: {self}")

    """    I MADE THIS ALGORITHM MYSELF
    
    God function, it's used to reset the normal behavior of ghost
    after pacman eats a god fruit and then ghosteat and ghostplan attributes for pacman resets after
    the boost effects of pacman eating a god fruit expires.
    It iterates through the ghost list and sets the speed back to normal if
    ghostplan is set to false, which means pacman's boost effects from eating a god fruit is expired
    this is some tricky logic mechanisms that allow seamless normal ghost behaviors."""
    def god(*ghosts):
            for ghost in ghosts:
                ghost.speed = 3
    """    I MADE THIS ALGORITHM MYSELF
    custom made scared switch function if pacman eats a god fruit and gains a boost
    if pacman eats a god fruit, ghost will switch into scatter mode or scared mode."""
    def scaredswitch(self, pacman):
        if pacman.eatghost == True:
            self.scatter(pacman, maze_walls)
            self.mode = "scatter"
        """if pacman eats a god fruit and the timer countdown expires, the ghost will
        switch back into chase pacman mode."""
        if pacman.eatghost == False:
            self.speed = 3
            self.move_towards(pacman)
            self.mode = "chase"
            self.speed = 3


    """    I MADE THIS ALGORITHM MYSELF
    A function to reset all the ghosts position back to their original positions after a game event
    such as when pacman is eaten by a ghost."""
    def reset_all_ghosts(*ghosts): # accepts ghosts as multiple arguments to be able to use any type of ghost.
        for ghost in ghosts: #iterates through the ghost list for the above command.
            """ghost reset function to reset the ghost position to their original position, as defined
            in resetcords, the subclasses override this to make their default position."""
            ghost.resetcords()  # Reset to a default position or specific positions
            print(f'reset')





"""Blinky ghost subclass of ghost, a red aggressive ghost."""
class Blinky(Ghost): # Red ghost, aggressive.
    def __init__(self, x, y, color):
        # Properly call the constructor of the Ghost class 
        super().__init__(x, y, color) # initalizing the inheritance from the ghost class.
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.image.load("graphics/blinky.png") # Blinky's default ghost image displayed on screen
        self.name = "Blinky" # original name of blinky.

        self.position = pygame.math.Vector2(x, y) # setting the position of blinky as a pygame vector for ease of cord calculations.
        self.scatter_target = (500, 500)  # Example corner (can be customized) goes to this area in scatter mode.
        
        
    def resetcords(self, x=500, y=500): # reset cords as defined in the ghost class but with a customized position for blinky ghost
        #overridden
        """Reset the position of the object to the given coordinates."""
        self.x = x
        self.y = y

    """    I MADE THIS ALGORITHM MYSELF
    
    Speed increase function for Blinky, using pacman's score as a counter, so the
    greater pacman's score is, the faster Blinky will chase pacman."""
    def speed_increase(self, pacman):

        if pacman.score >= 100:
            self.speed = 4
            print(f"Blinky gets a speed increase")
        if pacman.score >= 500:
            self.speed = 5
            print(f"Blinky gets another speed increase")
        """If blinky is dead, his speed is set to 0, to freeze him, until he is no longer dead
        as set by the revival function defined in the ghost class, this blinky ghost class inherits
        functionality from the ghost class/object."""
        if self.dead == True:
            self.speed = 0






"""Custom subclass/child class of the ghost, in this case Pinky!@#!@!
"""
class Pinky(Ghost): # creates child class of ghost, inheriting from it directly.
    def __init__(self, x, y, color):
        # Properly call the constructor of the Ghost class
        super().__init__(x, y, color)
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.image.load("graphics/pinky.png") # loads Pinky's default image.
        self.mode = "chase" # the default mode of pinky is to chase pacman.
        self.location_log = [] # History log of Pinky's position, if needed or wanted for future ghost behaviors, etc.
        self.name = "Pinky" # A default name to reference to Pinky's name if wanted.
        self.scatter_target = (600, 100)  # Example corner (can be customized) scatters to this area when scared or in scatter mode

    """Function to draw a circle of Pinky onto the screen if wanted, depreciated as load(self) is used instead."""
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)

    """    I MADE THIS ALGORITHM MYSELF
    if Pinky is ever reset, such as when eaten, or when pacman is eaten and the game resets
    this is the default location of Pinky to reset too."""
    def resetcords(self, x=600, y=100):
        """Reset the position of the object to the given coordinates."""
        self.x = x
        self.y = y


    """    I MADE THIS ALGORITHM MYSELF
    
    Switching mode for Pinky to either ambush PacMan or to chase him.
    highly customized and mostly made by me. I made the chasing algorthim for Pinky myself.
    """

    def switch_mode_pinky(self, pacman): 

        distance = self.distance_to(pacman)
        if distance > 50:  # Change 50 to whatever distance you feel is appropriate
            """If the distance to pacman is mroe than 50 pixels, the ghost will
            try to ambush pacman by predicting his position, but if the ghost
            gets close enough, it will 'move' directly towards pacman in a very
            aggressive manner."""
            self.mode = "ambush" # This mode will predict Pacman's position from 4 pixels or blocks away.
        else:
            """if the ghost is closer than 50 pixels away from pacman
            it will stop moving 4 blocks or pixels ahead of pacman and aggressively pursue pacman directly."""
            self.mode = "chase" # This is the simple move_towards functionality as defined in ghosts.

    """     I MADE THIS ALGORITHM MYSELF FOR THE MOST PART.

    Another method of updating Pinky's behaviors to chase pacman
    switching between the modes I defined, such as chase or ambush as defined above
    in the switch_mode_pinky function. This takes into account of the maze_walls for
    detectiion purposes, this method simply updates the modes of Pinky."""
    def updatecords(self, pacman):
        self.switch_mode_pinky(pacman)  # Switch between chase and scatter mode
        if self.mode == "chase":
            self.move_towards(pacman)
        elif self.mode == "ambush":
            self.ambush(pacman, maze_walls)
    """Function to get Pinky's position if wanted."""
    def get_position(self):
        return self.x, self.y
    
    """    I MADE THIS ALGORITHM MYSELF
    The ambush function for Pinky, this predicts pacman's position of up too 4 blocks or pixels
    ahead of his current position using a very simple algorthim that I made without
    using complex formulas or calculations."""
    def ambush(self, pacman, maze_walls):

        """Chase Pac-Man and avoid maze walls"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        best_direction = None
        min_distance = float('inf')

        #I wrote this algorithm myself
        #It was a lot more simple than the recommendations from 'other' sources.
        
        new_x, new_y = self.x, self.y
        new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)

        """# Iterate over a copy of the list to access the list directly.
           with the goal of avoiding collisions to walls. """
        for wall in maze_walls[:]:  

            
            """    #########I made this algorithm/code myself for th
            
            If there happens to ever be a collision between Blinky and the maze walls
            this code will execute, essentially preventing any morphing through the walls for Blinky
            or getting stuck in the walls, for example.
            I used debugging console for Blinky's positions when I noticed there was a glitch
            and made the following code to stop the glitches.
            """
            if new_rect.colliderect(wall):
                print("test blinky1")
                print(f"X: {self.x} Y: {self.y}")

                # First condition: between (170, 170) and (200, 200)
                if 170 <= self.x <= 200 and 170 <= self.y <= 200:
                    self.x += 25
                    self.y += 25

                # Second condition: between (515, 65) and (530, 80)
                elif 515 <= self.x <= 530 and 65 <= self.y <= 80:
                    self.x -= 25
                    self.y += 25

                # Second condition: between (515, 65) and (530, 80)
                elif 515 <= self.x <= 530 and 515 <= self.y <= 530:
                    self.x -= 25
                    self.y -= 25

                elif 68 <= self.x <= 95 and 515 <= self.y <= 540:
                    self.x += 25
                    self.y -= 25

                elif 68 <= self.x <= 95 and 68 <= self.y <= 95:
                    self.x += 25
                    self.y += 25
                    
                """    I MADE THIS ALGORITHM MYSELF
                
                If there's no collisions detected in the movements of the ghost
                between itself and the maze walls, it will predict pacman's movement
                of 4 blocks/pixels ahead and move towards that in his direction
                keep in mind this algorithm will make the ghost a lot more responsive
                to pacman's movement than the move_towards function and
                appears to be a lot more aggressive in the ghost's pursuit
                in pacman from the code that I written for this algorithm.
                """
                if not any(new_rect.colliderect(wall) for wall in maze_walls):
                    if self.x < (pacman.x + 4):
                        self.x -= self.speed
                        new_x -= self.speed
                    elif self.x > (pacman.x - 4):
                        self.x += self.speed
                        new_x += self.speed
                    if self.y < (pacman.y + 4):
                        self.y -= self.speed
                        new_y -= self.speed
                    elif self.y > (pacman.y - 4):
                        self.y += self.speed   
                        new_y += self.speed
                       

                """    I MADE THIS ALGORITHM MYSELF
                
                If there's no collisions detected in the movements of the ghost
                between itself and the maze walls, it will predict pacman's movement
                of 4 blocks/pixels ahead and move towards that in his direction
                keep in mind this algorithm will make the ghost a lot more responsive
                to pacman's movement than the move_towards function and
                appears to be a lot more aggressive in the ghost's pursuit
                in pacman from the code that I written for this algorithm.
                """
        if not any(new_rect.colliderect(wall) for wall in maze_walls):
                distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5
                self.x, self.y = new_x, new_y
                self.history.append((self.x, self.y)) # appends movement history if further refinement is wanted

                """   I MADE THIS ALGORITHM MYSELF
                
                If there's no collisions detected in the movements of the ghost
                between itself and the maze walls, it will predict pacman's movement
                of 4 blocks/pixels ahead and move towards that in his direction
                keep in mind this algorithm will make the ghost a lot more responsive
                to pacman's movement than the move_towards function and
                appears to be a lot more aggressive in the ghost's pursuit
                in pacman from the code that I written for this algorithm.
                """
                if self.x < (pacman.x + 4): # Move right if self.x is less than pacman.
                    self.x += self.speed
                    new_x += self.speed
                elif self.x > (pacman.x - 4): # Move left if self.x is more than pacman
                    self.x -= self.speed
                    new_x -= self.speed
                if self.y < (pacman.y + 4): # Move down if self.y is less than pacman 400, 600
                    self.y += self.speed
                    new_y += self.speed
                elif self.y > (pacman.y - 4): # move up if self.y is more than pacman 600, 400
                    self.y -= self.speed   
                    new_y -= self.speed


            # Check for collisions with maze walls
                    # Check for collisions with maze walls

        for direction in directions:
            new_x, new_y = self.x, self.y
            if direction == "UP":
                new_y -= self.speed
            elif direction == "DOWN":
                new_y += self.speed
            elif direction == "LEFT":
                new_x -= self.speed
            elif direction == "RIGHT":
                new_x += self.speed
            
            # Check for collisions with maze walls
            new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
            if not any(new_rect.colliderect(wall) for wall in maze_walls):
                # calculates distance between pacman and ghost.
                distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction


        if best_direction:
            if best_direction == "UP":
                self.y -= self.speed
            elif best_direction == "DOWN":
                self.y += self.speed
            elif best_direction == "LEFT":
                self.x -= self.speed
            elif best_direction == "RIGHT":
                self.x += self.speed
        else:
            # If no best direction found, follow the wall
            self.follow_wall()






"""Defining a subclass for ghost called Inky."""
class Inky(Ghost):
    def __init__(self, x, y, color):
        # Properly call the constructor of the Ghost class
        super().__init__(x, y, color)
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.image.load("graphics/inky.png") # loads Inky image.
        self.mode = "chase" # Default chase mode.
        self.location_log = []
        self.name = "inky" # customized name for inky.
        self.speed = 3 # default speed.
        self.scatter_target = (600, 500)  # Example corner (can be customized)

    """Depreciated function, to draw a circle of the ghost on screen, was essential for development."""
    def draw(self): 
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)

    """Customized original position for Inky."""
    def resetcords(self, x=600, y=600):
        """Reset the position of the object to the given coordinates."""
        self.x = x
        self.y = y


    # Way of getting Inky's x, y cords.
    def get_position(self):
        return self.x, self.y

    """Defining a class to calculate a target position to go to, using pacman and blinky's position
    this is similar to Pinky's behavior where Pinky can predict Pacman's position 4 blocks ahead.
    it sorts of creates a ambush effect for Inky, based off of pacmans and blinky's cords
    It's a very interesting algorithm."""
    def calculate_inky_target(self, pacman, blinky, ahead_distance=40):
        # Project a point ahead of Pac-Man (Pinky-style)
        projected = pacman.position + pacman.direction * ahead_distance
        
        # Reflect Blinky over that point
        vector = projected - blinky.position
        return projected + vector
    

    """Basic move_towards function for Inky that overrides the original move_towards function
    as defined in the parent ghost class."""

    def move_toward(self, target_pos):
        """Chase Pac-Man and avoid maze walls"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        best_direction = None
        min_distance = float('inf')
        #I wrote this algorithm myself
        #It was a lot more simple than the recommendations from 'other' sources.
        new_x, new_y = self.x, self.y
        new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
        """creates a target position for the direction in which Inky moves."""
        direction = target_pos - pygame.Vector2(self.x, self.y)
        """Returns, length can't really be 0 unless there's collision."""
        if direction.length() == 0:
            return
        """If there's no collisions with the wall, and there's a distance
        between the direction of the target position, Inky will move towards
        that direction."""
        if not any(new_rect.colliderect(wall) for wall in maze_walls):
            direction = direction.normalize()
            self.x += direction.x * self.speed
            self.y += direction.y * self.speed

        """accesses the maze_walls list for collision detection purposes."""
        for wall in maze_walls[:]:  # Iterate over a copy of the list
            """If there's a collision that occurs from this Inky moving algorithm
            and it's detected, Inky will move along the walls instead of getting stuck
            
            THIS ALGORITHM PART WAS MADE BY ME FOR THE MOST PART!"""
            if new_rect.colliderect(wall):
                self.follow_wall() # This function wasn't made by me. 
                """    #########I made this algorithm/code myself for the most part.
                
                If there happens to ever be a collision between Inky and the maze walls
                this code will execute, essentially preventing any morphing through the walls for Inky
                or getting stuck in the walls, for example.
                I used debugging console for Blinky's positions when I noticed there was a glitch
                and made the following code to stop the glitches, but it applies to INKY as well
                because it's the same game map/maze walls.

                """
                # First condition: between (170, 170) and (200, 200)
                if 170 <= self.x <= 200 and 170 <= self.y <= 200:
                    self.x += 25
                    self.y += 25

                # Second condition: between (515, 65) and (530, 80)
                elif 515 <= self.x <= 530 and 65 <= self.y <= 80:
                    self.x -= 25
                    self.y += 25

                # Second condition: between (515, 65) and (530, 80)
                elif 515 <= self.x <= 530 and 515 <= self.y <= 530:
                    self.x -= 25
                    self.y -= 25

                elif 68 <= self.x <= 95 and 515 <= self.y <= 540:
                    self.x += 25
                    self.y -= 25

                elif 68 <= self.x <= 95 and 68 <= self.y <= 95:
                    self.x += 25
                    self.y += 25

        




"""Creating a cylde child class of the parent class Ghost."""
class Clyde(Ghost):
    def __init__(self, x, y, color):
        # Properly call the constructor of the Ghost class
        super().__init__(x, y, color) # Initalizing the inheritance from the ghost parent class.
        self.x = x
        self.y = y
        self.color = color
        self.image = pygame.image.load("graphics/clyde.png") # sets the default image for Clyde.
        self.scatter_target = (100, 500)  # Example corner (can be customized)
        self.mode = "chase"  # Start in chase mode
        self.name = "Clyde" # Clydes name as a reference if needed or wanted

    #Depreciated function to draw circle of ghost on the screen with a specified color.
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)

    """Sets a default location for Clyde if it ever needs to be reset for whateve rreason."""
    def resetcords(self, x=100, y=500):
        """Reset the position of the object to the given coordinates."""
        self.x = x
        self.y = y
    """Mode switch function for Clyde if he gets too close to pacman
    Clyde is essentially a coward, he will chase pacman until he gets close
    and when he gets too close he will run away, but this can add some complexity
    to the game because Clyde's movement behavior can be a bit unpredictable
    like you won't know exactly when he scatters in-game so he can accidentally 
    eat you when you turn a corner or something like that.
    
    This switch mode function works directly with the update(self, pacman) function defined below
    after this function is defined
    
    this changes Clyde's mode based off of distance to pacman
    
    then the update function will execute a movement function based on the mode Clyde is in
    such as chase will execute move_towards and scatter will execute scatter. It's sort of like polymorphism in a way."""
    def switch_mode(self, pacman):
        # Switch to scatter mode if close to Pac-Man
        distance = self.distance_to(pacman)
        if distance < 200:  # Change 200 to whatever distance you feel is appropriate to scatter
            self.mode = "scatter"
        else:
            self.mode = "chase" # chases pacman if the distance to pacman is high enough.

    """Update function for Clyde's behavior if called, if his mode is set to chase
    this will call the function or movement behavir 'move_towards(pacman)' as defined in the parent
    ghost class and if the mode is set to 'scatter' then the function will use scatter(pacman, maze_walls) this will
     make Clyde scatter to his corner
      This update function works directly with the switch_mode function that changes the modes 'scatter' or 'chase
       based off of the distance to pacman. It's sort of polymorphism in a way. """
    def update(self, pacman):
        self.switch_mode(pacman)  # Switch between chase and scatter mode
        if self.mode == "chase":
            self.move_towards(pacman)
        elif self.mode == "scatter":
            self.scatter(pacman, maze_walls) # maze walls are called for collision detection purposes.

    """Optional chase_pacman function for Clyde that can be defined further
    
    very similar to the move_towards function. See move_towards function for reference.
    """
    def chase_pacman(self, pacman):
        """Chase Pac-Man and avoid maze walls"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        best_direction = None
        min_distance = float('inf')

        for direction in directions:
            new_x, new_y = self.x, self.y
            if direction == "UP":
                new_y -= self.speed
            elif direction == "DOWN":
                new_y += self.speed
            elif direction == "LEFT":
                new_x -= self.speed
            elif direction == "RIGHT":
                new_x += self.speed
            
            # Check for collisions with maze walls
            new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
            if not any(new_rect.colliderect(wall) for wall in maze_walls):
                distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction


        if best_direction:
            if best_direction == "UP":
                self.y -= self.speed
            elif best_direction == "DOWN":
                self.y += self.speed
            elif best_direction == "LEFT":
                self.x -= self.speed
            elif best_direction == "RIGHT":
                self.x += self.speed
        else:
            # If no best direction found, follow the wall
            self.follow_wall()


    """Scatter function, highly customized and made by me.
    The movement algorithm was modified by me heavily."""
    def scatter(self, pacman, maze_walls):
        """Chase Pac-Man and avoid maze walls"""

        """ #I wrote this algorithm myself """
        new_x, new_y = self.x, self.y

        # Move Clyde towards the scatter corner (100, 500)
        # Clyde directly moves towards the scatter target
        # I defined this movement behavior myself
        # Besides the scatter_target part.
        if self.x < self.scatter_target[0]:
            self.x += self.speed
            new_x += self.speed
        elif self.x > self.scatter_target[0]:
            self.x -= self.speed
            new_x -= self.speed
        if self.y < self.scatter_target[1]:
            self.y += self.speed
            new_y += self.speed
        elif self.y > self.scatter_target[1]:
            self.y -= self.speed
            new_y -= self.speed    

            
            # Check for collisions with maze walls, makes a rect collision for Clyde 
            # using this movement algorithm.
            new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
            """ Distance is greyed out but it still functions for some reason.
            It's collision detection for the above moving algorithm made mostly by me.
            and calculates distance from ghost to pacman."""
            if not any(new_rect.colliderect(wall) for wall in maze_walls):
                distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5



