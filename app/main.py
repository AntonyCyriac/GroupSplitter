"""GroupSplitter — Tkinter GUI."""

from __future__ import annotations

import random
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

# Allow running as script: python app/main.py
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app.generation_timing import COUNTDOWN_FROM, COUNTDOWN_STEP_MS, PDF_STEP_MS, assign_step_delay_ms
from app.generation_ui import GenerationProgressWindow
from app.family_loader import load_families
from app.pdf_writer import group_pdf_path, write_one_group_pdf
from app.splitter import groups_from_shuffled, shuffle_families, validate_split_params


class GroupSplitterApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("GroupSplitter")
        self.minsize(480, 280)
        self.resizable(True, True)

        self._input_path: Path | None = None
        self._families: list[str] = []
        self._output_dir: Path | None = None
        self._gen: dict | None = None
        self._progress: GenerationProgressWindow | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        pad = {"padx": 10, "pady": 6}
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Family list file").grid(row=0, column=0, sticky=tk.W, **pad)
        self.file_label = ttk.Label(frame, text="(none selected)", wraplength=360)
        self.file_label.grid(row=0, column=1, sticky=tk.W, **pad)
        ttk.Button(frame, text="Browse…", command=self._browse_input).grid(row=0, column=2, **pad)

        ttk.Label(frame, text="Number of groups (M)").grid(row=1, column=0, sticky=tk.W, **pad)
        self.m_var = tk.StringVar(value="4")
        ttk.Entry(frame, textvariable=self.m_var, width=8).grid(row=1, column=1, sticky=tk.W, **pad)

        self.count_label = ttk.Label(frame, text="Families loaded: 0")
        self.count_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, **pad)
        ttk.Button(frame, text="Reload file", command=self._reload_input).grid(row=2, column=2, **pad)

        ttk.Label(frame, text="Output folder").grid(row=3, column=0, sticky=tk.W, **pad)
        self.out_label = ttk.Label(frame, text="(none selected)", wraplength=360)
        self.out_label.grid(row=3, column=1, sticky=tk.W, **pad)
        ttk.Button(frame, text="Browse…", command=self._browse_output).grid(row=3, column=2, **pad)

        self.overwrite_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame,
            text="Overwrite existing PDFs in output folder",
            variable=self.overwrite_var,
        ).grid(row=4, column=0, columnspan=3, sticky=tk.W, **pad)

        self.generate_btn = ttk.Button(frame, text="Generate PDFs", command=self._generate)
        self.generate_btn.grid(row=5, column=0, columnspan=3, pady=16)

        frame.columnconfigure(1, weight=1)

    def _set_busy(self, busy: bool) -> None:
        state = tk.DISABLED if busy else tk.NORMAL
        self.generate_btn.configure(state=state)

    def _browse_input(self) -> None:
        path = filedialog.askopenfilename(
            title="Select family list",
            filetypes=[
                (
                    "Supported files",
                    "*.csv;*.tsv;*.txt;*.xlsx;*.xlsm",
                ),
                ("CSV", "*.csv"),
                ("Excel", "*.xlsx;*.xlsm"),
                ("Text", "*.txt"),
                ("TSV", "*.tsv"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return
        self._input_path = Path(path)
        self._load_input()

    def _reload_input(self) -> None:
        if self._input_path is None:
            messagebox.showinfo("Reload file", "Select a family list file first.")
            return
        self._load_input()

    def _load_input(self) -> None:
        assert self._input_path is not None
        try:
            self._families = load_families(self._input_path)
        except (OSError, ValueError, ImportError) as e:
            self._families = []
            self.count_label.config(text="Families loaded: 0")
            messagebox.showerror("File error", str(e))
            return

        self.file_label.config(text=str(self._input_path))
        self.count_label.config(text=f"Families loaded: {len(self._families)}")

    def _browse_output(self) -> None:
        path = filedialog.askdirectory(title="Select output folder for PDFs")
        if not path:
            return
        self._output_dir = Path(path)
        self.out_label.config(text=str(self._output_dir))

    def _parse_m(self) -> int:
        raw = self.m_var.get().strip()
        if not raw.isdigit():
            raise ValueError("Number of groups must be a whole number.")
        return int(raw)

    def _preflight_output(self, m: int) -> None:
        assert self._output_dir is not None
        self._output_dir.mkdir(parents=True, exist_ok=True)
        if self.overwrite_var.get():
            return
        for g in range(1, m + 1):
            path = group_pdf_path(g, m, self._output_dir)
            if path.exists():
                raise FileExistsError(
                    f"File already exists: {path.name}. Choose another folder or allow overwrite."
                )

    def _generate(self) -> None:
        if self._input_path is None or not self._families:
            messagebox.showwarning(
                "Generate PDFs", "Load a family list file with at least one name."
            )
            return
        if self._output_dir is None:
            messagebox.showwarning("Generate PDFs", "Choose an output folder.")
            return

        try:
            m = self._parse_m()
            validate_split_params(len(self._families), m)
            self._preflight_output(m)
        except ValueError as e:
            messagebox.showerror("Invalid settings", str(e))
            return
        except FileExistsError as e:
            messagebox.showerror("Files exist", str(e))
            return

        shuffled = shuffle_families(self._families, random.Random())
        groups = groups_from_shuffled(shuffled, m)
        n = len(shuffled)

        self._set_busy(True)
        self._progress = GenerationProgressWindow(self, total_families=n, num_groups=m)
        self._gen = {
            "m": m,
            "shuffled": shuffled,
            "groups": groups,
            "assign_i": 0,
            "pdf_i": 0,
            "paths": [],
            "assign_delay": assign_step_delay_ms(n),
            "phase": "countdown",
            "countdown": COUNTDOWN_FROM,
        }
        self._progress.set_countdown(COUNTDOWN_FROM)
        self.after(COUNTDOWN_STEP_MS, self._gen_countdown_step)

    def _gen_countdown_step(self) -> None:
        if not self._gen or not self._progress:
            return

        state = self._gen
        n = state["countdown"]
        if n > 0:
            state["countdown"] = n - 1
            self._progress.set_countdown(n - 1)
            self.after(COUNTDOWN_STEP_MS, self._gen_countdown_step)
            return

        self._progress.begin_assign_phase()
        state["phase"] = "assign"
        self.after(COUNTDOWN_STEP_MS, self._gen_assign_step)

    def _gen_assign_step(self) -> None:
        if not self._gen or not self._progress:
            return

        state = self._gen
        i = state["assign_i"]
        shuffled = state["shuffled"]
        m = state["m"]
        n = len(shuffled)

        if i < n:
            name = shuffled[i]
            group_num = (i % m) + 1
            self._progress.set_assign_progress(i + 1, name, group_num)
            state["assign_i"] = i + 1
            self.after(state["assign_delay"], self._gen_assign_step)
            return

        self._progress.start_pdf_phase()
        state["phase"] = "pdf"
        self.after(PDF_STEP_MS, self._gen_pdf_step)

    def _gen_pdf_step(self) -> None:
        if not self._gen or not self._progress:
            return

        state = self._gen
        k = state["pdf_i"]
        m = state["m"]
        groups = state["groups"]
        assert self._output_dir is not None

        if k < m:
            group_index = k + 1
            self._progress.set_pdf_progress(group_index)
            try:
                path = write_one_group_pdf(
                    group_index, groups[k], m, self._output_dir
                )
            except OSError as e:
                self._gen_finish(error=str(e))
                return
            state["paths"].append(path)
            state["pdf_i"] = k + 1
            self.after(PDF_STEP_MS, self._gen_pdf_step)
            return

        self._gen_finish()

    def _gen_finish(self, *, error: str | None = None) -> None:
        paths: list[Path] = []
        if self._gen:
            paths = self._gen.get("paths", [])
        if self._progress:
            self._progress.close()
            self._progress = None
        self._gen = None
        self._set_busy(False)

        if error:
            messagebox.showerror("Write error", error)
            return

        messagebox.showinfo(
            "Done",
            f"Created {len(paths)} PDF(s) in:\n{self._output_dir}",
        )


def main() -> None:
    app = GroupSplitterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
