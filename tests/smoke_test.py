"""CLI smoke test: 240 families -> 4 PDFs with balanced counts."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from app.pdf_writer import write_group_pdfs
from app.splitter import split_into_groups


def main() -> int:
    families = [f"Family_{i:03d}" for i in range(1, 241)]
    groups = split_into_groups(families, 4)
    sizes = [len(g) for g in groups]
    if sorted(sizes) != [60, 60, 60, 60]:
        print(f"FAIL: expected four groups of 60, got {sizes}")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        paths = write_group_pdfs(groups, out, overwrite=True)
        if len(paths) != 4:
            print(f"FAIL: expected 4 PDFs, got {len(paths)}")
            return 1
        for p in paths:
            if not p.is_file() or p.stat().st_size < 100:
                print(f"FAIL: bad PDF {p}")
                return 1

    print("OK: 240 families -> 4 PDFs, 60 names each")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
