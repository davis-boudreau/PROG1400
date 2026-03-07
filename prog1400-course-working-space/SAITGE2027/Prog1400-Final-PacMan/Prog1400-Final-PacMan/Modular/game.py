"""
Student: Walker Gould
Student ID: W0403704
Instructor: Davis Boudreau
Course: PROG1400
Assignment: Final Project: Pac-Man Enhanced
Date: April 18th, 2025 - Friday
Term: 2nd Semester - Winter of 2025.

"""


#Importing pygame and other classes/objects and their attributes importing settings/variables.

import pygame
from pacman import PacMan
from ghost import Ghost, Blinky, Clyde, Pinky, Inky
from maze import draw_maze
from settings import RED, BLACK, WHITE, screen, clock, ORANGE, PINK, CYAN
from handle_input import handle_input
from check_collision import check_collision
from pellets import Pellets
from fruit import FruitDrawer, FruitsGod
from display import LivesLoader, ScoreLoader, BSOD

"""
# Game.py 
# This is the main class where the game loop is running and where all objects are instantiated.

# Initialize pygame
pygame.init()
"""



"""
# Initialize game objects and instantiate objects from other classes.
# Assigning variables to objects.
"""

#Note: Most of the code in this class will be called from other classes, as defined in the top of the page.

""" This game.py file is mostly just to instantiate different classes and objects
# and is sort of a main hub for interactions/meshing with other objects by calling functions from those objects.
# and it's also a game loop, so the game loops and runs continously."""

pacman = PacMan(300, 300)
ghost = Ghost(100, 100, RED)
pellet = Pellets(200, 200, WHITE)
fruits = FruitDrawer()
lives = LivesLoader()
score = ScoreLoader()
blinky = Blinky(500, 500, RED)
clyde = Clyde(100, 500, ORANGE)
pinky = Pinky(600, 100, PINK)
inky = Inky(600, 600, CYAN)
screendeath = BSOD()
godfruit = FruitsGod()

