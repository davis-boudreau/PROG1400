from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional


# =========================
# Enumerations (UML exact)
# =========================

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


# =========================
# Coordinates & Movement
# =========================

@dataclass(frozen=True, slots=True)
class Cell:
    """Grid coordinate (row, col). Frozen so it is hashable for dict keys."""
    r: int
    c: int

    def moved(self, d: Direction) -> Cell:
        """Return a new Cell moved one tile in direction d."""
        if d == Direction.UP:
            return Cell(self.r - 1, self.c)
        if d == Direction.DOWN:
            return Cell(self.r + 1, self.c)
        if d == Direction.LEFT:
            return Cell(self.r, self.c - 1)
        if d == Direction.RIGHT:
            return Cell(self.r, self.c + 1)
        return self

    def equals(self, other: Cell) -> bool:
        """UML-style equality method (though Python supports ==)."""
        return self == other


# =========================
# Maze / Grid
# =========================

class Maze:
    def __init__(
        self,
        rows: int,
        cols: int,
        tiles: List[List[TileType]],
        items: Optional[Dict[Cell, Item]] = None,
        pacmanSpawn: Optional[Cell] = None,
        ghostSpawns: Optional[List[Cell]] = None,
    ) -> None:
        self.rows: int = rows
        self.cols: int = cols
        self.tiles: List[List[TileType]] = tiles
        self.items: Dict[Cell, Item] = items if items is not None else {}
        self.pacmanSpawn: Cell = pacmanSpawn if pacmanSpawn is not None else Cell(0, 0)
        self.ghostSpawns: List[Cell] = ghostSpawns if ghostSpawns is not None else []

    def is_walkable(self, cell: Cell) -> bool:
        """True if the cell can be entered by an actor."""
        if not (0 <= cell.r < self.rows and 0 <= cell.c < self.cols):
            return False
        tile = self.tiles[cell.r][cell.c]
        return tile != TileType.WALL

    def warp(self, cell: Cell) -> Cell:
        """Apply tunnel wrapping if the cell is a tunnel. Otherwise returns same cell.

        Note: For classic Pac-Man, tunnels usually wrap horizontally.
        """
        if not (0 <= cell.r < self.rows and 0 <= cell.c < self.cols):
            return cell
        if self.tiles[cell.r][cell.c] == TileType.TUNNEL:
            # Example simple wrap: wrap column around
            if cell.c <= 0:
                return Cell(cell.r, self.cols - 1)
            if cell.c >= self.cols - 1:
                return Cell(cell.r, 0)
        return cell

    def get_item(self, cell: Cell) -> Optional[Item]:
        """Return the item at this cell, if any."""
        return self.items.get(cell)

    def remove_item(self, cell: Cell) -> None:
        """Remove an item from this cell (if present)."""
        self.items.pop(cell, None)

    def pellets_remaining(self) -> int:
        """Count pellets remaining (Pellet + PowerPellet as pellets)."""
        count = 0
        for it in self.items.values():
            if isinstance(it, (Pellet, PowerPellet)):
                count += 1
        return count


# =========================
# Actors
# =========================

class Actor:
    """Abstract base for Pacman and Ghost. Tile-by-tile movement."""

    def __init__(
        self,
        cell: Cell,
        dir: Direction = Direction.NONE,
        nextDir: Direction = Direction.NONE,
        moveEveryTicks: int = 1
    ) -> None:
        self.cell: Cell = cell
        self.dir: Direction = dir
        self.nextDir: Direction = nextDir
        self.moveEveryTicks: int = max(1, moveEveryTicks)
        self.moveCounter: int = 0

    def update(self, game: Game) -> None:
        """Update actor logic once per game tick (tile-by-tile)."""
        raise NotImplementedError

    # "Protected" methods by convention (UML marks #)
    def try_turn(self, maze: Maze) -> None:
        """Attempt to switch to nextDir if it is walkable."""
        if self.nextDir == Direction.NONE:
            return
        target = maze.warp(self.cell.moved(self.nextDir))
        if maze.is_walkable(target):
            self.dir = self.nextDir

    def try_step(self, maze: Maze) -> None:
        """Attempt to move one tile in current dir if walkable."""
        if self.dir == Direction.NONE:
            return
        nxt = maze.warp(self.cell.moved(self.dir))
        if maze.is_walkable(nxt):
            self.cell = nxt

    def set_next_dir(self, d: Direction) -> None:
        self.nextDir = d

    def get_cell(self) -> Cell:
        return self.cell


