"""Unit tests for group splitting."""

import random
import unittest

from app.splitter import split_into_groups, validate_split_params


class TestSplitter(unittest.TestCase):
    def test_balanced_240_4(self):
        families = [f"Family_{i}" for i in range(240)]
        rng = random.Random(42)
        groups = split_into_groups(families, 4, rng=rng)
        self.assertEqual(len(groups), 4)
        sizes = [len(g) for g in groups]
        self.assertEqual(sorted(sizes), [60, 60, 60, 60])
        flat = [n for g in groups for n in g]
        self.assertEqual(sorted(flat), sorted(families))

    def test_balanced_241_4(self):
        families = [f"Family_{i}" for i in range(241)]
        groups = split_into_groups(families, 4, rng=random.Random(0))
        sizes = sorted(len(g) for g in groups)
        self.assertEqual(sizes, [60, 60, 60, 61])

    def test_single_group(self):
        families = ["A", "B", "C"]
        groups = split_into_groups(families, 1, rng=random.Random(1))
        self.assertEqual(len(groups), 1)
        self.assertEqual(sorted(groups[0]), sorted(families))

    def test_validate_rejects_m_gt_n(self):
        with self.assertRaises(ValueError):
            validate_split_params(3, 5)

    def test_validate_rejects_zero_groups(self):
        with self.assertRaises(ValueError):
            validate_split_params(10, 0)

    def test_split_rejects_zero_groups(self):
        with self.assertRaises(ValueError):
            split_into_groups(["a"], 0)


if __name__ == "__main__":
    unittest.main()
