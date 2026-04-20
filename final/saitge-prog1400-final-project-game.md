# PROG1400 Final Assignment

## Mini-Project 8 / Final Project

# OOP Game Development Project

### Building a Pac-Man-Like Game with Your Own Theme and Mechanics

**Course:** PROG1400 – Introduction to Object-Oriented Programming<br>
**Assignment Type:** Final Assignment / Guided Project<br>
**Delivery Mode:** Individual<br>
**Estimated Time:** 8–12 hours total<br>
**Format:** 8 mini-workshops (about 1–2 hours each)<br>
**Repository:** GitHub Classroom repository<br>
**Submission:** Source code, README, playable game, reflection, commit history<br>

---

## 1. Assignment Details

In this final assignment, students will build a complete **object-oriented Python game** based on a **Pac-Man-like gameplay structure**, while adapting the design to fit their own chosen game concept.

This project is structured as **8 mini-workshops** that guide students through the development of a playable game. The instructor-led case study uses a Pac-Man-like maze game, but students must continuously adapt the code, naming, theme, mechanics, and rules to match their own selected game.

Examples of acceptable game directions include:

* Snake Game
* Hunter Assassin
* Impossible Game
* Trap the Mouse
* Tank Game
* Minesweeper
* Maze Path of Light
* Other instructor-approved games with similar movement / collection / obstacle / enemy mechanics

The final result should demonstrate:

* object-oriented design
* modular code organization
* configurable game settings
* GitHub best practices
* a playable and understandable game
* evidence that the student adapted the case study to their own requirements

---

## 2. Overview / Purpose / Objectives

The purpose of this final project is to bring together the major concepts from the course into one complete programming artifact.

Students will move from a working instructor example toward an original variation of the same core design. The emphasis is not on building a massive commercial-quality game. The emphasis is on learning how to:

* model a game using classes and objects
* separate responsibilities into modules
* design maintainable code
* manage project files in a professional way
* make design decisions based on their own game requirements
* use GitHub Classroom correctly so the instructor can review and run the code

This assignment is intentionally structured as a guided build rather than a single large prompt. Each mini-workshop introduces a new feature and asks students to adapt the code to fit their own game.

---

## 3. Learning Outcomes Addressed

This final assignment aligns to the following PROG1400 course outcomes.

### LO1 – Describe applications using core OOP principles

Students will explain and apply:

* encapsulation
* inheritance where appropriate
* abstraction
* composition
* separation of responsibilities between classes

### LO2 – Implement OOP design principles

Students will:

* create classes and objects
* organize game logic across multiple modules
* manage interactions between game entities
* use methods and attributes appropriately

### LO3 – Manage and distribute code with Git

Students will:

* use GitHub Classroom repository structure
* commit regularly with meaningful messages
* organize files so the instructor can run the project
* maintain a readable repository

### LO4 – Develop an OOP solution using software modelling / structured design

Students will:

* think about entities, relationships, and responsibilities
* translate game requirements into classes and modules
* document and reflect on their design decisions

---

## 4. Assignment Description / Use Case

You are a junior game developer working on a small prototype project. The prototype is inspired by a Pac-Man-like gameplay loop:

* the player moves through a space
* obstacles or walls affect movement
* collectibles or objectives are gathered
* one or more enemies or hazards create challenge
* the player earns points
* the level ends when the collection objective is complete
* a scoreboard displays the current state of play

The instructor has demonstrated a Pac-Man-style case study. Your task is to build a complete object-oriented game using the same development process, while adapting the design to your own game concept.

You are expected to treat this like a real small software project. That means:

* your repository must be organized
* your code must be modular
* your variables should be configurable
* the instructor must be able to run your code easily
* your game should clearly reflect your own design decisions

---

## 5. Project Rules and Expectations

## A. You must build your game in Python

Use standard Python and any instructor-approved built-in or basic libraries used in class.

## B. Your game must be object-oriented

At minimum, your project must use classes for the major game components.

## C. Your game must be modular

Do not place everything in one file unless the instructor explicitly allows it for the starter demo. Your final project should be organized across multiple files.

Recommended structure:

```text
your_game/
│
├── main.py
├── game.py
├── config.py
├── models.py
├── loader.py
├── scoreboard.py
├── util.py
├── levels/
│   ├── level1.txt
│   ├── level2.txt
│   └── level3.txt
├── assets/              # optional
├── docs/                # optional diagrams / notes
└── README.md
```