class Pacman(Actor):
    def __init__(
        self,
        cell: Cell,
        dir: Direction = Direction.LEFT,
        nextDir: Direction = Direction.LEFT,
        moveEveryTicks: int = 1
    ) -> None:
        super().__init__(cell, dir, nextDir, moveEveryTicks)
        self.powerTicks: int = 0
        self.ghostCombo: int = 0

    def update(self, game: Game) -> None:
        """Tick-based movement + countdown power mode."""
        # Movement pacing
        self.moveCounter += 1
        if self.moveCounter >= self.moveEveryTicks:
            self.try_turn(game.maze)
            self.try_step(game.maze)
            self.moveCounter = 0

        # Power mode countdown
        if self.powerTicks > 0:
            self.powerTicks -= 1

    def is_powered(self) -> bool:
        return self.powerTicks > 0

    def power_up(self, ticks: int) -> None:
        self.powerTicks = max(self.powerTicks, ticks)
        self.reset_combo()

    def reset_combo(self) -> None:
        self.ghostCombo = 0

    def consume_ghost_points(self) -> int:
        """Return points for the next ghost eaten in the combo.
        Classic: 200, 400, 800, 1600 (cap at 1600).
        """
        self.ghostCombo += 1
        base = 200 * (2 ** (self.ghostCombo - 1))
        return min(base, 1600)


class Ghost(Actor):
    """Abstract ghost: movement controlled by choose_dir()."""

    def __init__(
        self,
        cell: Cell,
        home: Cell,
        dir: Direction = Direction.NONE,
        nextDir: Direction = Direction.NONE,
        moveEveryTicks: int = 1
    ) -> None:
        super().__init__(cell, dir, nextDir, moveEveryTicks)
        self.state: GhostState = GhostState.SCATTER
        self.home: Cell = home
        self._frightenedTicks: int = 0

    def update(self, game: Game) -> None:
        """Choose direction and move tile-by-tile, respecting frightened timer."""
        # Timer updates
        if self._frightenedTicks > 0:
            self._frightenedTicks -= 1
            self.state = GhostState.FRIGHTENED
        elif self.state == GhostState.FRIGHTENED:
            self.state = GhostState.CHASE

        # Decide next direction each movement opportunity
        self.moveCounter += 1
        if self.moveCounter >= self.moveEveryTicks:
            self.nextDir = self.choose_dir(game)
            self.try_turn(game.maze)
            self.try_step(game.maze)
            self.moveCounter = 0

    def choose_dir(self, game: Game) -> Direction:
        """Abstract AI hook: subclasses provide behavior."""
        raise NotImplementedError

    def frighten(self, ticks: int) -> None:
        self._frightenedTicks = max(self._frightenedTicks, ticks)
        self.state = GhostState.FRIGHTENED

    def is_frightened(self) -> bool:
        return self._frightenedTicks > 0 or self.state == GhostState.FRIGHTENED

    def reset_home(self) -> None:
        self.cell = self.home
        self.dir = Direction.NONE
        self.nextDir = Direction.NONE
        self._frightenedTicks = 0
        self.state = GhostState.SCATTER


class RandomGhost(Ghost):
    def choose_dir(self, game: Game) -> Direction:
        """Stub: choose randomly among valid directions."""
        # Implement later: pick from [UP,DOWN,LEFT,RIGHT] that is walkable
        return self.dir if self.dir != Direction.NONE else Direction.LEFT


class ChaserGhost(Ghost):
    def choose_dir(self, game: Game) -> Direction:
        """Stub: greedily move toward Pacman using Manhattan distance."""
        # Implement later: choose direction that minimizes distance to pacman.cell
        return self.dir if self.dir != Direction.NONE else Direction.LEFT


# =========================
# Items (scoring + effects)
# =========================

class Item:
    """Abstract collectible item."""
    def __init__(self, points: int) -> None:
        self.points: int = points

    def apply(self, game: Game) -> None:
        """Apply item effect to game (score/effects)."""
        raise NotImplementedError

    def get_points(self) -> int:
        return self.points


class Pellet(Item):
    def __init__(self, points: int = 10) -> None:
        super().__init__(points)

    def apply(self, game: Game) -> None:
        game.score.add(self.points)


class PowerPellet(Item):
    def __init__(self, points: int = 50, powerTicks: int = 60) -> None:
        super().__init__(points)
        self.powerTicks: int = powerTicks

    def apply(self, game: Game) -> None:
        game.score.add(self.points)
        game.pacman.power_up(self.powerTicks)
        for g in game.ghosts:
            g.frighten(self.powerTicks)


class Fruit(Item):
    def __init__(self, points: int = 100) -> None:
        super().__init__(points)

    def apply(self, game: Game) -> None:
        game.score.add(self.points)


# =========================
# Scoring System
# =========================

