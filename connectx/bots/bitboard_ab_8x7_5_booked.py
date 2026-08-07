"""Bitboard AB 8×7/5 with opening book.

Combines the 8×7/5 alpha-beta bot with the pre-computed opening book
for instant early-game moves. Falls back to full search for mid-game
positions not in the book.

Usage:
    from connectx.bots.bitboard_ab_8x7_5_booked import (
        bitboard_ab_bot_8x7_5_booked,
        bitboard_ab_bot_fast_8x7_5_booked,
    )

    move = bitboard_ab_bot_fast_8x7_5_booked(board, mark, legal, 8)
"""

from __future__ import annotations

import time
from typing import List, Optional, Sequence

from connectx.bots.bitboard_ab_8x7_5 import (
    bitboard_ab_bot_8x7_5 as _ab_full,
    bitboard_ab_bot_fast_8x7_5 as _ab_fast,
)
from connectx.bots.opening_book_8x7_5 import OpeningBook_8x7_5

_ROWS = 7
_COLS = 8
_INAROW = 5
_BOOK_PATH = "book_8x7_5.json"

# Lazy-load the book
_book_instance = None


def _get_book() -> OpeningBook_8x7_5:
    global _book_instance
    if _book_instance is None:
        try:
            _book_instance = OpeningBook_8x7_5(_BOOK_PATH)
        except Exception:
            _book_instance = OpeningBook_8x7_5()
    return _book_instance


def _book_move(board: List[int], mark: int, legal: List[int]) -> Optional[int]:
    """Get a move from the opening book. Returns None if no match."""
    book = _get_book()
    return book.best_move(board, mark, legal)


def bitboard_ab_bot_8x7_5_booked(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = _COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Full-depth 8×7/5 AB with opening book fallback.

    Uses the opening book for instant early-game moves, then falls back
    to full iterative-deepening AB search for mid-game positions.
    """
    board_list = list(board)
    legal_list = list(legal) if legal else []
    if not legal_list:
        legal_list = list(
            i for i in range(cols) if board_list[i * _ROWS + _ROWS - 1] == 0
        )
    if not legal_list:
        return 0

    # Check opening book first (covers early-game positions)
    book_move = _book_move(board_list, mark, legal_list)
    if book_move is not None:
        return book_move

    # Handle empty board — always pick center
    pieces = sum(1 for x in board_list if x != 0)
    if pieces == 0:
        return cols // 2  # Col 3 (center)

    # Fall back to full AB search
    time_limit = move_deadline if move_deadline is not None else 2.0
    return _ab_full(board_list, mark, legal_list, cols, move_deadline=time_limit)


def bitboard_ab_bot_fast_8x7_5_booked(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = _COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast 8×7/5 AB with opening book fallback.

    Uses the opening book for instant early-game moves, then falls back
    to fast AB search for mid-game positions.
    """
    board_list = list(board)
    legal_list = list(legal) if legal else []
    if not legal_list:
        legal_list = list(
            i for i in range(cols) if board_list[i * _ROWS + _ROWS - 1] == 0
        )
    if not legal_list:
        return 0

    # Check opening book first (covers early-game positions)
    book_move = _book_move(board_list, mark, legal_list)
    if book_move is not None:
        return book_move

    # Handle empty board — always pick center
    pieces = sum(1 for x in board_list if x != 0)
    if pieces == 0:
        return cols // 2  # Col 3 (center)

    # Fall back to fast AB search
    time_limit = move_deadline if move_deadline is not None else 2.0
    return _ab_fast(board_list, mark, legal_list, cols, move_deadline=time_limit)