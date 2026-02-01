import sys
import pygame

# Import from your skeleton module
# from pacman_skeleton import Game, Direction, GameState, TileType, Cell
#
# If everything is in one file for now, you can remove these imports and
# refer to the classes directly.

from pacman_skeleton import Game, Direction, GameState, TileType, Cell


# -----------------------------
# Configuration (easy to tweak)
# -----------------------------
CELL_SIZE = 24
FPS = 60

COLOR_BG = (0, 0, 0)
COLOR_WALL = (0, 0, 200)
COLOR_FLOOR = (20, 20, 20)
COLOR_PACMAN = (255, 230, 0)
COLOR_GHOST = (255, 0, 0)
COLOR_PELLET = (240, 240, 240)
COLOR_POWER = (255, 200, 255)

COLOR_TEXT = (255, 255, 255)
COLOR_OVERLAY = (0, 0, 0, 160)


# -----------------------------
# Helper: map keys to Direction
# -----------------------------
KEY_TO_DIR = {
    pygame.K_UP: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
}


class PacmanApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Pac-Man (Tile-by-Tile) - Loop Stub")

        self.game = Game()
        # Load a level (you will implement Game.load_level properly later)
        self.game.load_level(1)

        # If maze is not loaded yet, make a tiny fallback maze so the loop runs.
        self._ensure_fallback_level()

        # Create window sized to maze
        w = self.game.maze.cols * CELL_SIZE
        h = self.game.maze.rows * CELL_SIZE + 48  # HUD space
        self.screen = pygame.display.set_mode((w, h))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 48)

        self.running = True
        self.input_dir = Direction.NONE  # current input for the tick

    def _ensure_fallback_level(self) -> None:
        """Ensures there is something playable even before a level loader exists."""
        if self.game.maze.rows > 0 and self.game.maze.cols > 0 and self.game.maze.tiles:
            return

        rows, cols = 15, 19
        tiles = [[TileType.FLOOR for _ in range(cols)] for _ in range(rows)]
        # border walls
        for r in range(rows):
            tiles[r][0] = TileType.WALL
            tiles[r][cols - 1] = TileType.WALL
        for c in range(cols):
            tiles[0][c] = TileType.WALL
            tiles[rows - 1][c] = TileType.WALL

        # simple tunnel row in middle
        mid = rows // 2
        tiles[mid][0] = TileType.TUNNEL
        tiles[mid][cols - 1] = TileType.TUNNEL

        from pacman_skeleton import Maze, Pellet, PowerPellet, RandomGhost

        items = {}
        # sprinkle pellets
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                if (r, c) not in [(1, 1), (mid, 1), (mid, cols - 2)]:
                    items[Cell(r, c)] = Pellet()

        # power pellets
        items[Cell(1, cols - 2)] = PowerPellet(powerTicks=120)

        pac_spawn = Cell(1, 1)
        ghost_spawns = [Cell(mid, cols - 2)]

        self.game.maze = Maze(rows, cols, tiles, items, pac_spawn, ghost_spawns)
        self.game.pacman.cell = pac_spawn

        # one ghost just so collisions can be tested
        g0 = RandomGhost(cell=ghost_spawns[0], home=ghost_spawns[0], moveEveryTicks=2)
        self.game.ghosts = [g0]
        self.game.state = GameState.READY

    # -----------------------------
    # Main loop
    # -----------------------------
    def run(self) -> None:
        while self.running:
            dt_ms = self.clock.tick(FPS)  # keep constant FPS; dt_ms available if needed

            self.process_events()
            self.update(dt_ms)
            self.draw()

        pygame.quit()
        sys.exit()

    # -----------------------------
    # Event handling
    # -----------------------------
    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # Direction input: store for next tick
                if event.key in KEY_TO_DIR:
                    self.input_dir = KEY_TO_DIR[event.key]

                # Optional: restart
                if event.key == pygame.K_r:
                    self.game.score.reset_new_game()
                    self.game.load_level(1)
                    self._ensure_fallback_level()

                # Optional: pause toggle
                if event.key == pygame.K_p:
                    if self.game.state == GameState.PLAYING:
                        self.game.state = GameState.READY
                    elif self.game.state == GameState.READY:
                        self.game.state = GameState.PLAYING

    # -----------------------------
    # Update step (tile-by-tile)
    # -----------------------------
    def update(self, dt_ms: int) -> None:
        # Tile-by-tile classic: drive the model by ticks, not dt.
        # We still pass input each frame; the Game decides if it moves.
        self.game.update(self.input_dir)

        # You can optionally “consume” input so it behaves like a queued turn:
        # if the student wants to emulate classic turning behavior.
        # Uncomment to make direction a one-shot queue.
        # self.input_dir = Direction.NONE

        # Level complete -> advance (stub behavior)
        if self.game.state == GameState.LEVEL_COMPLETE:
            self.game.load_level(self.game.level + 1)
            self._ensure_fallback_level()

        # Game over -> do nothing until restart (R)
        # (kept simple for the stub)

    # -----------------------------
    # Drawing
    # -----------------------------
    def draw(self) -> None:
        self.screen.fill(COLOR_BG)

        self._draw_maze()
        self._draw_items()
        self._draw_actors()
        self._draw_hud()
        self._draw_overlay()

        pygame.display.flip()

    def _draw_maze(self) -> None:
        maze = self.game.maze
        for r in range(maze.rows):
            for c in range(maze.cols):
                x = c * CELL_SIZE
                y = r * CELL_SIZE
                tile = maze.tiles[r][c]
                if tile == TileType.WALL:
                    pygame.draw.rect(self.screen, COLOR_WALL, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(self.screen, COLOR_FLOOR, (x, y, CELL_SIZE, CELL_SIZE))

    def _draw_items(self) -> None:
        # Items are stored as dict[Cell, Item]
        from pacman_skeleton import Pellet, PowerPellet  # Fruit optional

        for cell, item in self.game.maze.items.items():
            cx = cell.c * CELL_SIZE + CELL_SIZE // 2
            cy = cell.r * CELL_SIZE + CELL_SIZE // 2

            if isinstance(item, Pellet):
                pygame.draw.circle(self.screen, COLOR_PELLET, (cx, cy), 3)
            elif isinstance(item, PowerPellet):
                pygame.draw.circle(self.screen, COLOR_POWER, (cx, cy), 7)
            else:
                # generic item
                pygame.draw.circle(self.screen, (0, 255, 0), (cx, cy), 5)

    def _draw_actors(self) -> None:
        # Pacman
        p = self.game.pacman
        px = p.cell.c * CELL_SIZE + CELL_SIZE // 2
        py = p.cell.r * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.screen, COLOR_PACMAN, (px, py), CELL_SIZE // 2 - 2)

        # Ghosts
        for g in self.game.ghosts:
            gx = g.cell.c * CELL_SIZE + CELL_SIZE // 2
            gy = g.cell.r * CELL_SIZE + CELL_SIZE // 2
            color = (0, 0, 255) if g.is_frightened() else COLOR_GHOST
            pygame.draw.circle(self.screen, color, (gx, gy), CELL_SIZE // 2 - 2)

    def _draw_hud(self) -> None:
        hud_y = self.game.maze.rows * CELL_SIZE
        pygame.draw.rect(self.screen, (10, 10, 10), (0, hud_y, self.screen.get_width(), 48))

        text = f"Score: {self.game.score.get_score()}   Lives: {self.game.score.get_lives()}   Level: {self.game.level}"
        surf = self.font.render(text, True, COLOR_TEXT)
        self.screen.blit(surf, (12, hud_y + 14))

        help_text = "Arrows: move | R: restart | P: toggle ready/play | Esc: quit"
        surf2 = self.font.render(help_text, True, (180, 180, 180))
        self.screen.blit(surf2, (12, hud_y + 30))

    def _draw_overlay(self) -> None:
        state = self.game.state
        if state not in (GameState.READY, GameState.GAME_OVER, GameState.LEVEL_COMPLETE):
            return

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.screen.blit(overlay, (0, 0))

        msg = ""
        if state == GameState.READY:
            msg = "READY - Press an arrow key"
        elif state == GameState.GAME_OVER:
            msg = "GAME OVER - Press R to restart"
        elif state == GameState.LEVEL_COMPLETE:
            msg = "LEVEL COMPLETE!"

        surf = self.big_font.render(msg, True, COLOR_TEXT)
        rect = surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(surf, rect)


if __name__ == "__main__":
    PacmanApp().run()