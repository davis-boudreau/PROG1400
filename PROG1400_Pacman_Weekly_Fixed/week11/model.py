from __future__ import annotations

import random
from typing import Dict, List, Optional

from util import Cell, Direction, GameState, TileType, GhostState

# Feature Flags (set per week)
ENABLE_LOADER = True
ENABLE_ITEMS = True
ENABLE_GHOSTS = True
ENABLE_CHASER = True
ENABLE_POWER = True
ENABLE_EAT_GHOST = True
ENABLE_LEVELS = False
ENABLE_HIGHSCORE = False


class ScoreBoard:
    def __init__(self, lives: int = 3) -> None:
        self.score = 0
        self.lives = lives
        self.highScore = 0
        self.nextExtraLifeAt = 10000

    def reset_new_game(self) -> None:
        self.score = 0
        self.lives = 3
        self.nextExtraLifeAt = 10000

    def reset_new_level(self, level: int) -> None:
        pass

    def add(self, points: int) -> None:
        self.score += max(0, points)
        self.maybe_extra_life()
        if self.score > self.highScore:
            self.highScore = self.score

    def lose_life(self) -> None:
        self.lives = max(0, self.lives - 1)

    def maybe_extra_life(self) -> bool:
        awarded = False
        while self.score >= self.nextExtraLifeAt:
            self.lives += 1
            self.nextExtraLifeAt += 10000
            awarded = True
        return awarded

    def get_score(self) -> int:
        return self.score

    def get_lives(self) -> int:
        return self.lives

    def get_high_score(self) -> int:
        return self.highScore

    def load_high_score(self, path: str) -> None:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.highScore = int((f.read().strip() or '0'))
        except FileNotFoundError:
            self.highScore = 0
        except Exception:
            self.highScore = 0

    def save_high_score(self, path: str) -> None:
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(self.highScore))
        except Exception:
            pass


class Item:
    def __init__(self, points: int) -> None:
        self.points = points

    def apply(self, game: 'Game') -> None:
        raise NotImplementedError


class Pellet(Item):
    def __init__(self, points: int = 10) -> None:
        super().__init__(points)

    def apply(self, game: 'Game') -> None:
        game.score.add(self.points)


class PowerPellet(Item):
    def __init__(self, points: int = 50, powerTicks: int = 180) -> None:
        super().__init__(points)
        self.powerTicks = powerTicks

    def apply(self, game: 'Game') -> None:
        game.score.add(self.points)
        if ENABLE_POWER:
            game.pacman.power_up(self.powerTicks)
            for g in game.ghosts:
                g.frighten(self.powerTicks)


class Fruit(Item):
    def __init__(self, points: int = 100) -> None:
        super().__init__(points)

    def apply(self, game: 'Game') -> None:
        game.score.add(self.points)


class Maze:
    def __init__(self, rows: int, cols: int, tiles: List[List[TileType]],
                 items: Optional[Dict[Cell, Item]] = None,
                 pacmanSpawn: Optional[Cell] = None,
                 ghostSpawns: Optional[List[Cell]] = None) -> None:
        self.rows = rows
        self.cols = cols
        self.tiles = tiles
        self.items = items if items is not None else {}
        self.pacmanSpawn = pacmanSpawn if pacmanSpawn is not None else Cell(1, 1)
        self.ghostSpawns = ghostSpawns if ghostSpawns is not None else []

    def is_walkable(self, cell: Cell) -> bool:
        if not (0 <= cell.r < self.rows and 0 <= cell.c < self.cols):
            return False
        return self.tiles[cell.r][cell.c] != TileType.WALL

    def warp(self, cell: Cell) -> Cell:
        if not (0 <= cell.r < self.rows and 0 <= cell.c < self.cols):
            return cell
        if self.tiles[cell.r][cell.c] == TileType.TUNNEL:
            if cell.c <= 0:
                return Cell(cell.r, self.cols - 1)
            if cell.c >= self.cols - 1:
                return Cell(cell.r, 0)
        return cell

    def get_item(self, cell: Cell) -> Optional[Item]:
        return self.items.get(cell)

    def remove_item(self, cell: Cell) -> None:
        self.items.pop(cell, None)

    def pellets_remaining(self) -> int:
        return sum(1 for it in self.items.values() if isinstance(it, (Pellet, PowerPellet)))