## D. Your game must be configurable

Students should promote values into variables or constants whenever possible. For example:

* screen width / height
* tile size
* player speed
* enemy speed
* score values
* starting lives
* colors
* level file paths
* item symbols
* win conditions

Avoid hard-coding values throughout the project.

## E. Your repository must be instructor-runnable

The instructor must be able to:

1. clone the repository
2. open the project
3. run the game with minimal effort

Provide clear run instructions in the `README.md`.

## F. You must adapt the project to your own game

You are not expected to submit a copy of the instructor’s Pac-Man case study with renamed files only. You must make meaningful choices to align the game with your selected mechanics.

---

## 6. Recommended Final OOP Structure

A good object-oriented structure for this project may look like this:

```text
Game
├── Level
├── ScoreBoard
├── Player
├── Enemy / Hazard
├── Collectible / Goal Item
└── Config / Utility Support
```

Possible class ideas:

* `Game`
* `Level`
* `Player`
* `Enemy`
* `Item`
* `ScoreBoard`
* `GameObject`
* `TileMap`
* `Bullet` (for tank-style projects)
* `Snake` (for snake projects)
* `MineCell` (for minesweeper-style projects)

Not all games need inheritance, but every game should show thoughtful object-oriented structure.

---

## 7. Development Plan: 8 Mini-Workshops

# Workshop 1 – Project Setup, Repository Structure, and Game Plan

**Estimated Time:** 1 hour

### Goal

Set up the project repository, files, folders, and basic design plan.

### Student Tasks

* clone the GitHub Classroom repository
* create a clean project folder structure
* add starter files
* create a README
* decide how the Pac-Man case study maps to your own game

### Required Output

* working repository structure
* initial README
* starter modules
* first commit

### OOP Concepts

**Classes represent parts of the system.**
Before students write code, they should think about what “things” exist in the game.

For a Pac-Man-like example:

* Player
* Enemy
* Level
* ScoreBoard
* Game

For a student game:

* Snake may replace Player
* Hazard may replace Enemy
* Goal orb may replace collectible dot
* Grid or map may replace maze

This workshop teaches that OOP begins with **thinking in objects and responsibilities**, not jumping directly into code.

### Guidance to Students

You are not building “Pac-Man exactly.” You are building **your own game with similar mechanical structure**. Use the case study as a design model, not as a copying template.

### GitHub Best Practices

* clone the correct repository
* commit after setup
* use meaningful commit messages such as:

```bash
git commit -m "Setup project structure and initial README"
```

### Suggested Reflection

* What is the theme of your game?
* Which game objects do you think need their own classes?
* What parts of the Pac-Man example will remain, and what parts will change?

---

# Workshop 2 – Building the Board / Level Representation

**Estimated Time:** 1–1.5 hours

### Goal

Create the map or game space and load it into the program.

### Student Tasks

* represent the maze / map / board in data
* create a `Level` or `TileMap` class
* load a level from a text file
* identify walls, walkable spaces, collectibles, hazards, and spawn points

### Required Output

* a level file such as `level1.txt`
* code that loads and interprets the level
* a visible game board or printed board representation

### OOP Concepts

**Encapsulation** means the `Level` class should manage level-related logic.

The `Level` class should know:

* the layout
* where the player starts
* where enemies start
* where items are
* whether a tile is blocked
* whether the level is complete

This is better than storing level logic everywhere in the program.

### Why This Matters

Students learn that the board is **data**, not just drawing code. This supports:

* easy changes
* new levels
* custom mechanics
* better testing

### Adaptation Examples

* **Snake:** your board may be open instead of maze-based
* **Trap the Mouse:** board may include blocked and open tiles
* **Tank Game:** walls may be destructible or solid
* **Maze Path of Light:** tiles may become “lit” when visited
* **Minesweeper:** board stores hidden states rather than visible walls

### Suggested Design Ideas

A level file could use symbols like:

```text
##########
#P......E#
#..##....#
#....o...#
##########
```

Possible meanings:

* `#` wall
* `P` player start
* `E` enemy start
* `.` collectible
* `o` power item
* space = empty floor

Students should modify symbols to fit their own game.

### GitHub Best Practices

Commit when the loader works:

```bash
git commit -m "Add level loader and initial board layout"
```

