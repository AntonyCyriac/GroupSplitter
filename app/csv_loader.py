"""Backward-compatible CSV loader; use family_loader.load_families for all formats."""

from __future__ import annotations

from pathlib import Path

from app.family_loader import load_families


def load_families_from_csv(path: Path | str) -> list[str]:
    return load_families(path)
