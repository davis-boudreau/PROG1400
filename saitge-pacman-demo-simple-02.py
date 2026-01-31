from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
from collections import deque
import random
import pygame


# =========================
# Core types / enums
# =========================

@dataclass(frozen=True)
class GridCoord:
    row: int
    col: int

    def moved(self, d: "Direction") -> "GridCoord":
        dr, dc = d.delta()
        return GridCoord(self.row + dr, self.col + dc)

    def add(self, dr: int, dc: int) -> "GridCoord":
        return GridCoord(self.row + dr, self.col + dc)


class TileType(Enum):
    WALL = auto()
    PATH = auto()
    PELLET = auto()
    POWER = auto()


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()

    def delta(self) -> Tuple[int, int]:
        return {
            Direction.UP: (-1, 0),
            Direction.DOWN: (1, 0),
            Direction.LEFT: (0, -1),
            Direction.RIGHT: (0, 1),
            Direction.NONE: (0, 0),
        }[self]

    def opposite(self) -> "Direction":
        return {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.NONE: Direction.NONE,
        }[self]


class GhostMode(Enum):
    """Overrides; FRIGHTENED or EATEN take precedence over scatter/chase phase."""
    NORMAL = auto()
    FRIGHTENED = auto()
    EATEN = auto()


class Phase(Enum):
    SCATTER = auto()
    CHASE = auto()


class GhostType(Enum):
    BLINKY = auto()
    PINKY = auto()
    INKY = auto()


# =========================
# Map / Maze
# =========================

class TileMap:
    def __init__(self, grid: List[List[TileType]]):
        self._grid = grid

    @property
    def height(self) -> int:
        return len(self._grid)

    @property
    def width(self) -> int:
        return len(self._grid[0]) if self._grid else 0

    def in_bounds(self, c: GridCoord) -> bool:
        return 0 <= c.row < self.height and 0 <= c.col < self.width

    def get(self, c: GridCoord) -> TileType:
        return self._grid[c.row][c.col]

    def set(self, c: GridCoord, t: TileType) -> None:
        self._grid[c.row][c.col] = t


