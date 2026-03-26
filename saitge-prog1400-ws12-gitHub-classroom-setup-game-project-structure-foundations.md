# PROG1400 Workshop 08

## Workshop Title: GitHub Classroom Setup and Pac-Man Project Structure Foundations

**Course:** PROG1400 – Introduction to Object-Oriented Programming
**Workshop Type:** Guided Setup and Project Foundation Lab
**Estimated Time:** 2–3 hours
**Delivery Mode:** In-class / Lab
**Prerequisites:** Basic VS Code use, introductory Git/GitHub awareness, Python fundamentals
**Due Date:** See Brightspace
**Related Learning Outcomes:**

* **LO2** Implement object-oriented design principles through class-based program structure
* **LO3** Manage and distribute code using Git and GitHub
* **LO4** Develop software models and connect design ideas to implementation
* **LO1** Describe applications using core OOP principles through analysis of an existing model

---

# 1. Workshop Overview

In this workshop, students will set up their **GitHub Classroom repository**, connect it to **VS Code**, and build the initial directory and file structure for their **Pac-Man-like game project**.

This workshop is about creating a **professional project foundation**. Before students begin building gameplay, movement, levels, or object interactions, they must organize their project properly. A well-structured project helps students:

* keep code readable and maintainable
* separate responsibilities across files
* prepare for future features such as level loading, utilities, models, and score management
* connect UML and design thinking to actual Python code

Once the structure is created, students will review and analyze an existing `models.py` example provided by the instructor. Students will use that file as a **reference model**, not something to copy blindly. The goal is to observe how a larger object-oriented game model is organized so they can begin designing their own version.

---

# 2. Workshop Purpose

The purpose of this lab is to help students establish the technical and conceptual starting point for their game project.

By the end of this workshop, students should have:

* accepted or opened their instructor-provided GitHub Classroom repository
* cloned the repository to their computer using VS Code
* created the required folders and files for the project
* added clear file header comments to each file
* created starter level files for `level1.txt` and `level2.txt`
* committed and pushed their setup to GitHub
* analyzed the provided `models.py` file and identified key classes, relationships, and design ideas

---

# 3. Learning Objectives

By the end of this workshop, students will be able to:

* connect a GitHub Classroom repository to their local development environment
* create a logical Python project structure for a game
* organize files and folders for future development
* document files with purpose statements
* interpret an existing object-oriented model as a guide for their own project
* identify key game classes such as `Game`, `Maze`, `Pacman`, `Ghost`, and `Item`
* recognize how a project can be split into multiple modules such as `models.py`, `loader.py`, and `util.py`

---

# 4. Scenario

You are beginning development of your own Pac-Man-like game. Before adding gameplay logic, you must create a clean development environment and a proper project structure.

Your instructor has already created a **GitHub Classroom repository** for you. You must connect to it, prepare your directory structure, and review a sample `models.py` file that demonstrates how an object-oriented game design can be organized.

Think of this workshop as building the **foundation of a house**. If the project structure is messy or incomplete, future development becomes confusing and difficult. If the structure is clean and intentional, your game will be easier to build, test, explain, and improve.

---

# 5. Required Project Structure

By the end of the workshop, your repository should look like this:

```text
your-repo-name/
│
├── README.md
├── models.py
├── loader.py
├── util.py
├── highscore.txt
│
└── levels/
    ├── level1.txt
    └── level2.txt
```

---

# 6. Part A – Set Up the GitHub Classroom Repository

## Step 1: Open the GitHub Classroom Assignment

Your instructor will provide a GitHub Classroom link. Open the link and accept the assignment.

After accepting it, GitHub Classroom will create a repository for you.

Typical result:

* a repository under your GitHub account or classroom organization
* a starter project space that only you and your instructor can access, depending on classroom settings

## Step 2: Open the Repository in VS Code

You may clone the repository using either the VS Code interface or the terminal.

### Option A – Using VS Code Terminal

Open VS Code and use the terminal:

```bash
git clone <your-repository-url>
cd <your-repository-folder>
code .
```

### Option B – Using VS Code Source Control / GitHub

You may also:

