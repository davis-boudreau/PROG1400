# PROG1400 OOP Game Starter Repo

This repository is a clean, instructor-ready Python starter for an object-oriented maze game inspired by Pac-Man-style mechanics.

It is designed for PROG1400 students who are building their own game with similar mechanics such as:

- Snake Game
- Hunter Assassin
- Impossible Game
- Trap the Mouse
- Tank Game
- Minesweeper
- Maze Path of Light

## Features

- modular Python structure
- level loading from text files
- object-oriented game entities
- player movement
- enemy chase behaviour
- collectibles and scoring
- power item support
- multiple levels
- persistent best-score file
- clean configuration variables for easy modification

## Project Structure

```text
prog1400_oop_game_starter/
├── main.py
├── game.py
├── config.py
├── models.py
├── loader.py
├── scoreboard.py
├── util.py
├── levels/
│   ├── level1.txt
│   └── level2.txt
└── docs/
    └── uml/
```

## How to Run

1. Make sure Python 3.11+ is installed.
2. Open a terminal in the project folder.
3. Run:

```bash
python main.py
```

## Controls

- Arrow keys: move player
- R: restart game

## Teaching Notes

This repo is intentionally organized so students can map the Pac-Man case study to their own game idea.

### Easy places for students to modify

- `config.py`: change game tuning, symbols, and colours
- `levels/*.txt`: redesign the maze or board
- `models.py`: adapt the player, enemy, and level rules
- `game.py`: extend win/lose conditions or UI feedback

## Suggested Student Tasks

- rename classes to match their game theme
- replace collectibles with goal objects from their own game
- change enemy logic to match their mechanics
- add extra levels
- improve the HUD or scoreboard
- refactor shared behaviour into inheritance if appropriate

## Notes

The project uses `tkinter`, which is included with standard Python on most systems.
