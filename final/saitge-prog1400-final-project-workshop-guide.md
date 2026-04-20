# 🧠 PROG1400 – FINAL PROJECT WORKSHOP GUIDE

## OOP Game Development (Pac-Man Case Study → Student Game)

This is your **instructor-facing delivery document**.

Each workshop includes:

* Starter code (progressive)
* Code explanation
* OOP teaching notes
* Step-by-step build tasks
* “Adapt to your game” prompts
* Git checkpoints
* Troubleshooting guidance

---

# 🔷 GLOBAL PROJECT BASELINE (Before Workshop 1)

Provide students with a **starter repo OR require them to scaffold this**.

## Minimal Starting Files

```text
project/
├── main.py
├── game.py
├── config.py
├── models.py
├── loader.py
├── scoreboard.py
├── util.py
├── levels/
│   └── level1.txt
└── README.md
```

---

# 🧪 WORKSHOP 1 – Project Setup + Game Design Thinking

## 🎯 Goal

Students understand **what they are building** before writing code.

---

## 🧩 Starter Code

### `main.py`

```python
from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
```

### `game.py`

```python
class Game:
    def __init__(self):
        print("Game initialized")

    def run(self):
        print("Game loop starting...")
```

---

## 🧠 Code Explanation

* `main.py` = entry point
* `Game` class = central controller
* No logic yet → intentional

---

## 🎓 OOP Teaching Notes

Key idea:

> “We don’t write code first. We design objects first.”

Introduce:

* Objects = things in the system
* Classes = blueprints
* Responsibilities = what each object owns

---

## 🛠️ Step-by-Step Tasks

1. Clone GitHub repo
2. Create folder structure
3. Add files
4. Run program
5. Write initial README

---

## 🔁 Adapt to Your Game

Prompt students:

> Replace “Pac-Man” thinking with your game.

Examples:

* Snake → Player = Snake
* Tank → Player = Tank
* Minesweeper → Player = Cursor/Selector

---

## ✅ Git Checkpoint

```bash
git commit -m "Setup project structure and base Game class"
```

---

## ⚠️ Troubleshooting

| Issue              | Fix                             |
| ------------------ | ------------------------------- |
| Python not running | Check PATH / interpreter        |
| Import error       | Ensure files are in same folder |

---

# 🧪 WORKSHOP 2 – Level / Board System

---

## 🎯 Goal

Represent the game world as **data**

---

## 🧩 Starter Code

### `loader.py`

```python
def load_level(path):
    with open(path) as f:
        return [list(line.strip()) for line in f.readlines()]
```

### `level1.txt`

```
##########
#P......E#
#..##....#
#....o...#
##########
```

---

## 🧠 Code Explanation

* Each row = list
* Each character = tile
* Grid = 2D list

---

## 🎓 OOP Teaching Notes

Introduce:

* **Encapsulation**
* Level owns:

  * layout
  * rules
  * items

---

## 🛠️ Tasks

1. Load level into Game
2. Print grid
3. Identify:

   * Player spawn
   * Enemy spawn
   * Walls
   * Items

---

## 🔁 Adapt Prompt

> What do your symbols represent?

Examples:

* Minesweeper → hidden cells
* Tank → destructible walls
* Snake → empty grid

---

## ✅ Git Checkpoint

```bash
git commit -m "Add level loader and board representation"
```

---

## ⚠️ Troubleshooting

* File path issues → use relative paths
* Index errors → check row/column bounds

---

# 🧪 WORKSHOP 3 – Player Class

---

## 🎯 Goal

Introduce player as an object

---

## 🧩 Starter Code

### `models.py`

```python
class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.score = 0

    def move(self, dr, dc):
        self.row += dr
        self.col += dc
```

---

## 🧠 Code Explanation

* `row`, `col` = position
* `score` stored inside object
* movement modifies state

---

## 🎓 OOP Notes

Concept:

> “State belongs inside objects”

Avoid:

```python
player_x = 5  # ❌ global
```

Use:

```python
player.row  # ✅ encapsulated
```

---

## 🛠️ Tasks

1. Create player from level
2. Add movement controls
3. Prevent walking into walls

---

## 🔁 Adapt Prompt

* Snake → body list
* Tank → direction + turret
* Impossible → auto movement

---

## ✅ Git Checkpoint

```bash
git commit -m "Implement player class and movement"
```

---

## ⚠️ Troubleshooting

* Player moves through walls → missing collision check
* Input not working → check key bindings

---

# 🧪 WORKSHOP 4 – Items + Score

---

## 🎯 Goal

Add interaction with environment

---

## 🧩 Starter Code

