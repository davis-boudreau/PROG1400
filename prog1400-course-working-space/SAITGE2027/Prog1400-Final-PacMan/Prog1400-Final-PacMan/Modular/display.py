"""
Student: Walker Gould
Student ID: W0403704
Instructor: Davis Boudreau
Course: PROG1400
Assignment: Final Project: Pac-Man Enhanced
Date: April 18th, 2025 - Friday
Term: 2nd Semester - Winter of 2025.

"""


"""Importing pygame module for pygame functionality since this is a video game."""
import pygame
"""Importing some settings from settings.py to use in this class or display.py module
includes settings like color, screen width and height and the screen it self
as a reference for the code written in this module, display.py."""
from settings import screen, BLUE, WIDTH, HEIGHT

"""Using pygame functionality to initalize the fonts to be displayed onto the screen
as written or defined in this module, per code written below, as needed."""
pygame.font.init()

"""Defining the class/object LivesLoader, it essentially functions to be called, by another class
in this case, it's called by the main game file called game.py which sort of as as a main.py
and will execute code to display fonts onto the screen as intended."""

class LivesLoader: # creating a class.
    def __init__(self): # Initalizes self as an object,
        pass

    def Livesloader(self, lives): #Defining a function for the LivesLoader class, the function is called LivesLoader, but could be called anything
        """Lives loader function has attributes called self and lives"""
        livesfont = pygame.font.SysFont('Arial', 15, bold=True) # Setting the font size, type and settings and setting them as bold.

        """rendering livesfont onto the screen and setting it as the variable 'lives_text_surface'
          rendering options are set, such as text color e.g white or 255,255,255
           bold = true, and the text 'pac-man lives:', and also renders 
          whatever was called as lives as {lives} onto the screen, in this case, its simply just 
          the amount of lives that pacman has left, which is the reason that this class was made in the first place."""
        lives_text_surface = livesfont.render(f'Pac-Man Lives: {lives}', True, (255, 255, 255)) 
        """draws the text onto the screen, that was just rendered, starting on the screen position 10 and 575 for x,y positions
        of the 600x600 pixel screen."""
        screen.blit(lives_text_surface, (10, 575))



"""This defines a score loader class, which is similar to the class livesLoader, it displays
the pacman's score on the screen, albeit with very slight differences as required to make it work. 
It will essentially function in almost the same exact way with slight differences to make it more specific for
the current score of pacman instead of pacman's live in reference to the livesloader class."""

