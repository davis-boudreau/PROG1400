"""Load level files into a grid structure."""

from __future__ import annotations

from pathlib import Path


def load_level_file(path: str | Path) -> list[list[str]]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        rows = [list(line.rstrip("\n")) for line in handle if line.strip("\n")]

    if not rows:
        raise ValueError(f"Level file is empty: {path}")

    row_length = len(rows[0])
    if any(len(row) != row_length for row in rows):
        raise ValueError(f"Level rows must all be the same width: {path}")

    return rows
