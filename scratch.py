from abc import ABC, abstractmethod

class GameObject(ABC):
    """Abstract base class for all game objects in Pac-Man."""

    @abstractmethod
    def move(self):
        """Defines movement behavior."""
        pass

    @abstractmethod
    def draw(self):
        """Defines how the object is drawn on the screen."""
        pass

class PacMan(GameObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        print(f"Pac-Man moves to a new position: ({self.x}, {self.y})")

    def draw(self):
        print("Drawing Pac-Man at position:", (self.x, self.y))

# Example usage
pacman = PacMan(5, 5)
pacman.move()
pacman.draw()