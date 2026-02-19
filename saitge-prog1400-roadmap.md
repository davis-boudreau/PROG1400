# 🧭 PROG1400 — Weekly Learning Roadmap

## From Game Idea to Object-Oriented Implementation

This course is structured so that **every line of code is justified by design**.
You will never code “randomly” — each week builds on the previous one.

---

## 🧠 Phase 1 — Thinking Like an Object-Oriented Designer

*(Weeks 1–4: Design before code)*

### **Week 1 — Python & OOP Foundations**

**Focus:**

* Python basics
* Variables, control flow, functions
* Introduction to classes and objects

**Outcome:**
You understand *what* objects are and *why* we use them.

---

### **Week 2 — Object Identification (CRC)**

**Focus:**

* Game idea selection
* CRC (Class–Responsibility–Collaborator) tables
* Identifying objects and responsibilities

**Deliverable:**

* CRC table for your game

**Outcome:**
You can explain *what objects exist* and *what each one does*.

---

### **Week 3 — UML Class Diagrams (Structure)**

**Focus:**

* UML class diagrams
* World grid / maze representation
* Ownership and relationships

**Deliverable:**

* UML Class Diagram (`.mmd`)

**Outcome:**
You understand *how objects are structured* and *how they relate*.

---

### **Week 4 — Game Rules, States & UML Sequences**

**Focus:**

* Writing game rules (Word document)
* Identifying game states
* UML Sequence Diagrams (per state)

**Deliverables:**

* Game Rules document
* UML Sequence Diagrams

**Outcome:**
You understand *how objects interact over time*.

---

## ⚙️ Phase 2 — Control & Behaviour

*(Weeks 5–6: Behaviour without chaos)*

### **Week 5 — State Machines (Control Flow)**

**Focus:**

* UML State Diagrams
* Mapping states to Python `Enum`
* State machine controller
* Controlled transitions

**Deliverables:**

* UML State Diagram (`.mmd`)
* `game_state_machine.py`
* Console proof

**Outcome:**
You can control *when* behaviour is allowed to occur.

---

### **Week 6 — World Grid & TileMap (Rules Engine)**

**Focus:**

* Tile types
* Position / coordinates
* TileMap as rule authority
* Walkability validation

**Deliverables:**

* `tile_type.py`
* `position.py`
* `tile_map.py`
* Console tests

**Outcome:**
You understand *where rules belong* and how to centralize them.

---

## 🎮 Phase 3 — Gameplay Foundations

*(Weeks 7–9: Movement & interaction)*

### **Week 7 — Player Movement**

**Focus:**

* Movement intent vs movement execution
* Player → TileMap validation
* UML sequence → code mapping

**Deliverables:**

* `player.py`
* Movement test script

**Outcome:**
You can move an object *safely* inside a world.

---

### **Week 8 — Collisions & Interactions**

**Focus:**

* Player ↔ world collisions
* Player ↔ entity collisions
* Collision outcomes by state

**Deliverables:**

* Collision handling methods
* Updated sequence diagrams

**Outcome:**
You understand *what happens when things meet*.

---

### **Week 9 — Collectibles & Scoring**

**Focus:**

* Pellets / items
* Score tracking
* Item consumption rules

**Deliverables:**

* `ScoreManager` or equivalent
* Updated UML class diagram

**Outcome:**
You can model **systems**, not just objects.

---

## 🧠 Phase 4 — Advanced OOP Concepts

*(Weeks 10–12: Behaviour variation & reuse)*

### **Week 10 — Enemies & Inheritance**

**Focus:**

* Base `Entity` class
* Player vs enemy differences
* Inheritance & polymorphism

**Outcome:**
You understand **“is-a” relationships** in real code.

---

### **Week 11 — State-Based Behaviour**

**Focus:**

* Enemy behaviour by state
* Power mode / frightened mode
* State + polymorphism

**Outcome:**
You can combine **state machines** and **polymorphism**.

---

### **Week 12 — Win/Loss & Game Flow**

**Focus:**

* Lives
* Level progression
* Game over conditions

**Outcome:**
You can manage a complete game lifecycle.

---

## 🧹 Phase 5 — Integration & Reflection

*(Weeks 13–15: Professional polish)*

### **Week 13 — Refactoring & Cleanup**

**Focus:**

* Removing duplication
* Improving readability
* Aligning code to UML

**Outcome:**
You understand why **refactoring is normal and healthy**.

---

### **Week 14 — Integration & Testing**

**Focus:**

* Full game loop integration
* Manual testing strategies
* Bug isolation

**Outcome:**
You can reason about a complete system.

---

### **Week 15 — Final Project & Reflection**

**Focus:**

* Final game submission
* UML vs code comparison
* Reflection on OOP design

**Outcome:**
You can explain *why your design works* — not just that it does.

---

## 🧠 One-Sentence Course Summary

> **PROG1400 teaches you to design, control, and build an object-oriented system step by step — so your code grows logically instead of collapsing under its own complexity.**

---