---

# Workshop 3 – Player Class and Movement

**Estimated Time:** 1–1.5 hours

### Goal

Implement the player object and allow movement through the board.

### Student Tasks

* create a `Player` class
* store position, score, lives, or other game state
* read keyboard input
* move only when legal
* prevent movement through walls or invalid tiles

### Required Output

* a movable player
* collision checking with the board
* player data stored in an object

### OOP Concepts

The `Player` object should contain the player’s own state, such as:

* row / column or x / y position
* score
* lives
* movement direction
* special states or power modes

This is a core example of **encapsulation**: player data belongs in the `Player` class.

### Why This Matters

Students often begin by storing everything in global variables. This workshop helps them move state into objects where it belongs.

### Adaptation Examples

* **Snake:** movement may shift the entire snake body
* **Hunter Assassin:** player movement may be stealth-based
* **Impossible Game:** movement may be automatic with jump logic
* **Tank Game:** movement and facing direction may both matter

### Instructor Emphasis

Encourage students to ask:

* What should my player know about itself?
* What should the player not be responsible for?
* Should the player decide if a wall exists, or should the level answer that question?

A strong answer is:

* the player asks to move
* the level decides whether movement is allowed

That is good class responsibility design.

### GitHub Best Practices

Students should commit after working movement is complete:

```bash
git commit -m "Implement player class and movement rules"
```

---

# Workshop 4 – Collectibles, Objectives, and Scoring

**Estimated Time:** 1 hour

### Goal

Add collectible items or objective tiles and award points.

### Student Tasks

* detect when the player reaches an item
* remove or mark collected items
* increase score
* track remaining objectives

### Required Output

* collectibles or objective items
* scoring logic
* visible count or progress display

### OOP Concepts

There are multiple valid OOP approaches here:

### Option 1 – Items managed by the `Level`

The level stores collectible positions and removes them when collected.

### Option 2 – Items as objects

Students create an `Item` class with:

* position
* point value
* type
* collected status

Either design can be valid if it is well explained.

### Why This Matters

This workshop teaches students that game rules should not be scattered across random code blocks. A good design gives each object a clear purpose.

### Adaptation Examples

* **Snake:** food increases score and snake length
* **Maze Path of Light:** tiles may change state from dark to lit
* **Trap the Mouse:** objectives may involve surrounding the target rather than collecting dots
* **Minesweeper:** score may be based on revealed safe cells or flags

### Instructor Emphasis

Students should promote values into configuration variables:

```python
DOT_POINTS = 10
POWER_ITEM_POINTS = 50
LEVEL_CLEAR_BONUS = 100
```

This improves flexibility and supports easy game balancing.

### GitHub Best Practices

```bash
git commit -m "Add collectibles and scoring system"
```

---

# Workshop 5 – Enemy / Hazard Behaviour

**Estimated Time:** 1–1.5 hours

### Goal

Add an enemy or hazard that creates challenge in the game.

### Student Tasks

* create an `Enemy` or hazard class
* move the enemy each update
* implement simple logic such as chasing, patrolling, random movement, or path-based movement
* detect contact with the player

### Required Output

* at least one functioning enemy / hazard
* movement logic
* visible game challenge

### OOP Concepts

This workshop is excellent for discussing:

* class responsibility
* method design
* reuse
* inheritance if appropriate

Possible approach:

```text
Entity
├── Player
└── Enemy
```

Shared features may include:

* position
* reset behavior
* move attempts

Unique features:

* player collects items
* enemy chases or patrols

### Why This Matters

Students see how shared behavior can be placed in a common parent class, while specialized behavior stays in child classes.

### Adaptation Examples

* **Hunter Assassin:** enemy AI may move toward line-of-sight
* **Tank Game:** enemy may shoot instead of chase
* **Snake:** hazards may be self-collision or moving blockers
* **Impossible Game:** hazards may be static obstacles rather than intelligent enemies

### Instructor Emphasis

Not every student game requires the same enemy logic. The important part is that the challenge mechanic fits the game and is implemented cleanly.

### GitHub Best Practices

```bash
git commit -m "Add enemy class and hazard movement"
```

---

# Workshop 6 – Collisions, Win/Lose Logic, and Game Rules

**Estimated Time:** 1–1.5 hours

### Goal

Combine systems into meaningful gameplay.

