# 🧩 PROG1400 — Workshop 11

## State-Based Enemy Behaviour

### *Combining State Machines and Polymorphism (Explained Step by Step)*

---

## 1. Workshop Details

**Course:** PROG1400 – Object-Oriented Programming
**Week:** 11
**Workshop Title:** Enemy Behaviour Controlled by Game State
**Workshop Type:** Guided Learning Workshop
**Estimated Time:** 2–3 hours

**Prerequisites:**

* Workshop 5 — Game State Machine
* Workshop 6 — World Grid & TileMap
* Workshop 7 — Player Movement
* Workshop 8 — Collisions & Interactions
* Workshop 9 — Collectibles & Scoring
* Workshop 10 — Enemies, Inheritance & Polymorphism

**Tools Required:**

* Visual Studio Code
* Python 3
* Existing PROG1400 repository

**Primary Learning Outcome:**
**Outcome 4 — Develop an object-oriented solution utilizing software modelling design documentation**

## Instructional Notes

This is a major conceptual leap for students:
they learn how polymorphism + game state work together to control behaviour cleanly.

Everything is explained slowly and explicitly, assuming new OOP learners.

Pac-Man is again the reference case, but **students must apply the same ideas to their own game.**

---

## 2. Why This Workshop Matters (Read This Carefully)

Right now, your game has:

* enemies that can move
* different enemy *types*
* collisions and scoring
* a working game state machine

But something is missing.

In real games, **enemy behaviour changes depending on the game state**.

In Pac-Man:

* ghosts chase the player during normal play
* ghosts run away when a power pellet is active
* ghosts behave differently after being eaten

This workshop answers the question:

> **How do we change enemy behaviour without rewriting or duplicating code?**

The answer is:

> **State + polymorphism working together**

---

## 3. Big Idea: Behaviour Depends on Context

A beginner approach:

```python
# ❌ BAD: behaviour scattered everywhere
if power_mode:
    run_away()
else:
    chase()
```

Why this is bad:

* logic is duplicated
* rules leak into many classes
* hard to extend

A professional approach:

```python
# ✅ GOOD
enemy.update(tile_map, game_state)
```

The **enemy decides what to do**, based on the **current game state**.

---

## 4. What You Will Build Today

By the end of this workshop, you will have:

1. Enemies that **read the game state**
2. Behaviour that changes automatically when state changes
3. Clean separation between:

   * state management
   * enemy behaviour
4. A console simulation showing enemies reacting to state changes

This is where your design starts to feel *alive*.

---

# 🧠 Part A — Review the UML Design

Before coding, review your UML diagrams:

### UML State Diagram

* shows when the game enters `POWER_MODE`, `PLAYING`, etc.

### UML Class Diagram

* shows `Enemy` inheritance hierarchy

### UML Sequence Diagrams

* show interactions like:

  ```
  GameStateMachine → Enemy : update()
  ```

🧠 **Reminder:**
UML is not theoretical — it tells us *where logic belongs*.

---

# 🧱 Part B — Passing Game State into Enemies

## Step B1 — Why Enemies Need Game State

Enemies do **not** decide when power mode starts.
They only **react** to it.

Therefore:

* enemies should *read* game state
* enemies should *not modify* game state

This keeps responsibilities clean.

---

## Step B2 — Update the Enemy Base Class

Open:

```
/src/entities/enemy.py
```

Modify the `update()` method:

```python
class Enemy(Entity):
    def __init__(self, start_pos):
        super().__init__(start_pos)

    def update(self, tile_map, game_state):
        """
        Base enemy update method.
        Subclasses will override this.
        """
        pass
```

### 🔍 Explanation

* `game_state` is passed **in**, not stored
* Enemy does not own the state machine
* This prevents tight coupling

🧠 **OOP principle:** *Loose coupling*

---

# 🧠 Part C — State-Aware Enemy Subclasses

Now we update enemy behaviour based on state.

---

## Step C1 — Chasing Enemy with State Awareness

Open:

```
/src/entities/chasing_enemy.py
```

---

```python
from entities.enemy import Enemy
from game_state_machine import GameState
```

### 🔍 Import explanation

* `GameState` is an Enum
* Allows us to compare current game state safely

---

```python
class ChasingEnemy(Enemy):
    def update(self, tile_map, game_state):
        if game_state == GameState.PLAYING:
            print("ChasingEnemy chases the player")

        elif game_state == GameState.POWER_MODE:
            print("ChasingEnemy runs away from the player")
```

### 🔍 What this shows

* Same enemy
* Same `update()` method
* Different behaviour depending on state

🧠 **This is polymorphism + state working together**

---

## Step C2 — Random Enemy with State Awareness

Open:

```
/src/entities/random_enemy.py
```

---

```python
from entities.enemy import Enemy
from game_state_machine import GameState
import random
```

---

```python
class RandomEnemy(Enemy):
    def update(self, tile_map, game_state):
        if game_state == GameState.PLAYING:
            print("RandomEnemy moves randomly")

        elif game_state == GameState.POWER_MODE:
            print("RandomEnemy avoids the player")
```

Each enemy reacts differently — without duplicated logic.

---

# 🧪 Part D — Console Simulation (Learning Proof)

Create:

```
/src/test_enemy_states.py
```

---

## Step D1 — Imports Explained

```python
from position import Position
from entities.chasing_enemy import ChasingEnemy
from entities.random_enemy import RandomEnemy
from game_state_machine import GameState
```

---

## Step D2 — Create Enemies

```python
enemies = [
    ChasingEnemy(Position(1, 1)),
    RandomEnemy(Position(2, 2)),
]
```

---

## Step D3 — Simulate State Changes

```python
print("=== PLAYING STATE ===")
for enemy in enemies:
    enemy.update(None, GameState.PLAYING)

print("\n=== POWER MODE STATE ===")
for enemy in enemies:
    enemy.update(None, GameState.POWER_MODE)
```

---

### Expected Output

```text
=== PLAYING STATE ===
ChasingEnemy chases the player
RandomEnemy moves randomly

=== POWER MODE STATE ===
ChasingEnemy runs away from the player
RandomEnemy avoids the player
```

🧠 **Important insight:**
No `if enemy_type == ...` anywhere.

The code doesn’t care *what* the enemy is —
it just calls `update()`.

---

# 🔁 Part E — Mapping Back to UML

Your UML diagrams show:

* Enemy subclasses
* Behaviour changes by state
* Game state influences interaction

Your code now matches the **design exactly**.

This is **model-driven development** in action.

---

## 📦 Deliverables

Submit:

1. Updated enemy subclasses (`chasing_enemy.py`, `random_enemy.py`)
2. Updated base `enemy.py`
3. `test_enemy_states.py`
4. Console output screenshot showing **two states**

---

## ✅ What You Learned

You now understand:

* how game state affects behaviour
* how to avoid giant `if` blocks
* how polymorphism simplifies logic
* how systems collaborate cleanly
* how professional games scale behaviour

This is **advanced OOP**, built step by step.

---

## 🔮 Week 12 Preview

Next week, you will implement:

> **Win / Lose Conditions & Game Flow**

You already have:

* states
* enemies
* collisions
* scoring

Next, you decide:

> **When does the game end — and why?**

You are now building a *complete system*.
