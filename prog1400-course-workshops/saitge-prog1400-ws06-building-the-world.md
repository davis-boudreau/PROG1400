# 🧩 PROG1400 — Workshop 10

## Enemies, Inheritance & Polymorphism

### *One Interface, Many Behaviours (Explained Step by Step)*

---

## 1. Workshop Details

**Course:** PROG1400 – Object-Oriented Programming
**Week:** 10
**Workshop Title:** Enemies & Inheritance
**Workshop Type:** Guided Learning Workshop
**Estimated Time:** 2–3 hours
**Instructor:** Davis Boudreau (w0305171)

**Prerequisites:**

* Workshop 6 — World Grid & TileMap
* Workshop 7 — Player Movement
* Workshop 8 — Collisions & Interactions
* Workshop 9 — Collectibles & Scoring

**Tools Required:**

* Visual Studio Code
* Python 3
* Existing PROG1400 repository

**Primary Learning Outcome:**
**Outcome 4 — Develop an object-oriented solution utilizing software modelling design documentation**

---

## 2. Why This Workshop Matters (Read This Carefully)

Up to now, your game has:

* a **Player**
* a **World**
* **Collisions**
* **Collectibles**
* **Scoring**

But games are not interesting without **opposition**.

This workshop introduces **enemies** — and more importantly:

> **How to design enemies without duplicating code**

Many beginners do this:

```python
ghost1_move()
ghost2_move()
ghost3_move()
```

That approach:

* does not scale
* creates bugs
* breaks OOP principles

This workshop teaches the professional approach:

> **One base class, many specialized behaviours**

---

## 3. Big Idea: Inheritance & Polymorphism

### Inheritance (Plain English)

Inheritance means:

> One class **reuses** another class’s code.

Example:

> A Ghost **is an** Entity

---

### Polymorphism (Plain English)

Polymorphism means:

> Different objects respond to the *same method call* in different ways.

Example:

```python
enemy.update()
```

* Ghost A chases
* Ghost B patrols
* Ghost C runs away

Same method name.
Different behaviour.

This workshop shows you **how to build that correctly**.

---

## 4. What You Will Build Today

By the end of this workshop, you will have:

1. A **base Enemy class**
2. Multiple **Enemy subclasses**
3. A shared `update()` interface
4. Different movement behaviours
5. A console simulation showing polymorphism in action

No AI yet — just **behaviour variation**.

---

# 🧠 Part A — Enemy Is an Entity

## Step A1 — Why Enemy Inherits from Entity

Enemies:

* exist in the world
* have positions
* move
* collide

This means:

> **Enemy is a specialized Entity**

---

## Step A2 — Create `enemy.py`

File location:

```
/src/entities/enemy.py
```

---

### Imports Explained

```python
from entities.entity import Entity
from position import Position
```

* `Entity` provides shared position logic
* `Position` represents grid coordinates

---

### Base Enemy Class

```python
class Enemy(Entity):
    def __init__(self, start_pos: Position):
        super().__init__(start_pos)
```

### 🔍 Explanation

* `Enemy` inherits from `Entity`
* `super().__init__(start_pos)`:

  * ensures the enemy has a position
* Enemy currently has **no behaviour**
* This is intentional

🧠 **OOP principle:** *Build simple, then extend*

---

# 🧠 Part B — The Update Contract

## Step B1 — Why `update()` Exists

Every moving object in a game eventually needs:

```python
enemy.update()
```

This method:

* is called once per game tick
* decides what the enemy does

By defining it in the base class, we create a **contract**.

---

## Step B2 — Add `update()` to Enemy

```python
class Enemy(Entity):
    def __init__(self, start_pos: Position):
        super().__init__(start_pos)

    def update(self, tile_map):
        pass
```

### 🔍 What `pass` means

* `pass` is a placeholder
* it allows subclasses to override behaviour
* the base class defines *what* must exist, not *how*

🧠 **This enables polymorphism.**

---

# 🧠 Part C — Creating Enemy Subclasses

Now we create **specific enemy behaviours**.

---

## Step C1 — Chasing Enemy (Pac-Man Reference)

Create:

```
/src/entities/chasing_enemy.py
```

---

```python
from entities.enemy import Enemy
from position import Position
```

---

```python
class ChasingEnemy(Enemy):
    def __init__(self, start_pos: Position):
        super().__init__(start_pos)

    def update(self, tile_map):
        # placeholder logic for now
        print("ChasingEnemy moves toward player")
```

### 🔍 Explanation

* Inherits from `Enemy`
* Overrides `update()`
* Same method name, different behaviour

🧠 **Polymorphism in action**

---

## Step C2 — Random Enemy

Create:

```
/src/entities/random_enemy.py
```

---

```python
from entities.enemy import Enemy
from position import Position
import random
```

### 🔍 Import explanation

* `random` is a Python standard library
* used to simulate unpredictable movement

---

```python
class RandomEnemy(Enemy):
    def __init__(self, start_pos: Position):
        super().__init__(start_pos)

    def update(self, tile_map):
        print("RandomEnemy moves randomly")
```

Each enemy responds differently to `update()`.

---

# 🧪 Part D — Demonstrating Polymorphism

Create:

```
/src/test_enemies.py
```

---

## Step D1 — Imports Explained

```python
from position import Position
from entities.chasing_enemy import ChasingEnemy
from entities.random_enemy import RandomEnemy
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

## Step D3 — Call `update()` on All Enemies

```python
for enemy in enemies:
    enemy.update(None)
```

---

### Expected Output

```text
ChasingEnemy moves toward player
RandomEnemy moves randomly
```

🧠 **Key insight:**
The loop doesn’t care *what type* of enemy it is.

It only knows:

> “This object has an `update()` method.”

That is **polymorphism**.

---

# 🔁 Part E — Connecting Back to UML

Your UML class diagram likely shows:

* `Enemy` extends `Entity`
* `ChasingEnemy` extends `Enemy`
* `RandomEnemy` extends `Enemy`

Your code now matches your UML **exactly**.

---

## 📦 Deliverables

Submit:

1. `enemy.py`
2. At least **two enemy subclasses**
3. `test_enemies.py`
4. Console output screenshot

---

## ✅ What You Learned

You now understand:

* how inheritance removes duplication
* how polymorphism enables flexibility
* why `update()` is a contract
* how professional games manage enemy behaviour
* how UML becomes real Python code

This is **core object-oriented programming**.

---

## 🔮 Week 11 Preview

Next week, you will combine:

> **Enemy Behaviour + Game State**

Enemies will:

* behave differently when powered up
* react to game modes
* use both **state machines** and **polymorphism**

You are now firmly in **real game architecture territory**.
