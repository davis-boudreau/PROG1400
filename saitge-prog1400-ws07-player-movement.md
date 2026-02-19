# 🧩 PROG1400 — Workshop 07

## Player Movement Using World Rules

### *From UML Sequence Diagrams to Safe, Professional Python Code*

---

## 1. Workshop Details

**Course:** PROG1400 – Object-Oriented Programming
**Week:** 7
**Workshop Title:** Player Movement with TileMap Validation
**Workshop Type:** Guided Learning Workshop
**Estimated Time:** 2–3 hours
**Instructor:** Davis Boudreau (w0305171)

**Prerequisites:**

* Workshop 5 — Game State Machine
* Workshop 6 — World Grid & TileMap

**Tools Required:**

* Visual Studio Code
* Python 3
* Existing PROG1400 repository

**Primary Learning Outcome:**
**Outcome 4 — Develop an object-oriented solution utilizing software modelling design documentation**

---

## 2. Why This Workshop Matters (Read First)

Your game now has:

* a **state machine** that controls *when* updates happen
* a **TileMap** that controls *where* movement is allowed

But nothing actually moves yet.

This workshop answers the question:

> **How does an object move safely inside a world without breaking the rules?**

The answer is **not**:

```python
self.row += 1
```

The correct answer is:

> *Movement is a conversation between the player and the world.*

---

## 3. Big Idea: Intent → Validation → Update

Professional movement follows **three steps**:

1. **Intent**
   “I want to move right.”

2. **Validation**
   “World, is this allowed?”

3. **Update**
   “Yes → update position”
   “No → stay where you are”

This workshop teaches you how to implement that pattern cleanly.

---

## 4. What You Will Build Today

By the end of this workshop, you will have:

1. A **Player class**
2. A **direction system**
3. A method to calculate a *potential* move
4. A method to *validate* movement using the TileMap
5. A console test proving movement works

Still no graphics — this is **engine-level logic**.

---

# 🧠 Part A — Review the UML Sequence Diagram

Before coding, open your **movement UML sequence diagram** from Workshop 4.

It should resemble:

```
Player → TileMap : isWalkable(nextPosition)
TileMap → Player : true / false
Player → Player : update position
```

🧠 **Key point:**
The player never looks at the grid directly.

---

# 🧱 Part B — Player Class Structure

## Step B1 — File Location

Create:

```
/src/entities/player.py
```

Keeping entities in their own folder reinforces **separation of concerns**.

---

## Step B2 — Imports Explained

```python
from position import Position
```

### 🔍 What this import does

* `position` is a file in your project
* `Position` is a class defined in that file
* This allows the Player to **use Position objects**

🧠 This matches UML:

> Player **uses** Position

---

## Step B3 — Player Class Definition

```python
class Player:
    def __init__(self, start_pos: Position):
        self.position = start_pos
```

### 🔍 What’s happening here

* `Player` is a class (a blueprint)
* `__init__` runs when a Player object is created
* `position` is stored as part of the player’s state

🧠 **OOP principle:** *Encapsulation*
The player owns its own position.

---

# 🧭 Part C — Directions as Data (Not Logic)

## Step C1 — Direction Dictionary

```python
DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}
```

### 🔍 Why a dictionary?

* keys are **intent** (`"UP"`, `"LEFT"`)
* values are **row/column offsets**
* easy to read
* easy to extend

🧠 **Design principle:**
Data-driven design > hardcoded logic.

---

# 🧠 Part D — Calculating the Next Position (Intent Only)

## Step D1 — Next Position Method

```python
    def get_next_position(self, direction: str) -> Position:
        dr, dc = DIRECTIONS[direction]
        return Position(
            self.position.row + dr,
            self.position.col + dc
        )
```

### 🔍 Line-by-line explanation

* `direction` is a string like `"UP"`
* `dr, dc` unpack the movement offset
* A **new Position** is created
* The player is **not moved yet**

🧠 **Critical idea:**
This method answers:

> *“If I moved, where would I go?”*

---

# 🧱 Part E — Validated Movement (The Core Pattern)

## Step E1 — Importing the World

```python
    def try_move(self, direction: str, tile_map) -> bool:
```

### 🔍 Why pass `tile_map`?

* The player does not own the world
* The player must *ask* the world for permission

🧠 **OOP principle:** *Separation of concerns*

---

## Step E2 — Movement Logic Explained

```python
        next_pos = self.get_next_position(direction)
```

* calculate intent
* no movement yet

---

```python
        if tile_map.is_walkable(next_pos):
            self.position = next_pos
            return True
```

* ask the TileMap if the move is allowed
* update position only if allowed
* return `True` to indicate success

---

```python
        return False
```

* movement blocked
* player stays in place

🧠 **This method guarantees:**

* no wall clipping
* no duplicated rules
* safe movement everywhere

---

# 🧪 Part F — Testing Movement (Console Simulation)

Create:

```
/src/test_player_movement.py
```

---

## Step F1 — Imports Explained

```python
from tile_type import TileType
from tile_map import TileMap
from position import Position
from entities.player import Player
```

Each import brings in **one responsibility**:

* TileType → what tiles exist
* TileMap → world rules
* Position → coordinates
* Player → movable object

---

## Step F2 — Create a Small World

```python
grid = [
    [TileType.WALL, TileType.WALL, TileType.WALL],
    [TileType.WALL, TileType.PATH, TileType.WALL],
    [TileType.WALL, TileType.PATH, TileType.WALL],
    [TileType.WALL, TileType.WALL, TileType.WALL],
]

world = TileMap(grid)
player = Player(Position(1, 1))
```

🧠 Player starts inside a valid path tile.

---

## Step F3 — Try Moving the Player

```python
print("Start:", player.position)

player.try_move("DOWN", world)
print("After DOWN:", player.position)

player.try_move("LEFT", world)
print("After LEFT:", player.position)
```

---

## Expected Output

```text
Start: Position(row=1, col=1)
After DOWN: Position(row=2, col=1)
After LEFT: Position(row=2, col=1)
```

🧠 **Why LEFT failed:**
There was a wall.
The world blocked the move.

---

# 🔁 Part G — Mapping Back to UML

Your UML sequence diagram said:

* Player asks TileMap
* TileMap responds
* Player updates itself

Your code does **exactly that**.

This is **model-driven development**.

---

## 📦 Deliverables

Submit:

1. `player.py`
2. `test_player_movement.py`
3. Console screenshot showing:

   * one successful move
   * one blocked move

---

## ✅ What You Learned

You now understand:

* why movement is a process
* how to separate intent from rules
* how objects collaborate
* how UML becomes Python
* how to prevent beginner mistakes

This is **real OOP thinking**.

---

## 🔮 Week 8 Preview

Next week, you will decide:

> **What happens when objects collide**

Movement is working.
Next, the game reacts.
