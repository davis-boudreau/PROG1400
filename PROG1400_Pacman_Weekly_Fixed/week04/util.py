from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class GameState(Enum):
    READY = auto()
    PLAYING = auto()
    DYING = auto()
    LEVEL_COMPLETE = auto()
    GAME_OVER = auto()


class TileType(Enum):
    WALL = auto()
    FLOOR = auto()
    TUNNEL = auto()


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()


class GhostState(Enum):
    CHASE = auto()
    SCATTER = auto()
    FRIGHTENED = auto()


@dataclass(frozen=True, slots=True)
class Cell:
    r: int
    c: int

    def moved(self, d: Direction) -> Cell:
        if d == Direction.UP:
            return Cell(self.r - 1, self.c)
        if d == Direction.DOWN:
            return Cell(self.r + 1, self.c)
        if d == Direction.LEFT:
            return Cell(self.r, self.c - 1)
        if d == Direction.RIGHT:
            return Cell(self.r, self.c + 1)
        return self