# Game is running equals true
running = True
# While running = true the game loop keeps going.
while running:
    #Back ground color
    screen.fill(BLACK)
        #Exit the loop if running = false
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input for Pacman from handle_input.py class.
    handle_input(pacman)

   # Loading objects into the game and calling class function to draw ghost images.
    blinky.load()
    clyde.load()
    inky.load()
    pinky.load()
    pacman.load()
    pellet.load()
    fruits.load()
    godfruit.load()
    ghost.load()

    # Drawing the maze onto the screen defined by maze.py class.
    draw_maze()

    #Calling ghost classes and ghost subclasses behaviors from ghost.py class
    ghost.move_towards(pacman)
    blinky.move_towards(pacman)
    clyde.chase_pacman(pacman)
    blinky.speed_increase(pacman)

    #Switching clydes behavior for chasing pacman
    clyde.update(pacman)

    # Switching Pinky into their behavior and method of chasing Pac Man.
    pinky.updatecords(pacman)

    """# Calling the functions needed to initiate Inky's chasing behavior
    # based off of blinkys position, using a similar method to Pinky's chase behavior."""
    inky_target = inky.calculate_inky_target(pacman, blinky)
    inky.move_toward(inky_target)

    #Making pacmans position a vector for Inky so Inky can chase properly.
    pacman.position = pygame.Vector2(pacman.x, pacman.y)

    # Starts the timer to respawn a god fruit, so that it doesn't immediately respawn after eating it.
    godfruit.start_fruit_timer()

    # Spawns fruit into the game.
    fruits.spawn_fruit()

    # Loading the display from display.py to show pacman's score and lives on the screen
    lives.Livesloader(pacman.lives)
    score.ScoreLoader(pacman.score)

    ### Making a list of the ghost variables for each ghost so that it's iterable and behaviors can be adjusted as needed.
    ghosts = [ghost, clyde, pinky, blinky, inky]


    """############## Defining pacman collisions with ghosts if he can't eat ghost
    ############## I made this algorithm myself."""

    if pacman.eatghost == False:  ### Algorithm made by Walker Gould.
        # Checks for collision if eatghost = false
        if check_collision(pacman, ghost, blinky, pinky, clyde, inky):
            ###console feedback
            print("You got hit by a GHOST")
            """
            # Takes the ghost list I made earlier in this file and uses the ghost function from the ghost class
            # to reset all the ghost to their original position after pacman is eaten by the ghost."""
            ghost.reset_all_ghosts(blinky, pinky, clyde, inky)
            

            """
            ## This is defined in the pacman.py class referring to 'pacman.lifetaker()'
            ## It resets Pacman's position after being eaten, takes a life off his lives.
            ## Resets any sort of speed boost and self images from interacting with other game objects
            ## It's basically a total reset and clean state of the original pacman..
            ## It had some console output as well for the game development.
            """
            pacman.lifetaker()

            # Flashes the screen read quickly so that there's an interactive effect of being eaten/damaged
            screen.fill(RED)

            # This is executed if Pacman has no lives left, it will end the game usiung the code that follows it.
            if pacman.lives <= 0:

                # Creates a blue screen of death on the screen after losing the game, e.g no lives left.
                screendeath.BlueScreenOfDeath()

                """
                # Shows the final score you had before you died, on the screen.
                # and will display different messages depending on your score."""
                score.ScoreRecord(pacman.score)


                # Update display for the previous code above for display fonts, visual effects, etc. in this case death.
                pygame.display.flip()


                """
                # This is to create a constant collision between the pacman and ghost
                # because this code is called under if there's a collision, so therefore
                # to keep displaying the screen with the code defined above, e.g screendeath and score record
                # I set pacman position to ghost position so that there's a
                    perpetual collision between pacman and ghost that keeps the code in effect or active.
                    """
                pacman.x = ghost.x
                pacman.y = ghost.y

                """
                # Waits 25 seconds before executing 'running = false' or exiting the game.
                # gives time for the player to read the messages and see the display after losing the game."""

                pygame.time.wait(25000)

                ##### Exits the game, since pacman has no lives left.
                running = False


    """####### Note: I made this algorithm myself.

    # If pacman can eat ghost as defined in the pacman.py class as true or false. 
    # This is set to true after Pacman eats the god fruit inside pacman.py and therefore can eat ghost at this time.
    #  and is later reset in the pacman.py class back to false
    # so that he can be eaten by ghost again, after the boost is over."""
    if pacman.eatghost == True: ### Algorithm made by Walker Gould

        ###iterates through the list of ghost
        for ghosts in ghosts:
            """
            # same thing as earlier, if pacman can eat ghost, the first one was more so that the game would catch the 
            # if statement and then I could iterate into the ghost and then define another if statement
            # which happens to be the same if statement in this code."""

            if pacman.eatghost == True:

                """
                # From the list of ghosts, the scared switch function is intiated (from ghost.py class)
                # referring to the code below, ghosts.scaredswitch(pacman)
                # Its' based off of pacman.eatghost being true or not
                # if it's true then the ghost will be scared of Pacman.
                # It's tied into pacman eating the god fruit in the pacman.py class.
                # Pacman is able to eat ghost while the boost from the god fruit is active."""
                
                ghosts.scaredswitch(pacman) # Ghost switching behavior based off of pacman eating a god fruit.
                """
                # Note: With the ghost being scared of pacman after the behavior switch, the ghost's speed increases, which needs
                # to be reset later back to normal, the scatter mode increases ghost speed
                # But this will be reset later using another true/false statement in a another if statement below somewhere.
                # This one will be called 'ghostplan' or 'pacman.ghostplan'"""


                """
                # This interacts with only live ghost, checks for collision between pacman and ghost
                # if this happens while pacman can eat ghost, the ghost will be eaten and will die."""
                if check_collision(pacman, ghosts):  
                    """
                    # After collision is checked and pacman eats a ghost, the ghost will 'die' as defined
                    # in the ghost.py class. This will reset the ghost to it's original position
                    # set the ghost.dead to true, set the ghost speed to 0 so that it cant move
                    # so that the ghost that is dead won't move or interact with Pac Man.
                    # and then it activates another ghost.py function with a timer for it the ghost to be revived
                    # after a certain amount of time."""
                    ghosts.died() #initates the dead sequence and revival sequence in ghost.py.

    """
    ######## Note: I made this algorithm myself.
    # This ties into the code above that starts with "if pacman.eatghost == True:"
    # It's so that once pacman effect of eating a god fruit resets and he can't
    # eat ghost any more, that the ghost speed will go back to normal.
    #
    # pacman.ghostplan starts off as 'false' in the pacman class/object and
    # switches to 'true' once a god fruit is eaten
    #
    # and then it switches back to false once the god fruit is eaten and the effects are over, it switches back to TRUE
    # 
    # so that the command won't be continously executed 
    # and that the speed reset back to 'normal' isn't permanent
    #
    # This means that the ghost will resume their normal behaviors outside of this code.
    # True essentially means it's not doing anything or being executed.
    # ghost plan = false (what it starts out as, list is iterated through)"""
    if pacman.ghostplan == False:
        #iterates through the list of ghost
        for ghosts in ghosts:
            # Checks if ghost.plan is false for pacman. (defined in  pacman.py)
            if pacman.ghostplan == False:
                """
                # resets the ghost speed back to normal (iterates through ghost list)
                # executes god function from ghost.py ghost class/object (speed reset)"""
                ghost.god(blinky, pinky, clyde, inky)
                """
                # Resets pacman.ghostplan to true in pacman.py
                # this essentially makes pacman.ghostplan inactive
                # so that it won't affect the normal behaviors of ghost. and they won't get speed reductions, etc.
                # The true does nothing, so it essentially acts as an off/on switch."""
                pacman.ghostplan = True


    # Update display
    pygame.display.flip()
    # Tick rate for the game.
    clock.tick(30)
# Quit the game.
pygame.quit()
