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
    CHASE = auto()
    FRIGHTENED = auto()
    EATEN = auto()


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
        """World coords inside the maze (no top margin). Center of tile."""
        return pygame.Vector2((c.col + 0.5) * self.tile_size, (c.row + 0.5) * self.tile_size)

    def world_to_grid(self, p: pygame.Vector2) -> GridCoord:
        """Convert world coords to tile index by flooring."""
        col = int(p.x // self.tile_size)
        row = int(p.y // self.tile_size)
        return GridCoord(row, col)

    def is_centered(self, p: pygame.Vector2, tol: float = 1.5) -> bool:
        """True if p is near the center of its current tile."""
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
    """
    Return the neighbor tile to step into from 'start' along a shortest path to 'goal'.
    BFS is fine for small grids.
    """
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
        return None  # unreachable

    # reconstruct: walk backward from goal until we reach start's neighbor
    step = goal
    while came_from[step] is not None and came_from[step] != start:
        step = came_from[step]
    return step if came_from[step] == start else step


def dir_from_to(a: GridCoord, b: GridCoord) -> Direction:
    dr = b.row - a.row
    dc = b.col - a.col
    if dr == -1 and dc == 0: return Direction.UP
    if dr ==  1 and dc == 0: return Direction.DOWN
    if dr ==  0 and dc == -1: return Direction.LEFT
    if dr ==  0 and dc ==  1: return Direction.RIGHT
    return Direction.NONE


# =========================
# Entities (continuous movement)
# =========================

class PacMan:
    def __init__(self, start_tile: GridCoord, maze: Maze):
        self.grid: GridCoord = start_tile                 # authoritative tile
        self.prev_grid: GridCoord = start_tile            # for pass-through checks
        self.world: pygame.Vector2 = maze.grid_to_world(start_tile)
        self.current_dir: Direction = Direction.LEFT
        self.desired_dir: Direction = Direction.LEFT
        self.speed_px: float = maze.tile_size * 6.0       # tiles/sec ~ 6
        self.lives: int = 3

    def queue_turn(self, d: Direction) -> None:
        if d != Direction.NONE:
            self.desired_dir = d

    def update(self, maze: Maze, dt: float) -> None:
        """
        Smooth movement with buffered turns:
        - Try to turn at centers if desired_dir is valid.
        - If blocked ahead at center, stop.
        """
        self.prev_grid = self.grid

        # Turn logic at tile center
        if maze.is_centered(self.world):
            self.grid = maze.world_to_grid(self.world)  # commit to tile at center
            self.world = maze.grid_to_world(self.grid)  # snap to exact center

            # attempt buffered turn
            desired_next = self.grid.moved(self.desired_dir)
            if self.desired_dir != Direction.NONE and maze.is_walkable(desired_next):
                self.current_dir = self.desired_dir

            # if current direction blocked, stop
            forward_next = self.grid.moved(self.current_dir)
            if self.current_dir != Direction.NONE and not maze.is_walkable(forward_next):
                self.current_dir = Direction.NONE

        # Move smoothly in current direction
        if self.current_dir != Direction.NONE:
            dr, dc = self.current_dir.delta()
            vel = pygame.Vector2(dc, dr) * self.speed_px
            self.world += vel * dt
            # update grid (authoritative tile is still based on tile position; we’ll commit at centers)
            self.grid = maze.world_to_grid(self.world)

    def take_damage(self) -> None:
        self.lives -= 1


class Ghost:
    def __init__(self, start_tile: GridCoord, maze: Maze, color: Tuple[int, int, int], house_tile: GridCoord):
        self.grid: GridCoord = start_tile
        self.prev_grid: GridCoord = start_tile
        self.world: pygame.Vector2 = maze.grid_to_world(start_tile)

        self.mode: GhostMode = GhostMode.CHASE
        self.current_dir: Direction = Direction.LEFT

        self.speed_px_chase: float = maze.tile_size * 5.2
        self.speed_px_fright: float = maze.tile_size * 4.0
        self.speed_px_eaten: float = maze.tile_size * 7.0

        self.color = color
        self.house_tile = house_tile

    def speed_px(self) -> float:
        if self.mode == GhostMode.FRIGHTENED:
            return self.speed_px_fright
        if self.mode == GhostMode.EATEN:
            return self.speed_px_eaten
        return self.speed_px_chase

    def choose_direction(self, maze: Maze, target: GridCoord) -> None:
        """
        Decision only at tile centers:
        - CHASE: BFS to target and follow shortest path
        - FRIGHTENED: random at intersections (avoid reversing if possible)
        - EATEN: BFS back to ghost house
        """
        options = []
        for d in (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT):
            n = self.grid.moved(d)
            if maze.is_walkable(n):
                options.append(d)

        if not options:
            self.current_dir = Direction.NONE
            return

        # Prefer not to reverse unless forced
        non_reverse = [d for d in options if d != self.current_dir.opposite()]
        use_options = non_reverse if non_reverse else options

        if self.mode == GhostMode.FRIGHTENED:
            self.current_dir = random.choice(use_options)
            return

        goal = self.house_tile if self.mode == GhostMode.EATEN else target
        step = bfs_next_step(maze, self.grid, goal)

        if step is None:
            # fallback: keep going if possible, else random
            if self.current_dir in use_options:
                return
            self.current_dir = random.choice(use_options)
            return

        desired = dir_from_to(self.grid, step)
        # If desired direction is blocked by no-reverse constraint, pick best available
        if desired in use_options:
            self.current_dir = desired
        else:
            # choose direction that minimizes distance as a fallback
            def manhattan_after(d: Direction) -> int:
                nxt = self.grid.moved(d)
                return abs(nxt.row - goal.row) + abs(nxt.col - goal.col)
            self.current_dir = min(use_options, key=manhattan_after)

    def update(self, maze: Maze, target: GridCoord, dt: float) -> None:
        self.prev_grid = self.grid

        if maze.is_centered(self.world):
            self.grid = maze.world_to_grid(self.world)
            self.world = maze.grid_to_world(self.grid)

            # If eaten and reached house, return to chase
            if self.mode == GhostMode.EATEN and self.grid == self.house_tile:
                self.mode = GhostMode.CHASE

            self.choose_direction(maze, target)

            # Stop if blocked (rare due to choice logic)
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
        self.fright_timer = 0.0

        # points
        self.pellet_points = 10
        self.power_points = 50
        self.ghost_points = 200

        # spawns for reset
        self.pac_spawn = pacman.grid
        self.ghost_spawns = [g.grid for g in ghosts]

    def set_frightened(self, seconds: float) -> None:
        self.fright_timer = seconds
        for g in self.ghosts:
            if g.mode != GhostMode.EATEN:
                g.mode = GhostMode.FRIGHTENED

    def update(self, dt: float) -> None:
        if not self.is_running:
            return

        # 1) Update frightened timer
        if self.fright_timer > 0:
            self.fright_timer = max(0.0, self.fright_timer - dt)
            if self.fright_timer == 0.0:
                for g in self.ghosts:
                    if g.mode == GhostMode.FRIGHTENED:
                        g.mode = GhostMode.CHASE

        # 2) Move entities continuously
        self.pacman.update(self.maze, dt)

        # 3) Consume pellets only when PacMan is at tile center (avoids double-consumption mid-tile)
        if self.maze.is_centered(self.pacman.world):
            eaten = self.maze.consume_at(self.pacman.grid)
            if eaten == TileType.PELLET:
                self.score += self.pellet_points
            elif eaten == TileType.POWER:
                self.score += self.power_points
                self.set_frightened(7.0)

        # 4) Ghost movement (target is PacMan tile)
        for g in self.ghosts:
            g.update(self.maze, self.pacman.grid, dt)

        # 5) Tile-based collision (+ pass-through)
        self.check_collisions()

    def check_collisions(self) -> None:
        p = self.pacman
        for g in self.ghosts:
            same_tile = (p.grid == g.grid)
            pass_through = (p.prev_grid == g.grid and p.grid == g.prev_grid)

            if same_tile or pass_through:
                if g.mode == GhostMode.FRIGHTENED:
                    # ghost eaten
                    self.score += self.ghost_points
                    g.mode = GhostMode.EATEN
                    # snap to center to avoid jitter
                    g.world = self.maze.grid_to_world(g.grid)
                elif g.mode != GhostMode.EATEN:
                    # pacman hit
                    p.take_damage()
                    if p.lives <= 0:
                        self.is_running = False
                        return
                    self.reset_positions()
                    return

    def reset_positions(self) -> None:
        # reset pacman
        self.pacman.grid = self.pac_spawn
        self.pacman.prev_grid = self.pac_spawn
        self.pacman.world = self.maze.grid_to_world(self.pac_spawn)
        self.pacman.current_dir = Direction.LEFT
        self.pacman.desired_dir = Direction.LEFT

        # reset ghosts
        for g, sp in zip(self.ghosts, self.ghost_spawns):
            g.grid = sp
            g.prev_grid = sp
            g.world = self.maze.grid_to_world(sp)
            g.mode = GhostMode.CHASE
            g.current_dir = Direction.LEFT

        self.fright_timer = 0.0

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
    W, P, D, O = TileType.WALL, TileType.PELLET, TileType.PATH, TileType.POWER

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

    ghosts = [
        Ghost(start_tile=GridCoord(1, 9), maze=maze, color=(220, 60, 60), house_tile=house_tile),
        Ghost(start_tile=GridCoord(1, 1), maze=maze, color=(255, 105, 180), house_tile=house_tile),
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

    # simple "mouth" triangle based on direction
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

    color = CYAN if g.mode == GhostMode.FRIGHTENED else g.color
    pygame.draw.circle(screen, color, pos, radius)

    # eyes
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

    if game.fright_timer > 0:
        t2 = font.render(f"Fright: {game.fright_timer:0.1f}s", True, CYAN)
        screen.blit(t2, (width_px - t2.get_width() - 10, 10))


# =========================
# Input
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


# =========================
# Main
# =========================

def main():
    pygame.init()
    pygame.display.set_caption("Arcade-like Pac-Man (Continuous + Buffered Turns + Ghost AI)")

    tile_size = 32
    top_margin = 52

    game = make_demo_game(tile_size)
    width_px = game.maze.width * tile_size
    height_px = top_margin + game.maze.height * tile_size

    screen = pygame.display.set_mode((width_px, height_px))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)

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