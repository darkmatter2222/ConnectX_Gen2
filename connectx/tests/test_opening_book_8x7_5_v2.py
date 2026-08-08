"""Tests for the 8×7/5 opening book v2 and v2 booked bot."""

from __future__ import annotations

import sys
sys.path.insert(0, '.')

import time
import connectx
from connectx.bots.bitboard_ab_8x7_5_v2_booked import (
    bitboard_ab_bot_8x7_5_v2_booked,
    bitboard_ab_bot_fast_8x7_5_v2_booked,
)
from connectx.bots.opening_book_8x7_5_v2 import (
    OpeningBook_8x7_5_v2,
    build_book,
    build_book as _build_book,
)


# ── v2 Book builder tests ─────────────────────────────────────────────────────

def test_opening_book_v2_import():
    from connectx.bots.opening_book_8x7_5_v2 import OpeningBook_8x7_5_v2, build_book
    assert callable(build_book)
    assert OpeningBook_8x7_5_v2 is not None


def test_opening_book_v2_build_small():
    """Build a small book and verify structure."""
    book = build_book(max_depth=4, branching=3, timeout_s=5.0)
    assert len(book) > 0
    for key, entry in book.items():
        assert isinstance(key, str)
        assert len(key) == 56
        for mark, col in entry.items():
            mark_val = int(mark) if isinstance(mark, str) else mark
            assert mark_val in (1, 2), f"Bad mark: {mark}"
            assert isinstance(col, int) and 0 <= col < 8, f"Bad col: {col}"


# ── v2 Booked bot tests ──────────────────────────────────────────────────────

def test_booked_v2_bot_import():
    assert callable(bitboard_ab_bot_8x7_5_v2_booked)
    assert callable(bitboard_ab_bot_fast_8x7_5_v2_booked)


def test_booked_v2_bot_from_package():
    from connectx.bots import (
        bitboard_ab_bot_8x7_5_v2_booked,
        bitboard_ab_bot_fast_8x7_5_v2_booked,
    )
    assert callable(bitboard_ab_bot_8x7_5_v2_booked)
    assert callable(bitboard_ab_bot_fast_8x7_5_v2_booked)


def test_booked_v2_bot_without_book():
    """When no book file exists, bot should fall back to AB search."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    m = bitboard_ab_bot_fast_8x7_5_v2_booked(board, 1, legal, 8)
    assert m in legal, f"Move {m} not in legal moves"


def test_booked_v2_bot_empty_board():
    """Booked bot should return center on empty board (book miss → AB)."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    m = bitboard_ab_bot_fast_8x7_5_v2_booked(board, 1, legal, 8)
    assert m in (3, 4), f"Empty board should pick center (3 or 4), got {m}"
    assert m in legal


def test_booked_v2_bot_legal_moves():
    """All moves from v2 booked bot should be legal."""
    board = connectx.make_board(7, 8)
    for turn in range(8):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5_v2_booked(board, mark, legal, 8)
        assert m in legal, f"Turn {turn}: move {m} not in legal {legal}"
        connectx.drop(board, m, mark, 7, 8)


def test_booked_v2_bot_timing_empty():
    """v2 booked bot should be fast on empty board."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    t0 = time.time()
    m = bitboard_ab_bot_fast_8x7_5_v2_booked(board, 1, legal, 8, move_deadline=1.5)
    elapsed = time.time() - t0
    assert elapsed < 1.5, f"Empty board move took {elapsed:.3f}s"
    assert m in legal


def test_booked_v2_bot_timing_with_pieces():
    """v2 booked bot should be fast after some pieces placed."""
    board = connectx.make_board(7, 8)
    # Place several pieces
    for col in [3, 2, 4, 3, 4, 2]:
        mark = 1 if col % 2 == 0 else 2
        connectx.drop(board, col, mark, 7, 8)
    legal = connectx.valid_moves(board, 8)
    if not legal:
        return
    t0 = time.time()
    m = bitboard_ab_bot_fast_8x7_5_v2_booked(board, 1, legal, 8, move_deadline=1.5)
    elapsed = time.time() - t0
    assert elapsed < 1.6, f"With pieces move took {elapsed:.3f}s"
    assert m in legal


def test_booked_v2_full_depth():
    """Full-depth v2 booked bot should work."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    m = bitboard_ab_bot_8x7_5_v2_booked(board, 1, legal, 8)
    assert m in legal


def test_booked_v2_seat_reversed():
    """Two v2 booked bots should play a valid game."""
    board = connectx.make_board(7, 8)
    for turn in range(10):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5_v2_booked(board, mark, legal, 8)
        assert m in legal
        connectx.drop(board, m, mark, 7, 8)
        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            break


def test_booked_v2_no_crash_invalid():
    """30 turns of play, no crashes."""
    board = connectx.make_board(7, 8)
    for turn in range(30):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5_v2_booked(board, mark, legal, 8)
        assert m in legal
        connectx.drop(board, m, mark, 7, 8)
        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            break


# ── Integration test ─────────────────────────────────────────────────────────

def test_booked_v2_game():
    """Two v2 booked bots play a valid game to a conclusion."""
    board = connectx.make_board(7, 8)
    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5_v2_booked(board, mark, legal, 8)
        assert m in legal, f"Turn {turn}: invalid move {m}"
        connectx.drop(board, m, mark, 7, 8)
        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            break