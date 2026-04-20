"""Utility helpers and shared data structures."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def moved(self, dr: int, dc: int) -> "Position":
        return Position(self.row + dr, self.col + dc)


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @property
    def delta(self) -> tuple[int, int]:
        return self.value
