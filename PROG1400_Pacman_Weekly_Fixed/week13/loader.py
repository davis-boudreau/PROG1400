from __future__ import annotations

from typing import Dict, List, Optional

from util import Cell, TileType
from model import Maze, Pellet, PowerPellet, Fruit, Item


class LevelFormatError(ValueError):
    pass


def load_level_from_ascii(
    path: str,
    *,
    power_ticks: int = 180,
    default_fruit_points: int = 100,
    pad_with_walls: bool = True,
) -> Maze:
    lines = _read_lines_keep_spaces(path)
    if not lines:
        raise LevelFormatError(f"Level file is empty: {path}")

    width = max(len(line) for line in lines)
    height = len(lines)
    pad_char = "#" if pad_with_walls else " "
    lines = [line.ljust(width, pad_char) for line in lines]

    tiles: List[List[TileType]] = [[TileType.FLOOR for _ in range(width)] for _ in range(height)]
    items: Dict[Cell, Item] = {}
    pacman_spawn: Optional[Cell] = None
    ghost_spawns: List[Cell] = []

    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            cell = Cell(r, c)
            if ch == "#":
                tiles[r][c] = TileType.WALL
            elif ch == "T":
                tiles[r][c] = TileType.TUNNEL
            elif ch == ".":
                tiles[r][c] = TileType.FLOOR
                items[cell] = Pellet()
            elif ch == "o":
                tiles[r][c] = TileType.FLOOR
                items[cell] = PowerPellet(powerTicks=power_ticks)
            elif ch == "F":
                tiles[r][c] = TileType.FLOOR
                items[cell] = Fruit(points=default_fruit_points)
            elif ch == "P":
                tiles[r][c] = TileType.FLOOR
                if pacman_spawn is not None:
                    raise LevelFormatError("Multiple Pacman spawns 'P' found.")
                pacman_spawn = cell
            elif ch == "G":
                tiles[r][c] = TileType.FLOOR
                ghost_spawns.append(cell)
            elif ch == " ":
                tiles[r][c] = TileType.FLOOR
            else:
                raise LevelFormatError(f"Unknown symbol '{ch}' at row {r}, col {c}")

    if pacman_spawn is None:
        raise LevelFormatError("No Pacman spawn 'P' found.")

    return Maze(height, width, tiles, items=items, pacmanSpawn=pacman_spawn, ghostSpawns=ghost_spawns)


def _read_lines_keep_spaces(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    while lines and lines[-1] == "":
        lines.pop()
    return lines
