# 🧩 PROG1400 — Workshop 08

## Collisions & Interactions

### *Designing What Happens When Objects Meet (Explained Step by Step)*

---

## 1. Workshop Details

**Course:** PROG1400 – Object-Oriented Programming
**Week:** 8
**Workshop Title:** Collision Detection & Interaction Rules
**Workshop Type:** Guided Learning Workshop
**Estimated Time:** 2–3 hours
**Instructor:** Davis Boudreau (w0305171)

**Prerequisites:**

* Workshop 5 — Game State Machine
* Workshop 6 — World Grid & TileMap
* Workshop 7 — Player Movement

**Tools Required:**

* Visual Studio Code
* Python 3
* Existing PROG1400 repository

**Primary Learning Outcome:**
**Outcome 4 — Develop an object-oriented solution utilizing software modelling design documentation**

---

## 2. Why This Workshop Matters (Read This Carefully)

At this point, your game can:

* control **when** logic runs (state machine)
* control **where** movement is allowed (TileMap)
* move the player safely (validated movement)

But games are not interesting unless **objects interact**.

This workshop answers a fundamental question:

> **What should happen when two objects occupy the same space?**

This is called a **collision**.

In Pac-Man:

* Player + pellet → score increases
* Player + ghost (normal) → life lost
* Player + ghost (power mode) → ghost defeated

In *your* game, the objects and outcomes may be different —
but the **design pattern is the same**.

---

## 3. Big Idea: Collisions Are Rules, Not Accidents

A very common beginner mistake looks like this:

```python
# ❌ BAD: everything mixed together
if player.position == ghost.position:
    lives -= 1
```

Why this is bad:

* logic is duplicated everywhere
* behaviour depends on state, but state is ignored
* adding new collision rules becomes messy

A professional design separates concerns:

```python
# ✅ GOOD: responsibilities are clear
if CollisionSystem.has_collision(player, ghost):
    CollisionSystem.resolve_player_enemy(player, ghost, state_machine)
```

This workshop teaches you **how to build that separation**.

---

## 4. What You Will Build Today

By the end of this workshop, you will have:

1. A **base `Entity` class**
2. A **Player class that inherits from Entity**
3. A **CollisionSystem**
4. Collision rules that depend on **game state**
5. A **console-based simulation** that proves interactions work

Still no graphics — we are building the **engine**, not the UI.

---

# 🧠 Part A — Shared Concepts: The Entity Base Class

## Step A1 — Why We Need an Entity Class

Think about objects in your game:

* Player
* Enemy
* NPC
* Item
* Obstacle

All of these:

* exist in the world
* have a position
* can potentially collide

Instead of repeating the same code in every class, we create a **base class**.

This is called **inheritance**.

---

## Step A2 — Create `entity.py`

File location:

```
/src/entities/entity.py
```

```python
from position import Position
```

### 🔍 What this import means

* `position` is a Python file in your project
* `Position` is a class inside that file
* This allows `Entity` to *use* the `Position` type

This matches your UML:

> Entity **uses** Position

---

```python
class Entity:
    def __init__(self, position: Position):
        self.position = position
```

### 🔍 Line-by-line explanation

* `Entity` is a class (a blueprint)
* `__init__` runs when an object is created
* `position` is stored as part of the object

🧠 **OOP principle: Encapsulation**
Each entity *owns* its own position.

---

# 🧠 Part B — Player Inherits from Entity

## Step B1 — What “inherits” Means

When we say:

```python
class Player(Entity):
```

We are saying:

> “A Player **is an** Entity.”

That means:

* Player automatically has a `position`
* Player can collide with other entities
* Player can add *extra behaviour* later

---

## Step B2 — Update `player.py`

```python
from entities.entity import Entity
from position import Position
```

### 🔍 Import explanation

* `entities.entity` points to the `entity.py` file
* We import `Entity` so Player can inherit from it
* We import `Position` to pass coordinates when creating a Player

---

```python
class Player(Entity):
    def __init__(self, start_pos: Position):
        super().__init__(start_pos)
```

### 🔍 What `super().__init__()` means (very important)