### Student Tasks

* detect player collision with enemy or hazard
* define what happens on collision
* add lives, health, restart logic, or game over rules
* implement level completion when all objectives are complete

### Required Output

* clear win condition
* clear lose condition
* stable gameplay loop

### OOP Concepts

This workshop highlights **coordination between objects**.

Typical object interactions:

* `Game` controls the update loop
* `Player` updates position
* `Enemy` updates movement
* `Level` checks item states
* `Game` decides whether win/lose conditions are met

This is a good example of **composition**: the `Game` object is composed of several smaller objects working together.

### Why This Matters

Students often try to put all rules into one class. This workshop shows why a top-level `Game` controller is useful.

### Adaptation Examples

* all dots collected = level complete
* all lights activated = level complete
* all safe tiles revealed = level complete
* target defeated = level complete
* survive a certain time = level complete

### GitHub Best Practices

```bash
git commit -m "Implement collisions and win lose conditions"
```

---

# Workshop 7 – Scoreboard, Persistence, and Modular Cleanup

**Estimated Time:** 1 hour

### Goal

Add a scoreboard and improve code organization.

### Student Tasks

* create a `ScoreBoard` class or module
* display current score and possibly lives, level, or best score
* optionally save a high score to file
* refactor repeated code into functions and modules
* improve naming and configuration variables

### Required Output

* scoreboard visible in the game
* optional persistent high score
* cleaner code structure than earlier workshops

### OOP Concepts

The `ScoreBoard` is a strong example of **single responsibility**.

It should manage score-related information, not player movement or level loading.

Students learn that strong OOP design often means:

* smaller classes
* focused responsibilities
* less duplication
* easier maintenance

### Why This Matters

This workshop helps move students from “it works” to “it is designed well.”

### Instructor Emphasis

Ask students to refactor:

* magic numbers into constants
* repeated logic into methods
* long files into modules
* unclear variable names into descriptive names

### GitHub Best Practices

```bash
git commit -m "Add scoreboard and refactor project structure"
```

---

# Workshop 8 – Polish, Customization, README, and Final Submission

**Estimated Time:** 1–2 hours

### Goal

Finalize the game, improve usability, and prepare for grading.

### Student Tasks

* add final polish
* verify all code runs correctly
* ensure project reflects their own game theme
* finish README instructions
* test from a clean clone
* complete reflection questions

### Required Output

* final playable game
* instructor-runnable repository
* completed README
* reflection submission

### OOP Concepts

The final workshop focuses less on new concepts and more on **evaluating the design** students built.

Students should now be able to explain:

* why classes were chosen
* how responsibilities were separated
* what could be improved
* how their game differs from the Pac-Man case study

### Final README Must Include

* game title
* short description
* controls
* how to run the game
* file/module overview
* features
* known limitations
* credits if applicable

### GitHub Best Practices

Students should make final cleanup commits rather than one giant “done” commit.

Example:

```bash
git commit -m "Polish final game and update README"
```

---

## 8. Minimum Functional Requirements

Your final game must include all of the following in some form:

1. A playable game loop
2. A player-controlled object
3. A board, map, maze, or defined play space
4. At least one challenge mechanic (enemy, hazard, timer, obstacle, etc.)
5. A collectible, objective, or progress mechanic
6. A score or progress display
7. A level completion condition
8. A lose condition or failure state
9. Object-oriented structure using classes
10. Multiple Python files / modular organization
11. A GitHub repository the instructor can run
12. A README with run instructions

---

## 9. Required Design Expectations

Students must demonstrate the following design expectations.

### A. Modularization

Your code should be separated into logical files.

### B. Meaningful naming

Classes, methods, and variables should have clear names.

### C. Configurable variables

Values that may need balancing or adjustment should be stored in constants or config variables.

### D. Original adaptation

Your final game should reflect your chosen concept, not just the instructor example.

### E. Maintainability

The instructor should be able to read the project and understand the design.

---

## 10. GitHub Classroom Expectations

Students are expected to use professional repository practices throughout the project.

### Required Git Practices

* commit regularly
* use meaningful commit messages
* keep the repository clean
* do not leave broken code in the final main branch
* ensure the instructor can run the final project

### Good Commit Examples

```bash
git commit -m "Create Player and Enemy classes"
git commit -m "Add item collection and score logic"
git commit -m "Refactor config values into constants"
git commit -m "Complete final README and cleanup"
```

