# 🧩 PROG1400 — Workshop 09

## Collectibles & Scoring Systems

### *Turning Interactions into Progress and Reward (Explained Step by Step)*

---

## 1. Workshop Details

**Course:** PROG1400 – Object-Oriented Programming
**Week:** 9
**Workshop Title:** Collectibles & Scoring
**Workshop Type:** Guided Learning Workshop
**Estimated Time:** 2–3 hours

**Prerequisites:**

* Workshop 5 — Game State Machine
* Workshop 6 — World Grid & TileMap
* Workshop 7 — Player Movement
* Workshop 8 — Collisions & Interactions

**Tools Required:**

* Visual Studio Code
* Python 3
* Existing PROG1400 repository

**Primary Learning Outcome:**
**Outcome 4 — Develop an object-oriented solution utilizing software modelling design documentation**

---

## 2. Why This Workshop Matters (Read First)

Your game can now:

* control **when** logic runs (state machine)
* control **where** movement is allowed (TileMap)
* move the player safely
* detect and resolve collisions

But right now, collisions only cause *consequences* (like losing a life).

Games also need **reward**.

This workshop answers a key question:

> **What should happen when the player collects something?**

In Pac-Man:

* Player + pellet → score increases
* Player + power pellet → score + state change

In *your* game:

* coins, gems, keys, pickups, objectives, etc.

The **pattern is universal**.

---

## 3. Big Idea: Collectibles Are Objects, Scoring Is a System

A common beginner mistake:

```python
# ❌ BAD: scoring logic mixed everywhere
score += 10
```

Why this is bad:

* scoring rules are duplicated
* score updates are hard to track
* changes require editing many files

A professional approach:

```python
# ✅ GOOD
score_manager.add_points(10)
```

Why?

* scoring rules live in one place
* easier to debug and extend
* matches real game architecture

---

## 4. What You Will Build Today

By the end of this workshop, you will have:

1. A **Collectible entity**
2. A **ScoreManager system**
3. Collision-based collection logic
4. Clean separation between:

   * object existence
   * interaction detection
   * scoring rules
5. A console simulation proving it works

Still no graphics — we are strengthening the **game engine**.

---

# 🧠 Part A — Collectibles as Entities

## Step A1 — Why Collectibles Are Entities

A collectible:

* exists in the world
* has a position
* can be collided with
* may be removed after collection

That makes it an **Entity**.

---

## Step A2 — Create `collectible.py`

File location:

```
/src/entities/collectible.py
```

```python
from entities.entity import Entity
from position import Position
```

### 🔍 Import explanation

* `Entity` → base class (position, collision capability)
* `Position` → location in the world

---

```python
class Collectible(Entity):
    def __init__(self, position: Position, value: int):
        super().__init__(position)
        self.value = value
        self.collected = False
```

### 🔍 Line-by-line explanation

* `Collectible` **inherits** from `Entity`
* `super().__init__(position)`:

  * ensures the collectible has a position
* `value`:

  * how many points this item is worth
* `collected`:

  * prevents collecting the same item twice

🧠 **OOP principle:** *Encapsulation*
The collectible knows its own value and state.

---

# 🧠 Part B — Scoring as a System (Not an Entity)

## Step B1 — Why Score Is Not an Entity

Score:

* does not exist in the world
* does not have a position
* should not collide with anything

Score is **game-wide information**, so it belongs in a **system class**.

---

## Step B2 — Create `score_manager.py`

File location:

```
/src/systems/score_manager.py
```

```python
class ScoreManager:
    def __init__(self):
        self.score = 0
```

### 🔍 What this does

* initializes score to zero
* stores score in one place

---

## Step B3 — Adding Points

```python
    def add_points(self, amount: int):
        self.score += amount
        print(f"[SCORE] +{amount} → Total: {self.score}")
```

### 🔍 Why this method matters

* all score changes go through one method
* easy to debug
* easy to modify later (multipliers, bonuses, etc.)

🧠 **Design principle:** *Single Responsibility*

---

# 🧠 Part C — Collectible Collision Logic

## Step C1 — Update Collision System

Open:

```
/src/systems/collision_system.py
```

Add a new resolution method:

```python
    @staticmethod
    def resolve_player_collectible(player, collectible, score_manager):
        if not collectible.collected:
            collectible.collected = True
            score_manager.add_points(collectible.value)
```

### 🔍 Explanation

* check if already collected
* mark as collected
* update score via the ScoreManager

🧠 **Important:**
CollisionSystem still decides *rules*, not Player.

---

# 🧪 Part D — Console Simulation (Learning Proof)

Create:

```
/src/test_collectibles.py
```

---

## Step D1 — Imports Explained

```python
from position import Position
from entities.player import Player
from entities.collectible import Collectible
from systems.score_manager import ScoreManager
from systems.collision_system import CollisionSystem
```

Each import brings in **one responsibility**.

---

## Step D2 — Simulate Collecting an Item

```python
player = Player(Position(1, 1))
coin = Collectible(Position(1, 1), value=10)
score_manager = ScoreManager()

print("Initial score:", score_manager.score)

if CollisionSystem.has_collision(player, coin):
    CollisionSystem.resolve_player_collectible(player, coin, score_manager)

print("Final score:", score_manager.score)
```

---

### Expected Output

```text
Initial score: 0
[SCORE] +10 → Total: 10
Final score: 10
```

🧠 This proves:

* collision detected
* collectible consumed
* score updated correctly

---

# 🔁 Part E — Mapping Back to UML

Your UML sequence diagram likely shows:

```
Player → CollisionSystem : checkCollision()
CollisionSystem → ScoreManager : addPoints()
```

You have now implemented this **exactly**.

---

## 📦 Deliverables

Submit:

1. `collectible.py`
2. `score_manager.py`
3. Updated `collision_system.py`
4. `test_collectibles.py`
5. Console output screenshot

---

## ✅ What You Learned

You now understand:

* why collectibles are entities
* why scoring is a system
* how to prevent duplicate collection
* how to centralize reward logic
* how UML becomes Python systems

You are now building **game progression**, not just mechanics.

---

## 🔮 Week 10 Preview

Next week, you will introduce:

> **Enemies & Inheritance**
> Base `Entity` → Specialized Enemy Types

Your game can now:

* move
* collide
* reward

Next, it will **challenge the player**.