class Actor:
    def __init__(self, cell: Cell, dir: Direction = Direction.NONE,
                 nextDir: Direction = Direction.NONE, moveEveryTicks: int = 1) -> None:
        self.cell = cell
        self.dir = dir
        self.nextDir = nextDir
        self.moveEveryTicks = max(1, moveEveryTicks)
        self.moveCounter = 0

    def set_next_dir(self, d: Direction) -> None:
        self.nextDir = d

    def _try_turn(self, maze: Maze) -> None:
        if self.nextDir == Direction.NONE:
            return
        target = maze.warp(self.cell.moved(self.nextDir))
        if maze.is_walkable(target):
            self.dir = self.nextDir

    def _try_step(self, maze: Maze) -> None:
        if self.dir == Direction.NONE:
            return
        nxt = maze.warp(self.cell.moved(self.dir))
        if maze.is_walkable(nxt):
            self.cell = nxt


class Pacman(Actor):
    def __init__(self, cell: Cell) -> None:
        super().__init__(cell, dir=Direction.LEFT, nextDir=Direction.LEFT, moveEveryTicks=1)
        self.powerTicks = 0
        self.ghostCombo = 0

    def update(self, game: 'Game') -> None:
        self.moveCounter += 1
        if self.moveCounter >= self.moveEveryTicks:
            self._try_turn(game.maze)
            self._try_step(game.maze)
            self.moveCounter = 0
        if ENABLE_POWER and self.powerTicks > 0:
            self.powerTicks -= 1

    def is_powered(self) -> bool:
        return ENABLE_POWER and self.powerTicks > 0

    def power_up(self, ticks: int) -> None:
        if not ENABLE_POWER:
            return
        self.powerTicks = max(self.powerTicks, ticks)
        self.ghostCombo = 0

    def consume_ghost_points(self) -> int:
        self.ghostCombo += 1
        base = 200 * (2 ** (self.ghostCombo - 1))
        return min(base, 1600)


class Ghost(Actor):
    def __init__(self, cell: Cell, home: Cell, moveEveryTicks: int = 2) -> None:
        super().__init__(cell, dir=Direction.LEFT, nextDir=Direction.LEFT, moveEveryTicks=moveEveryTicks)
        self.state = GhostState.SCATTER
        self.home = home
        self._frightenedTicks = 0

    def frighten(self, ticks: int) -> None:
        if not ENABLE_POWER:
            return
        self._frightenedTicks = max(self._frightenedTicks, ticks)
        self.state = GhostState.FRIGHTENED

    def is_frightened(self) -> bool:
        return ENABLE_POWER and (self._frightenedTicks > 0 or self.state == GhostState.FRIGHTENED)

    def reset_home(self) -> None:
        self.cell = self.home
        self.dir = Direction.LEFT
        self.nextDir = Direction.LEFT
        self._frightenedTicks = 0
        self.state = GhostState.SCATTER

    def update(self, game: 'Game') -> None:
        if ENABLE_POWER:
            if self._frightenedTicks > 0:
                self._frightenedTicks -= 1
                self.state = GhostState.FRIGHTENED
            elif self.state == GhostState.FRIGHTENED:
                self.state = GhostState.CHASE

        self.moveCounter += 1
        if self.moveCounter >= self.moveEveryTicks:
            self.nextDir = self.choose_dir(game)
            self._try_turn(game.maze)
            self._try_step(game.maze)
            self.moveCounter = 0

    def choose_dir(self, game: 'Game') -> Direction:
        raise NotImplementedError


class RandomGhost(Ghost):
    def choose_dir(self, game: 'Game') -> Direction:
        candidates = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        random.shuffle(candidates)
        for d in candidates:
            nxt = game.maze.warp(self.cell.moved(d))
            if game.maze.is_walkable(nxt):
                return d
        return self.dir


class ChaserGhost(Ghost):
    def choose_dir(self, game: 'Game') -> Direction:
        target = game.pacman.cell
        best = self.dir
        best_dist = 10**9
        for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            nxt = game.maze.warp(self.cell.moved(d))
            if not game.maze.is_walkable(nxt):
                continue
            dist = abs(nxt.r - target.r) + abs(nxt.c - target.c)
            if dist < best_dist:
                best_dist = dist
                best = d
        return best