class ScoreLoader: # Class name
    def __init__(self): # initalize self as an object
        pass

        """Creating a ScoreLoader function, it doesn't have to be the same as the class name but I made it that way anyways
        It's similar to the LiveLoaders class and function but for the scores of pacman instead of the pacmans lives."""
    def ScoreLoader(self, score): # Defines a score
        """Setting the variable scorefont as the font for pygame, using font type, size, bold, etc"""
        scorefont = pygame.font.SysFont('Arial', 15, bold=True)
        """Setting the variable score_text_surface as the whatever is rendered in the variable scorefont using .render
        What is being rendered is the font type, size, bold = true, etc defined in scorefont
        and then rendering additional things, such as the text 'Score: and {score} which is whatever is
        passed into the ScoreLoader(self, score) function, score parameter which is simply pacman's score, in this case.
        bold is true and the font color is 255,255,255 rgb which is white. I probably could of passed settings
        from settings.py but I didn't think of this as of until writing this."""
        score_text_surface = scorefont.render(f'Score: {score}', True, (255, 255, 255))
        """Drawing the text that was just rendered and set as variable score_text_surface onto the screen
        at the position of x, y 120, 575 onto the screen."""
        screen.blit(score_text_surface, (120, 575))

    """Defining another function inside the ScoreLoader class, this isn't referring to ScoreLoader function directly. Just
    to add some clarity, hopefully.
    The function we are now defining is now called 'ScoreRecord' with parameters (self, score): 
    This function is simply to display different outputs or messages to the player/user depending on the score
    that they had when they lost the game or died too many times, e.g no pacman lives left.
    It sort of gives you feedback of how your score was in a humorous way."""
    
    def ScoreRecord(self, score): # Defining the function.
        """If your score is less than 100 when you lose the game, the game screen display will display the message of
        you lost the game score of whatever is less than or equal to 100."""
        if score <= 100:
            """Prepping the font to be displayed based on font type, size, bold, etc for the font/message to be displayed to the screen.
            as scorefont"""
            scorefont = pygame.font.SysFont('Arial', 15, bold=True)
            """Setting variable score_text_surface as the rendered scorefont, as just previously defined.
            This includes things like additional text, e.g 'You lost the game with a score of:, {score} which
            is whatever we passed into the function ScoreRecord(self, score): score part of the function
            in this case, it's simply the current score of Pac Man when he lost the game or ran out of lives
            Bold equals true, the font color is 255,255,255 which is white in RGB."""
            score_text_surface = scorefont.render(f'You lost the game with a score of: {score}', True, (255, 255, 255))
            """Draw the rendered text onto the screen, e.g score_text_surface, onto the screen at x,y position
            using WIDTH and HEIGHT settings from settings.py, which are 600 and 600 pixels each respectively.
            however we are dividing WIDTH by 4 using WIDTH/4, and HEIGHT by HEIGHT/1.8, this is
            to align the text properly onto the screen, at the position we want, the width and height
            settings are for more universal use, e.g on different pixel sized screens, for eaxmple."""
            screen.blit(score_text_surface, (WIDTH/4, HEIGHT/1.8))

            """"This is exactly the same logic as above, with slight differences, but it should be self explanatory at this point.
            If pacman's score is between 100 and 500 then the screen will display this message instead of the above message"""
        if score >= 100 and score < 500:
            scorefont = pygame.font.SysFont('Arial', 15, bold=True)
            score_text_surface = scorefont.render(f'You lost the game with a score of: {score} which is pretty good, man.', True, (255, 255, 255))
            screen.blit(score_text_surface, (WIDTH/4.8, HEIGHT/1.8))

            scorerfont = pygame.font.SysFont('Arial', 15, bold=True) # additonal message displayed to score, depending on pacman score
            scorer_text_surface = scorerfont.render(f'I seen better, though...', True, (255, 255, 255))
            screen.blit(scorer_text_surface, (WIDTH/4, HEIGHT/1.6))



            """"This is exactly the same logic as above, with slight differences, but it should be self explanatory at this point.
            If pacman's score is between 500 and 1000 then the screen will display this message instead of the above message"""

        if score >= 500 and score < 1000:
            scorefont = pygame.font.SysFont('Arial', 15, bold=True)
            score_text_surface = scorefont.render(f'You lost the game with a score of: {score}', True, (255, 255, 255))

            screen.blit(score_text_surface, (WIDTH/4, HEIGHT/1.8))

            scorerfont = pygame.font.SysFont('Arial', 15, bold=True) # Font types, etc

            """# additonal message displayed to score, depending on pacman score"""
            scorer_text_surface = scorerfont.render(f'You are an absolute G.O.D!', True, (255, 255, 255))
            screen.blit(scorer_text_surface, (WIDTH/4, HEIGHT/1.6)) # position of text displayed on screen

            """"This is exactly the same logic as above, with slight differences, but it should be self explanatory at this point.
            If pacman's score is between 1000 and 5000 then the screen will display this message instead of the above message
            the logic/code below will be exactly the same as the above logicistics, only with increasing amount of messages
            displayed to the user and different messages. However all the principles are the exact same."""

        if score >= 1000 and score < 5000:
            scorefont = pygame.font.SysFont('Arial', 15, bold=True)
            score_text_surface = scorefont.render(f'I hate to say, You lost the game with a score of: {score}', True, (255, 255, 255))
            screen.blit(score_text_surface, (WIDTH/4, HEIGHT/1.8))

            scorerfont = pygame.font.SysFont('Arial', 15, bold=True)
            scorer_text_surface = scorerfont.render(f'This is absolutely ridiculous.', True, (255, 255, 255))
            screen.blit(scorer_text_surface, (WIDTH/4, HEIGHT/1.6))

            scorer2font = pygame.font.SysFont('Arial', 15, bold=True)
            scorer2_text_surface = scorer2font.render(f'Have you ever considered going outside in real life?', True, (255, 255, 255))
            screen.blit(scorer2_text_surface, (WIDTH/4, HEIGHT/1.4))

            """"This is exactly the same logic as above, with slight differences, but it should be self explanatory at this point.
            If pacman's score is between 5000 and 10000 then the screen will display this message instead of the above message"""

        if score >= 5000 and score < 10000:
            scorefont = pygame.font.SysFont('Arial', 15, bold=True)
            score_text_surface = scorefont.render(f'I hate to say, You lost the game with a score of: {score}', True, (255, 255, 255))
            screen.blit(score_text_surface, (WIDTH/4, HEIGHT/1.8))
            
            scorerfont = pygame.font.SysFont('Arial', 15, bold=True)
            scorer_text_surface = scorerfont.render(f'You are insane...', True, (255, 255, 255))
            screen.blit(scorer_text_surface, (WIDTH/4, HEIGHT/1.6))

            scorer2font = pygame.font.SysFont('Arial', 15, bold=True)
            scorer2_text_surface = scorer2font.render(f'Go outside, right now. I do not care.', True, (255, 255, 255))
            screen.blit(scorer2_text_surface, (WIDTH/4, HEIGHT/1.4))

            """"This is exactly the same logic as above, with slight differences, but it should be self explanatory at this point.
            If pacman's score is greater or equal to 10000 then the screen will display this message instead of the above message
            This is technicially the point of which you have 'won' or finished the game and the BSOD message as later defined below,
            will be removed. This message means you won the game... The video game that is, not anything else."""

        if score >= 10000: # You won the fricking game at this point if your score is greater than 10000.
            scorefont = pygame.font.SysFont('Arial', 15, bold=True) # Font types, etc
            score_text_surface = scorefont.render(f'You won the game with a of {score}', True, (255, 255, 255)) # different message
            # than lower scores.
            screen.blit(score_text_surface, (WIDTH/4, HEIGHT/1.8)) # position of text displayed on screen

            scorerfont = pygame.font.SysFont('Arial', 15, bold=True) # Font types, etc
            scorer_text_surface = scorerfont.render(f'You arent right in the head. Go outside', True, (255, 255, 255)) # different message
            # than lower scores
            # .
            screen.blit(scorer_text_surface, (WIDTH/4, HEIGHT/1.6))  # position of text displayed on screen

            scorer2font = pygame.font.SysFont('Arial', 15, bold=True)  # Font types, etc
            """different message than lower scores"""
            scorer2_text_surface = scorer2font.render(f'Go outside, you won! okay? uninstall this game too.', True, (255, 255, 255))

            screen.blit(scorer2_text_surface, (WIDTH/4, HEIGHT/1.4))  # position of text displayed on screen

            scorer2font = pygame.font.SysFont('Arial', 15, bold=True)  # Font types, etc
            scorer2_text_surface = scorer2font.render(f'Go outside, you won! okay? uninstall this game too.', True, (255, 255, 255))
            screen.blit(scorer2_text_surface, (WIDTH/4, HEIGHT/1.4)) # position of text displayed on screen

            scorewonfont = pygame.font.SysFont('Arial', 15, bold=True)  # Font types, etc

            """different message than lower scores, this one below crosses out the you lose message from the BSOD function and class
            defined later in this class. This only means that you have won the game.
            notice this text is rendered at the same place as the BSOD class function position, it essentially
            crosses the message out, indicating to the player that they won the game."""
            scorewon_text_surface = scorewonfont.render(f'-------------------------------------------------------------------------', True, (255, 255, 255))
            screen.blit(scorewon_text_surface, (WIDTH/4, HEIGHT/2))  # position of text displayed on screen
            

"""Defining a new class in this display.py module. This is a message that is displayed once pacman runs out of lives."""
class BSOD: # Class name
    def __init__(self): # Initalizes BSOD as an object.
        pass
    def BlueScreenOfDeath(self): # Defining a function inside the class BSOD, this function is called BlueScreenOfDeath, referring to self.
        """Fills the screen, the background as all the colored BLUE."""
        screen.fill(BLUE)
        """Starting to render the text to be displayed to the screen with parameters, font type, size, bold = true, etc"""
        BSODfont = pygame.font.SysFont('Arial', 15, bold=True)
        """setting BSOD_text_surface as the rendered version of the above code, BSODfont with additional values
        such as color, etc."""
        BSOD_text_surface = BSODfont.render(f'Blue screen of death: You lost the game, LOSER!', True, (255, 255, 255))
        """Drawing the rendered text onto the screen at screen positions for x, y at WIDTH/4 and HEIGHT/2
        or Width divided by 4 and height divided by 2."""
        screen.blit(BSOD_text_surface, (WIDTH/4, HEIGHT/2))

