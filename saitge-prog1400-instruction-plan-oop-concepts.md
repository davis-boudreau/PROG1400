# **Week 2 Instructional Plan – PROG1400**

**Focus:** Core OOP Principles
**Concepts:** Encapsulation & Abstraction
**UML State:** Pre-UML → preparing for **UML v1**
**Student Artifact:** Object & Responsibility Identification (feeds UML v1)

---

## 1. Instructional Intent (Why Week 2 Matters)

Week 2 is where students **stop thinking in terms of “code”** and start thinking in terms of:

> **Who is responsible for what?**

If Week 1 answers *“What am I building?”*,
Week 2 answers *“Who does the work in my game?”*

This is the **conceptual foundation** for UML v1 in Week 3.

---

## 2. Lesson Flow (Aligned to Your Instructional Planning Model)

### A. Hook (10–15 minutes)

**Instructor-Led: Pac-Man Responsibility Demo**

Do **not show code yet**.

Instead:

* Show Pac-Man gameplay (short clip or live demo)
* Ask the class:

> “When Pac-Man moves, who is responsible for that?”

Write responses on the board:

* Player?
* Pac-Man?
* Game?
* Maze?

Then ask:

> “What *should* know how to move — and what *should not*?”

This naturally introduces **encapsulation** without naming it yet.

---

### B. Concept Introduction (Encapsulation)

#### Key Message (Student-Friendly)

> **Encapsulation means an object manages its own data and behavior.**

Use Pac-Man examples:

| Object | What it SHOULD control              | What it should NOT control |
| ------ | ----------------------------------- | -------------------------- |
| PacMan | Position, direction, movement rules | Score display, enemy AI    |
| Ghost  | Movement behavior                   | Player input               |
| Maze   | Walls, valid paths                  | Player score               |

Say explicitly:

> “If another object needs something, it *asks* — it doesn’t reach inside.”

This sets up **access control** later without syntax.

---

### C. Concept Introduction (Abstraction)

Now introduce **abstraction**:

> **Abstraction means focusing on what an object does, not how it does it.**

Pac-Man example:

* Pac-Man can `move()`
* Ghosts can `move()`
* How they move is different

Ask:

> “What do Pac-Man and Ghosts have in common at a high level?”

You’re laying the groundwork for:

* shared responsibilities
* later inheritance / interfaces
* polymorphism (without naming it yet)

---

## 3. Guided Activity (Whole Class – Pac-Man)

### Activity: Responsibility Sorting (15–20 min)

On the board (or slides), list:

* Pac-Man
* Ghost
* Maze
* Pellet
* GameController

For each, ask:

* What data does this object own?
* What actions does it perform?

Example:

**Pac-Man**

* Data: position, direction
* Actions: move, collide

**Ghost**

* Data: position, state
* Actions: move, chase, scatter

Emphasize:

> “If an object owns the data, it owns the behavior.”

---

## 4. Student Application (Own Game)

### Individual / Small Group Activity (25–30 min)

Students now apply the **same thinking** to *their own game*.

#### Student Task: Object & Responsibility Sheet (Assessment – No Grade)

Students must produce:

### A. Object List (Minimum 5)

For each object:

* Name
* Responsibility (1–2 sentences)

Example (student game):

| Object         | Responsibility                            |
| -------------- | ----------------------------------------- |
| Player         | Controls movement and collisions          |
| Enemy          | Moves independently and challenges player |
| Item           | Can be collected for points               |
| Level          | Defines layout and obstacles              |
| GameController | Manages game state                        |

### B. Responsibility Check Questions

Students must answer:

1. Which object controls player movement?
2. Which object should NOT know the score?
3. Which object would change if you added another enemy?

These questions force abstraction thinking.

---

## 5. Assessment of Understanding (Formative)

### Assessment (No Grade)

* Object list + responsibilities
* Instructor circulates and checks for:

  * “God objects”
  * duplicated responsibilities
  * unclear ownership

You are **not correcting syntax** — only thinking.

---

## 6. Re-Assessment / Closure

### Closure Activity: 3-2-1 (5 minutes)

Students submit:

* **3 objects** they are confident about
* **2 responsibilities** they are unsure about
* **1 question** about object design

This gives you:

* early warning signs
* material to address in Week 3 UML

---

## 7. Explicit Bridge to Next Week (Critical)

End Week 2 by saying:

> “Next week, we will take the objects and responsibilities you identified and **lock them into your first UML class diagram (UML v1)**.
> Once UML v1 is created, your code must follow it.”

This frames UML as a **design contract**, not busywork.

---

## 8. What You Should NOT Do in Week 2

Avoid:

* UML notation rules
* Access modifiers (`private`, `public`)
* Inheritance
* Interfaces
* Writing full classes

Those belong later.

Week 2 is about **thinking**, not tooling.

---

## 9. Deliverables Summary (Week 2)

| Item                         | Type       | Purpose                           |
| ---------------------------- | ---------- | --------------------------------- |
| Object & Responsibility List | Assessment | Prepares UML v1                   |
| Practice Quiz                | Evaluation | Confirms conceptual understanding |
| 3-2-1 Reflection             | Assessment | Reveals misconceptions            |

---

## Instructor Verdict

✔ This approach:

* Keeps Pac-Man central
* Prevents premature coding
* Makes UML feel inevitable
* Smoothly sets up Week 3

If you want next, I can:

* Write the **Week 2 practice quiz**
* Create a **student worksheet** for object responsibilities
* Draft **exact instructor talking points / slides**
* Show **common Week 2 student mistakes** and how to respond

Just tell me what you want next.