* sign into GitHub in VS Code
* use the clone repository option
* choose a local folder
* open the cloned project

## Step 3: Confirm the Repository is Connected

In the terminal, run:

```bash
git status
```

You should see that you are on your main branch and that your repository is ready.

---

# 7. Part B – Build the Required Directory and File Structure

## Step 4: Create the Levels Directory

Inside your project folder, create a directory called:

```text
levels
```

## Step 5: Create the Required Files

Create the following files in the root folder:

* `README.md`
* `models.py`
* `loader.py`
* `util.py`
* `highscore.txt`

Create the following files inside `levels/`:

* `level1.txt`
* `level2.txt`

---

# 8. Part C – Add Header Comments to Each File

Each file should begin with a short comment stating what the file is for.

This is important because:

* it documents file purpose
* it helps instructors and teammates understand your structure
* it reinforces software organization habits

Use the examples below.

---

## `README.md`

```md
# Pac-Man-Like Game

This repository contains my PROG1400 Pac-Man-like game project.
This project includes level files, game models, utility code, and loader logic.
```

---

## `models.py`

```python
# models.py
# This file contains the main object-oriented game models such as the game, maze, actors, items, and ghosts.
```

---

## `loader.py`

```python
# loader.py
# This file is responsible for loading and interpreting level data from text files.
```

---

## `util.py`

```python
# util.py
# This file contains shared utility classes, enums, and helper structures used by the game.
```

---

## `highscore.txt`

```text
0
```

You may also include a note in your submission or README that this file stores the current high score value.

---

## `levels/level1.txt`

```text
# level1.txt
# This file contains the layout data for level 1 of the game.
```

---

## `levels/level2.txt`

```text
# level2.txt
# This file contains the layout data for level 2 of the game.
```

---

# 9. Part D – Add Starter Level Layouts

After adding the header comments, place simple starter layouts into the level files. These are not final maps. They are initial placeholders to help establish the project.

You may use a simple ASCII map style like this.

## Example `level1.txt`

```text
# level1.txt
# This file contains the layout data for level 1 of the game.

###################
#P...............G#
#........#........#
#........#........#
#........#........#
#.................#
###################
```

## Example `level2.txt`

```text
# level2.txt
# This file contains the layout data for level 2 of the game.

###################
#P.....#..........#
#......#......G...#
#......#..........#
#..#############..#
#.................#
###################
```

You may decide later what each symbol means, but a common interpretation is:

* `#` = wall
* `.` = pellet / floor item
* `P` = player spawn
* `G` = ghost spawn
* space or another symbol = floor / open tile

At this stage, the files do not need to run yet. They only need to exist and demonstrate intended structure.

---

# 10. Part E – Suggested Initial `util.py` Planning

At this stage, `util.py` does not need to be complete, but students should understand its purpose.

A file like `util.py` often stores small reusable structures such as:

* `Cell`
* `Direction`
* `TileType`
* `GameState`
* `GhostState`

These are shared concepts used by multiple classes.

A future version of `util.py` might eventually contain code like:

```python
# util.py
# This file contains shared utility classes, enums, and helper structures used by the game.

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Cell:
    r: int
    c: int


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    NONE = "NONE"
```

You are not required to complete all of this in today’s lab unless your instructor asks you to, but you should understand why a file like this belongs in the project.

---

# 11. Part F – Suggested Initial `loader.py` Planning

The `loader.py` file is where the game may eventually load map data from `level1.txt` and `level2.txt`.

At this stage, you may add a placeholder function:

```python
# loader.py
# This file is responsible for loading and interpreting level data from text files.

def load_level_from_ascii(path):
    """Placeholder function for loading a level file."""
    pass
```

This shows your project is being organized in a modular way.

---

# 12. Part G – Suggested Initial `models.py` Planning

You are not required to fully recreate the instructor sample right now. However, you should begin preparing your own `models.py` file as the place where your main game classes will live.

A possible placeholder might be:

```python
# models.py
# This file contains the main object-oriented game models such as the game, maze, actors, items, and ghosts.

class Game:
    pass


class Maze:
    pass


class Actor:
    pass


class Pacman(Actor):
    pass


class Ghost(Actor):
    pass
```

