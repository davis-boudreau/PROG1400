"""Main game controller and tkinter UI."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path

import config
from loader import load_level_file
from models import Level
from scoreboard import ScoreBoard
from util import Direction, Position


class Game:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.configure(bg=config.BG_COLOR)

        self.level_index = 0
        self.tick_count = 0
        self.status_message = "Collect all items to clear the level."
        self.scoreboard = ScoreBoard(config.SCOREBOARD_FILE)
        self.level = self._load_level(config.LEVEL_FILES[self.level_index])

        canvas_width = self.level.width * config.TILE_SIZE
        canvas_height = self.level.height * config.TILE_SIZE + config.HUD_HEIGHT
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_width,
            height=canvas_height,
            bg=config.BG_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.root.bind("<Up>", lambda _: self.handle_player_move(Direction.UP))
        self.root.bind("<Down>", lambda _: self.handle_player_move(Direction.DOWN))
        self.root.bind("<Left>", lambda _: self.handle_player_move(Direction.LEFT))
        self.root.bind("<Right>", lambda _: self.handle_player_move(Direction.RIGHT))
        self.root.bind("r", lambda _: self.restart_game())

        self.draw()
        self.schedule_tick()

    def _load_level(self, path: str | Path) -> Level:
        return Level(load_level_file(path))

    def restart_game(self) -> None:
        self.level_index = 0
        self.level = self._load_level(config.LEVEL_FILES[self.level_index])
        self.status_message = "Game restarted."
        self.draw()

    def handle_player_move(self, direction: Direction) -> None:
        if self.level.player.lives <= 0:
            return

        dr, dc = direction.delta
        result = self.level.try_move_player(dr, dc)
        self.level.player.score += result.points_gained

        if result.level_completed:
            self.advance_level()
            return

        collision_result = self.level.handle_collisions()
        self.level.player.score += collision_result.points_gained
        if collision_result.enemy_defeated:
            self.status_message = "Enemy defeated while powered up!"
        elif self.level.player.lives <= 0:
            self.status_message = "Game over. Press R to restart."
            self.scoreboard.finish_game(self.level.player.score)
        elif result.item_collected:
            self.status_message = "Item collected."

        self.draw()

    def advance_level(self) -> None:
        self.level_index += 1
        if self.level_index >= len(config.LEVEL_FILES):
            final_score = self.level.player.score
            self.scoreboard.finish_game(final_score)
            self.status_message = f"You cleared all levels! Final score: {final_score}. Press R to restart."
            self.level_index = len(config.LEVEL_FILES) - 1
            self.draw()
            return

        carry_score = self.level.player.score
        carry_lives = self.level.player.lives
        self.level = self._load_level(config.LEVEL_FILES[self.level_index])
        self.level.player.score = carry_score
        self.level.player.lives = carry_lives
        self.status_message = f"Level {self.level_index + 1} loaded."
        self.draw()

    def schedule_tick(self) -> None:
        self.root.after(int(1000 / config.FPS), self.tick)

    def tick(self) -> None:
        if self.level.player.lives > 0:
            self.tick_count += 1
            self.level.player.tick()
            if self.tick_count % config.ENEMY_MOVE_DELAY == 0:
                self.level.move_enemies()
                collision_result = self.level.handle_collisions()
                self.level.player.score += collision_result.points_gained
                if collision_result.enemy_defeated:
                    self.status_message = "Enemy defeated while powered up!"
                elif self.level.player.lives <= 0:
                    self.status_message = "Game over. Press R to restart."
                    self.scoreboard.finish_game(self.level.player.score)
        self.draw()
        self.schedule_tick()

    def draw(self) -> None:
        self.canvas.delete("all")
        self._draw_board()
        self._draw_entities()
        self._draw_hud()

    def _draw_board(self) -> None:
        for row in range(self.level.height):
            for col in range(self.level.width):
                x1 = col * config.TILE_SIZE
                y1 = row * config.TILE_SIZE
                x2 = x1 + config.TILE_SIZE
                y2 = y1 + config.TILE_SIZE
                tile = self.level.tiles[row][col]
                fill = config.FLOOR_COLOR if tile != config.WALL else config.WALL_COLOR
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#202020")
                if tile == config.DOT:
                    self.canvas.create_oval(x1 + 12, y1 + 12, x2 - 12, y2 - 12, fill=config.DOT_COLOR, outline="")
                elif tile == config.POWER:
                    self.canvas.create_oval(x1 + 8, y1 + 8, x2 - 8, y2 - 8, fill=config.POWER_COLOR, outline="")

    def _draw_entities(self) -> None:
        self._draw_circle(self.level.player.position, config.PLAYER_COLOR)
        for enemy in self.level.enemies:
            color = config.FRIGHTENED_ENEMY_COLOR if self.level.player.is_powered else config.ENEMY_COLOR
            self._draw_circle(enemy.position, color)

    def _draw_circle(self, pos: Position, color: str) -> None:
        x1 = pos.col * config.TILE_SIZE + 4
        y1 = pos.row * config.TILE_SIZE + 4
        x2 = x1 + config.TILE_SIZE - 8
        y2 = y1 + config.TILE_SIZE - 8
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="")

    def _draw_hud(self) -> None:
        y = self.level.height * config.TILE_SIZE
        self.canvas.create_rectangle(
            0,
            y,
            self.level.width * config.TILE_SIZE,
            y + config.HUD_HEIGHT,
            fill=config.HUD_BG_COLOR,
            outline="",
        )
        player = self.level.player
        hud_lines = [
            f"Score: {player.score}",
            f"Best: {self.scoreboard.best_score}",
            f"Lives: {player.lives}",
            f"Level: {self.level_index + 1}/{len(config.LEVEL_FILES)}",
            f"Items Left: {self.level.remaining_items}",
            f"Powered: {'Yes' if player.is_powered else 'No'}",
        ]
        self.canvas.create_text(12, y + 10, anchor="nw", fill=config.TEXT_COLOR, text="   ".join(hud_lines), font=("Arial", 12, "bold"))
        self.canvas.create_text(12, y + 44, anchor="nw", fill=config.TEXT_COLOR, text=self.status_message, font=("Arial", 11))
        self.canvas.create_text(
            12,
            y + 68,
            anchor="nw",
            fill=config.TEXT_COLOR,
            text="Controls: Arrow keys = move, R = restart",
            font=("Arial", 10),
        )

    def run(self) -> None:
        self.root.mainloop()
