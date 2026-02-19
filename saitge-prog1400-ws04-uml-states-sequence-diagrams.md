# 🧩 PROG1400 — Workshop 4

## Game States & UML Sequence Diagrams

*(Game States Document → Rules → State-Based Interaction Modelling)*

---

## 1. Assignment Details

**Course:** PROG1400 – Object-Oriented Programming
**Assignment:** 4
**Title:** Game States & UML Sequence Diagrams
**Type:** Design Assignment (Software Modelling)
**Estimated Effort:** 3–4 hours
**Prerequisites:**

* Assignment 3 — Game Rules & UML Class Diagram
* UML Class Diagram (`.mmd`) stored in your VS Code repository

**Tools Required:**

* Visual Studio Code
* GitHub Copilot (enabled in VS Code)
* VS Code Extension: **Mermaid Chart** (official)
* **Game States Document Template (Word)**
* Mermaid Online Editor: [https://www.mermaid.ai/app/dashboard](https://www.mermaid.ai/app/dashboard)

**Learning Outcome Addressed:**

> **Outcome 4**
> Develop an object-oriented solution utilizing software modelling design documentation.

---

## 2. Assignment Overview / Purpose

In **Assignment 3**, you designed **what exists** in your game:

* the rules of the game
* the structure of the system
* a UML class diagram

In **Assignment 4**, you will design **how your game behaves over time**.

Rather than modelling the entire game in a single diagram, you will:

> **Define your game states in a structured Word document, then create one UML sequence diagram per state.**

This mirrors how professional teams work:

* written requirements first
* behavioural modelling second
* implementation later

No game code is written in this assignment.

---

## 3. Learning Objectives

By completing this assignment, you will be able to:

* Identify and clearly define **game states**
* Associate specific **rules** with each state
* Use a structured design document as input for UML modelling
* Translate game states into **UML sequence diagrams**
* Use GitHub Copilot responsibly to assist with modelling
* Organize modelling artifacts in a professional repository structure

---

## 4. Key Concept: The Game State Document Is the Source of Truth

For this assignment:

> **Your Game States Word document is the authoritative design artifact.**

Everything else comes from it:

* Copilot prompts
* UML sequence diagrams
* PNG exports

If a rule or interaction is **not described in the Word document**, it should **not appear** in your UML.

---

## 5. Game States vs Rules (Reminder)

### Game Rules

Rules describe **constraints** and **logic**.

Example:

* “The player cannot move through walls.”

### Game States

States describe **when rules apply or change**.

Example:

* Playing
* PowerMode
* PlayerDead
* LevelComplete

> The same rule may behave differently depending on the state.

This is why you will create **one UML sequence diagram per state**.

---

## 6. Pac-Man Example Game States (Reference Only)

You may use these as inspiration.
You do **not** need to copy them exactly.

1. **Game Start / Level Initialization**

   * load level
   * reset positions
   * initialize entities

2. **Main Tick Update (Playing State)**

   * player movement
   * enemy movement
   * collision checks

3. **Power Pellet → Frightened Mode**

   * ghosts change behaviour
   * collision outcome reverses

4. **Collision (Normal) → Lose Life / Reset**

   * player loses a life
   * positions reset

5. *(Optional)* **Level Complete**

   * all objectives met
   * prepare next level

---

# 🧠 Part A — Complete the Game States Document (Required)

## Step A1 — Download and Rename the Template

Use the provided **Game States Document Template (Word)**.

Rename it using the required convention:

```
w#######-<game_name>-Game-States.docx
```

---

## Step A2 — Define Your Game States in Word

Using the template, define **2–5 game states**.

For **each state**, complete **all sections**:

* State Name
* Description
* Active Rules
* Objects Involved
* Expected Outcome

Be clear and specific.
This document will be used directly to generate UML.

---

## Important Rule

> If a state is not documented here, it must not have a UML sequence diagram.

---

# 🧠 Part B — Preparing for UML Sequence Diagrams

Before creating any UML:

1. Open your **UML Class Diagram (`.mmd`)**
2. Verify that all objects listed in the Word document:

   * exist as classes
   * have appropriate responsibilities
3. Identify for each state:

   * which object initiates actions
   * which object makes decisions
   * which objects respond

If inconsistencies exist, revise your design.

---

## CRC Thinking Still Applies

Use CRC logic:

* **Responsibility** → who decides?
* **Collaborator** → who is asked?

Sequence diagrams make this visible.

---

# 🤖 Part C — Using GitHub Copilot (Required)

GitHub Copilot is used as a **design assistant**, not an answer generator.

Your **Game States Document** is the input.

---

## Required Copilot Prompt Template

For each state, paste the following at the top of a new `.mmd` file
and replace the placeholders using text from your Word document:

```text
I am designing a game for a PROG1400 course.

Game state:
[STATE NAME]

State description:
[PASTE FROM GAME STATES DOCUMENT]

Active rules:
[PASTE RULES]

Objects involved:
[PASTE OBJECT LIST]

Generate a UML sequence diagram using Mermaid that shows:
- how objects interact in this state
- how the rules are enforced
- which object makes decisions
Use simple, beginner-friendly interactions.
```

You **must** review and edit the generated output.

You are responsible for correctness.

---

# 🧪 Part D — Create UML Sequence Diagrams (One per State)

## Step D1 — File Location & Naming

Inside your PROG1400 repository:

```
/docs/uml/
```

Create **one Mermaid file per state**:

```
w#######-<game_name>-UML-Sequence-<state>-01.mmd
```

Example:

```
w1234567-pacman_clone-UML-Sequence-PowerMode-01.mmd
```

---

## Step D2 — Diagram Requirements

Each UML sequence diagram must:

* represent **exactly one state**
* be derived from the Word document
* include only rules active in that state
* align with your UML class diagram
* use valid Mermaid syntax

---

# 👁️ Part E — Previewing in VS Code

To preview your diagram:

* Right-click inside the `.mmd` file
* Select **Open Mermaid Preview**

OR

* Press `Ctrl + Shift + P`
* Run **Mermaid: Preview Diagram**

---

# 🌐 Part F — Exporting PNGs (Required)

For **each state**:

1. Copy the Mermaid code
2. Go to: [https://www.mermaid.ai/app/dashboard](https://www.mermaid.ai/app/dashboard)
3. Paste the code
4. Choose **Layout → Adaptive**
5. Export as **PNG**

File naming:

```
w#######-<game_name>-UML-Sequence-<state>-01.png
```

---

# 📦 Part G — Deliverables (All Required)

Submit **all of the following**:

### 1. Game States Document (Word)

```
w#######-<game_name>-Game-States.docx
```

### 2. UML Sequence Diagrams

* One `.mmd` file per state
* One `.png` export per state

Upload all files to Brightspace.

---

## 8. Assessment Criteria (High-Level)

You will be assessed on:

* clarity and completeness of game states
* correct mapping of rules to states
* alignment between Word document and UML
* correctness and clarity of sequence diagrams
* correct repository structure and naming
* professional use of Copilot and Mermaid

---

## ✅ Assignment Summary

In this assignment, you:

* defined game behaviour using explicit states
* documented rules in a structured Word template
* used that document to drive UML modelling
* created one sequence diagram per state
* practised professional, rules-first design workflow

This is how real software teams model **behaviour before code**.

---
