"""
Alpha-beta with opening book: faster moves in early game.

Uses pre-computed optimal moves for the first few moves of the game.
After the opening book is exhausted, falls back to full v2 search.

Timing benefit: 0ms for moves covered by the opening book,
compared to ~20ms for full v2 search.
"""

from __future__ import annotations

import time
from typing import Optional, Sequence

from connectx.engine import (
    valid_moves,
    ROWS, COLS, INAROW,
)
from connectx.bots.opening_book import OpeningBook


# Shared opening book instance
_opening_book = OpeningBook()


def bitboard_ab_bot_v2_book(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Alpha-beta with opening book for early-game speedup."""
    board_list = list(board)
    legal = valid_moves(board_list, cols)
    if not legal:
        return 0

    # Try opening book first
    board_str = "".join(str(c) for c in board_list)
    book_move = _opening_book.best_move(board_str, mark)
    if book_move is not None and book_move in legal:
        return book_move

    # Fall back to full v2 search (same as bitboard_ab_bot_v2)
    # Import lazily to avoid circular dependency
    from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2 as _v2_bot
    return _v2_bot(
        board_list, mark, legal, cols,
        move_deadline=move_deadline,
        remaining_overage=remaining_overage,
        seed=seed,
    )