This gives you a starting point and reinforces the idea that `models.py` is about the game’s object model.

---

# 13. Part H – Analyze the Instructor `models.py` Example

After building the file structure, review the provided `models.py` file carefully. Do not treat it as something to memorize line by line. Treat it as a **design reference**.

Your goal is to answer:

* What classes exist?
* What responsibility does each class appear to have?
* Which classes inherit from others?
* Which classes work together?
* What features appear to be turned on or off through flags?
* What ideas could be reused in your own game design?

---

## 13.1 Major Design Ideas Students Should Notice

### 1. The code is divided into responsibilities

The file is not just one giant script. Different classes handle different parts of the game.

Examples:

* `ScoreBoard` handles score and lives
* `Maze` handles the level structure and walkability
* `Actor` provides movement-related behavior
* `Pacman` and `Ghost` specialize from `Actor`
* `Item` and its subclasses manage collectible behavior
* `Game` coordinates the entire system

This is a strong example of **separation of concerns**.

---

### 2. Inheritance is being used

Some classes are designed as general parents, and others are more specific child classes.

Examples:

* `Pacman` inherits from `Actor`
* `Ghost` inherits from `Actor`
* `RandomGhost` and `ChaserGhost` inherit from `Ghost`
* `Pellet`, `PowerPellet`, and `Fruit` inherit from `Item`

This is an example of **object-oriented hierarchy**.

---

### 3. The `Game` class acts as the controller

The `Game` class appears to manage the overall state of the game.

It:

* tracks the current level
* keeps score
* owns the maze
* creates Pacman
* creates ghosts
* loads levels
* updates game progress
* resolves collisions
* checks if a level is complete

This suggests that `Game` is the central coordinating class.

---

### 4. The `Maze` class stores the world

The `Maze` class appears to represent the play area.

It stores:

* number of rows
* number of columns
* tile layout
* item locations
* player spawn
* ghost spawns

It also provides methods such as:

* `is_walkable()`
* `warp()`
* `get_item()`
* `remove_item()`
* `pellets_remaining()`

This means the maze is not just visual data. It also provides game logic services.

---

### 5. `Actor` is a reusable movement base class

The `Actor` class appears to be a shared parent for moving game objects.

It includes:

* current cell
* current direction
* next direction
* movement speed control
* turning logic
* step movement logic

This avoids duplication because Pacman and Ghosts both need movement behavior.

---

### 6. Ghosts have specialized behavior

There is a general `Ghost` class, but different ghost types choose directions differently.

Examples:

* `RandomGhost` chooses a random valid direction
* `ChaserGhost` chooses a direction that reduces distance to Pacman

This is a good example of **polymorphism**:
different subclasses respond to the same idea, `choose_dir()`, in different ways.

---

### 7. Items apply effects to the game

`Item` is a base class. Specific items implement their own `apply()` behavior.

Examples:

* `Pellet` adds score
* `PowerPellet` adds score and powers up Pacman
* `Fruit` adds score

This shows how objects can represent game events and interactions.

---

### 8. Feature flags are used

The provided file includes flags such as:

* `ENABLE_LOADER`
* `ENABLE_ITEMS`
* `ENABLE_GHOSTS`
* `ENABLE_CHASER`
* `ENABLE_POWER`
* `ENABLE_EAT_GHOST`
* `ENABLE_LEVELS`
* `ENABLE_HIGHSCORE`

These flags allow features to be enabled or disabled as the course progresses. This is very helpful in a learning environment because it allows complexity to grow over time.

---

# 14. Part I – Student Analysis Questions

After reviewing the provided `models.py`, answer the following questions in a separate section of your `README.md` or in a document your instructor requests.

## Analysis Questions

1. Which class appears to be the central controller of the game? Why?
2. Which classes show inheritance? List at least three parent-child examples.
3. What is the role of the `Maze` class?
4. Why do you think `Actor` exists as a separate class instead of putting all movement code directly in `Pacman` and `Ghost`?
5. What is the difference between `RandomGhost` and `ChaserGhost`?
6. What does the `ScoreBoard` class manage?
7. What is the purpose of loading level data from text files instead of hard-coding everything directly into one class?
8. Which parts of this model do you think you could reuse in your own game?
9. Which parts would you likely redesign to better match your own game theme?
10. What does this example teach you about project organization in Python?

