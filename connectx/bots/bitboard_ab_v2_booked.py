"""v2 with opening book lookup.

If the current position is in the opening book, return the book move immediately.
Otherwise, fall back to full v2 search.

Usage:
    # As a drop-in replacement for v2:
    from connectx.bots.bitboard_ab_v2_booked import bitboard_ab_bot_fast_v2_booked
    move = bitboard_ab_bot_fast_v2_booked(board, mark, legal, move_deadline)

    # With a custom book path:
    move = bitboard_ab_bot_fast_v2_booked(board, mark, legal, move_deadline, "my_book.json")
"""

from __future__ import annotations

import time
from typing import Optional, Sequence

_DEFAULT_BOOK = "connectx/bots/book.json"


def bitboard_ab_bot_fast_v2_booked(
    board: Sequence[int],
    mark: int,
    legal: Sequence[int],
    move_deadline: Optional[float] = None,
    book_path: str = _DEFAULT_BOOK,
) -> int:
    """v2 with opening book lookup.

    If the current position is in the opening book, return the book move immediately.
    Otherwise, fall back to full v2 search.

    Args:
        board: Current board state (flat list, row-major).
        mark: Player mark (1 or 2).
        legal: List of legal column indices.
        move_deadline: Time deadline for the move.
        book_path: Path to the opening book JSON file.

    Returns:
        Best column index.
    """
    board_list = list(board)
    legal_list = list(legal)
    if not legal_list:
        return 0

    # ── Step 1: Opening book lookup ──────────────────────────────────────
    from connectx.bots.opening_book import OpeningBook

    book = OpeningBook(book_path)
    board_str = "".join(str(c) for c in board_list)
    best = book.best_move(board_str, mark)

    if best is not None and best in legal_list:
        return best

    # ── Step 2: Fall back to full v2 search ─────────────────────────────
    from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_fast_v2

    return bitboard_ab_bot_fast_v2(
        board_list, mark, legal_list, move_deadline=move_deadline
    )