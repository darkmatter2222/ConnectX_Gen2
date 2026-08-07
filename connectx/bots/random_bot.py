"""
Random Bot — uniform random move over legal columns.

The simplest possible baseline. Useful for confirming the environment
correctly identifies wins/losses and for G1/G2 sanity checks.
"""

from __future__ import annotations
import random

from typing import Sequence


def random_bot(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    cols: int,
) -> int:
    """
    Select a random legal column.

    Args:
        board: flat board array
        mark: this bot's mark (1 or 2)
        legal: list of legal column indices
        cols: number of columns

    Returns:
        column index (0-based)
    """
    return random.choice(list(legal))