class Game:
    def __init__(self) -> None:
        self.state = GameState.READY
        self.level = 1
        self.tick = 0
        self.score = ScoreBoard()

        if ENABLE_HIGHSCORE:
            self.score.load_high_score('highscore.txt')

        self.maze = self._make_fallback_maze()
        self.pacman = Pacman(self.maze.pacmanSpawn)
        self.ghosts: List[Ghost] = []

        if ENABLE_GHOSTS:
            self._spawn_default_ghosts()

    def _make_fallback_maze(self) -> Maze:
        rows, cols = 15, 19
        tiles = [[TileType.FLOOR for _ in range(cols)] for _ in range(rows)]
        for r in range(rows):
            tiles[r][0] = TileType.WALL
            tiles[r][cols - 1] = TileType.WALL
        for c in range(cols):
            tiles[0][c] = TileType.WALL
            tiles[rows - 1][c] = TileType.WALL

        mid = rows // 2
        tiles[mid][0] = TileType.TUNNEL
        tiles[mid][cols - 1] = TileType.TUNNEL

        items: Dict[Cell, Item] = {}
        if ENABLE_ITEMS:
            for r in range(1, rows - 1):
                for c in range(1, cols - 1):
                    items[Cell(r, c)] = Pellet()
            items[Cell(1, cols - 2)] = PowerPellet(powerTicks=180)

        return Maze(rows, cols, tiles, items=items, pacmanSpawn=Cell(1, 1), ghostSpawns=[Cell(mid, cols - 2)])

    def _spawn_default_ghosts(self) -> None:
        self.ghosts = []
        spawns = self.maze.ghostSpawns or [Cell(self.maze.rows // 2, self.maze.cols // 2)]
        for i, spawn in enumerate(spawns):
            if ENABLE_CHASER and i == 0:
                self.ghosts.append(ChaserGhost(spawn, home=spawn, moveEveryTicks=2))
            else:
                self.ghosts.append(RandomGhost(spawn, home=spawn, moveEveryTicks=2))

    def load_level(self, n: int) -> None:
        self.level = n
        self.tick = 0

        if ENABLE_LOADER:
            from loader import load_level_from_ascii
            path = f'levels/level{n}.txt'
            try:
                self.maze = load_level_from_ascii(path)
            except FileNotFoundError:
                self.level = 1
                self.maze = load_level_from_ascii('levels/level1.txt')
        else:
            self.maze = self._make_fallback_maze()

        self.pacman = Pacman(self.maze.pacmanSpawn)

        if ENABLE_GHOSTS:
            self._spawn_default_ghosts()
        else:
            self.ghosts = []

        self.state = GameState.READY

    def update(self, inputDir: Direction) -> None:
        self.tick += 1

        if self.state == GameState.GAME_OVER:
            return

        if self.state == GameState.READY and inputDir != Direction.NONE:
            self.state = GameState.PLAYING

        if self.state != GameState.PLAYING:
            return

        self.pacman.set_next_dir(inputDir)
        self.pacman.update(self)

        if ENABLE_GHOSTS:
            for g in self.ghosts:
                g.update(self)

        self.resolve_collisions()
        self.check_level_complete()

    def reset_positions(self) -> None:
        self.pacman.cell = self.maze.pacmanSpawn
        self.pacman.dir = Direction.LEFT
        self.pacman.nextDir = Direction.LEFT

        if ENABLE_POWER:
            self.pacman.powerTicks = 0
        self.pacman.ghostCombo = 0

        for i, g in enumerate(self.ghosts):
            if i < len(self.maze.ghostSpawns):
                g.home = self.maze.ghostSpawns[i]
            g.reset_home()

    def resolve_collisions(self) -> None:
        if ENABLE_ITEMS:
            item = self.maze.get_item(self.pacman.cell)
            if item is not None:
                item.apply(self)
                self.maze.remove_item(self.pacman.cell)

        if ENABLE_GHOSTS:
            for g in self.ghosts:
                if g.cell == self.pacman.cell:
                    edible = ENABLE_EAT_GHOST and self.pacman.is_powered() and g.is_frightened()
                    if edible:
                        self.score.add(self.pacman.consume_ghost_points())
                        g.reset_home()
                    else:
                        self.score.lose_life()
                        if self.score.get_lives() <= 0:
                            self.state = GameState.GAME_OVER
                            if ENABLE_HIGHSCORE:
                                self.score.save_high_score('highscore.txt')
                        else:
                            self.state = GameState.DYING
                            self.reset_positions()
                            self.state = GameState.PLAYING
                    break

    def check_level_complete(self) -> None:
        if ENABLE_ITEMS and self.maze.pellets_remaining() == 0:
            self.state = GameState.LEVEL_COMPLETE
            if ENABLE_LEVELS:
                self.load_level(self.level + 1)
