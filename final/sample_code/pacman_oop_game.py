import json
import random
import tkinter as tk
from collections import deque
from pathlib import Path

CELL_SIZE = 28
HUD_HEIGHT = 60
STEP_MS = 140
ENEMY_STEP_MS = 240
PLAYER_COLOR = "gold"
ENEMY_COLOR = "tomato"
WALL_COLOR = "navy"
FLOOR_COLOR = "black"
DOT_COLOR = "white"
POWER_COLOR = "cyan"
TEXT_COLOR = "white"

LEVELS = [
    [
        "####################",
        "#P................E#",
        "#.###.#.#.####.#.#.#",
        "#.....#.#....#.#.#.#",
        "#.#####.####.#.#.#.#",
        "#.............#.#..#",
        "#.###.#####.###.##.#",
        "#...#.....#.....#..#",
        "###.#.###.#####.#.##",
        "#...#...#...o...#..#",
        "#.#####.#######.##.#",
        "#.......#.....#....#",
        "#.#####.#.###.####.#",
        "#.................##",
        "####################",
    ],
    [
        "####################",
        "#P....#.......#....#",
        "#.##.#.#####.#.##..#",
        "#....#...#...#..#..#",
        "#.######.#.####.#.##",
        "#......#.#....#.#..#",
        "#.####.#.####.#.##.#",
        "#.#....#....#.#....#",
        "#.#.######.#.#.###.#",
        "#...#..o...#...#E..#",
        "###.#.#########.#.##",
        "#...#.....#.....#..#",
        "#.#######.#.######.#",
        "#.........#........#",
        "####################",
    ],
]

SCORES_FILE = Path(__file__).with_name("pacman_scores.json")


class ScoreBoard:
    def __init__(self, path: Path):
        self.path = path
        self.best_score = 0
        self.games_played = 0
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
                self.best_score = int(data.get("best_score", 0))
                self.games_played = int(data.get("games_played", 0))
            except Exception:
                self.best_score = 0
                self.games_played = 0

    def save_result(self, score: int):
        self.games_played += 1
        self.best_score = max(self.best_score, score)
        self.path.write_text(
            json.dumps(
                {"best_score": self.best_score, "games_played": self.games_played},
                indent=2,
            )
        )


class Entity:
    def __init__(self, row: int, col: int, color: str):
        self.row = row
        self.col = col
        self.start_row = row
        self.start_col = col
        self.color = color

    def reset(self):
        self.row = self.start_row
        self.col = self.start_col


class Player(Entity):
    def __init__(self, row: int, col: int):
        super().__init__(row, col, PLAYER_COLOR)
        self.score = 0
        self.lives = 3
        self.power_ticks = 0

    @property
    def powered_up(self) -> bool:
        return self.power_ticks > 0


class Enemy(Entity):
    def __init__(self, row: int, col: int):
        super().__init__(row, col, ENEMY_COLOR)
        self.is_frightened = False


class Level:
    WALL = "#"
    DOT = "."
    POWER = "o"
    EMPTY = " "
    PLAYER = "P"
    ENEMY = "E"

    def __init__(self, level_map):
        self.original = [list(row) for row in level_map]
        self.height = len(self.original)
        self.width = len(self.original[0])
        self.grid = []
        self.player_start = (1, 1)
        self.enemy_starts = []
        self.remaining_items = 0
        self.reset()

    def reset(self):
        self.grid = [row[:] for row in self.original]
        self.enemy_starts = []
        self.remaining_items = 0
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == self.PLAYER:
                    self.player_start = (r, c)
                    self.grid[r][c] = self.EMPTY
                elif cell == self.ENEMY:
                    self.enemy_starts.append((r, c))
                    self.grid[r][c] = self.EMPTY
                elif cell in (self.DOT, self.POWER):
                    self.remaining_items += 1

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def is_wall(self, row: int, col: int) -> bool:
        return self.grid[row][col] == self.WALL

    def is_walkable(self, row: int, col: int) -> bool:
        return self.in_bounds(row, col) and not self.is_wall(row, col)

    def collect_at(self, row: int, col: int) -> int:
        cell = self.grid[row][col]
        if cell == self.DOT:
            self.grid[row][col] = self.EMPTY
            self.remaining_items -= 1
            return 10
        if cell == self.POWER:
            self.grid[row][col] = self.EMPTY
            self.remaining_items -= 1
            return 50
        return 0

    def is_power_item(self, row: int, col: int) -> bool:
        return self.grid[row][col] == self.POWER


