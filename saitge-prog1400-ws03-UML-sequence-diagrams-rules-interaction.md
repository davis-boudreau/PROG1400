# 🧩 PROG1400 — Workshop 3

## Game Rules → UML Class Design using Copilot & Mermaid

---

## 1. Assignment Details

**Course:** PROG1400 – Object-Oriented Programming
**Workshop:** 3
**Title:** Game Rules & UML Class Design (Mermaid + Copilot)
**Type:** Guided Design Workshop
**Estimated Time:** 2–3 hours
**Prerequisite:**

* Workshop 2 — CRC / Responsibility Table
* A basic game idea (student-defined)

**Tools Required:**

* Visual Studio Code
* GitHub Copilot (enabled in VS Code)
* VS Code Extension: **Mermaid Chart** (official)
* Mermaid Online Editor: [https://www.mermaid.ai/app/dashboard](https://www.mermaid.ai/app/dashboard)

**Learning Outcome Addressed:**

> **Outcome 4**
> Develop an object-oriented solution utilizing software modelling design documentation.

---

## 2. Overview / Purpose

Before writing code, professional developers **define the rules of the system**.

In this workshop, you will:

1. Clearly define the **rules of your game**
2. Use those rules to **design UML classes**
3. Use **GitHub Copilot** to help generate Mermaid UML code
4. Store and manage UML design artifacts in your **PROG1400 VS Code repository**

This workshop emphasizes **design thinking before coding**.

No game code is written in this workshop.

---

## 3. Learning Objectives

By the end of this workshop, you will be able to:

* Describe your game using clear, structured rules
* Translate game rules into object-oriented design
* Use Copilot to assist with UML modelling
* Create UML Class Diagrams using Mermaid
* Organize design documentation professionally in VS Code
* Export and submit UML diagrams correctly

---

## 4. Why We Start with Game Rules

Game rules define:

* what exists in the game
* what actions are allowed
* what constraints apply
* how the game progresses or ends

Without rules, UML diagrams are guesswork.

### Rule-first design helps you:

* avoid missing classes
* avoid incorrect responsibilities
* build cleaner object models
* design before you implement

In this workshop:

> **Rules come first. UML comes second.**

---

# 🧠 Part A — Define Your Game Rules (Design First)

## Step A1 — Choose Your Game Idea

Choose a simple game idea. Examples:

* Pac-Man–style maze game
* Grid-based puzzle game
* Turn-based board game
* Arena survival game

Your game **does not need to be complex**.

---

## Step A2 — Write Your Game Rules (Required)

You must define your game rules **before UML**.

Your rules should answer:

* What is the goal of the game?
* What entities exist?
* How does the player interact with the world?
* What actions are allowed?
* What rules restrict movement or actions?
* How does the game end (win/lose)?

---

## 📄 Game Rules Document — Required Submission

You must submit your game rules in a **Word document**.

### File naming:

```
w#######-<game_name>-Game-Rules.docx
```

---

### 📄 Game Rules Template (Students Copy This)

```text
PROG1400 – Workshop 3
Game Rules Document

Student Name:
Student Number:
Game Name:

1. Game Overview
Briefly describe the game concept and objective.

2. Game World
Describe the game environment (grid, board, arena, rooms, etc.).

3. Player Rules
Describe what the player can do and cannot do.

4. Game Entities
List and describe any entities (enemies, obstacles, items, NPCs).

5. Movement Rules
Explain how movement works and any restrictions.

6. Interaction Rules
Explain how entities interact (collisions, pickups, combat, etc.).

7. Win Conditions
Explain how the player wins.

8. Lose Conditions
Explain how the player loses.

9. Assumptions
List any assumptions or constraints.
```

---

# 🧠 Part B — From Rules to UML Classes

Once rules are written, you can identify:

* classes
* responsibilities
* relationships

Your **rules document + CRC table** are the inputs for UML.

---

## Step B1 — Open Your PROG1400 VS Code Repository

In VS Code:

* Open your existing **PROG1400 repository**
* Create a folder (if not already present):

```
/docs/uml/
```

All UML diagrams will live here.

---

## Step B2 — Install Mermaid Extension (Required)

1. Open VS Code
2. Go to Extensions
3. Search for:

```
Mermaid Chart
```

4. Install the **official extension by Mermaid**

---

## Step B3 — Create Your UML File

Inside `/docs/uml/`, create a new file named:

```
w#######-<game_name>-UML-Diagram-01.mmd
```

This naming convention is **required**.

---

# 🤖 Part C — Using GitHub Copilot to Generate UML

You are encouraged to use **GitHub Copilot** as a **design assistant**, not as an answer generator.

Copilot should help you translate **rules → structure**.

---

## Example Copilot Prompt (Students May Use)

Paste a comment at the top of your `.mmd` file:

```text
I am designing a game for a PROG1400 course.

Here are the game rules:
[PASTE YOUR GAME RULES HERE]

Based on these rules, generate a Mermaid UML class diagram.
Include:
- World or board class
- Player class
- Entity base class (if appropriate)
- Position or coordinate class
- Clear ownership relationships
Use simple beginner-friendly structure.
```

Copilot will generate Mermaid code suggestions.

👉 **You must review and edit the output.**
You are responsible for correctness.

---

# 🧱 Part D — UML Class Diagram Requirements

Your UML diagram must include:

* At least **5 classes**
* Classes clearly derived from your game rules
* Attributes and methods
* At least one **composition (owns)** relationship
* Clear separation between world and player
* Mermaid syntax only
* Saved as a `.mmd` file in your repo

---

# 👁️ Part E — Previewing UML in VS Code

To preview your diagram:

1. Right-click inside the `.mmd` file
2. Select **“Open Mermaid Preview”**

OR

1. Press `Ctrl + Shift + P`
2. Run: **Mermaid: Preview Diagram**

Your diagram updates live as you edit.

---

# 🌐 Part F — Exporting UML Diagram as PNG (Required)

You must also export a **PNG image** of your UML diagram.

## Steps:

1. Copy your Mermaid code
2. Go to: [https://www.mermaid.ai/app/dashboard](https://www.mermaid.ai/app/dashboard)
3. Paste your code
4. Select **Layout**
5. Choose **Adaptive**
6. Export as **PNG**

Save the PNG using:

```
w#######-<game_name>-UML-Diagram-01.png
```

---

# 📦 Part G — Deliverables (Submit All)

You must submit **both design artifacts**:

### 1. Game Rules Document (Word)

* `w#######-<game_name>-Game-Rules.docx`

### 2. UML Class Diagram

* Mermaid file:
  `w#######-<game_name>-UML-Diagram-01.mmd`
* Exported PNG:
  `w#######-<game_name>-UML-Diagram-01.png`

Upload all files to Brightspace.

---

# ✍️ Optional Reflection (Instructor Discretion)

(If required)

* What rule had the biggest impact on your design?
* What class became central to your UML?
* What did Copilot help with the most?

---

## ✅ Workshop Summary

In this workshop, you:

* defined game rules before coding
* translated rules into object-oriented design
* used Copilot responsibly as a design assistant
* created UML class diagrams using Mermaid
* organized professional design documentation
* practiced real-world design workflow

This is how **software engineers design systems**.

---
