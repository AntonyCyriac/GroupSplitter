"""Timing helpers for the on-screen generation animation."""

from __future__ import annotations

ASSIGN_DISPLAY_SECONDS = 4.0
MIN_ASSIGN_STEP_MS = 25
MAX_ASSIGN_STEP_MS = 120
PDF_STEP_MS = 700
COUNTDOWN_FROM = 10
COUNTDOWN_STEP_MS = 1000


def assign_step_delay_ms(num_families: int) -> int:
    """Spread assignment updates over roughly ASSIGN_DISPLAY_SECONDS."""
    if num_families <= 0:
        return MIN_ASSIGN_STEP_MS
    ms = int(ASSIGN_DISPLAY_SECONDS * 1000 / num_families)
    return max(MIN_ASSIGN_STEP_MS, min(MAX_ASSIGN_STEP_MS, ms))