### Poor Commit Examples

```bash
git commit -m "stuff"
git commit -m "final"
git commit -m "update"
```

### Instructor Checkpoints

The instructor may review:

* repository history
* project organization
* evidence of staged development
* whether the student followed workshop progression

---

## 11. Deliverables

Submit the following through your GitHub Classroom repository and any LMS instructions provided by the instructor.

### Required Deliverables

1. Final source code
2. Playable Python game
3. Organized project structure
4. `README.md` with run instructions
5. At least one level / playable scenario
6. Reflection answers
7. Commit history showing workshop progress

### Optional Deliverables

* UML diagram
* class diagram
* level design notes
* screenshot or gameplay gif
* extra levels
* sound or art assets where permitted

---

## 12. Reflection Questions

Answer the following in a reflection file or LMS submission.

1. What game did you choose, and how does it relate to the Pac-Man case study?
2. Which classes did you create, and why?
3. How did you apply encapsulation in your design?
4. Did you use inheritance or composition? Explain where and why.
5. What values did you make configurable, and why was that helpful?
6. What part of the project was most difficult?
7. What would you improve if you had more time?
8. How did you ensure the instructor could run your project easily?

---

## 13. Assessment & Rubric

# Final Assignment Rubric

| Criterion                                | Excellent                                                                                                   | Proficient                                                             | Developing                                                          | Beginning                                               |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- |
| **OOP Design**                           | Classes are well designed, responsibilities are clear, and object interactions are logical and maintainable | Classes and responsibilities are mostly clear with minor design issues | Some class design exists, but responsibilities are unclear or mixed | Minimal or weak OOP structure                           |
| **Game Functionality**                   | Game is fully playable with complete mechanics and stable behavior                                          | Game is mostly playable with only minor issues                         | Game is partially playable but major features are incomplete        | Game does not run properly or core features are missing |
| **Adaptation to Student’s Own Game**     | Strong, meaningful adaptation of case study into an original game design                                    | Good adaptation with some original features                            | Limited adaptation; still heavily resembles the case study          | Minimal evidence of customization                       |
| **Modularization and Code Organization** | Code is clean, modular, readable, and well structured across files                                          | Code is organized with minor issues                                    | Some modular structure exists but project is inconsistent           | Poor organization; difficult to follow                  |
| **Use of Configurable Variables**        | Game values are consistently externalized and easy to modify                                                | Most major values are configurable                                     | Some values are configurable, many are hard-coded                   | Little or no effort to make the game configurable       |
| **GitHub / Repository Practice**         | Repository is professional, easy to run, and includes strong commit history                                 | Repository is functional and mostly organized                          | Repository shows uneven practice or unclear run process             | Repository is disorganized or difficult to run          |
| **README / Documentation**               | README is complete, clear, and helpful                                                                      | README is mostly complete                                              | README is limited or unclear                                        | README is missing or inadequate                         |
| **Reflection / Design Understanding**    | Reflection shows strong understanding of OOP and design choices                                             | Reflection shows good understanding                                    | Reflection shows partial understanding                              | Reflection is weak or missing                           |

### Suggested Weighting

* OOP Design – 20%
* Game Functionality – 20%
* Adaptation / Originality – 15%
* Modularization / Code Quality – 15%
* Configurability – 10%
* GitHub Practice – 10%
* README / Documentation – 5%
* Reflection – 5%

---

## 14. Submission Guidelines

Submit by ensuring your GitHub Classroom repository contains:

* final code
* final README
* all required files
* clean runnable version on the main branch unless otherwise instructed

The instructor must be able to:

* clone the repo
* read the README
* run the game
* inspect the code and commit history

Test your project from a clean start before submitting.

---

## 15. Resources / Equipment

Students may use:

* Python
* VS Code
* GitHub Classroom repository
* course notes and workshop materials
* instructor starter example
* approved Python libraries used in class

Students should review:

* classes and objects
* encapsulation
* inheritance
* composition
* methods and attributes
* file organization
* basic game loop structure
* Git basics

---

## 16. Academic Policies

Students must submit their own work.
You may learn from the case study, course notes, and instructor demonstrations, but your final project must show your own implementation and adaptation.

If external code, assets, or tools are used, they must be approved and acknowledged appropriately.

---

