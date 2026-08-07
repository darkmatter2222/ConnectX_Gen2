"""Tests for the 8×7/5 opening book and booked bot."""

from __future__ import annotations

import sys
sys.path.insert(0, '.')

import time
import connectx
from connectx.bots.bitboard_ab_8x7_5_booked import (
    bitboard_ab_bot_8x7_5_booked,
    bitboard_ab_bot_fast_8x7_5_booked,
    _get_book,
)
from connectx.bots.opening_book_8x7_5 import OpeningBook_8x7_5, build_book


# ── Opening book tests ───────────────────────────────────────────────────────

def test_opening_book_import():
    from connectx.bots.opening_book_8x7_5 import OpeningBook_8x7_5, build_book
    assert callable(build_book)
    assert OpeningBook_8x7_5 is not None


def test_opening_book_load():
    book = OpeningBook_8x7_5("book_8x7_5.json")
    assert book._loaded
    assert len(book._entries) > 0


def test_opening_book_in_book():
    book = OpeningBook_8x7_5("book_8x7_5.json")
    # Book contains positions with pieces (not empty board)
    assert len(book._entries) > 0
    # Pick a known entry and verify it's valid
    sample_key = next(iter(book._entries))
    sample = book._entries[sample_key]
    assert isinstance(sample, dict)
    for mark, col in sample.items():
        # JSON parses numeric keys as strings
        mark_val = int(mark) if isinstance(mark, str) else mark
        assert mark_val in (1, 2), f"Bad mark: {mark}"
        assert isinstance(col, int), f"Bad col: {col}"


def test_opening_book_best_move_from_book():
    book = OpeningBook_8x7_5("book_8x7_5.json")
    # Use a known book position: first one in the dict
    sample_key = next(iter(book._entries))
    sample = book._entries[sample_key]
    # The board key encodes row heights. Reconstruct the board from key.
    # Book stores the board state as a string of digits.
    board = [int(c) for c in sample_key]
    assert len(board) == 56
    mark = 1
    legal = connectx.valid_moves(board, 8)
    move = book.best_move(board, mark, legal)
    # Book should have a recommended move for mark 1
    move_from_book = sample.get("1") or sample.get(1)
    if move_from_book is not None:
        assert move is not None
        assert move == move_from_book
        assert move in legal


# ── Booked bot tests ─────────────────────────────────────────────────────────

def test_booked_bot_import():
    assert callable(bitboard_ab_bot_8x7_5_booked)
    assert callable(bitboard_ab_bot_fast_8x7_5_booked)


def test_booked_bot_from_package():
    from connectx.bots import bitboard_ab_bot_8x7_5_booked, bitboard_ab_bot_fast_8x7_5_booked
    assert callable(bitboard_ab_bot_8x7_5_booked)
    assert callable(bitboard_ab_bot_fast_8x7_5_booked)


def test_booked_bot_empty_board():
    """Booked bot should return book move on empty board."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    m = bitboard_ab_bot_fast_8x7_5_booked(board, 1, legal, 8)
    assert m in (3, 4), f"Empty board should use book move (3 or 4), got {m}"
    assert m in legal


def test_booked_bot_legal_moves():
    """All moves from booked bot should be legal."""
    board = connectx.make_board(7, 8)
    for turn in range(8):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5_booked(board, mark, legal, 8)
        assert m in legal, f"Turn {turn}: move {m} not in legal {legal}"
        connectx.drop(board, m, mark, 7, 8)


def test_booked_bot_timing():
    """Booked bot should be fast on book-covered positions."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    t0 = time.time()
    m = bitboard_ab_bot_fast_8x7_5_booked(board, 1, legal, 8, move_deadline=1.5)
    elapsed = time.time() - t0
    # Book move should be instant (< 10ms)
    assert elapsed < 0.1, f"Book move took {elapsed:.3f}s (expected instant)"
    assert m in legal


def test_booked_bot_timing_after_book():
    """Booked bot should fall back to AB search for non-book positions."""
    board = connectx.make_board(7, 8)
    # Place several pieces to get past the book
    for col in [3, 2, 4, 3]:
        connectx.drop(board, col, 1, 7, 8)
        connectx.drop(board, col, 2, 7, 8)
    legal = connectx.valid_moves(board, 8)
    if not legal:
        return
    t0 = time.time()
    m = bitboard_ab_bot_fast_8x7_5_booked(board, 1, legal, 8, move_deadline=1.5)
    elapsed = time.time() - t0
    assert elapsed < 2.0, f"Non-book move took {elapsed:.1f}s"
    assert m in legal


# ── Integration test ─────────────────────────────────────────────────────────

def test_booked_game():
    """Two booked bots should play a valid game."""
    board = connectx.make_board(7, 8)
    for turn in range(12):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        t0 = time.time()
        m = bitboard_ab_bot_fast_8x7_5_booked(board, mark, legal, 8)
        elapsed = time.time() - t0
        assert m in legal, f"Turn {turn}: invalid move {m}"
        connectx.drop(board, m, mark, 7, 8)
        w = connectx.check_win(board, m, mark, 7, 8, 5)
        # Don't break on win — just continue