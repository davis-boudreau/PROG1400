"""Persistent scoreboard support."""

from __future__ import annotations

import json
from pathlib import Path


class ScoreBoard:
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self.best_score = 0
        self.games_played = 0
        self.load()

    def load(self) -> None:
        if not self.file_path.exists():
            return
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
            self.best_score = int(data.get("best_score", 0))
            self.games_played = int(data.get("games_played", 0))
        except (OSError, ValueError, json.JSONDecodeError):
            self.best_score = 0
            self.games_played = 0

    def save(self) -> None:
        data = {
            "best_score": self.best_score,
            "games_played": self.games_played,
        }
        self.file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def finish_game(self, score: int) -> None:
        self.games_played += 1
        self.best_score = max(self.best_score, score)
        self.save()
