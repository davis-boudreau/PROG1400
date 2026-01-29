"""
Student: Walker Gould
Student ID: W0403704
Instructor: Davis Boudreau
Course: PROG1400
Assignment: Final Project: Pac-Man Enhanced
Date: April 18th, 2025 - Friday
Term: 2nd Semester - Winter of 2025.

"""


"""# Importing pygame, time and threading for Pacman functions, interactions and behavior."""
import pygame
import time
import threading
"""
# Calling 'settings' or variables from other classes, e.g the py files such as settings.py, maze.py, etc.
# need for proper code execution as they sort of interact with each other in the code."""

from settings import YELLOW, screen, PINK, WHITE
from maze import maze_walls
from pellets import pellet_locations
"""
# For example, this imports fruit.py into this pacman.py class, specifically the "fruit_locations"
# and 'god_fruit_locations' which is a pygame vector object or list of one item.
# this is so the code defined below can iterate through this list, in the god fruit function part."""
from fruit import fruit_locations, god_fruit_locations

"""
# This defines the object pacman, and all his properties, attributes, behaviors, etc.
# This is what makes pacman and what is instantiated and called in by other classes
# but mainly the game.py file."""

class PacMan:
    def __init__(self, x, y): #Initiates Pac-Man.
        self.x = x
        self.y = y
        self.speed = 5 # default speed of 5
        self.history = [] #pacman's movement history, starts off as empty list and is later appended too.
        self.score = 0 # Pacman's score starts at 0.
        self.lives = 3 # Pacman's lives start at 3.  

        self.image = pygame.image.load("graphics/pacmanmeh.png") # Loads Pacman's default image

        self.position = pygame.math.Vector2(x, y) #Creates a pyvector for pacman's position for easy position calculations.

        self.direction = pygame.math.Vector2(1, 0) # Creates a pyvector for pacman's moving direction for easy direction calculations.

        self.eatghost = False # The property that defines if and when pacman can eat a ghost or not. (Made this algorithm myself)

        self.ghostplan = False # A algorithm I made, it's so that after 'pacman can eat ghost' effects wear off
        # so that the ghost speed resets in a way which doesn't affect normal ghost behaviors.

    # Defining the god fruit, after pacman 'collides' with the ghost fruit or eats it.
    def godfruit(self):
        screen.fill(WHITE) #Visual effects associated with eating a god fruit, a white flash.

        self.image = pygame.image.load("graphics/pacmangod.png") # Loads new pacman image while 'boosted' and effects are active

        self.speed = 15 # Pacman's speed is set to 15 (increased) for a temporary period of time.

        self.eatghost = True # Pacman can eat ghost.

        self.ghostplan = True # Pacman ghostplan = true, explanation mentioned earlier, used for seamless ghost behavior reset after boost wears off

        """timer is set for 25 seconds below further code is executed"""
        time.sleep(25) #The period of time which the boost last from the god fruit before it resets things back to normal

        """# Things are reset back to normal after 25 seconds, which is the following code below:"""
        self.eatghost = False # resets pacmans ability to eat ghost, to false.
        self.ghostplan = False # This intiates the ghost speed reset for normal ghost behavior.
        self.image = pygame.image.load("graphics/pacmanmeh.png") # Loads the normal image for pacman.
        self.speed = 5 # resets pacmans speed back to the default of 5.


    def move(self, direction): # Defines pacman's move behaviors
        """Move Pac-Man within screen boundaries and avoid maze walls"""
        print(f"{self.x} {self.y}") #moves pacman and his rect e.g collison area.s
        new_x, new_y = self.x, self.y
        if direction == "UP":
            new_y -= self.speed
        elif direction == "DOWN":
            new_y += self.speed
        elif direction == "LEFT":
            new_x -= self.speed
        elif direction == "RIGHT":
            new_x += self.speed
        print(f"pacman's direction {direction}") #console log for game development
        
        """
        # Check for collisions with maze walls
        # This creates a rectangular boundary for the moving entity (e.g., Pac-Man or a ghost) at its new potential position (new_x, new_y).
        # The pygame.Rect() function defines a rectangle using four parameters:
        # new_x - 15: The top-left X coordinate (subtracting 15 centers it correctly).
        # new_y - 15: The top-left Y coordinate (subtracting 15 centers it correctly).
        # 30, 30: The width and height of the entity (assuming it's a circle with a 15-pixel radius).
        # This rectangle acts as a hitbox for collision detection."""
        new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
        if not any(new_rect.colliderect(wall) for wall in maze_walls):
            self.x, self.y = new_x, new_y
            self.history.append((self.x, self.y))

        """# Checks for collisions with pellets, from the pellet_locations from the pellet.py class."""
        if not any(new_rect.colliderect(p) for p in pellet_locations): # If there's no collision, no collision takes place.

            """#Prints pacman's score to the console."""
            print(F'Pac is moving with score of {self.score}')

        for p in pellet_locations[:]:  # Iterate over a copy of the list to modify the original while looping

            if new_rect.colliderect(p): # If pacman collides with a pellet, so collision takes place.

                pellet_locations.remove(p)  # Remove the pellet from the list/game.

                self.score = self.score + 1 # Pacman gets score increase after eating pellet.

                timer_thread = threading.Thread(target=self.marriediguanas) #executes pacman's function marriediguanas
                #on a timer, on a separate thread so the game loop won't freeze.

                timer_thread.start() #starts the timer on a separate thread (used for counters or countdowns, etc)

                print('Pac ate')  # Optionally, you can add other actions like score increase

                break  # Stop after removing the first pellet
            
        """#same as above as the pellet logic, but this one is for fruit.
                #grabs the list fruit_locations from fruit.py"""
        
        # Start of fruit logic.
        if not any(new_rect.colliderect(fruit) for fruit in fruit_locations): # no collision

            print(F'Pac is moving with score of ') #Originally here for debugging purposes, can literally do anything with this line.

        for fruit in fruit_locations[:]:  # Iterate over a copy of the list to modify the original while looping

            if new_rect.colliderect(fruit): # collision detection for pacman and fruit

                fruit_locations.remove(fruit) # once collision occurs, the fruit is removed.

                self.score = self.score + 10 # pacman score is increased and more than when eating a pellet.

                timer_thread = threading.Thread(target=self.reset_speed) # Timed seperate thread for countdown effect
                # and boost of eating a fruit, calls reset_speed function in pacman object or pacman.py

                timer_thread.start() # start the thread count and execute command.

            elif new_rect.colliderect(fruit) == False: # if there's no collison.

                self.score = self.score # no score increase

                print('Pac ate')  # Optionally, you can add other actions like score increase

                break  # Stop after removing the first fruit (stops the game from removing fruits infinitely.)

            """#same as above but for god fruit instead, uses list from fruit.py, using the god_fruit_locations list."""
        if not any(new_rect.colliderect(fruit) for fruit in god_fruit_locations): # no collision while iterating through list.

            print(F'Pac is moving with score of ')

        for fruit in god_fruit_locations[:]:  # Iterate over a copy of the list to modify the original while looping

            if new_rect.colliderect(fruit): # collision detection with pacman and fruit

                god_fruit_locations.remove(fruit) # remove the god fruit once collision occurs.

                self.score = self.score + 100 # pacman score is increased by a lot.

                timer_thread = threading.Thread(target=self.godfruit) #god fruit function for pacman is activated on a timer

                timer_thread.start()  # starts timer

            elif new_rect.colliderect(fruit) == False: # no collision

                self.score = self.score

                print('Pac ate')  # Optionally, you can add other actions like score increase

                break # stops removal infinity loop.

    """#The function executed on a timer after pacman eats a pellet."""

    def marriediguanas(self): #defines the function inside pacman object. # Made by Walker Gould.

        screen.fill(YELLOW) # adds visual effects when pellet is eaten

        screen.fill(PINK) # adds visual effects when pellet is eaten

        self.image = pygame.image.load("graphics/pacmanhigh2.png") # loads new pacman image after pellet is eaten

        self.speed = 7 # gives pacman a temporary speed boost.

        time.sleep(25) # boost effects only last 25 seconds after eating the pellet, after that boost is reset.
        """Starts resetting things back to normal after 25 seconds so that it only lasts so long."""

        self.image = pygame.image.load("graphics/pacmanmeh.png") #resets pacman image.

        self.speed = 5 #resets pacman speed.

    """# The function executed on a timer after pacman eats a fruit - Made by Walker Gould"""
    def reset_speed(self): #defines the function inside pacman object or pacman.py

        self.speed = 10 # pacman speed is increased to 10

        self.image = pygame.image.load("graphics/pacmanhigh.png") # new pacman image is loaded

        time.sleep(25)  # wait for 25 seconds before reset occurs

        """Starts resetting things back to normal after 25 seconds so that it only lasts so long."""
        self.speed = 5  # reset speed to normal

        self.image = pygame.image.load("graphics/pacmanmeh.png") # reset to normal

        self.is_boosted = False # reset to normal (not fully defined but the option is there.)

        print(f"{self}'s speed is back to normal.") # console output

    def current_speed(self): #function to check current pacman speed for debugging, development and console logging purposes
        print(f"{self}'s current speed is {self.speed}.")

    def get_position(self): #function to check pacmans position for debugging, development and console logging purposes
        return self.x, self.y
    
    """### Function to load pacman object into game after it's instantiated in the game.py class using pacman.load(), etc.
    # loads self or pacman into game with own player image."""
    def load(self): 
        """# loads self image, loads pixel size of 30, 30."""
        self.image = pygame.transform.scale(self.image, (30, 30))  # Self.image = pacmans image as defined earlier in pacman class

        """# loads image rect onto the exact cords of pacmans actual in-game position so that img equals pacman position."""
        img_rect = self.image.get_rect(center=(self.x, self.y))
        """#draws pacmans image on screen."""
        screen.blit(self.image, img_rect) 


    def draw(self): #used to draw a circle of pacman as an image, not used any more, it's just here, still handy.

        """# it helped a lot into actual game development and getting def load(self) to work properly by cross referencing them."""

        pygame.draw.circle(screen, YELLOW, self.get_position(), 45) # draws the actual pacman character on screen.


    """#the function that is called in game.py once there's a collision between pacman and a ghost
    # if pacman isn't able to eat a ghost, e.g pacman.ghosteat = false aka not boosted by a god fruit."""

    def lifetaker(self): #refers to self, e.g pacman

        print("You got hit by a GHOST") #console output

        global running # if game running = true, global

        if self.lives > 0: #if lives are greater than 0, then once you get eaten/hit by a ghost, pacman

            """# resets back to normal, e.g original pacman position, image, speed, etc and minus one life, if any lives are left."""
            running = True

            """# Resets pacman's position after ghost eats pacman."""
            self.x = 300
            self.y = 300

            """ # takes pacman life by one."""
            self.lives = self.lives -1

            self.speed = 5 # speed reset

            self.image = pygame.image.load("graphics/pacmanmeh.png") # image reset

            """# console log saying you got hit by a ghost and shows your current lives left."""

            print(f"You got hit by a GHOST your number of lives is now {self.lives}") 

            """ #If you get hit by a ghost and your lives now equals 0 lives or less."""
        if self.lives <= 0:
            self.lives = 0 # no lives left
            print(f"Your a loser, you got {self.lives} lives or no life") # proper thing
            running = False # game ends.

        