class ScoreBoard:
    def __init__(self, lives: int = 3) -> None:
        self.score: int = 0
        self.lives: int = lives
        self.highScore: int = 0
        self.nextExtraLifeAt: int = 10000

    def reset_new_game(self) -> None:
        self.score = 0
        self.lives = 3
        self.nextExtraLifeAt = 10000

    def reset_new_level(self, level: int) -> None:
        """Hook for per-level changes (optional)."""
        # Could adjust fruit values per level externally.
        pass

    def add(self, points: int) -> None:
        self.score += max(0, points)
        self.maybe_extra_life()
        # Track high score in-memory
        if self.score > self.highScore:
            self.highScore = self.score

    def lose_life(self) -> None:
        self.lives = max(0, self.lives - 1)

    def maybe_extra_life(self) -> bool:
        """Award an extra life at score thresholds (e.g., every 10,000)."""
        awarded = False
        while self.score >= self.nextExtraLifeAt:
            self.lives += 1
            self.nextExtraLifeAt += 10000
            awarded = True
        return awarded

    def save_high_score(self, path: str) -> None:
        """Persist high score to disk. (Simple text file recommended for beginners.)"""
        # TODO: implement file I/O
        pass

    def load_high_score(self, path: str) -> None:
        """Load high score from disk (if it exists)."""
        # TODO: implement file I/O
        pass

    def get_score(self) -> int:
        return self.score

    def get_lives(self) -> int:
        return self.lives

    def get_high_score(self) -> int:
        return self.highScore


# =========================
# Game Orchestration
# =========================

class Game:
    def __init__(self) -> None:
        self.maze: Maze = Maze(rows=0, cols=0, tiles=[])
        self.pacman: Pacman = Pacman(cell=Cell(0, 0))
        self.ghosts: List[Ghost] = []
        self.score: ScoreBoard = ScoreBoard()
        self.state: GameState = GameState.READY
        self.level: int = 1
        self.tick: int = 0

    
def load_level(self, n: int) -> None:
    from level_loader import load_level_from_ascii  # local import avoids circular imports
    self.level = n
    self.score.reset_new_level(n)

    # Load maze from file
    path = f"levels/level{n}.txt"
    self.maze = load_level_from_ascii(path, power_ticks=120)

    # Spawn Pacman
    self.pacman = Pacman(cell=self.maze.pacmanSpawn, dir=Direction.LEFT, nextDir=Direction.LEFT, moveEveryTicks=1)

    # Spawn ghosts (simple defaults)
    self.ghosts = []
    for i, spawn in enumerate(self.maze.ghostSpawns):
        if i == 0:
            self.ghosts.append(ChaserGhost(cell=spawn, home=spawn, moveEveryTicks=2))
        else:
            self.ghosts.append(RandomGhost(cell=spawn, home=spawn, moveEveryTicks=2))

    self.state = GameState.READY
    self.tick = 0


    def update(self, inputDir: Direction) -> None:
        """Advance the game by one tick. Tile-by-tile update."""
        self.tick += 1

        if self.state in (GameState.GAME_OVER, GameState.LEVEL_COMPLETE):
            return

        # Transition READY -> PLAYING once the first input arrives (optional)
        if self.state == GameState.READY:
            if inputDir != Direction.NONE:
                self.state = GameState.PLAYING

        if self.state != GameState.PLAYING:
            return

        # Apply input
        self.pacman.set_next_dir(inputDir)

        # Update actors
        self.pacman.update(self)
        for g in self.ghosts:
            g.update(self)

        # Resolve pickups/collisions
        self.resolve_collisions()

        # Check level completion
        self.check_level_complete()

    def reset_positions(self) -> None:
        """Reset Pacman and ghosts to spawn points."""
        self.pacman.cell = self.maze.pacmanSpawn
        self.pacman.dir = Direction.LEFT
        self.pacman.nextDir = Direction.LEFT
        self.pacman.powerTicks = 0
        self.pacman.reset_combo()

        for i, g in enumerate(self.ghosts):
            if i < len(self.maze.ghostSpawns):
                g.cell = self.maze.ghostSpawns[i]
            g.reset_home()

    def resolve_collisions(self) -> None:
        """Handle Pacman with items and ghosts (scoring + lives)."""
        # Item pickup (O(1) due to dict)
        item = self.maze.get_item(self.pacman.cell)
        if item is not None:
            item.apply(self)
            self.maze.remove_item(self.pacman.cell)

        # Ghost collision (cell equality)
        for g in self.ghosts:
            if g.cell == self.pacman.cell:
                if self.pacman.is_powered() and g.is_frightened():
                    pts = self.pacman.consume_ghost_points()
                    self.score.add(pts)
                    g.reset_home()
                else:
                    self.score.lose_life()
                    if self.score.get_lives() <= 0:
                        self.state = GameState.GAME_OVER
                    else:
                        self.state = GameState.DYING
                        self.reset_positions()
                        self.state = GameState.PLAYING
                break

    def check_level_complete(self) -> None:
        """Detect level completion when pellets are gone."""
        if self.maze.pellets_remaining() == 0:
            self.state = GameState.LEVEL_COMPLETE