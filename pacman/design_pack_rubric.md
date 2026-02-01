# Pac‑Man Design Pack — Rubric (Aligned to Sections)

> **Total Suggested Points:** 100 (adjustable)
>
> This rubric evaluates both **process** and **product-ready design**. Each criterion is aligned to a section of the Design Pack.

---

## 1) Project Brief (15 pts)
**Excellent (13–15)**
- Clear scope and constraints; includes non-goals to prevent scope creep.
- Overview is specific and matches the project constraints (tile-by-tile, ASCII levels).
- Definition of Done includes 6+ testable success criteria.

**Good (10–12)**
- Mostly clear; minor gaps in constraints or success criteria.
- Non-goals present but not very specific.

**Developing (6–9)**
- Brief is vague; constraints or success criteria incomplete.
- Non-goals missing or unclear.

**Needs Work (0–5)**
- Missing major sections or unclear project scope.

---

## 2) Rules Specification (20 pts)
**Excellent (18–20)**
- Rules are numbered, testable, and cover movement, items/scoring, collisions/lives, power/combo, and level progression.
- Includes key parameters (points, tick durations, lives).
- Minimal ambiguity; includes edge-case rules (e.g., tunnels, queued turning).

**Good (14–17)**
- Covers most required areas; some rules are slightly vague.
- Parameters present but incomplete.

**Developing (9–13)**
- Missing one or more rule categories or rules aren’t testable.
- Many rules read like descriptions rather than requirements.

**Needs Work (0–8)**
- Rules are largely missing or not usable for implementation.

---

## 3) CRC Deck (20 pts)
**Excellent (18–20)**
- CRC cards exist for all required classes.
- Responsibilities are written as verbs and align with Variant A architecture.
- Collaborators are appropriate; responsibilities are not duplicated across many classes.

**Good (14–17)**
- Most CRC cards completed; minor duplication or vague responsibilities.
- Collaborators mostly correct.

**Developing (9–13)**
- Several CRC cards missing or responsibilities too broad.
- Collaborators unclear or inconsistent.

**Needs Work (0–8)**
- CRC deck incomplete or not aligned with the design.

---

## 4) UML Class Diagram (15 pts)
**Excellent (13–15)**
- Diagram matches Variant A (or clearly justified variation).
- Correct relationships: composition/aggregation/inheritance consistent with responsibilities.
- Attributes and method signatures support the rules spec.

**Good (10–12)**
- Mostly correct structure; minor relationship/syntax errors.
- Some methods/attributes missing but core is coherent.

**Developing (6–9)**
- Multiple inconsistencies with CRC/rules.
- Missing key relationships or classes.

**Needs Work (0–5)**
- Diagram incomplete or does not represent the intended system.

---

## 5) UML Sequence Diagrams #1–#6 (20 pts)
**Excellent (18–20)**
- All six diagrams included and consistent with the class diagram and rules.
- Message order supports correct gameplay (move → collide → score/state updates).
- Students provide brief “guarantee” statements explaining each diagram.

**Good (14–17)**
- Most diagrams correct; minor inconsistencies or missing notes.

**Developing (9–13)**
- Several diagrams missing or message flow unclear.
- Some diagrams conflict with rules or class responsibilities.

**Needs Work (0–8)**
- Few diagrams present or diagrams are not usable.

---

## 6) Traceability (10 pts)
**Excellent (9–10)**
- At least 3 complete trace entries linking rule → CRC → UML class → UML sequence → code → test.
- Evidence shows tests performed (screenshots, notes, or reproducible steps).

**Good (7–8)**
- 3 entries present but missing one component (e.g., test evidence).

**Developing (4–6)**
- Fewer than 3 entries or links are incomplete.

**Needs Work (0–3)**
- Traceability missing or not meaningful.

---

## 7) Professionalism / Presentation (Optional 0–5 bonus)
- Clear formatting, consistent naming, spelling, and readable diagrams.
- Document is kept current as implementation progresses.

---

# Quick Instructor Notes (Optional)
- **Common pitfall:** students put scoring in many places. Encourage centralized ScoreBoard usage.
- **Common pitfall:** sequence diagrams not updated when code changes.
- **Fast teams:** allow optional Fruit, extra ghosts, or improved tunnel logic.
