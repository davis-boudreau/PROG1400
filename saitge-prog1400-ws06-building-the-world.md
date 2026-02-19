# 🧩 PROG1400 — Workshop 06

## Building the World: TileMap, Grid, and Movement Rules

### *Turning UML Class Diagrams into Python (Explained Line by Line)*

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
* Workshop 5 — Game State Machine

**Tools Required:**

* Visual Studio Code
* Python 3
* Existing PROG1400 repository

**Primary Learning Outcome:**
**Outcome 4 — Develop an object-oriented solution utilizing software modelling design documentation**

---

## 2. Why This Workshop Matters (Read First)

So far, you have controlled **when** things happen using a **state machine**.

Now you will define **where** things are allowed to exist and move.

This workshop builds the **world itself** — the part of the game that:

* stores the layout
* defines walls and paths
* answers movement questions

> The world does **not** move.
> The world enforces rules.

This is a critical object-oriented idea.

---

## 3. Big Idea: World Rules Live in One Place

A beginner mistake is letting the player decide what is allowed:

```python
# ❌ BAD
if grid[row][col] != "#":
    move_player()
```

A professional design looks like this:

```python
# ✅ GOOD
if tile_map.is_walkable(position):
    move_player()
```

The rule belongs to the **world**, not the player.

---

## 4. What You Will Build Today

By the end of this workshop, you will have:

1. A **TileType Enum**
2. A **Position class**
3. A **TileMap class**
4. Clean methods for:

   * bounds checking
   * tile lookup
   * walkability validation
5. A console test proving the world works

---

# 🧠 Part A — Folder Structure & Imports

Before coding, create this structure:

```
/src/world/
    tile_type.py
    position.py
    tile_map.py
```

Separating files helps keep **responsibilities clear**.

---

# 🧩 Part B — Tile Types (`tile_type.py`)

## Step B1 — Why an Enum?

A tile can only be one of a **fixed set of values**.

Using an `Enum`:

* prevents invalid tiles
* improves readability
* matches UML `<<enumeration>>`

---

## Step B2 — Code with Explanation

```python
from enum import Enum
```

### 🔍 Import explanation

* `enum` is part of Python’s standard library
* `Enum` allows us to define named constants

---

```python
class TileType(Enum):
    WALL = "#"
    PATH = "."
    START = "S"
    EXIT = "E"
```

### 🔍 Line-by-line meaning

* `TileType` is a **new type**
* Each entry is a possible tile
* The symbols (`"#"`, `"."`) are how tiles might appear in a text map

🧠 **OOP idea:** *Abstraction* — we use names instead of raw symbols.

---

# 🧭 Part C — Position Class (`position.py`)

## Step C1 — Why a Position Class?

Instead of passing `(row, col)` everywhere, we wrap them in an object.

Benefits:

* clearer code
* fewer bugs
* easier to extend later

---

## Step C2 — Code with Explanation

```python
from dataclasses import dataclass
```

### 🔍 Import explanation

* `dataclasses` automatically generate common methods
* reduces boilerplate code

---

```python
@dataclass(frozen=True)
class Position:
    row: int
    col: int
```

### 🔍 What this means

* `@dataclass` creates:

  * `__init__`
  * `__repr__`
  * `__eq__`
* `frozen=True` means:

  * position cannot change
  * positions represent **data**, not behaviour

🧠 **OOP idea:** *Immutability* improves safety.

---

# 🧱 Part D — TileMap Class (`tile_map.py`)

## Step D1 — Imports Explained

```python
from tile_type import TileType
from position import Position
```

### 🔍 Why these imports?

* `TileMap` needs to know:

  * what tile types exist
  * how positions are represented

This mirrors the UML relationship:

> TileMap **uses** Position and TileType

---

## Step D2 — Constructor (`__init__`)

```python
class TileMap:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
```

### 🔍 What happens here?

* `grid` is a 2D list of `TileType`
* `rows` and `cols` are cached for fast checks
* this object now **owns the world data**

🧠 **OOP idea:** *Encapsulation* — world data lives inside TileMap.

---

## Step D3 — Bounds Checking

```python
    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols
```

### 🔍 Why this matters

* prevents index errors
* defines the edges of the world

🧠 **Rule:** Anything outside the map is invalid.

---

## Step D4 — Tile Lookup

```python
    def get_tile(self, pos: Position) -> TileType:
        if not self.in_bounds(pos):
            return TileType.WALL
        return self.grid[pos.row][pos.col]
```

### 🔍 Design decision explained

* Out-of-bounds counts as a wall
* This avoids checking bounds everywhere else

🧠 **OOP idea:** *Fail-safe defaults*

---

## Step D5 — Walkability Rule

```python
    def is_walkable(self, pos: Position) -> bool:
        tile = self.get_tile(pos)
        return tile != TileType.WALL
```

### 🔍 Why this method is important

* every moving object will call this
* rules are centralized
* future changes happen here only

🧠 **This method is the “gatekeeper” of movement.**

---

# 🧪 Part E — Console Test (Proof the World Works)

Add this to the bottom of `tile_map.py`:

```python
if __name__ == "__main__":
    grid = [
        [TileType.WALL, TileType.WALL, TileType.WALL],
        [TileType.WALL, TileType.PATH, TileType.WALL],
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

---

# 🔁 Part F — Mapping Back to UML

Your UML class diagram said:

* TileMap **owns** grid
* TileMap **uses** Position
* TileMap **returns** TileType

You have now implemented that diagram **exactly**.

---

## 📦 Deliverables

Submit:

1. `tile_type.py`
2. `position.py`
3. `tile_map.py`
4. Console test screenshot

---

## ✅ What You Learned

You now understand:

* how enums model fixed concepts
* why dataclasses are useful
* how imports connect classes
* where rules belong in OOP
* how UML becomes Python

This is **foundational game architecture**.

---
