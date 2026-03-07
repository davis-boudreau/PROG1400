**Abstract Classes and Methods in Python using the `abc` module**, with a **Pac-Man** game context.

---

# **Lesson: Abstract Classes and Methods in Pac-Man (Using `abc` Module)**  

## **Lesson Objectives**  
By the end of this lesson, students should be able to:  
1. Understand the concept of **abstract classes and methods**.  
2. Use Python’s `abc` module to define abstract classes.  
3. Implement concrete subclasses that inherit from an abstract class.  
4. Apply these concepts in the **Pac-Man game**, defining abstract behaviors for different game entities.

---

## **1. Introduction to Abstract Classes**  

### **What is an Abstract Class?**  
An **abstract class** is a blueprint for other classes. It:  
✅ **Cannot be instantiated** (i.e., you cannot create objects from it directly).  
✅ **Defines abstract methods** that must be implemented by subclasses.  

We use the **`abc` (Abstract Base Class) module** in Python to define abstract classes and methods.  

---

## **2. Using Abstract Classes in Pac-Man**  

In **Pac-Man**, different game entities share common behaviors:  

- **Pac-Man and Ghosts move**, but they move differently.  
- **Ghosts have different AI behaviors**, but they all need an update mechanism.  
- **All game objects should be able to draw themselves on the screen**.  

We will use an **abstract class `GameObject`** as a base class for all game objects.  

---

### **3. Implementing Abstract Classes in Pac-Man**  

### **Step 1: Define an Abstract Base Class**
We will define an **abstract class** `GameObject` with two abstract methods:  
- `move()`: Defines how an object moves.  
- `draw()`: Defines how an object is rendered.  

```python
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
```

👉 **Why `@abstractmethod`?**  
It forces subclasses to implement `move()` and `draw()`.

---

### **Step 2: Create a Concrete Subclass for Pac-Man**  
Now, we define `PacMan`, inheriting from `GameObject`, and implement the required methods:

```python
class PacMan(GameObject):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        print(f"Pac-Man moves to a new position: ({self.x}, {self.y})")

    def draw(self):
        print("Drawing Pac-Man at position:", self.x, self.y)

# Example usage
pacman = PacMan(5, 5)
pacman.move()
pacman.draw()
```

✔️ **Now `PacMan` can be instantiated** because it implements all abstract methods.

---

### **Step 3: Create Concrete Subclasses for Ghosts**  
Ghosts move differently, so we create a `Ghost` class:

```python
class Ghost(GameObject):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self):
        print(f"{self.color} Ghost moves unpredictably to ({self.x}, {self.y})")

    def draw(self):
        print(f"Drawing {self.color} Ghost at position: ({self.x}, {self.y})")

# Example usage
blinky = Ghost(10, 10, "Red")
blinky.move()
blinky.draw()
```

✔️ **Each ghost has unique behavior but follows the abstract class structure.**

---

### **Step 4: Testing the Abstract Class Restrictions**  

What happens if we try to instantiate `GameObject` directly?  

```python
obj = GameObject()  # ❌ Error! Cannot instantiate abstract class
```

---

## **4. Summary of Key Takeaways**  
✔ **Abstract classes provide a blueprint** for shared functionality.  
✔ **Subclasses must implement abstract methods** from the base class.  
✔ **We used `GameObject` as an abstract class** for `PacMan` and `Ghost`.  
✔ **Attempting to instantiate an abstract class results in an error**.  

---

## **5. Complete Assignment  (Please refer to Brightspace)**  

### Assignment Overview
✅ **Task 1:** Create a new class `Fruit` (e.g., cherries or power pellets) that inherits from `GameObject`.  
✅ **Task 2:** Modify the `Ghost` class so that different ghosts (Blinky, Pinky, Inky, Clyde) have slightly different move behaviors.