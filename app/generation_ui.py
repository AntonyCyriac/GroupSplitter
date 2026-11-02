"""Progress window shown while groups are assigned and PDFs are written."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from app.generation_timing import COUNTDOWN_FROM


class GenerationProgressWindow:
    def __init__(self, parent: tk.Misc, *, total_families: int, num_groups: int) -> None:
        self.win = tk.Toplevel(parent)
        self.win.title("Creating groups…")
        self.win.transient(parent)
        self.win.grab_set()
        self.win.resizable(False, False)

        frame = ttk.Frame(self.win, padding=20)
        frame.pack()

        ttk.Label(frame, text="Random group assignment", font=("Segoe UI", 11, "bold")).pack(
            anchor=tk.W
        )

        self.counter_var = tk.StringVar(value=str(COUNTDOWN_FROM))
        ttk.Label(frame, textvariable=self.counter_var, font=("Segoe UI", 28)).pack(pady=(8, 4))

        self.status_var = tk.StringVar(value="Shuffling families…")
        ttk.Label(frame, textvariable=self.status_var, wraplength=420).pack(anchor=tk.W, pady=(0, 12))

        self._progress = ttk.Progressbar(frame, length=400, mode="determinate", maximum=total_families)
        self._progress.pack(fill=tk.X)

        self._total_families = total_families
        self._num_groups = num_groups
        self._begin_countdown()

    def _begin_countdown(self) -> None:
        self.win.title("Get ready…")
        self._progress.configure(maximum=COUNTDOWN_FROM, value=0)
        self.status_var.set("Random assignment starts when the counter reaches 0")

    def set_countdown(self, value: int) -> None:
        self.counter_var.set(str(value))
        self._progress["value"] = COUNTDOWN_FROM - value
        if value > 0:
            self.status_var.set("Random assignment starts when the counter reaches 0")
        else:
            self.status_var.set("Go!")

    def begin_assign_phase(self) -> None:
        self.win.title("Creating groups…")
        self.counter_var.set(f"0 / {self._total_families}")
        self._progress.configure(maximum=self._total_families, value=0)
        self.status_var.set("Assigning families to groups…")

    def set_assign_progress(self, index: int, family_name: str, group_number: int) -> None:
        self.counter_var.set(f"{index} / {self._total_families}")
        self._progress["value"] = index
        self.status_var.set(f"{family_name}  →  Group {group_number}")

    def start_pdf_phase(self) -> None:
        self.win.title("Writing PDFs…")
        self.counter_var.set(f"0 / {self._num_groups}")
        self._progress.configure(maximum=self._num_groups, value=0)
        self.status_var.set("Preparing PDF files…")

    def set_pdf_progress(self, group_index: int) -> None:
        self.counter_var.set(f"{group_index} / {self._num_groups}")
        self._progress["value"] = group_index
        self.status_var.set(f"Writing Group {group_index} of {self._num_groups}…")

    def close(self) -> None:
        self.win.grab_release()
        self.win.destroy()