class Maze:
    def __init__(self, tile_map: TileMap, tile_size: int):
        self._map = tile_map
        self.tile_size = tile_size

    @property
    def width(self) -> int:
        return self._map.width

    @property
    def height(self) -> int:
        return self._map.height

    def is_walkable(self, c: GridCoord) -> bool:
        if not self._map.in_bounds(c):
            return False
        return self._map.get(c) != TileType.WALL

    def tile_at(self, c: GridCoord) -> TileType:
        return self._map.get(c)

    def consume_at(self, c: GridCoord) -> TileType:
        """If tile is PELLET/POWER, flip to PATH and return what was eaten."""
        t = self._map.get(c)
        if t in (TileType.PELLET, TileType.POWER):
            self._map.set(c, TileType.PATH)
            return t
        return t

    def grid_to_world(self, c: GridCoord) -> pygame.Vector2:
        """Center of tile in world coords (maze space)."""
        return pygame.Vector2((c.col + 0.5) * self.tile_size, (c.row + 0.5) * self.tile_size)

    def world_to_grid(self, p: pygame.Vector2) -> GridCoord:
        col = int(p.x // self.tile_size)
        row = int(p.y // self.tile_size)
        return GridCoord(row, col)

    def is_centered(self, p: pygame.Vector2, tol: float = 1.75) -> bool:
        c = self.world_to_grid(p)
        center = self.grid_to_world(c)
        return (p - center).length() <= tol

    def neighbors(self, c: GridCoord) -> List[GridCoord]:
        out: List[GridCoord] = []
        for d in (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT):
            n = c.moved(d)
            if self.is_walkable(n):
                out.append(n)
        return out


# =========================
# Pathfinding (BFS)
# =========================

def bfs_next_step(maze: Maze, start: GridCoord, goal: GridCoord) -> Optional[GridCoord]:
    """Return neighbor tile to step into from start along a shortest path to goal."""
    if start == goal:
        return None

    q = deque([start])
    came_from: Dict[GridCoord, Optional[GridCoord]] = {start: None}

    while q:
        cur = q.popleft()
        if cur == goal:
            break
        for n in maze.neighbors(cur):
            if n not in came_from:
                came_from[n] = cur
                q.append(n)

    if goal not in came_from:
        return None

    step = goal
    while came_from[step] is not None and came_from[step] != start:
        step = came_from[step]
    return step


def dir_from_to(a: GridCoord, b: GridCoord) -> Direction:
    dr = b.row - a.row
    dc = b.col - a.col
    if dr == -1 and dc == 0: return Direction.UP
    if dr ==  1 and dc == 0: return Direction.DOWN
    if dr ==  0 and dc == -1: return Direction.LEFT
    if dr ==  0 and dc ==  1: return Direction.RIGHT
    return Direction.NONE


def nearest_walkable(maze: Maze, start: GridCoord) -> GridCoord:
    """If start isn't walkable, BFS outward until finding a walkable tile."""
    if maze.is_walkable(start):
        return start
    q = deque([start])
    seen = {start}
    while q:
        cur = q.popleft()
        for d in (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT):
            n = cur.moved(d)
            if not maze._map.in_bounds(n) or n in seen:
                continue
            if maze.is_walkable(n):
                return n
            seen.add(n)
            q.append(n)
    return start


# =========================
# Entities
# =========================

class PacMan:
    def __init__(self, start_tile: GridCoord, maze: Maze):
        self.grid: GridCoord = start_tile
        self.prev_grid: GridCoord = start_tile
        self.world: pygame.Vector2 = maze.grid_to_world(start_tile)

        self.current_dir: Direction = Direction.LEFT
        self.desired_dir: Direction = Direction.LEFT

        self.speed_px: float = maze.tile_size * 6.2
        self.lives: int = 3

    def queue_turn(self, d: Direction) -> None:
        if d != Direction.NONE:
            self.desired_dir = d

    def update(self, maze: Maze, dt: float) -> None:
        self.prev_grid = self.grid

        if maze.is_centered(self.world):
            self.grid = maze.world_to_grid(self.world)
            self.world = maze.grid_to_world(self.grid)

            desired_next = self.grid.moved(self.desired_dir)
            if self.desired_dir != Direction.NONE and maze.is_walkable(desired_next):
                self.current_dir = self.desired_dir

            forward_next = self.grid.moved(self.current_dir)
            if self.current_dir != Direction.NONE and not maze.is_walkable(forward_next):
                self.current_dir = Direction.NONE

        if self.current_dir != Direction.NONE:
            dr, dc = self.current_dir.delta()
            vel = pygame.Vector2(dc, dr) * self.speed_px
            self.world += vel * dt
            self.grid = maze.world_to_grid(self.world)

    def take_damage(self) -> None:
        self.lives -= 1


class Ghost:
    def __init__(
        self,
        ghost_type: GhostType,
        start_tile: GridCoord,
        maze: Maze,
        color: Tuple[int, int, int],
        house_tile: GridCoord,
        home_corner: GridCoord,
        # Pinky tuning knobs:
        pinky_lookahead_tiles: int = 4,
        pinky_corner_bias: float = 0.7,
    ):
        self.type = ghost_type

        self.grid: GridCoord = start_tile
        self.prev_grid: GridCoord = start_tile
        self.world: pygame.Vector2 = maze.grid_to_world(start_tile)

        self.mode: GhostMode = GhostMode.NORMAL
        self.current_dir: Direction = Direction.LEFT

        self.speed_px_normal: float = maze.tile_size * 5.2
        self.speed_px_fright: float = maze.tile_size * 4.0
        self.speed_px_eaten: float = maze.tile_size * 7.0

        self.color = color
        self.house_tile = house_tile
        self.home_corner = nearest_walkable(maze, home_corner)

        # Inky randomness
        self.inky_erratic_chance = 0.35

        # Phase reversal handling
        self.force_reverse = False

        # Pinky tuning
        self.pinky_lookahead_tiles = pinky_lookahead_tiles
        self.pinky_corner_bias = max(0.0, min(1.0, pinky_corner_bias))

    def speed_px(self) -> float:
        if self.mode == GhostMode.FRIGHTENED:
            return self.speed_px_fright
        if self.mode == GhostMode.EATEN:
            return self.speed_px_eaten
        return self.speed_px_normal

    def _valid_dirs(self, maze: Maze) -> List[Direction]:
        options: List[Direction] = []
        for d in (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT):
            if maze.is_walkable(self.grid.moved(d)):
                options.append(d)
        return options

    def _prefer_non_reverse(self, dirs: List[Direction]) -> List[Direction]:
        non_rev = [d for d in dirs if d != self.current_dir.opposite()]
        return non_rev if non_rev else dirs

    def _pinky_ambush_tile(self, maze: Maze, pac: PacMan) -> GridCoord:
        dr, dc = pac.current_dir.delta()
        look = self.pinky_lookahead_tiles
        ambush = pac.grid.add(dr * look, dc * look)
        return nearest_walkable(maze, ambush)

    def _pinky_target(self, maze: Maze, pac: PacMan) -> GridCoord:
        """
        Tunable Pinky:
        - Compute ambush tile (ahead of Pac-Man)
        - With probability pinky_corner_bias, target home-corner-ish ambush route:
          choose the corner closest to ambush tile.
        - Otherwise target ambush tile directly.
        """
        ambush = self._pinky_ambush_tile(maze, pac)

        # Choose corner closest to the ambush tile (corner-based "setup")
        corners = [
            nearest_walkable(maze, GridCoord(1, 1)),
            nearest_walkable(maze, GridCoord(1, maze.width - 2)),
            nearest_walkable(maze, GridCoord(maze.height - 2, 1)),
            nearest_walkable(maze, GridCoord(maze.height - 2, maze.width - 2)),
        ]

        def manhattan(a: GridCoord, b: GridCoord) -> int:
            return abs(a.row - b.row) + abs(a.col - b.col)

        corner_target = min(corners, key=lambda c: manhattan(c, ambush))

        # Corner ambush bias
        if random.random() < self.pinky_corner_bias:
            return corner_target
        return ambush

    def _blinky_target(self, pac: PacMan) -> GridCoord:
        return pac.grid

    def _inky_target(self, pac: PacMan, maze: Maze) -> GridCoord:
        # Mild wobble: occasionally target a neighbor of Pac-Man
        if random.random() < 0.25:
            nbrs = maze.neighbors(pac.grid)
            if nbrs:
                return random.choice(nbrs)
        return pac.grid

    def set_phase_reversal(self) -> None:
        """Called by Game when Scatter/Chase phase changes."""
        self.force_reverse = True

    def choose_direction(self, maze: Maze, pac: PacMan, phase: Phase) -> None:
        dirs = self._valid_dirs(maze)
        if not dirs:
            self.current_dir = Direction.NONE
            return

        # If phase changed, allow reversal immediately if possible.
        if self.force_reverse:
            opp = self.current_dir.opposite()
            if opp in dirs:
                self.current_dir = opp
            self.force_reverse = False

        # Avoid reversing in normal decisions (classic feel)
        dirs = self._prefer_non_reverse(dirs)

        # FRIGHTENED: random at intersections
        if self.mode == GhostMode.FRIGHTENED:
            self.current_dir = random.choice(dirs)
            return

        # EATEN: go to house
        if self.mode == GhostMode.EATEN:
            goal = self.house_tile
        else:
            # SCATTER: go to home corner
            if phase == Phase.SCATTER:
                goal = self.home_corner
            else:
                # CHASE: personality targets
                if self.type == GhostType.BLINKY:
                    goal = self._blinky_target(pac)
                elif self.type == GhostType.PINKY:
                    goal = self._pinky_target(maze, pac)
                else:  # INKY
                    if random.random() < self.inky_erratic_chance:
                        self.current_dir = random.choice(dirs)
                        return
                    goal = self._inky_target(pac, maze)

        step = bfs_next_step(maze, self.grid, goal)
        if step is None:
            # fallback: keep direction if possible else random
            if self.current_dir in dirs:
                return
            self.current_dir = random.choice(dirs)
            return

        desired = dir_from_to(self.grid, step)
        if desired in dirs:
            self.current_dir = desired
        else:
            # fallback: minimize manhattan distance
            def manhattan_after(d: Direction) -> int:
                nxt = self.grid.moved(d)
                return abs(nxt.row - goal.row) + abs(nxt.col - goal.col)
            self.current_dir = min(dirs, key=manhattan_after)

    def update(self, maze: Maze, pac: PacMan, phase: Phase, dt: float) -> None:
        self.prev_grid = self.grid

        if maze.is_centered(self.world):
            self.grid = maze.world_to_grid(self.world)
            self.world = maze.grid_to_world(self.grid)

            # If eaten and reached house, return to normal
            if self.mode == GhostMode.EATEN and self.grid == self.house_tile:
                self.mode = GhostMode.NORMAL

            self.choose_direction(maze, pac, phase)

            nxt = self.grid.moved(self.current_dir)
            if self.current_dir != Direction.NONE and not maze.is_walkable(nxt):
                self.current_dir = Direction.NONE

        if self.current_dir != Direction.NONE:
            dr, dc = self.current_dir.delta()
            vel = pygame.Vector2(dc, dr) * self.speed_px()
            self.world += vel * dt
            self.grid = maze.world_to_grid(self.world)


# =========================
# Game orchestration
# =========================

class Game:
    def __init__(self, maze: Maze, pacman: PacMan, ghosts: List[Ghost], house_tile: GridCoord):
        self.maze = maze
        self.pacman = pacman
        self.ghosts = ghosts
        self.house_tile = house_tile

        self.score = 0
        self.is_running = True

        # Points
        self.pellet_points = 10
        self.power_points = 50
        self.ghost_points = 200

        # Frightened timer overrides phase
        self.fright_timer = 0.0

        # Scatter/Chase schedule (simple classic-ish pattern)
        # You can tweak these numbers freely.
        self.phase_schedule: List[Tuple[Phase, float]] = [
            (Phase.SCATTER, 7.0),
            (Phase.CHASE, 20.0),
            (Phase.SCATTER, 7.0),
            (Phase.CHASE, 20.0),
            (Phase.SCATTER, 5.0),
            (Phase.CHASE, 20.0),
            (Phase.SCATTER, 5.0),
            (Phase.CHASE, 9999.0),  # essentially forever
        ]
        self.phase_index = 0
        self.phase: Phase = self.phase_schedule[0][0]
        self.phase_timer = self.phase_schedule[0][1]

        # Spawns for reset
        self.pac_spawn = pacman.grid
        self.ghost_spawns = [g.grid for g in ghosts]

    def set_frightened(self, seconds: float) -> None:
        self.fright_timer = seconds
        for g in self.ghosts:
            if g.mode != GhostMode.EATEN:
                g.mode = GhostMode.FRIGHTENED

    def _advance_phase(self) -> None:
        """Advance scatter/chase phase and force reversal on ghosts."""
        self.phase_index = (self.phase_index + 1) % len(self.phase_schedule)
        self.phase, self.phase_timer = self.phase_schedule[self.phase_index]
        for g in self.ghosts:
            g.set_phase_reversal()

    def update(self, dt: float) -> None:
        if not self.is_running:
            return

        # 1) Phase timer only counts down when not frightened (fright overrides phase behavior)
        if self.fright_timer <= 0:
            self.phase_timer -= dt
            if self.phase_timer <= 0:
                self._advance_phase()

        # 2) Frightened timer
        if self.fright_timer > 0:
            self.fright_timer = max(0.0, self.fright_timer - dt)
            if self.fright_timer == 0.0:
                for g in self.ghosts:
                    if g.mode == GhostMode.FRIGHTENED:
                        g.mode = GhostMode.NORMAL

        # 3) Move PacMan
        self.pacman.update(self.maze, dt)

        # 4) Consume pellets only when centered (avoids double-consumption)
        if self.maze.is_centered(self.pacman.world):
            eaten = self.maze.consume_at(self.pacman.grid)
            if eaten == TileType.PELLET:
                self.score += self.pellet_points
            elif eaten == TileType.POWER:
                self.score += self.power_points
                self.set_frightened(7.0)

        # 5) Move ghosts using current phase (scatter/chase) unless frightened/eaten override in Ghost.mode
        for g in self.ghosts:
            g.update(self.maze, self.pacman, self.phase, dt)

        # 6) Collisions (tile-based + pass-through)
        self.check_collisions()

    def check_collisions(self) -> None:
        p = self.pacman
        for g in self.ghosts:
            same_tile = (p.grid == g.grid)
            pass_through = (p.prev_grid == g.grid and p.grid == g.prev_grid)

            if same_tile or pass_through:
                if g.mode == GhostMode.FRIGHTENED:
                    self.score += self.ghost_points
                    g.mode = GhostMode.EATEN
                    g.world = self.maze.grid_to_world(g.grid)
                elif g.mode != GhostMode.EATEN:
                    p.take_damage()
                    if p.lives <= 0:
                        self.is_running = False
                        return
                    self.reset_positions()
                    return

    def reset_positions(self) -> None:
        self.pacman.grid = self.pac_spawn
        self.pacman.prev_grid = self.pac_spawn
        self.pacman.world = self.maze.grid_to_world(self.pac_spawn)
        self.pacman.current_dir = Direction.LEFT
        self.pacman.desired_dir = Direction.LEFT

        for g, sp in zip(self.ghosts, self.ghost_spawns):
            g.grid = sp
            g.prev_grid = sp
            g.world = self.maze.grid_to_world(sp)
            g.mode = GhostMode.NORMAL
            g.current_dir = Direction.LEFT
            g.force_reverse = False

        self.fright_timer = 0.0
        self.phase_index = 0
        self.phase, self.phase_timer = self.phase_schedule[0]

    def remaining_pellets(self) -> int:
        count = 0
        for r in range(self.maze.height):
            for c in range(self.maze.width):
                t = self.maze.tile_at(GridCoord(r, c))
                if t in (TileType.PELLET, TileType.POWER):
                    count += 1
        return count


# =========================
# Demo level builder
# =========================

def make_demo_game(tile_size: int) -> Game:
    W, P, O = TileType.WALL, TileType.PELLET, TileType.POWER

    grid = [
        [W,W,W,W,W,W,W,W,W,W,W],
        [W,P,P,P,P,P,P,P,P,P,W],
        [W,P,W,W,P,W,W,P,W,P,W],
        [W,P,P,P,O,P,P,P,W,P,W],
        [W,P,W,W,P,W,W,P,W,P,W],
        [W,P,P,P,P,P,P,P,P,P,W],
        [W,P,W,W,P,W,W,W,W,P,W],
        [W,P,P,P,P,P,P,P,P,P,W],
        [W,W,W,W,W,W,W,W,W,W,W],
    ]

    maze = Maze(TileMap(grid), tile_size)

    pac_spawn = GridCoord(7, 1)
    house_tile = GridCoord(4, 5)

    pac = PacMan(pac_spawn, maze)

    # Home corners (classic-ish):
    # Blinky: top-right, Pinky: top-left, Inky: bottom-right (Clyde would be bottom-left)
    top_left = GridCoord(1, 1)
    top_right = GridCoord(1, maze.width - 2)
    bottom_right = GridCoord(maze.height - 2, maze.width - 2)

    # Pinky tuning knobs HERE:
    pinky_lookahead_tiles = 4   # 2..8
    pinky_corner_bias = 0.75    # 0.0..1.0 (higher = more corner-ambushy)

    ghosts = [
        Ghost(GhostType.BLINKY, start_tile=GridCoord(1, 9), maze=maze, color=(220, 60, 60),
              house_tile=house_tile, home_corner=top_right),
        Ghost(GhostType.PINKY, start_tile=GridCoord(1, 1), maze=maze, color=(255, 105, 180),
              house_tile=house_tile, home_corner=top_left,
              pinky_lookahead_tiles=pinky_lookahead_tiles, pinky_corner_bias=pinky_corner_bias),
        Ghost(GhostType.INKY, start_tile=GridCoord(7, 9), maze=maze, color=(60, 220, 220),
              house_tile=house_tile, home_corner=bottom_right),
    ]

    return Game(maze, pac, ghosts, house_tile)


# =========================
# Rendering (Pygame)
# =========================

BLACK = (0, 0, 0)
BLUE  = (40, 40, 200)
WHITE = (240, 240, 240)
YELLOW = (255, 220, 0)
CYAN = (60, 220, 220)
NAVY = (15, 15, 70)

def draw_maze(screen: pygame.Surface, game: Game, top_margin: int) -> None:
    maze = game.maze
    ts = maze.tile_size

    screen.fill(BLACK)

    for r in range(maze.height):
        for c in range(maze.width):
            coord = GridCoord(r, c)
            t = maze.tile_at(coord)
            rect = pygame.Rect(c * ts, top_margin + r * ts, ts, ts)

            if t == TileType.WALL:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect)

            if t == TileType.PELLET:
                pygame.draw.circle(screen, WHITE, rect.center, max(2, ts // 10))
            elif t == TileType.POWER:
                pygame.draw.circle(screen, WHITE, rect.center, max(4, ts // 5))

def draw_pacman(screen: pygame.Surface, game: Game, top_margin: int) -> None:
    ts = game.maze.tile_size
    p = game.pacman
    radius = ts // 2 - 3
    pos = (int(p.world.x), int(top_margin + p.world.y))

    pygame.draw.circle(screen, YELLOW, pos, radius)

    d = p.current_dir
    if d != Direction.NONE:
        if d == Direction.RIGHT:
            tri = [pos, (pos[0]+radius, pos[1]-radius//2), (pos[0]+radius, pos[1]+radius//2)]
        elif d == Direction.LEFT:
            tri = [pos, (pos[0]-radius, pos[1]-radius//2), (pos[0]-radius, pos[1]+radius//2)]
        elif d == Direction.UP:
            tri = [pos, (pos[0]-radius//2, pos[1]-radius), (pos[0]+radius//2, pos[1]-radius)]
        else:
            tri = [pos, (pos[0]-radius//2, pos[1]+radius), (pos[0]+radius//2, pos[1]+radius)]
        pygame.draw.polygon(screen, BLACK, tri)

def draw_ghost(screen: pygame.Surface, g: Ghost, maze: Maze, top_margin: int) -> None:
    ts = maze.tile_size
    radius = ts // 2 - 3
    pos = (int(g.world.x), int(top_margin + g.world.y))

    if g.mode == GhostMode.FRIGHTENED:
        color = CYAN
    elif g.mode == GhostMode.EATEN:
        color = (200, 200, 200)
    else:
        color = g.color

    pygame.draw.circle(screen, color, pos, radius)

    eye_offset_x = radius // 3
    eye_offset_y = radius // 4
    eye_r = max(2, radius // 5)
    pygame.draw.circle(screen, WHITE, (pos[0] - eye_offset_x, pos[1] - eye_offset_y), eye_r)
    pygame.draw.circle(screen, WHITE, (pos[0] + eye_offset_x, pos[1] - eye_offset_y), eye_r)
    pygame.draw.circle(screen, NAVY, (pos[0] - eye_offset_x, pos[1] - eye_offset_y), max(1, eye_r // 2))
    pygame.draw.circle(screen, NAVY, (pos[0] + eye_offset_x, pos[1] - eye_offset_y), max(1, eye_r // 2))

def draw_hud(screen: pygame.Surface, game: Game, font: pygame.font.Font, width_px: int) -> None:
    status = "RUNNING" if game.is_running else "GAME OVER"
    txt = f"Score: {game.score}   Lives: {game.pacman.lives}   Pellets: {game.remaining_pellets()}   {status}"
    screen.blit(font.render(txt, True, WHITE), (10, 10))

    t_phase = font.render(f"Phase: {game.phase.name} ({max(0.0, game.phase_timer):0.1f}s)", True, WHITE)
    screen.blit(t_phase, (10, 30))

    if game.fright_timer > 0:
        t2 = font.render(f"Fright: {game.fright_timer:0.1f}s", True, CYAN)
        screen.blit(t2, (width_px - t2.get_width() - 10, 10))


# =========================
# Input / Main
# =========================

def handle_input(game: Game) -> None:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        game.pacman.queue_turn(Direction.UP)
    elif keys[pygame.K_DOWN]:
        game.pacman.queue_turn(Direction.DOWN)
    elif keys[pygame.K_LEFT]:
        game.pacman.queue_turn(Direction.LEFT)
    elif keys[pygame.K_RIGHT]:
        game.pacman.queue_turn(Direction.RIGHT)

def main():
    pygame.init()
    pygame.display.set_caption("Pac-Man (Scatter/Chase + Tunable Pinky)")

    tile_size = 32
    top_margin = 52

    game = make_demo_game(tile_size)
    width_px = game.maze.width * tile_size
    height_px = top_margin + game.maze.height * tile_size

    screen = pygame.display.set_mode((width_px, height_px))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game = make_demo_game(tile_size)

        handle_input(game)
        game.update(dt)

        draw_maze(screen, game, top_margin)
        draw_pacman(screen, game, top_margin)
        for g in game.ghosts:
            draw_ghost(screen, g, game.maze, top_margin)
        draw_hud(screen, game, font, width_px)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()