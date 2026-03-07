"""
Student: Walker Gould
Student ID: W0403704
Instructor: Davis Boudreau
Course: PROG1400
Assignment: Final Project: Pac-Man Enhanced
Date: April 18th, 2025 - Friday
Term: 2nd Semester - Winter of 2025.

"""


"""Importing pygame module and functionality"""
import pygame

"""Importing random module and functionality for more algorithmic randomness logically magic."""
import random

"""Calling code from settings.py to keep more consistency in game and code logic."""
from settings import screen, RED, HEIGHT, WIDTH, BLUE

"""Importing threading module and functionality to call parts of program/code to a separate CPU thread
so that the main game loop won't freeze up when executing certain code in this module/class."""
import threading

"""Making a iterable list of pygame rect objects as fruits, this is the locations of the fruits in game on the screen
initially but then it is randomized after pacman eats the first fruit."""
fruit_locations = [pygame.Rect(x, y, 20, 20) for x, y in [(100, 100)]]

"""Defines the fruit size in pixels, this could of been defined in settings.py but it wasn't."""
FRUIT_SIZE = 20

"""Defining the class that makes the object fruit in the game."""
class FruitDrawer: # Fruit class name.
    def __init__(self): # Initalize FruitDrawer class as an object.
        self.screen = screen # Defines self.screen to screen, so once screen is called, it refers to this code.
        self.fruit_locations = []  # Initialize an empty list to hold fruit locations
        self.spawn_fruit()  # Spawn an initial fruit
        self.image = pygame.image.load("graphics/cherry.png") #sets self.image as this particular png image file in the folder graphics
        #essentially setting the graphics for this fruit as a cherry.png image.


    def spawn_fruit(self): # Defining the function that spawns the fruit in-game.
        # Randomly spawn a new fruit at a random location within the screen bounds, notice the use of WIDTH, HEIGHT from settings.py
        # and how FRUIT_SIZE refers to 20 pixels above declared earlier in this module.
        x = random.randint(0, WIDTH - FRUIT_SIZE)
        y = random.randint(0, HEIGHT - FRUIT_SIZE)
        """# Adding the fruit to the game, into the the list of fruit_locations defined earlier in this module.
        with proper fruit size and random locations just defined above."""
        fruit_locations.append(pygame.Rect(x, y, FRUIT_SIZE, FRUIT_SIZE)) 
        
    """Draws the fruit onto the screen, as red, then breaks, so it won't draw them infinitely.
    note, this code isn't used in the game logic any more as the load(self) function replaced it
    but this draw_fruits function was essential to the game development for debugging, etc."""
    def draw_fruits(self):
        # Draw all the fruits
        for fruit in fruit_locations: #Goes through list of fruit locations, then draws a fruit.
            pygame.draw.rect(self.screen, RED, fruit)
            break # breaks the code after drawing a fruit to prevent the infinity loops.

    """This function, load(self) will draw the image as defined in self.image above using the png image file
    from the above code, from the graphics folder."""
    def load(self): # Defining the function.

        self.image = pygame.transform.scale(self.image, (30, 30)) # using pygame to scale the image into 30 by 30 pixels
        """iterating to the list of fruit locations as defined earlier as fruit_locations"""
        for fruit in fruit_locations:
            """Draws the fruit onto the screen"""
            screen.blit(self.image, fruit)
            """Breaks the code to prevent infinite replication of drawing fruits onto the screen like a virus."""
            break

    """Checks for if fruit is eaten or not, but this isn't used or fully defined as pacman.py defines this itself."""
    def check_for_eat(self, pos, pacman):
        # Create a rect for the click position
        new_rect = pygame.Rect(pos[0] - FRUIT_SIZE // 2, pos[1] - FRUIT_SIZE // 2, FRUIT_SIZE, FRUIT_SIZE)
        

        # Check if the click overlaps with any fruit rect
        for fruit in fruit_locations[:]:
            if new_rect.colliderect(fruit):  # If a collision is detected
                fruit_locations.remove(fruit)  # "Eat" the fruit
                self.spawn_fruit()  # Spawn a new fruit at a random location
                break  # Only eat one fruit per click

"""sets the initial location of god fruits class, as defined lower in this module."""
god_fruit_locations = [pygame.Rect(x, y, 20, 20) for x, y in [(500, 500)]]

"""Defining the class FruitsGod()"""
class FruitsGod(): # Defining the FruitsGod class
    def __init__(self): # Initalizes the FruitsGod object.
        self.screen = screen # Defines self.screen to screen, so once screen is called, it refers to this code.
        self.god_fruit_locations = []  # Initialize an empty list to hold fruit locations
        self.image = pygame.image.load("graphics/godfruit.png") #sets self.image as this particular png image file in the folder graphics
        #essentially setting the graphics for this fruit as a godfruit.png image whatever that may be.
        self.running = False # Allows for self execution of this code in this class, if needed, once it is called.
        self.timer = None # initializes as a timer as none, null or nothing, no timer exists yet but it is there.

    def spawn_fruit(self): # Spawn fruit function, spawns itself onto the screen.
        """Spawns the fruit at random locations at x, y cords using minus fruit size """
        x = random.randint(0, WIDTH - FRUIT_SIZE)
        y = random.randint(0, HEIGHT - FRUIT_SIZE)
        """appends the location of the fruit to god_fruit_locations, essentially adding it to the game or list"""
        god_fruit_locations.append(pygame.Rect(x, y, FRUIT_SIZE, FRUIT_SIZE))
        """Debugging console output"""
        print(f"Spawned fruit at {x}, {y} — total: {len(god_fruit_locations)}")

    """Function defines spawning schedule after initially spawning it."""
    def _spawn_and_schedule_next(self):
        """If self running = true, as defined earlier"""
        if self.running:
            """Spawns a god fruit looping back into the function spawn_fruit afterwards"""
            self.spawn_fruit()
            """starts a timer for the next god fruit spawn initation after looping from spawn_fruit function."""
            self.timer = threading.Timer(60, self._spawn_and_schedule_next) #timer is set, to spawn after 60 seconds
            """starts the timer above."""
            self.timer.start()

    """defines the timer function for god fruit spawn."""
    def start_fruit_timer(self):
        if not self.running: #if the self.running isn't enabled
            self.running = True # sets self.running to true so that spawn fruit loop is enabled as previously defined.
            """timer is set, to spawn after 60 seconds"""
            self.timer = threading.Timer(60, self._spawn_and_schedule_next)
            """starts the above code"""
            self.timer.start()
            print("Fruit timer started.") # console feedback.

    """defining a function to stop or cancel the timer for the god fruit respawn loop if wanted"""
    def stop_fruit_timer(self):
        self.running = False # the running self is disabled, therfore timer and respawn is disabled if function is called.
        if self.timer: # if timer is true
            self.timer.cancel() # if timer is true, cancels timer.
            print("Fruit timer stopped.") # console debugger output.

    """function to draw god fruit onto the screen as a blue circle, depreciated, load is the new function"""
    def draw_fruits(self): 
        # Draw all the fruits
        for fruit in god_fruit_locations: # iterates through god fruity location.
            pygame.draw.rect(self.screen, BLUE, fruit) # draws fruit on screen
            break #breaks infinity drawing loop.

    """Draws the god fruit onto the screen as an image later defined"""
    def load(self): # defining the function
        """setting the self.image to be drawn as a god fruit object on the screen as self.image defined
        earlier as a png image, and sets the size to 30 by 30 pixels using pygame.transform.scale."""
        self.image = pygame.transform.scale(self.image, (30, 30))  # can resize
        """Iterates through the god_fruit_locations list, which are locations for the god fruit to be drawn."""
        for fruit in god_fruit_locations:
            """drawing the actual god fruit on the screen"""
            screen.blit(self.image, fruit)
            break # preventing the infinity loop from continously drawing god fruits on the screen.

    """function to check if the god fruit is eaten, not used, it's defined in the pacman.py and pacman class instead."""
    def check_for_eat(self, pos, pacman):
        # Create a rect for the click position
        new_rect = pygame.Rect(pos[0] - FRUIT_SIZE // 2, pos[1] - FRUIT_SIZE // 2, FRUIT_SIZE, FRUIT_SIZE)
        
        # Check if the click overlaps with any fruit rect
        for fruit in god_fruit_locations[:]:
            if new_rect.colliderect(fruit):  # If a collision is detected
                god_fruit_locations.remove(fruit)  # "Eat" the fruit
                self.spawn_fruit()  # Spawn a new fruit at a random location
                break  # Only eat one fruit per click

