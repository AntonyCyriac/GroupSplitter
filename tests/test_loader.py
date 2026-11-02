"""Tests for family list file loading."""

import csv
import tempfile
import unittest
from pathlib import Path

from app.family_loader import SUPPORTED_EXTENSIONS, load_families


class TestLoader(unittest.TestCase):
    def test_csv_with_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "f.csv"
            p.write_text("Family Name\nA\nB\n", encoding="utf-8")
            self.assertEqual(load_families(p), ["A", "B"])

    def test_tsv(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "f.tsv"
            with p.open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, delimiter="\t")
                w.writerow(["Name"])
                w.writerow(["One"])
                w.writerow(["Two"])
            self.assertEqual(load_families(p), ["One", "Two"])

    def test_txt_one_per_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "f.txt"
            p.write_text("Alpha\nBeta\n", encoding="utf-8")
            self.assertEqual(load_families(p), ["Alpha", "Beta"])

    def test_unsupported_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "f.doc"
            p.write_text("x", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_families(p)

    def test_supported_extensions_non_empty(self):
        self.assertIn(".xlsx", SUPPORTED_EXTENSIONS)


if __name__ == "__main__":
    unittest.main()