---

# 15. Part J – Commit and Push Your Work

Once your structure is complete, save all files and commit your work.

Use the terminal:

```bash
git add .
git commit -m "Set up Pac-Man project structure and starter files"
git push
```

Then verify on GitHub that:

* all files exist
* the `levels` folder exists
* your level files are in the correct location
* the file headers are visible
* your commit has been uploaded

---

# 16. Deliverables

Students must submit or demonstrate the following:

## Required Deliverables

1. A connected GitHub Classroom repository
2. A complete project structure containing:

   * `README.md`
   * `models.py`
   * `loader.py`
   * `util.py`
   * `highscore.txt`
   * `levels/level1.txt`
   * `levels/level2.txt`
3. File header comments in each file explaining file purpose
4. Starter map content in both level files
5. A commit pushed to GitHub
6. Written analysis of the instructor-provided `models.py` example

---

# 17. Suggested Evaluation Criteria

## Workshop Rubric Alignment

### Attendance / Presence

* Student attended and participated in the workshop process

### Participation

* Student followed setup steps and engaged with repository and file creation tasks

### Task Progress

* Student successfully created the required directory and files
* Student added file header comments
* Student committed and pushed their work
* Student completed the code analysis

### Focus

* Student remained on task and used lab time productively

### Reflection

* Student provided thoughtful responses to the analysis questions

---

# 18. Reflection Questions

Answer the following before leaving the lab:

1. Why is it valuable to organize a game project into multiple files instead of writing everything in one Python file?
2. What did you learn about the relationship between project structure and object-oriented programming?
3. Which class in the sample `models.py` made the most sense to you? Why?
4. Which class or design idea felt confusing or more advanced?
5. How will your own Pac-Man-like game be similar to the sample model?
6. How will your own game be different?
7. What part of today’s setup work will make future coding easier?

---

# 19. Instructor Notes

This workshop is intended to establish both **technical setup** and **design awareness**.

Students are not expected to fully understand every line of the provided `models.py`. Instead, they should begin recognizing:

* class responsibilities
* inheritance structures
* modular file design
* the value of separating game systems into manageable components

This lab works well as an early foundation before students begin:

* building utility types
* loading levels
* implementing movement
* designing UML class diagrams
* translating models into working code

---

# 20. Starter File Pack for Students

Below is a compact version students may copy into their repository.

## `README.md`

```md
# Pac-Man-Like Game

This repository contains my PROG1400 Pac-Man-like game project.

## Project Structure

- `models.py` - main game models
- `loader.py` - level loading logic
- `util.py` - shared utilities and data types
- `highscore.txt` - stored high score
- `levels/level1.txt` - level 1 layout
- `levels/level2.txt` - level 2 layout
```

## `models.py`

```python
# models.py
# This file contains the main object-oriented game models such as the game, maze, actors, items, and ghosts.
```

## `loader.py`

```python
# loader.py
# This file is responsible for loading and interpreting level data from text files.
```

## `util.py`

```python
# util.py
# This file contains shared utility classes, enums, and helper structures used by the game.
```

## `highscore.txt`

```text
0
```

## `levels/level1.txt`

```text
# level1.txt
# This file contains the layout data for level 1 of the game.

###################
#P...............G#
#........#........#
#........#........#
#........#........#
#.................#
###################
```

## `levels/level2.txt`

```text
# level2.txt
# This file contains the layout data for level 2 of the game.

###################
#P.....#..........#
#......#......G...#
#......#..........#
#..#############..#
#.................#
###################
```

---

# 21. Closing

This workshop is the beginning of your game project, not the end of it. A properly structured repository gives you a place to grow your game in a logical way. As the course continues, you will build from this structure by adding:

* utility classes and enums
* maze loading logic
* actor movement
* item handling
* ghost behaviors
* game state management
* UML diagrams that connect your design to your implementation

Today’s goal is simple but important: **set up your game project like a developer, not just like a coder**.
