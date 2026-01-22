## PROG 1400 Final Project: Pac-Man Enhanced

**Objective:**

This assignment challenges you to significantly enhance the provided "pacman starter" project, transforming it into a fully functional and engaging Pac-Man game. You will demonstrate your mastery of Python's object-oriented programming (OOP) principles, library integration, and **thorough code documentation**.

**Starter Code Overview:**

The provided "pacman starter" code provides a foundational structure for a Pac-Man game, including:

* **Pygame Initialization:** Sets up the Pygame library for graphics and input handling.
* **Screen and Clock:** Defines the game window and a clock for frame rate control.
* **Color Definitions:** Establishes color constants for use in drawing.
* **Maze Representation:** Uses a list of `pygame.Rect` objects to define the maze walls.
* **`PacMan` Class:**
    * Contains methods for moving Pac-Man, tracking its position, and drawing it.
    * Includes collision detection with maze walls.
    * Adds a history attribute to keep track of the pacman's movements.
* **`Ghost` Class:**
    * Contains methods for moving the ghost towards Pac-Man and avoiding maze walls.
    * Implements a basic chasing algorithm and wall-following behavior.
    * Allows for color definition.
* **Input Handling:** A function to process keyboard input for Pac-Man's movement.
* **Collision Detection:** A function to check for collisions between Pac-Man and the ghost.
* **Game Loop:** Manages the game's main execution cycle.

**Task Requirements:**

1.  **Pellets:**
    * Implement pellets (small circles) that Pac-Man can eat.
    * Store pellet locations using a list or set.
    * Remove pellets when Pac-Man collides with them.
    * Utilize class-based object creation for the pellet.
    * **Document all code within the pellet module using clear and concise comments.**

2.  **Fruit (Cherry):**
    * Introduce a cherry (or another fruit) that appears randomly on the screen.
    * Implement a scoring system that awards more points for eating the cherry than pellets.
    * Utilize class-based object creation for the fruit.
    * **Document all code within the fruit module using clear and concise comments.**

3.  **Score Keeping:**
    * Display the player's score on the screen.
    * Update the score when Pac-Man eats pellets and the cherry.
    * Use a font to display the score.
    * **Document all scoring related code within the game logic and display modules.**

4.  **Additional Ghosts (Pinky, Inky, Clyde, Blinky):**
    * Expand the ghost population to include Pinky (pink), Inky (cyan), Clyde (orange), and retain Blinky (red, already partially implemented).
    * Utilize inheritance to create these ghost classes, derived from the base `Ghost` class. This allows for code reuse while enabling specific behaviors for each ghost.
    * **Blinky (Red):**
        * Retain or refine the existing aggressive chasing algorithm, possibly incorporating speed increases as the game progresses.
    * **Pinky (Pink):**
        * Implement a behavior where Pinky attempts to move to a position four tiles ahead of Pac-Man's current direction. This requires tracking Pac-Man's movement history and predicting its future location.
    * **Inky (Cyan):**
        * Implement a behavior that combines Blinky's and Pinky's positions. Inky's target position should be calculated as a reflection of Blinky's position relative to Pinky's. This requires more complex coordinate calculations.
    * **Clyde (Orange):**
        * Implement a behavior where Clyde chases Pac-Man when far away but switches to a scatter mode (moving to a specific corner) when close. This requires distance calculations and state management.
    * **Color Implementation:**
        * Ensure each ghost is rendered with its correct color (red, pink, cyan, orange).
    * **Ghost AI Complexity:**
        * Consider using vectors or pathfinding algorithms (e.g., A\*) for more sophisticated movement.
        * Implement different ghost behaviors based on game state (e.g., "scatter" mode, "chase" mode, "frightened" mode - if you wish to expand the game further).
        * Use timers or counters to switch between different ghost modes.
        * Consider adding ghost collision detection with other ghosts.
    * **Document all Ghost behaviour code within the ghost module using clear and concise comments.**

5.  **Icons:**
    * Replace the simple circles for Pac-Man and the ghosts with image icons.
    * Use images for pellets and the cherry.
    * Use the pygame image loading functionality.
    * **Document how images are loaded and used within the display module.**

6.  **Lives System:**
    * Implement a lives system, giving Pac-Man three attempts before the game ends.
    * Display the number of remaining lives on the screen.
    * When the PacMan collides with a ghost, decrease the lives counter, and reset the PacMan and Ghost positions.
    * **Document the lives system logic within the game logic and display modules.**

7.  **Modularization:**
    * Divide the code into multiple modules (e.g., `game.py`, `fruits.py`, `pellets.py`, `main.py`, `pacman.py`, `ghosts.py`, `display.py`).
    * Organize classes and functions logically across these modules.
    * **Document the purpose and interactions between each module.**

8.  **Documentation:**
    * **Document ALL aspects of your code using comments.** Explain the purpose of classes, methods, variables, and algorithms.
    * Use docstrings to describe the functionality of functions and classes.

9.  **OOP Principles:**
    * **Control Structures:** Use `if/else`, `for`, and `while` loops to manage game logic.
    * **Modular Programming:** Divide the project into modules.
    * **Variables, Data Types, and Scope:** Use appropriate data types and manage variable scope effectively.
    * **Basic Inheritance:** Create subclasses for different ghost behaviors.
    * **Encapsulation:** Use attributes, methods, and access control to protect data.
    * **Polymorphism:** Override methods in subclasses to implement different behaviors.
    * **Python's OOP Paradigm:** Utilize classes and objects to structure the game.
    * **Abstract Classes and Methods (Optional):** Consider using abstract classes for common behaviors.
    * **Collections:** Use lists, dictionaries, or sets to store game data (e.g., pellet locations, ghost positions).
    * **Library Integration:** Use the Pygame library effectively.

**Recommended Approaches:**

* **Modular Design:** Plan your modules before coding.
* **Class Design:** Create classes for game objects (Pac-Man, Ghost, Pellet, Fruit) to encapsulate their behavior and attributes.
* **Collision Detection:** Use `pygame.Rect.colliderect()` for efficient collision detection.
* **Scoring:** Use a variable to track the score and display it using `pygame.font`.
* **Lives:** Manage lives using a counter and display it using `pygame.font`.
* **Image Loading:** Use `pygame.image.load()` to load image files for icons.
* **Ghost AI:** Start with simple chasing algorithms and gradually increase complexity.
* **Testing:** Test your code incrementally to ensure each feature works correctly.
* **Document as you go:** Document each function and class as it is created.

**Evaluation:**

Your assignment will be evaluated based on:

* **Correct implementation of all features (33%).**
* **Effective use of OOP principles (20%).**
* **Code modularity and organization (14%).**
* **Code readability and thorough documentation using comments (33%).**
* **Game functionality and playability (10%).**

**Final Statement:**

This assignment is designed to provide you with a comprehensive opportunity to demonstrate your understanding of Python OOP and game development. Pay close attention to documenting your code thoroughly, as this will be a significant portion of your grade. Remember that clear and well-documented code is essential for maintainability and collaboration.

Please feel free to reach out to your instructor if you have any questions or require assistance. Good luck!
