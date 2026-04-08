# PROG1400 – Final Assignment

## MP3 / Capstone Project

# Refactor, Modularize, and Transform an OOP Game

---

## 1. Assignment Details

**Course:** PROG1400 – Introduction to Object-Oriented Programming<br>
**Assignment Type:** Final Project (Capstone)<br>
**Delivery Mode:** Individual<br>
**Estimated Time:** 8–12 hours<br>
**Starting Point:** Instructor-provided `pacman_oop_game.py`<br>
**Repository:** GitHub Classroom (required)<br>
**Final Submission:** GitHub repository link<br>

---

## 2. Overview / Purpose / Objectives

In this final project, students will take a **fully working, monolithic Pac-Man-style Python game** and transform it into:

1. A **modular, multi-file project**
2. A **custom game** based on their own chosen concept
3. A **clean, object-oriented design**

This project represents the transition from:

```text
"Following code"
→ "Understanding code"
→ "Redesigning systems"
→ "Building your own software"
```

You are not starting from scratch. Instead, you are doing something far more valuable in real-world development:

> **You are taking an existing codebase and improving, restructuring, and adapting it.**

---

## 3. Learning Outcomes Addressed

### LO1 – Describe applications using core OOP principles

* Identify and explain existing class structures
* Improve encapsulation and separation of concerns

### LO2 – Implement OOP design principles

* Refactor a monolithic file into modular components
* Improve class design and relationships

### LO3 – Manage and distribute code with Git

* Use GitHub Classroom professionally
* Maintain clean commit history
* Submit a runnable repository

### LO4 – Develop an OOP solution using structured design

* Adapt an existing system into a new application
* Make design decisions based on game requirements

---

## 4. Assignment Description / Use Case

You are a junior developer tasked with improving an internal prototype game.

The current version:

* works
* demonstrates core gameplay
* is written in a **single file**
* is not scalable or maintainable

Your job is to:

### Phase 1 – Understand the System

* Read and run the provided Pac-Man-like game
* Identify key components (Player, Enemy, Level, Game, Score)

### Phase 2 – Refactor the Code

* Break the single file into a modular project
* Separate responsibilities into multiple files
* Improve readability and maintainability

### Phase 3 – Transform the Game

* Adapt the game to your own concept
* Modify mechanics, naming, visuals, and rules
* Ensure the game reflects your design, not just the original

---

## 5. Core Requirements

## A. You MUST start from the provided code

You are required to:

* use the provided `pacman_oop_game.py`
* not replace it with a completely different project

---

## B. You MUST modularize the code

You must refactor into multiple files.

### Minimum expected structure:

```text
your_game/
├── main.py
├── game.py
├── models.py
├── level.py
├── loader.py
├── scoreboard.py
├── config.py
├── util.py
├── levels/
│   └── level1.txt
└── README.md
```

---

## C. You MUST maintain object-oriented design

Your project must include:

* classes for major game entities
* separation of responsibilities
* clear relationships between objects

---

## D. You MUST adapt the game

You are required to change the game into your own concept.

### Acceptable examples:

* Snake Game
* Tank Game
* Hunter Assassin
* Trap the Mouse
* Maze Path of Light
* Minesweeper-style grid system
* Any instructor-approved variation

### Minimum adaptation expectations:

* rename classes appropriately
* change gameplay mechanics
* modify scoring or objectives
* update symbols, rules, or logic

---

## E. You MUST make the game configurable

Move hard-coded values into variables:

```python
PLAYER_SPEED = 1
ENEMY_SPEED = 1
DOT_POINTS = 10
STARTING_LIVES = 3
```

---

## F. Your project MUST be runnable by the instructor

The instructor must be able to:

```bash
git clone <your-repo>
cd your_game
python main.py
```

If your project does not run, it cannot be fully evaluated.

---

## G. GitHub Classroom is REQUIRED

You must:

* use your assigned repository
* commit regularly
* submit your GitHub link

---

## 6. Suggested Refactoring Approach (Step-by-Step)

### Step 1 – Run the original game

Understand:

* where logic lives
* how objects interact

---

### Step 2 – Identify components

Find:

* Player
* Enemy
* Level / grid
* Game loop
* Score system

