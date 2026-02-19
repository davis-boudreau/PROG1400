# 🧩 PROG1400 — Workshop 7

## Player Movement: From Intent → Validation → Update

### *Applying OOP, UML Sequence Diagrams, and World Rules*

---

## 1. Workshop Details

**Course:** PROG1400 – Object-Oriented Programming
**Week:** 7
**Workshop Title:** Player Movement Using TileMap Validation
**Workshop Type:** Guided Learning Workshop
**Estimated Time:** 2–3 hours
**Prerequisites:**

* Workshop 5 — Game State Machine (Python)
* Workshop 6 — World Grid & TileMap Implementation

**Tools Required:**

* Visual Studio Code
* Python 3
* Existing PROG1400 repository

**Primary Learning Outcome:**
**Outcome 4 — Develop an object-oriented solution utilizing software modelling design documentation**

---

## 2. Why This Workshop Matters (Read First)

You now have:

* a **state machine** that controls *when* the game can update
* a **TileMap** that controls *where* movement is allowed

What you **do not** yet have is:

> a clean way for a player to move *inside* the world.

This workshop teaches you the **professional movement pattern** used in real games:

> **Intent → Validation → Update**

Instead of letting the player “just move,” the player must:

1. **request** a move
2. **ask the world** if it is allowed
3. **update position only if permitted**

This prevents:

* walking through walls
* duplicated logic
* future collision bugs

---

## 3. Big Idea: The Player Does NOT Own the Rules

A beginner mistake looks like this:

```python
# ❌ BAD
self.row += 1
```

A professional design looks like this:

```python
# ✅ GOOD
if tile_map.is_walkable(next_position):
    self.position = next_position
```

Why?

Because:

* the **world** knows the rules
* the **player** follows them
* this separation scales to enemies, NPCs, and AI

---

## 4. What You Will Build Today

By the end of this workshop, you will have:

1. A **Player class**
2. A **movement intent method**
3. A **safe movement validation process**
4. Code that matches your **UML sequence diagram**
5. A **console-based movement simulation**

Still no graphics — and that’s intentional.

---

# 🧠 Part A — Revisit the UML Sequence Diagram (Design First)

Open your **movement UML sequence diagram** from Workshop 4.

It should resemble this Pac-Man reference:

```
Player → TileMap : isWalkable(nextPosition)
TileMap → Player : true / false
Player → Player : update position (if allowed)
```

🧠 **Key point:**
Movement is a *conversation* between objects — not a single line of code.

---

# 🧱 Part B — Create the Player Class

## Step B1 — File Structure

Inside your repository:

```
/src/entities/
```

Create:

```
player.py
```

---

## Step B2 — Player Class (Minimal and Focused)

```python
from position import Position


class Player:
    def __init__(self, start_pos: Position):
        self.position = start_pos
```

🧠 **Design note:**
The Player knows **where it is**, but not **where it is allowed to go**.

---

# 🧭 Part C — Movement Intent (Not Movement Yet)

## Step C1 — Define Direction Offsets

```python
DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}
```

🧠 This converts player input into **intent**, not action.

---

## Step C2 — Calculate the Next Position

```python
    def get_next_position(self, direction: str) -> Position:
        dr, dc = DIRECTIONS[direction]
        return Position(
            self.position.row + dr,
            self.position.col + dc
        )
```

🧠 **Important:**
This does **not** move the player.

It only asks: *“If I moved, where would I end up?”*

---

# 🧱 Part D — Validated Movement (The Core Pattern)

## Step D1 — Safe Movement Method

```python
    def try_move(self, direction: str, tile_map) -> bool:
        next_pos = self.get_next_position(direction)

        if tile_map.is_walkable(next_pos):
            self.position = next_pos
            return True

        return False
```

🧠 **This is the most important method so far.**

It ensures:

* the world controls movement rules
* the player never clips through walls
* all movement goes through one place

---

# 🧪 Part E — Console Simulation (Proof of Design)

Create a test file:

```
/src/test_player_movement.py
```

---

## Step E1 — Setup a Small World

```python
from tile_type import TileType
from tile_map import TileMap
from position import Position
from entities.player import Player

grid = [
    [TileType.WALL, TileType.WALL, TileType.WALL],
    [TileType.WALL, TileType.PATH, TileType.WALL],
    [TileType.WALL, TileType.PATH, TileType.WALL],
    [TileType.WALL, TileType.WALL, TileType.WALL],
]

world = TileMap(grid)
player = Player(Position(1, 1))
```

---

## Step E2 — Try Moving the Player

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

🧠 **Why LEFT didn’t work:**
There was a wall.
The TileMap blocked the move.

---

# 🔁 Part F — Connecting Back to UML & OOP

You have now implemented:

* **Encapsulation**
  World rules live in `TileMap`

* **Single Responsibility**
  Player handles intent, not rules

* **Abstraction**
  Player asks questions instead of inspecting grid data

* **Sequence Diagram Accuracy**
  Code matches the diagram exactly

This is **model-driven development**.

---

# 🤖 Part G — Using Copilot as a Learning Tool

You may use Copilot to help generate structure — but **you must understand the flow**.

### Suggested Copilot Prompt

```text
Generate a Python Player class that:
- stores a Position
- calculates a next position based on direction
- asks a TileMap if movement is allowed
- updates position only if permitted
Use clean OOP design.
```

Compare Copilot output to:

* your UML sequence diagram
* the code you wrote manually

Fix mismatches.

---

# 📦 Deliverables

Submit:

1. **Player class**

   * `player.py`

2. **Movement test**

   * `test_player_movement.py`

3. **Screenshot**

   * Console output showing at least:

     * one successful move
     * one blocked move

---

## ✅ What You Learned

You now know how to:

* implement movement *correctly*
* respect world boundaries
* map UML interactions into code
* prevent logic duplication
* prepare for enemies and AI

This is a **huge milestone**.

---
