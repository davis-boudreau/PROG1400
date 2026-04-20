"""Core game models and domain objects."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

import config
from util import Position


class Entity:
    """Base class for movable game objects."""

    def __init__(self, start: Position) -> None:
        self.start = start
        self.position = start

    def reset(self) -> None:
        self.position = self.start


class Player(Entity):
    def __init__(self, start: Position) -> None:
        super().__init__(start)
        self.score = 0
        self.lives = config.PLAYER_STARTING_LIVES
        self.power_mode_turns = 0

    @property
    def is_powered(self) -> bool:
        return self.power_mode_turns > 0

    def tick(self) -> None:
        if self.power_mode_turns > 0:
            self.power_mode_turns -= 1


class Enemy(Entity):
    def choose_next_position(self, level: "Level", target: Position) -> Position:
        """Use a shortest-path step toward the target when possible."""
        if self.position == target:
            return self.position

        frontier = deque([(self.position, None)])
        visited = {self.position}
        parent: dict[Position, Position | None] = {self.position: None}

        while frontier:
            current, _ = frontier.popleft()
            if current == target:
                break
            for neighbor in level.walkable_neighbors(current):
                if neighbor not in visited and neighbor != level.player.position:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    frontier.append((neighbor, current))

        if target not in parent:
            for fallback in level.walkable_neighbors(self.position):
                if fallback != level.player.position:
                    return fallback
            return self.position

        step = target
        while parent[step] != self.position and parent[step] is not None:
            step = parent[step]  # walk back to first step
        return step


@dataclass
class LevelResult:
    points_gained: int = 0
    enemy_defeated: bool = False
    item_collected: bool = False
    level_completed: bool = False


class Level:
    def __init__(self, grid: list[list[str]]) -> None:
        self.height = len(grid)
        self.width = len(grid[0])
        self.tiles = [row[:] for row in grid]
        self.player = self._build_player()
        self.enemies = self._build_enemies()
        self.remaining_items = self._count_items()

    def _build_player(self) -> Player:
        for r, row in enumerate(self.tiles):
            for c, tile in enumerate(row):
                if tile == config.PLAYER_START:
                    self.tiles[r][c] = config.EMPTY
                    return Player(Position(r, c))
        raise ValueError("Level must include a player start tile 'P'.")

    def _build_enemies(self) -> list[Enemy]:
        enemies: list[Enemy] = []
        for r, row in enumerate(self.tiles):
            for c, tile in enumerate(row):
                if tile == config.ENEMY_START:
                    self.tiles[r][c] = config.EMPTY
                    enemies.append(Enemy(Position(r, c)))
        if not enemies:
            raise ValueError("Level must include at least one enemy start tile 'E'.")
        return enemies

    def _count_items(self) -> int:
        return sum(tile in {config.DOT, config.POWER} for row in self.tiles for tile in row)

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < self.height and 0 <= pos.col < self.width

    def tile_at(self, pos: Position) -> str:
        return self.tiles[pos.row][pos.col]

    def is_walkable(self, pos: Position) -> bool:
        return self.in_bounds(pos) and self.tile_at(pos) != config.WALL

    def walkable_neighbors(self, pos: Position) -> Iterable[Position]:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nxt = pos.moved(dr, dc)
            if self.is_walkable(nxt):
                yield nxt

    def try_move_player(self, dr: int, dc: int) -> LevelResult:
        result = LevelResult()
        next_pos = self.player.position.moved(dr, dc)
        if not self.is_walkable(next_pos):
            return result

        self.player.position = next_pos
        tile = self.tile_at(next_pos)

        if tile == config.DOT:
            self.tiles[next_pos.row][next_pos.col] = config.EMPTY
            self.remaining_items -= 1
            result.points_gained += config.DOT_POINTS
            result.item_collected = True
        elif tile == config.POWER:
            self.tiles[next_pos.row][next_pos.col] = config.EMPTY
            self.remaining_items -= 1
            self.player.power_mode_turns = config.POWER_MODE_TURNS
            result.points_gained += config.POWER_ITEM_POINTS
            result.item_collected = True

        if self.remaining_items == 0:
            result.points_gained += config.LEVEL_CLEAR_BONUS
            result.level_completed = True

        return result

    def move_enemies(self) -> list[Position]:
        target = self.player.position
        new_positions: list[Position] = []
        for enemy in self.enemies:
            enemy.position = enemy.choose_next_position(self, target)
            new_positions.append(enemy.position)
        return new_positions

    def handle_collisions(self) -> LevelResult:
        result = LevelResult()
        for enemy in self.enemies:
            if enemy.position == self.player.position:
                if self.player.is_powered:
                    enemy.reset()
                    result.points_gained += config.ENEMY_DEFEAT_POINTS
                    result.enemy_defeated = True
                else:
                    self.player.lives -= 1
                    self.player.reset()
                    for e in self.enemies:
                        e.reset()
                    break
        return result
