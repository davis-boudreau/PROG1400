import sys
import pygame

from util import Direction, TileType, GameState
from model import Game, Pellet, PowerPellet, ENABLE_ITEMS, ENABLE_POWER

CELL_SIZE = 24
FPS = 60

COLOR_BG = (0, 0, 0)
COLOR_WALL = (0, 0, 200)
COLOR_FLOOR = (20, 20, 20)
COLOR_PACMAN = (255, 230, 0)
COLOR_GHOST = (255, 0, 0)
COLOR_FRIGHT = (0, 120, 255)
COLOR_PELLET = (240, 240, 240)
COLOR_POWER = (255, 200, 255)

KEY_TO_DIR = {
    pygame.K_UP: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
}


class PacmanApp:
    def __init__(self, enable_pause: bool = False) -> None:
        pygame.init()
        pygame.display.set_caption('PROG1400 Pac-Man (Weekly Snapshot)')

        self.game = Game()
        self.game.load_level(1)

        w = self.game.maze.cols * CELL_SIZE
        h = self.game.maze.rows * CELL_SIZE + 48
        self.screen = pygame.display.set_mode((w, h))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 48)

        self.running = True
        self.input_dir = Direction.NONE
        self.enable_pause = enable_pause
        self.paused = False

    def run(self) -> None:
        while self.running:
            self.clock.tick(FPS)
            self._events()
            self._update()
            self._draw()
        pygame.quit()
        sys.exit()

    def _events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key in KEY_TO_DIR:
                    self.input_dir = KEY_TO_DIR[event.key]
                if event.key == pygame.K_r:
                    self.game.load_level(1)
                if enable_pause and event.key == pygame.K_p:
                    self.paused = not self.paused

    def _update(self) -> None:
        if self.paused:
            return
        self.game.update(self.input_dir)

    def _draw(self) -> None:
        self.screen.fill(COLOR_BG)
        self._draw_maze()
        if ENABLE_ITEMS:
            self._draw_items()
        self._draw_actors()
        self._draw_hud()
        self._draw_overlay()
        pygame.display.flip()

    def _draw_maze(self) -> None:
        m = self.game.maze
        for r in range(m.rows):
            for c in range(m.cols):
                x = c * CELL_SIZE
                y = r * CELL_SIZE
                t = m.tiles[r][c]
                if t == TileType.WALL:
                    pygame.draw.rect(self.screen, COLOR_WALL, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(self.screen, COLOR_FLOOR, (x, y, CELL_SIZE, CELL_SIZE))

    def _draw_items(self) -> None:
        m = self.game.maze
        for cell, item in m.items.items():
            cx = cell.c * CELL_SIZE + CELL_SIZE // 2
            cy = cell.r * CELL_SIZE + CELL_SIZE // 2
            if isinstance(item, Pellet):
                pygame.draw.circle(self.screen, COLOR_PELLET, (cx, cy), 3)
            elif isinstance(item, PowerPellet):
                pygame.draw.circle(self.screen, COLOR_POWER, (cx, cy), 7)
            else:
                pygame.draw.circle(self.screen, (0, 255, 0), (cx, cy), 5)

    def _draw_actors(self) -> None:
        p = self.game.pacman
        px = p.cell.c * CELL_SIZE + CELL_SIZE // 2
        py = p.cell.r * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(self.screen, COLOR_PACMAN, (px, py), CELL_SIZE // 2 - 2)

        for g in self.game.ghosts:
            gx = g.cell.c * CELL_SIZE + CELL_SIZE // 2
            gy = g.cell.r * CELL_SIZE + CELL_SIZE // 2
            color = COLOR_FRIGHT if (ENABLE_POWER and g.is_frightened()) else COLOR_GHOST
            pygame.draw.circle(self.screen, color, (gx, gy), CELL_SIZE // 2 - 2)

    def _draw_hud(self) -> None:
        y = self.game.maze.rows * CELL_SIZE
        pygame.draw.rect(self.screen, (10, 10, 10), (0, y, self.screen.get_width(), 48))
        text = f"Score: {self.game.score.get_score()}   Lives: {self.game.score.get_lives()}   Level: {self.game.level}"
        surf = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surf, (12, y + 14))

    def _draw_overlay(self) -> None:
        if self.paused:
            msg = 'PAUSED'
        elif self.game.state == GameState.READY:
            msg = 'READY - Press an arrow key'
        elif self.game.state == GameState.GAME_OVER:
            msg = 'GAME OVER - Press R'
        else:
            return
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        surf = self.big_font.render(msg, True, (255, 255, 255))
        rect = surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(surf, rect)


if __name__ == '__main__':
    enable_pause = False
    PacmanApp(enable_pause=enable_pause).run()
