"""
Student-level solution (simplified):
- Focus: translate UML -> Python classes
- No abstract base classes, no typing imports
- Method bodies are stubs (pass)
"""

# ---------------------------
# Pellet
# ---------------------------
class Pellet:
    def __init__(self, position, value):
        self.position = position
        self.value = value


# ---------------------------
# Maze
# ---------------------------
class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pellets = []

    def load_maze(self):
        pass


# ---------------------------
# Entity (parent class)
# ---------------------------
class Entity:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def move(self):
        pass


# ---------------------------
# Pacman (inherits from Entity)
# ---------------------------
class Pacman(Entity):
    def __init__(self, position):
        super().__init__("Pacman", position)
        self.direction = "RIGHT"

    def move(self):
        pass

    def eat_pellet(self):
        pass


# ---------------------------
# Ghost (inherits from Entity)
# ---------------------------
class Ghost(Entity):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.state = "CHASE"

    def move(self):
        pass

    def chase(self):
        pass


# ---------------------------
# Game
# ---------------------------
class Game:
    def __init__(self, maze, pacman, ghosts):
        self.maze = maze
        self.pacman = pacman
        self.ghosts = ghosts
        self.score = 0
        self.lives = 3

    def start_game(self):
        pass

    def update(self):
        pass


# ---------------------------
# Tiny sanity check (optional)
# ---------------------------
if __name__ == "__main__":
    maze = Maze(10, 10)
    pacman = Pacman((1, 1))
    ghosts = [Ghost("Blinky", (5, 5)), Ghost("Pinky", (6, 5))]
    game = Game(maze, pacman, ghosts)

    print("OK: Classes created.")
    print("Maze:", maze.width, "x", maze.height)
    print("Pacman:", pacman.name, pacman.position, pacman.direction)
    print("Ghosts:", [g.name for g in ghosts])
    print("Game score/lives:", game.score, game.lives)