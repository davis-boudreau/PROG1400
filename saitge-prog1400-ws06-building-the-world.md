# 🧩 PROG1400 — Workshop 6

## Building the World: TileMap, Grid, and Movement Rules

### *Turning UML Class Diagrams into Real Python Classes*

---

## 1. Workshop Details

**Course:** PROG1400 – Object-Oriented Programming
**Week:** 6
**Workshop Title:** World Grid & TileMap Implementation
**Workshop Type:** Guided Learning Workshop
**Estimated Time:** 2–3 hours
**Prerequisites:**

* Workshop 3 — UML Class Diagram (World + Entities)
* Workshop 4 — Game Rules + UML Sequence Diagrams
* Workshop 5 — State Machine Starter Code

**Tools Required:**

* Visual Studio Code
* Python 3
* VS Code Extension: **Mermaid Chart** (official)
* Existing PROG1400 repository

**Primary Learning Outcome:**
**Outcome 4 — Develop an object-oriented solution utilizing software modelling design documentation**

---

## 2. Why This Workshop Matters (Read First)

Up to now, you have built the **control logic** of your game:

* You designed the **world structure** (UML class diagram)
* You defined **how objects interact** (sequence diagrams)
* You implemented **state control** (state machine)

Now it is time to build the **world itself**.

> The world is not the player.
> The world is not the enemy.
> The world is the **rules and boundaries** everything else must obey.

In this workshop, you will implement the **TileMap / WorldGrid** that:

* defines where movement is allowed
* stores the layout of your game
* acts as the *single source of truth* for collision rules

This is the foundation of **every grid-based game**.

---

## 3. Big Idea: The World Owns the Rules

One of the most common beginner mistakes is putting world rules in the player:

```python
# ❌ BAD (what beginners do)
if next_tile != "#":
    move_player()
```

Instead, we do this:

```python
# ✅ GOOD (professional design)
if tile_map.is_walkable(next_position):
    move_player()
```

Why?

Because:

* multiple objects need the same rules
* rules change over time
* logic must live in **one place**

This workshop teaches you how to do that **correctly**.

---

## 4. What You Will Build Today

By the end of this workshop, you will have:

1. A **TileType enum** (what tiles exist)
2. A **GridCoord / Position class**
3. A **TileMap class** that:

   * stores the grid
   * validates positions
   * answers movement questions
4. A **console-based test** proving your world works
5. Code that directly matches your **UML class diagram**

No graphics yet.
No player movement yet.
Just **clean world logic**.

---

# 🧠 Part A — Review the UML (Design Anchoring)

Before writing code, open your **UML Class Diagram** from Workshop 3.

You should see concepts similar to:

* `Level`
* `TileMap` or `WorldGrid`
* `TileType`
* `Position` / `GridCoord`

🧠 **Reminder:**
UML is not decoration.
Your code should *look like* your diagram.

---

# 🧱 Part B — Create the World Module

## Step B1 — Folder Structure

Inside your repository:

```
/src/world/
```

Create the following files:

```
tile_type.py
position.py
tile_map.py
```

This separation keeps responsibilities clear.

---

# 🧩 Part C — Tile Types (What Exists in the World)

## Step C1 — Create `tile_type.py`

```python
from enum import Enum


class TileType(Enum):
    WALL = "#"
    PATH = "."
    START = "S"
    EXIT = "E"
```

🧠 **Why an Enum?**

* prevents invalid tiles
* improves readability
* matches UML `<<enumeration>>`

🧠 **Pac-Man mapping:**

* `#` → wall
* `.` → path
* `S` → player spawn
* `E` → exit or goal

Students may customize this for their game.

---

# 🧭 Part D — Position / Grid Coordinates

## Step D1 — Create `position.py`

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    row: int
    col: int
```

🧠 **Why a class for position?**

* avoids passing raw numbers everywhere
* improves readability
* easier to extend later
* matches UML design

🧠 **Important:**
`frozen=True` makes positions immutable — they represent **data**, not behaviour.

---

# 🧱 Part E — The TileMap (The Heart of the World)

## Step E1 — Create `tile_map.py`

```python
from tile_type import TileType
from position import Position


class TileMap:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
```

🧠 **What this does:**

* stores the world layout
* remembers its dimensions

---

## Step E2 — Bounds Checking

```python
    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols
```

🧠 **Why this matters:**
Objects should never assume the map is infinite.

---

## Step E3 — Tile Lookup

```python
    def get_tile(self, pos: Position) -> TileType:
        if not self.in_bounds(pos):
            return TileType.WALL
        return self.grid[pos.row][pos.col]
```

🧠 **Design choice:**
Out-of-bounds counts as a wall — safe default.

---

## Step E4 — Movement Rule (Key Method)

```python
    def is_walkable(self, pos: Position) -> bool:
        tile = self.get_tile(pos)
        return tile != TileType.WALL
```

🧠 **This method is critical.**
Every moving object will call this later.

---

# 🧪 Part F — Console Test (Prove the World Works)

Add this test at the bottom of `tile_map.py`:

```python
if __name__ == "__main__":
    grid = [
        [TileType.WALL, TileType.WALL, TileType.WALL],
        [TileType.WALL, TileType.PATH, TileType.WALL],
        [TileType.WALL, TileType.WALL, TileType.WALL],
    ]

    world = TileMap(grid)

    print(world.is_walkable(Position(1, 1)))  # True
    print(world.is_walkable(Position(0, 0)))  # False
    print(world.is_walkable(Position(5, 5)))  # False
```

### Expected Output

```text
True
False
False
```

If you see this, your world rules work.

---

# 🔁 Part G — Connecting Back to UML & Sequence Diagrams

Recall your **movement sequence diagram**:

```
Player → TileMap : isWalkable(nextPosition)
TileMap → Player : true / false
```

You have now implemented that interaction — **exactly**.

🧠 This is not accidental.
This is **model-driven development**.

---

# 🤖 Part H — Using Copilot Responsibly

You may use Copilot to:

* generate boilerplate
* check syntax
* speed up typing

But you must:

* understand every method
* ensure code matches UML
* rename concepts to match your game

### Suggested Copilot Prompt

```text
Generate a Python TileMap class that:
- stores a grid
- checks bounds
- returns tile types
- determines walkability
Use clean OOP design.
```

---

# 📦 Deliverables

Submit:

1. **World Code**

   * `tile_type.py`
   * `position.py`
   * `tile_map.py`

2. **Screenshot**

   * Console output showing walkability tests

---

## ✅ What You Learned

You now understand:

* why world rules belong in one class
* how UML class diagrams map to Python
* how to prevent logic duplication
* how to test systems without graphics
* how professional games are structured

This is **real OOP**.

---
