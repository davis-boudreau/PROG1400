"""Configuration values for the OOP maze game starter project.

Students should modify these values to suit their own game theme and mechanics.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LEVELS_DIR = BASE_DIR / "levels"
SCOREBOARD_FILE = BASE_DIR / "scoreboard.json"

# Rendering
TILE_SIZE = 32
HUD_HEIGHT = 96
FPS = 10
WINDOW_TITLE = "PROG1400 OOP Game Starter"

# Gameplay tuning
PLAYER_STARTING_LIVES = 3
DOT_POINTS = 10
POWER_ITEM_POINTS = 50
ENEMY_DEFEAT_POINTS = 200
LEVEL_CLEAR_BONUS = 100
POWER_MODE_TURNS = 20
ENEMY_MOVE_DELAY = 2  # enemy moves every N ticks

# Tile symbols used in level files
WALL = "#"
EMPTY = " "
DOT = "."
POWER = "o"
PLAYER_START = "P"
ENEMY_START = "E"

# Colors
BG_COLOR = "black"
WALL_COLOR = "navy"
FLOOR_COLOR = "black"
DOT_COLOR = "gold"
POWER_COLOR = "orange"
PLAYER_COLOR = "yellow"
ENEMY_COLOR = "red"
FRIGHTENED_ENEMY_COLOR = "cyan"
TEXT_COLOR = "white"
HUD_BG_COLOR = "#111111"

LEVEL_FILES = [
    LEVELS_DIR / "level1.txt",
    LEVELS_DIR / "level2.txt",
]
