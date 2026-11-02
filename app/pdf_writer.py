"""Write one PDF per group."""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF


def _group_filename(group_index: int, num_groups: int) -> str:
    width = max(1, len(str(num_groups)))
    return f"Group_{group_index:0{width}d}.pdf"


def group_pdf_path(group_index: int, num_groups: int, output_dir: Path | str) -> Path:
    return Path(output_dir) / _group_filename(group_index, num_groups)


def write_one_group_pdf(
    group_index: int,
    names: list[str],
    num_groups: int,
    output_dir: Path | str,
) -> Path:
    """Write a single group PDF. Caller must ensure output_dir exists and overwrite policy."""
    output_dir = Path(output_dir)
    out_path = group_pdf_path(group_index, num_groups, output_dir)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=16, style="B")
    pdf.cell(0, 12, f"Group {group_index} of {num_groups}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", size=12)

    for i, name in enumerate(names, start=1):
        pdf.cell(0, 8, f"{i}. {name}", new_x="LMARGIN", new_y="NEXT")

    pdf.output(str(out_path))
    return out_path


def write_group_pdfs(
    groups: list[list[str]],
    output_dir: Path | str,
    *,
    overwrite: bool = False,
) -> list[Path]:
    """Create Group_1.pdf … Group_M.pdf in output_dir. Returns paths written."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    num_groups = len(groups)
    written: list[Path] = []

    for g, names in enumerate(groups, start=1):
        out_path = group_pdf_path(g, num_groups, output_dir)
        if out_path.exists() and not overwrite:
            raise FileExistsError(
                f"File already exists: {out_path.name}. Choose another folder or allow overwrite."
            )
        written.append(write_one_group_pdf(g, names, num_groups, output_dir))

    return written
