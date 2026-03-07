# **Lesson: Derived Classes and Inheritance with `super()` in Pac-Man**  

## **Lesson Objectives**  
By the end of this lesson, students should be able to:  
1. Understand **class inheritance** and how derived classes extend base classes.  
2. Use `super()` to call methods from the parent class.  
3. Apply these concepts in the **Pac-Man** game by creating a hierarchy of game objects.

---

## **1. Introduction to Inheritance**  

### **What is Inheritance?**  
Inheritance allows a class (**child/derived class**) to inherit attributes and methods from another class (**parent/base class**). This helps in:  
✅ Code reusability (avoid duplicate code)  
✅ Organization and structure in large programs  
✅ Extending existing functionality  

### **What is `super()`?**  
`super()` lets us call methods from the **parent class** inside a derived class. It is used to:  
✅ Initialize attributes of the parent class  
✅ Extend the behavior of inherited methods  

---

## **2. Using Inheritance in Pac-Man**  

### **Scenario**  
In **Pac-Man**, all characters (Pac-Man and Ghosts) share common attributes:  
- **Position (`x, y`)**  
- **Movement (`move()` method)**  

Instead of repeating this in multiple classes, we create a **base class `Character`** and make **Pac-Man and Ghosts inherit from it**.  

---

## **3. Implementing Inheritance in Pac-Man**  

### **Step 1: Create the Parent Class (`Character`)**  

The `Character` class will have:  
✔ A constructor (`__init__()`) to initialize `x, y` position.  
✔ A `move()` method (which will be overridden in child classes).  

```python
class Character:
    """Base class for all moving characters in Pac-Man."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Moves the character by dx, dy."""
        self.x += dx
        self.y += dy
        print(f"Character moves to ({self.x}, {self.y})")

    def draw(self):
        """Placeholder for drawing the character."""
        print(f"Drawing character at ({self.x}, {self.y})")
```

---

### **Step 2: Create the Derived Class for Pac-Man**  

Pac-Man **inherits** from `Character`, but has additional behavior.  
- We use `super().__init__(x, y)` to initialize the parent class.  
- We **override** `move()` to change how Pac-Man moves.  

```python
class PacMan(Character):
    def __init__(self, x, y, lives=3):
        super().__init__(x, y)  # Call Character's constructor
        self.lives = lives  # Additional attribute specific to Pac-Man

    def move(self, dx, dy):
        """Pac-Man moves in a controlled way."""
        super().move(dx, dy)  # Call the parent class move()
        print("Pac-Man is munching pellets!")

    def lose_life(self):
        """Reduces Pac-Man's lives when hit by a ghost."""
        if self.lives > 0:
            self.lives -= 1
            print(f"Pac-Man lost a life! Remaining lives: {self.lives}")
        else:
            print("Game Over!")
```

✔ **Pac-Man uses `super().move(dx, dy)`** to retain the base movement functionality.  
✔ **Adds a `lose_life()` method** unique to Pac-Man.  

---

### **Step 3: Create the Derived Class for Ghosts**  

Ghosts also **inherit** from `Character`, but:  
- They have **different colors**.  
- They **override `move()`** to include randomized AI behavior.  

```python
class Ghost(Character):
    def __init__(self, x, y, color):
        super().__init__(x, y)  # Call Character's constructor
        self.color = color

    def move(self, dx, dy):
        """Ghosts move unpredictably."""
        super().move(dx, dy)  # Keep base movement
        print(f"{self.color} Ghost is chasing Pac-Man!")

    def scare_mode(self):
        """Ghost enters scared mode after Pac-Man eats a power pellet."""
        print(f"{self.color} Ghost is now scared and running away!")
```

✔ **Ghosts use `super().move(dx, dy)`** but customize behavior.  
✔ **They have a special `scare_mode()` method** not available to Pac-Man.  

---

## **4. Testing the Inheritance Structure**  

Let's create a **Pac-Man and a Ghost**, move them, and test their methods.  

```python
# Create Pac-Man
pacman = PacMan(5, 5)
pacman.move(1, 0)  # Moves right
pacman.lose_life()

# Create a Ghost
blinky = Ghost(10, 10, "Red")
blinky.move(-1, 0)  # Moves left
blinky.scare_mode()
```

### **Expected Output**
```
Character moves to (6, 5)
Pac-Man is munching pellets!
Pac-Man lost a life! Remaining lives: 2
Character moves to (9, 10)
Red Ghost is chasing Pac-Man!
Red Ghost is now scared and running away!
```

✔ **Pac-Man and Ghosts inherit `move()` but modify behavior using `super()`**.  
✔ **Pac-Man has `lose_life()`, Ghosts have `scare_mode()`**.  

---

## **5. Summary of Key Takeaways**  
✅ **Inheritance allows code reuse** by defining a base class (`Character`).  
✅ **Derived classes (`PacMan`, `Ghost`) extend and modify behavior**.  
✅ **`super()` calls the parent class methods** for consistency.  

---

## **6. Complete Assignment  (Please refer to Brightspace)**  

### Assignment Overview  

✅ **Task 1:** Add a new class `Fruit`, inheriting from `Character`, but making it **stationary (no movement)**.  
✅ **Task 2:** Modify the `Ghost` class so different ghosts (Blinky, Pinky, Inky, Clyde) have unique movement strategies.

