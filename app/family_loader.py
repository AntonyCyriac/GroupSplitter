"""Load family names from CSV, TSV, TXT, or Excel (.xlsx)."""

from __future__ import annotations

import csv
import re
from pathlib import Path

SUPPORTED_EXTENSIONS = frozenset({".csv", ".tsv", ".txt", ".xlsx", ".xlsm"})

_HEADER_HINTS = re.compile(r"family|name|surname|last\s*name", re.IGNORECASE)


def _looks_like_header(first_cell: str) -> bool:
    cell = first_cell.strip()
    if not cell:
        return False
    if _HEADER_HINTS.search(cell):
        return True
    if cell.lower() in ("family name", "family", "name", "surname"):
        return True
    return False


def _families_from_rows(rows: list[list[str]]) -> list[str]:
    if not rows:
        raise ValueError("File is empty.")

    start = 0
    if rows[0] and _looks_like_header(rows[0][0]):
        start = 1

    families: list[str] = []
    for row in rows[start:]:
        if not row:
            continue
        name = row[0].strip()
        if name:
            families.append(name)

    if not families:
        raise ValueError("No family names found (use the first column or one name per line).")

    return families


def _read_csv_rows(path: Path, delimiter: str) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.reader(f, delimiter=delimiter))


def _read_txt_rows(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    with path.open(encoding="utf-8-sig") as f:
        for line in f:
            name = line.strip()
            if name:
                rows.append([name])
    return rows


def _read_xlsx_rows(path: Path) -> list[list[str]]:
    try:
        from openpyxl import load_workbook
    except ImportError as e:
        raise ImportError("Excel support requires openpyxl. Reinstall from requirements.txt.") from e

    rows: list[list[str]] = []
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        sheet = wb.active
        if sheet is None:
            raise ValueError("Excel workbook has no sheets.")
        for row in sheet.iter_rows(values_only=True):
            if not row:
                rows.append([])
                continue
            first = row[0]
            if first is None:
                rows.append([""])
            else:
                rows.append([str(first).strip()])
    finally:
        wb.close()
    return rows


def load_families(path: Path | str) -> list[str]:
    """Read family names from a supported file (first column or one name per line for .txt)."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"Unsupported file type '{ext}'. Supported: {supported}")

    if ext == ".csv":
        rows = _read_csv_rows(path, ",")
    elif ext == ".tsv":
        rows = _read_csv_rows(path, "\t")
    elif ext == ".txt":
        rows = _read_txt_rows(path)
    else:
        rows = _read_xlsx_rows(path)

    return _families_from_rows(rows)