* `super()` refers to the **parent class** (`Entity`)
* `__init__` is the constructor
* This line says:

> “When creating a Player, first run the Entity setup code.”

Without this line:

* Player would not have a position
* Collision detection would fail

🧠 **OOP principle:** *Code reuse through inheritance*

---

# 🧠 Part C — Collision System (Separate Responsibility)

## Step C1 — Why a CollisionSystem Class?

Collisions:

* are not movement
* are not player logic
* depend on **state**

So we isolate collision logic into its own **system class**.

This prevents logic from being scattered across:

* Player
* Enemy
* Game loop

---

## Step C2 — Create `collision_system.py`

File location:

```
/src/systems/collision_system.py
```

```python
class CollisionSystem:
```

This class groups **collision-related behaviour**.

---

## Step C3 — Collision Detection

```python
    @staticmethod
    def has_collision(entity_a, entity_b) -> bool:
        return entity_a.position == entity_b.position
```

### 🔍 What is `@staticmethod`?

Normally, methods:

* belong to an object (`self`)
* can access object data

A **static method**:

* does **not** use `self`
* does **not** store data
* performs a simple calculation or check
* is grouped inside a class for organization

🧠 Think of it as:

> “This function belongs conceptually to CollisionSystem, but it doesn’t need memory.”

This makes it perfect for **pure logic**.

---

# 🧠 Part D — Collision Resolution (Rules Live Here)

## Step D1 — Importing Game State

```python
from game_state_machine import GameState
```

### 🔍 Why import GameState?

Collision outcomes depend on:

* whether the game is playing
* whether power mode is active

We check **state**, not random flags.

---

## Step D2 — Resolving Player vs Enemy

```python
    @staticmethod
    def resolve_player_enemy(player, enemy, state_machine):
        if state_machine.state == GameState.PLAYING:
            state_machine.collision_normal()

        elif state_machine.state == GameState.POWER_MODE:
            enemy.defeated = True
```

### 🔍 What this code does

* Same collision
* Different outcome
* Decision based on **state**

This directly matches:

* your UML state diagram
* your UML sequence diagrams

🧠 **OOP principle:** *Separation of concerns*
CollisionSystem decides rules, not Player or Enemy.

---

# 🧪 Part E — Console Simulation (Proof It Works)

Create:

```
/src/test_collisions.py
```

---

## Step E1 — Imports Explained

```python
from position import Position
from entities.player import Player
from entities.entity import Entity
from systems.collision_system import CollisionSystem
from game_state_machine import GameStateMachine
```

Each import brings in **one responsibility**:

* Position → coordinates
* Player → movable object
* Entity → enemy placeholder
* CollisionSystem → collision rules
* GameStateMachine → game state

---

## Step E2 — Simulate a Collision

```python
player = Player(Position(1, 1))
ghost = Entity(Position(1, 1))
gsm = GameStateMachine()

print("Before collision:", gsm.state)

if CollisionSystem.has_collision(player, ghost):
    CollisionSystem.resolve_player_enemy(player, ghost, gsm)

print("After collision:", gsm.state)
```

---

### Expected Output

```text
Before collision: PLAYING
[STATE] PLAYING -> LIFE_LOST
After collision: LIFE_LOST
```

🧠 This proves:

* collision detected
* rules applied
* state changed correctly

---

# 🔁 Part F — Mapping Back to UML

Your UML said:

* Player and Ghost interact
* CollisionSystem resolves outcome
* GameStateMachine updates state

Your code does **exactly that**.

This is **model-driven development**.

---

## 📦 Deliverables

Submit:

1. `entity.py`
2. Updated `player.py`
3. `collision_system.py`
4. `test_collisions.py`
5. Screenshot of console output

---

## ✅ What You Learned

You now understand:

* why collisions are a system
* how inheritance reduces duplication
* what `super()` really does
* why `@staticmethod` is useful
* how UML becomes Python

You are now building **real game interactions**, not hacks.

---

## 🔮 Week 9 Preview

Next week, you will implement:

> **Collectibles & Scoring Systems**

Your game now reacts to collisions.
Next, it will **remember and reward**.
