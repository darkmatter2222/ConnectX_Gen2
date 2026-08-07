"""Alpha-beta 8×7/5 bot with v2 evaluation + opening book.

Uses the v2 opening book (if available) for instant early-game move selection,
falling back to the original 8x7/5 book (if available), then to full
iterative-deepening alpha-beta search.
"""

from __future__ import annotations

from typing import Optional, Sequence

from connectx.bots.opening_book_8x7_5_v2 import OpeningBook_8x7_5_v2
from connectx.bots.opening_book_8x7_5 import OpeningBook_8x7_5 as _OrigBook
from connectx.bots.bitboard_ab_8x7_5_v2 import (
    bitboard_ab_bot_8x7_5_v2 as _ab_v2,
    bitboard_ab_bot_fast_8x7_5_v2 as _ab_v2_fast,
    ROWS, COLS,
)

# Default book paths — v2 book first, original book as fallback
_V2_BOOK_PATH = "book_8x7_5_v2.json"
_ORIG_BOOK_PATH = "book_8x7_5.json"

# Global book instances (lazy-loaded)
_book_v2: Optional[OpeningBook_8x7_5_v2] = None
_book_orig: Optional[object] = None


def _get_book_v2() -> OpeningBook_8x7_5_v2:
    """Lazy-load the v2 opening book."""
    global _book_v2
    if _book_v2 is None:
        _book_v2 = OpeningBook_8x7_5_v2(_V2_BOOK_PATH)
    return _book_v2


def _get_book_orig() -> object:
    """Lazy-load the original opening book as fallback."""
    global _book_orig
    if _book_orig is None:
        try:
            _book_orig = _OrigBook(_ORIG_BOOK_PATH)
        except Exception:
            _book_orig = _OrigBook()  # empty book
    return _book_orig


def _book_move(board_list: list[int], mark: int,
               legal: Optional[list[int]]) -> Optional[int]:
    """Look up move in v2 book, then original book, then return None."""
    # Try v2 book first
    book_v2 = _get_book_v2()
    move = book_v2.best_move(board_list, mark, legal)
    if move is not None:
        return move

    # Fallback to original book
    book_orig = _get_book_orig()
    return book_orig.best_move(board_list, mark, legal)


def bitboard_ab_bot_8x7_5_v2_booked(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """8×7/5 AB v2 with opening book lookup."""
    board_list = list(board)

    # Quick book lookup for early-game positions
    book_move = _book_move(board_list, mark, legal)
    if book_move is not None:
        return book_move

    # Full v2 search for mid/end-game
    return _ab_v2(board, mark, legal, cols, move_deadline, remaining_overage, seed)


def bitboard_ab_bot_fast_8x7_5_v2_booked(
    board: Sequence[int],
    mark: int,
    legal: Optional[Sequence[int]] = None,
    cols: int = COLS,
    move_deadline: Optional[float] = None,
    remaining_overage: float = 0.0,
    seed: Optional[int] = None,
) -> int:
    """Fast 8×7/5 AB v2 with opening book lookup."""
    board_list = list(board)

    # Quick book lookup for early-game positions
    book_move = _book_move(board_list, mark, legal)
    if book_move is not None:
        return book_move

    # Full v2 search for mid/end-game
    return _ab_v2_fast(board, mark, legal, cols, move_deadline, remaining_overage, seed)