---

### Step 3 – Extract classes into files

Example:

| Original     | New Location    |
| ------------ | --------------- |
| Player class | `models.py`     |
| Game logic   | `game.py`       |
| Constants    | `config.py`     |
| Score logic  | `scoreboard.py` |

---

### Step 4 – Clean dependencies

* remove circular imports
* organize imports logically
* ensure each file has a clear purpose

---

### Step 5 – Improve naming

Replace:

```python
x, y
```

With:

```python
row, col
```

---

### Step 6 – Add configuration

Move magic numbers to `config.py`

---

### Step 7 – Modify gameplay

Change:

* rules
* enemies
* objectives
* scoring

---

### Step 8 – Final cleanup

* remove unused code
* format consistently
* add comments

---

## 7. Required Features (Final Game)

Your final game must include:

1. Player movement
2. Game board / level system
3. At least one challenge (enemy, hazard, timer, etc.)
4. Objective or collectible system
5. Score tracking
6. Win condition
7. Lose condition
8. Object-oriented structure
9. Modular file structure
10. Configurable values

---

## 8. GitHub Requirements

## A. Commit Expectations

Students should show progress:

```bash
git commit -m "Initial refactor into modules"
git commit -m "Move Player and Enemy into models.py"
git commit -m "Add config constants"
git commit -m "Adapt game to Snake mechanics"
git commit -m "Finalize gameplay and README"
```

---

## B. Repository Quality

Your repo should:

* be clean and organized
* not contain unnecessary files
* include a clear structure
* include working code

---

## C. Submission

Submit:

👉 **Your GitHub repository link**

The instructor will clone and run your project.

---

## 9. README Requirements

Your `README.md` must include:

### 1. Game Title

### 2. Description

### 3. Controls

### 4. How to Run

### 5. File Structure

### 6. Features

### 7. Customizations from Original Game

---

## 10. Reflection Questions

Submit answers separately or in README:

1. What changes did you make to the original game?
2. How did you modularize the code?
3. What classes did you create or modify?
4. Where did you apply encapsulation?
5. Did you use inheritance? Why or why not?
6. What part was most challenging?
7. What would you improve next?

---

## 11. Assessment & Rubric

| Criteria                   | Excellent                                              | Proficient                       | Developing                           | Beginning                      |
| -------------------------- | ------------------------------------------------------ | -------------------------------- | ------------------------------------ | ------------------------------ |
| **Refactoring Quality**    | Clean modular structure, strong separation of concerns | Mostly modular with minor issues | Some modularization but inconsistent | Minimal or poor modularization |
| **OOP Design**             | Strong use of classes, clear responsibilities          | Good structure with minor issues | Basic class usage                    | Weak or incorrect OOP          |
| **Game Adaptation**        | Fully transformed into new game                        | Good customization               | Limited changes                      | Mostly original unchanged      |
| **Functionality**          | Fully playable and stable                              | Mostly working                   | Partially working                    | Broken or incomplete           |
| **Configurable Design**    | Well parameterized system                              | Some configuration               | Limited configuration                | Hard-coded values              |
| **GitHub Practice**        | Excellent commit history and organization              | Good usage                       | Inconsistent commits                 | Poor usage                     |
| **README / Documentation** | Clear, complete, professional                          | Mostly complete                  | Limited                              | Missing                        |

---

## 12. Submission Guidelines

You must submit:

👉 **Your GitHub Classroom repository link**

Ensure:

* project runs
* README is complete
* code is clean

---

## 13. Instructor Notes (Why This Assignment Matters)

This assignment simulates **real-world development**:

Students are not just writing code.

They are:

* reading existing systems
* refactoring legacy code
* designing improvements
* making architectural decisions

This is the difference between:

```text
Beginner → writes code
Intermediate → organizes code
Advanced → designs systems
```

---

## 14. Optional Extensions (High Achievers)

Students may extend with:

* multiple levels
* improved AI
* sound or visuals
* menus
* difficulty scaling

---

## 🔚 Final Reminder to Students

> This is YOUR game now.

You are not submitting Pac-Man.

You are submitting:

* your design
* your decisions
* your codebase

And most importantly:

👉 **Your GitHub repository is your final submission.**
