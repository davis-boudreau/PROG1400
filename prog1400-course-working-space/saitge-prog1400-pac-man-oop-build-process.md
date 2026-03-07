## Pac-Man OOP Build Process (end-to-end)

### 1) Define the game “contract”

**Produce**

* One-page **Game Spec**: win/lose conditions, scoring rules, level rules, input rules, timings
* A short **glossary** of terms (tile, pellet, power pellet, ghost state, collision)

**OOP alignment**

* Problem decomposition
* Turning requirements into **objects, responsibilities, and rules**

---

### 2) Identify the main objects and responsibilities

**Produce**

* Object list (classes) + a **responsibility table** (owns data / performs actions / must not do)
* Initial relationships: “has-a”, “uses”, “contains”

**Typical “parent” objects**

* `Game`, `World/Level`, `TileMap`
* `Entity` (base), `MovableEntity` (optional)
* `Player` (Pacman), `Ghost` (base) → `Blinky/Inky/Pinky/Clyde`
* `Pellet`, `PowerPellet`, `Fruit`
* `ScoreManager`, `LifeManager`, `InputHandler`, `CollisionSystem`, `Renderer`

**OOP alignment**

* Classes vs objects
* **Responsibility-driven design**
* Early **encapsulation boundaries**

---

### 3) Model the world (grid/tile map)

**Produce**

* Level representation (2D grid, tile codes, walls, paths)
* Load a level from a simple text file / array

**OOP alignment**

* Encapsulation: `TileMap` hides storage details
* Separation of concerns: world data vs entity behavior

---

### 4) Create the game loop architecture

**Produce**

* A `Game` loop that calls `update(dt)` and `render()`
* A clear “single source of truth” order:

  1. read input
  2. decide intent (direction)
  3. move
  4. resolve collisions
  5. apply rules (score, power mode, win/lose)
  6. render

**OOP alignment**

* Object collaboration
* “Who owns the loop?” / orchestration role of `Game`

---

### 5) Build the Entity base class

**Produce**

* `Entity` with shared fields (position, sprite, bounds)
* Common methods (`update`, `draw`, `getBounds`)

**OOP alignment**

* **Inheritance** (or composition alternative)
* Shared interface / shared behavior

---

### 6) Implement movement as a reusable component

**Produce**

* A `MovementController` or `Velocity`/`Direction` model
* Movement rules: grid snapping, turn rules, wall blocking

**OOP alignment**

* Composition (“movement is a component”)
* Encapsulation of tricky logic (movement isn’t scattered everywhere)

---

### 7) Implement the Player (Pacman)

**Produce**

* `Player` extends `Entity`
* Input → intent → movement
* Mouth animation (optional), lives handling hooks

**OOP alignment**

* Encapsulation: player state is private, modified through methods
* Clear responsibility: player *doesn’t* manage world rules

---

### 8) Implement collectibles (pellets, power pellets, fruit)

**Produce**

* `Collectible` base (or interface)
* `Pellet`, `PowerPellet`, `Fruit` subclasses
* Consumption rules + scoring hooks

**OOP alignment**

* Polymorphism: `onCollected(byEntity)` differs by item type
* Open/Closed Principle feel: add new collectible without rewriting the engine

---

### 9) Build the collision system

**Produce**

* `CollisionSystem` that can detect:

  * player vs walls (blocking)
  * player vs collectible (consume)
  * player vs ghost (life/state interaction)

**OOP alignment**

* Single responsibility: collisions are centralized
* Collaboration: collisions trigger events into other objects

---

### 10) Implement Ghost base + ghost AI strategy

**Produce**

* `Ghost` base: position, speed, state, home box rules
* Movement decision logic using:

  * **Strategy pattern** (simple version): each ghost has a `TargetingStrategy`
  * Or per-ghost override method `getTargetTile()`

**OOP alignment**

* **Polymorphism** in a way students *feel*: each ghost behaves differently
* “Template method” style: shared ghost update flow + customized target

---

### 11) Model Ghost states (Chase / Scatter / Frightened / Eaten)

**Produce**

* `GhostState` enum + state machine logic
* Timer-based transitions, speed changes, behavior changes

**OOP alignment**

* State modeling (often the first “serious” OOP design win)
* Encapsulation: state transitions live in ghost/state system—not in Game UI code

---

### 12) Power mode + rule system

**Produce**

* `PowerModeController` (timer, effects)
* Rule: when power pellet eaten → ghosts frightened; collisions flip outcomes

**OOP alignment**

* Clear boundaries between “rules” and “entities”
* Avoiding god-class Game: controllers coordinate but don’t *become* everything

---

### 13) Scoring + HUD

**Produce**

* `ScoreManager` (points, multipliers for ghost chain in power mode)
* HUD drawing

**OOP alignment**

* Encapsulation + single responsibility
* Data ownership (score isn’t stored inside random classes)

---

### 14) Lives, respawn, and round reset

**Produce**

* `LifeManager`
* Spawn points, reset positions, reset states, pause after death

**OOP alignment**

* Lifecycle management
* Coordinating resets without spaghetti: `Level.resetRound()` etc.

---

### 15) Win/lose conditions + level progression

**Produce**

* Rule: all pellets consumed → next level
* Lose when lives reach 0
* Level manager loads maps in sequence

**OOP alignment**

* Composition: `Game` contains `LevelManager`
* Clean “state of the game” modeling

---

### 16) Sound, polish, and performance cleanup

**Produce**

* Sound manager (optional)
* Refactors: reduce duplication, improve naming, constants/config
* Simple profiling (don’t overdo it)

**OOP alignment**

* Refactoring as part of OOP practice
* Maintainability: students experience why structure matters

---

### 17) Testing harness (even minimal)

**Produce**

* Micro-tests / debug tools:

  * collision debug overlay
  * tile occupancy checks
  * “step mode” for movement
  * deterministic ghost choice mode (seeded)

**OOP alignment**

* Designing for testability (dependency control)
* Confidence-building tooling

---