```python
def collect_item(tile):
    if tile == ".":
        return 10
    elif tile == "o":
        return 50
    return 0
```

---

## 🧠 Code Explanation

* Tile determines score
* Level updates state

---

## 🎓 OOP Notes

Discuss:

* Should items be:

  * data in level?
  * or objects?

Both acceptable → discuss trade-offs

---

## 🛠️ Tasks

1. Detect item collision
2. Increase score
3. Remove item

---

## 🔁 Adapt Prompt

* Minesweeper → reveal tiles
* Snake → food growth
* Light Maze → activate tiles

---

## ✅ Git Checkpoint

```bash
git commit -m "Add item collection and scoring"
```

---

## ⚠️ Troubleshooting

* Items not disappearing → not updating grid
* Score not updating → not tied to player

---

# 🧪 WORKSHOP 5 – Enemy / Hazard

---

## 🎯 Goal

Introduce challenge

---

## 🧩 Starter Code

```python
class Enemy:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move_towards(self, player):
        if self.row < player.row:
            self.row += 1
        elif self.row > player.row:
            self.row -= 1
```

---

## 🧠 Code Explanation

* Simple AI: vertical chase
* Expand later

---

## 🎓 OOP Notes

Introduce:

* Inheritance (optional)
* Shared behavior

```text
Entity
 ├── Player
 └── Enemy
```

---

## 🛠️ Tasks

1. Add enemy
2. Move each update
3. Detect collision

---

## 🔁 Adapt Prompt

* Tank → bullets
* Snake → self-collision
* Impossible → static hazards

---

## ✅ Git Checkpoint

```bash
git commit -m "Add enemy behavior"
```

---

## ⚠️ Troubleshooting

* Enemy not moving → update loop missing
* Enemy stuck → movement logic flawed

---

# 🧪 WORKSHOP 6 – Game Rules

---

## 🎯 Goal

Make game playable

---

## 🧩 Starter Code

```python
def check_collision(player, enemy):
    return player.row == enemy.row and player.col == enemy.col
```

---

## 🎓 OOP Notes

Introduce:

* **Composition**
* Game orchestrates objects

---

## 🛠️ Tasks

1. Add win condition
2. Add lose condition
3. Reset or end game

---

## 🔁 Adapt Prompt

* Win = all items collected
* Lose = hit hazard
* Alternative: survive timer

---

## ✅ Git Checkpoint

```bash
git commit -m "Implement win and lose conditions"
```

---

## ⚠️ Troubleshooting

* Game not ending → condition not checked
* Infinite loop → missing break

---

# 🧪 WORKSHOP 7 – Scoreboard + Refactor

---

## 🎯 Goal

Clean architecture

---

## 🧩 Starter Code

```python
class ScoreBoard:
    def __init__(self):
        self.best = 0

    def update(self, score):
        if score > self.best:
            self.best = score
```

---

## 🎓 OOP Notes

Introduce:

* Single Responsibility Principle

---

## 🛠️ Tasks

1. Display score
2. Add high score
3. Refactor code

---

## 🔁 Adapt Prompt

* Add lives?
* Add levels?
* Add UI elements?

---

## ✅ Git Checkpoint

```bash
git commit -m "Add scoreboard and refactor code"
```

---

## ⚠️ Troubleshooting

* Score resets → not persisted
* Duplicate logic → refactor needed

---

# 🧪 WORKSHOP 8 – Final Polish

---

## 🎯 Goal

Finalize submission

---

## 🛠️ Tasks

1. Test from fresh clone
2. Improve README
3. Clean code
4. Add polish

---

## 🎓 OOP Reflection Notes

Students should now explain:

* Why classes exist
* How objects interact
* What they would improve

---

## 🔁 Adapt Prompt

Push students:

> “Does your game feel like YOUR game?”

---

## ✅ Final Git Commit

```bash
git commit -m "Final project submission"
```

---

## ⚠️ Troubleshooting

* Instructor can’t run → missing instructions
* Broken imports → wrong structure

---

# 🧠 FINAL INSTRUCTOR INSIGHT

This structure does something powerful:

It teaches students to move from:

```text
“I can write code”
→ “I can design systems”
```

And more importantly:

```text
“I followed the tutorial”
→ “I built MY game”
```

---

# 🚀 If you want next level

I can build:

* ✅ Full **starter repo (clean, production-ready)**
* ✅ Complete **UML diagram pack (Mermaid)**
* ✅ **Assessment checkpoint rubrics per workshop**
* ✅ **Auto-grading checklist for GitHub repos**
* ✅ **Student version vs Instructor version split**

Just tell me 👍
