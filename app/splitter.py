"""Random balanced split of families into M groups."""

from __future__ import annotations

import random
from copy import deepcopy


def shuffle_families(
    families: list[str], rng: random.Random | None = None
) -> list[str]:
    if rng is None:
        rng = random.Random()
    shuffled = deepcopy(families)
    rng.shuffle(shuffled)
    return shuffled


def groups_from_shuffled(shuffled: list[str], num_groups: int) -> list[list[str]]:
    groups: list[list[str]] = [[] for _ in range(num_groups)]
    for i, name in enumerate(shuffled):
        groups[i % num_groups].append(name)
    return groups


def split_into_groups(families: list[str], num_groups: int, rng: random.Random | None = None) -> list[list[str]]:
    """
    Shuffle families randomly, then assign round-robin into num_groups.
    Group sizes differ by at most one.
    """
    if num_groups < 1:
        raise ValueError("Number of groups must be at least 1.")
    if not families:
        raise ValueError("No families to split.")

    if rng is None:
        rng = random.Random()

    shuffled = shuffle_families(families, rng)
    return groups_from_shuffled(shuffled, num_groups)


def validate_split_params(num_families: int, num_groups: int) -> None:
    if num_groups < 1:
        raise ValueError("Number of groups must be at least 1.")
    if num_families < 1:
        raise ValueError("Load a CSV with at least one family name.")
    if num_groups > num_families:
        raise ValueError(
            f"Number of groups ({num_groups}) cannot exceed number of families ({num_families})."
        )