class Game:
    DIRECTIONS = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1),
        "w": (-1, 0),
        "s": (1, 0),
        "a": (0, -1),
        "d": (0, 1),
        "W": (-1, 0),
        "S": (1, 0),
        "A": (0, -1),
        "D": (0, 1),
    }

    def __init__(self, root):
        self.root = root
        self.root.title("OOP Pac-Man Like Game")
        self.scoreboard = ScoreBoard(SCORES_FILE)
        self.level_index = 0
        self.level = Level(LEVELS[self.level_index])
        self.player = Player(*self.level.player_start)
        self.enemies = [Enemy(r, c) for r, c in self.level.enemy_starts]
        self.game_over = False
        self.win = False
        self.message = "Collect all dots. Arrow keys or WASD to move."
        self.pending_move = None
        self.enemy_loop_id = None
        self.player_loop_id = None

        width = self.level.width * CELL_SIZE
        height = self.level.height * CELL_SIZE + HUD_HEIGHT
        self.canvas = tk.Canvas(root, width=width, height=height, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.root.bind("<KeyPress>", self.handle_keypress)
        self.restart_button = tk.Button(root, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=6)

        self.start_loops()
        self.draw()

    def start_loops(self):
        self.stop_loops()
        self.player_loop_id = self.root.after(STEP_MS, self.game_tick)
        self.enemy_loop_id = self.root.after(ENEMY_STEP_MS, self.enemy_tick)

    def stop_loops(self):
        if self.player_loop_id is not None:
            self.root.after_cancel(self.player_loop_id)
            self.player_loop_id = None
        if self.enemy_loop_id is not None:
            self.root.after_cancel(self.enemy_loop_id)
            self.enemy_loop_id = None

    def restart_game(self):
        self.level_index = 0
        self.level = Level(LEVELS[self.level_index])
        self.player = Player(*self.level.player_start)
        self.enemies = [Enemy(r, c) for r, c in self.level.enemy_starts]
        self.game_over = False
        self.win = False
        self.message = "New game started."
        self.pending_move = None
        self.start_loops()
        self.draw()

    def next_level(self):
        self.level_index += 1
        if self.level_index >= len(LEVELS):
            self.win = True
            self.game_over = True
            self.message = "You cleared all levels! Press Restart Game to play again."
            self.finish_game()
            return
        self.level = Level(LEVELS[self.level_index])
        self.player.row, self.player.col = self.level.player_start
        self.player.start_row, self.player.start_col = self.level.player_start
        self.player.power_ticks = 0
        self.enemies = [Enemy(r, c) for r, c in self.level.enemy_starts]
        self.message = f"Level {self.level_index + 1}"

    def finish_game(self):
        self.stop_loops()
        self.scoreboard.save_result(self.player.score)

    def handle_keypress(self, event):
        if event.keysym in self.DIRECTIONS:
            self.pending_move = self.DIRECTIONS[event.keysym]

    def game_tick(self):
        if not self.game_over and self.pending_move:
            self.move_player(*self.pending_move)
        if self.player.power_ticks > 0:
            self.player.power_ticks -= 1
        for enemy in self.enemies:
            enemy.is_frightened = self.player.powered_up
        self.check_level_complete()
        self.draw()
        if not self.game_over:
            self.player_loop_id = self.root.after(STEP_MS, self.game_tick)

    def enemy_tick(self):
        if not self.game_over:
            for enemy in self.enemies:
                self.move_enemy(enemy)
            self.check_collisions()
            self.draw()
            self.enemy_loop_id = self.root.after(ENEMY_STEP_MS, self.enemy_tick)

    def move_player(self, dr: int, dc: int):
        nr = self.player.row + dr
        nc = self.player.col + dc
        if not self.level.is_walkable(nr, nc):
            self.message = "Wall hit. Choose another direction."
            return

        was_power = self.level.is_power_item(nr, nc)
        self.player.row, self.player.col = nr, nc
        gained = self.level.collect_at(nr, nc)
        self.player.score += gained

        if was_power:
            self.player.power_ticks = 35
            self.message = "Power item collected! Enemies are frightened."
        elif gained > 0:
            self.message = f"Collected item. Score +{gained}"
        else:
            self.message = ""

        self.check_collisions()

    def move_enemy(self, enemy: Enemy):
        neighbors = self.valid_neighbors(enemy.row, enemy.col)
        if not neighbors:
            return

        if enemy.is_frightened:
            target = self.farthest_neighbor_from_player(neighbors)
            enemy.row, enemy.col = target
            return

        path = self.shortest_path((enemy.row, enemy.col), (self.player.row, self.player.col))
        if len(path) >= 2:
            enemy.row, enemy.col = path[1]
        else:
            enemy.row, enemy.col = random.choice(neighbors)

    def farthest_neighbor_from_player(self, neighbors):
        best = None
        best_distance = -1
        for cell in neighbors:
            dist = abs(cell[0] - self.player.row) + abs(cell[1] - self.player.col)
            if dist > best_distance:
                best_distance = dist
                best = cell
        return best

    def valid_neighbors(self, row: int, col: int):
        moves = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if self.level.is_walkable(nr, nc):
                moves.append((nr, nc))
        return moves

    def shortest_path(self, start, goal):
        queue = deque([start])
        came_from = {start: None}
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            for nxt in self.valid_neighbors(*current):
                if nxt not in came_from:
                    came_from[nxt] = current
                    queue.append(nxt)
        if goal not in came_from:
            return [start]
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        return path

    def check_collisions(self):
        for enemy in self.enemies:
            if enemy.row == self.player.row and enemy.col == self.player.col:
                if self.player.powered_up:
                    self.player.score += 200
                    enemy.reset()
                    self.message = "Enemy caught! Score +200"
                else:
                    self.player.lives -= 1
                    self.message = f"Caught by enemy. Lives remaining: {self.player.lives}"
                    self.reset_positions()
                    if self.player.lives <= 0:
                        self.game_over = True
                        self.message = "Game Over. Press Restart Game to try again."
                        self.finish_game()
                break

    def reset_positions(self):
        self.player.reset()
        self.player.power_ticks = 0
        for enemy in self.enemies:
            enemy.reset()
            enemy.is_frightened = False

    def check_level_complete(self):
        if self.level.remaining_items == 0 and not self.game_over:
            self.player.score += 500
            self.message = "Level complete! Bonus +500"
            self.next_level()

    def draw(self):
        self.canvas.delete("all")
        self.draw_hud()
        self.draw_board()
        self.draw_entities()
        if self.game_over:
            self.draw_overlay()

    def draw_hud(self):
        width = self.level.width * CELL_SIZE
        self.canvas.create_rectangle(0, 0, width, HUD_HEIGHT, fill="#111", outline="#333")
        hud_text = (
            f"Level: {self.level_index + 1}    "
            f"Score: {self.player.score}    "
            f"Best: {self.scoreboard.best_score}    "
            f"Lives: {self.player.lives}    "
            f"Items Left: {self.level.remaining_items}"
        )
        self.canvas.create_text(12, 18, anchor="w", text=hud_text, fill=TEXT_COLOR, font=("Consolas", 14, "bold"))
        state_text = "POWER MODE" if self.player.powered_up else self.message
        self.canvas.create_text(12, 42, anchor="w", text=state_text, fill="lightgreen" if self.player.powered_up else "#ddd", font=("Consolas", 10))

    def draw_board(self):
        for r in range(self.level.height):
            for c in range(self.level.width):
                x1 = c * CELL_SIZE
                y1 = HUD_HEIGHT + r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                cell = self.level.grid[r][c]
                fill = WALL_COLOR if cell == Level.WALL else FLOOR_COLOR
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#222")
                if cell == Level.DOT:
                    self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=DOT_COLOR, outline=DOT_COLOR)
                elif cell == Level.POWER:
                    self.canvas.create_oval(x1 + 6, y1 + 6, x2 - 6, y2 - 6, fill=POWER_COLOR, outline=POWER_COLOR)

    def draw_entities(self):
        self.draw_entity(self.player, 5, 5, self.player.color)
        for enemy in self.enemies:
            color = "pink" if enemy.is_frightened else enemy.color
            self.draw_entity(enemy, 6, 6, color)

    def draw_entity(self, entity: Entity, pad_x: int, pad_y: int, color: str):
        x1 = entity.col * CELL_SIZE + pad_x
        y1 = HUD_HEIGHT + entity.row * CELL_SIZE + pad_y
        x2 = (entity.col + 1) * CELL_SIZE - pad_x
        y2 = HUD_HEIGHT + (entity.row + 1) * CELL_SIZE - pad_y
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="")

    def draw_overlay(self):
        width = self.level.width * CELL_SIZE
        height = self.level.height * CELL_SIZE + HUD_HEIGHT
        self.canvas.create_rectangle(0, 0, width, height, fill="black", stipple="gray50")
        title = "YOU WIN" if self.win else "GAME OVER"
        self.canvas.create_text(width / 2, height / 2 - 20, text=title, fill="white", font=("Consolas", 26, "bold"))
        self.canvas.create_text(
            width / 2,
            height / 2 + 18,
            text=f"Final Score: {self.player.score}   Best Score: {max(self.scoreboard.best_score, self.player.score)}",
            fill="white",
            font=("Consolas", 12),
        )
        self.canvas.create_text(width / 2, height / 2 + 48, text="Press Restart Game to play again.", fill="white", font=("Consolas", 12))


def main():
    root = tk.Tk()
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
