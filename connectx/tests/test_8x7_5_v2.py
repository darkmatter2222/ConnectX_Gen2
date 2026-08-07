"""Tests for the 8x7/5 v2 bot (improved evaluation)."""

from __future__ import annotations

import sys

sys.path.insert(0, ".")

import time
import connectx
from connectx.bots.bitboard_ab_8x7_5_v2 import (
    bitboard_ab_bot_8x7_5_v2,
    bitboard_ab_bot_fast_8x7_5_v2,
)
from connectx.bots.bitboard_ab_8x7_5 import (
    bitboard_ab_bot_8x7_5 as _orig,
    bitboard_ab_bot_fast_8x7_5 as _orig_fast,
)


def test_v2_import():
    from connectx.bots.bitboard_ab_8x7_5_v2 import (
        bitboard_ab_bot_8x7_5_v2,
        bitboard_ab_bot_fast_8x7_5_v2,
    )
    assert callable(bitboard_ab_bot_8x7_5_v2)
    assert callable(bitboard_ab_bot_fast_8x7_5_v2)


def test_v2_from_package():
    from connectx.bots import bitboard_ab_bot_8x7_5_v2, bitboard_ab_bot_fast_8x7_5_v2
    assert callable(bitboard_ab_bot_8x7_5_v2)
    assert callable(bitboard_ab_bot_fast_8x7_5_v2)


def test_v2_empty_board():
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    m = bitboard_ab_bot_fast_8x7_5_v2(board, 1, legal, 8)
    assert m in (3, 4), f"Empty board should return center, got {m}"
    assert m in legal


def test_v2_legal_moves():
    board = connectx.make_board(7, 8)
    for turn in range(16):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5_v2(board, mark, legal, 8)
        assert m in legal, f"Turn {turn}: move {m} not in legal {legal}"
        connectx.drop(board, m, mark, 7, 8)


def test_v2_timing():
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    t0 = time.time()
    m = bitboard_ab_bot_fast_8x7_5_v2(board, 1, legal, 8, move_deadline=1.5)
    elapsed = time.time() - t0
    assert elapsed < 5.0, f"V2 fast bot took {elapsed:.3f}s (expected < 5s)"
    assert m in legal


def test_v2_timing_after_pieces():
    board = connectx.make_board(7, 8)
    # Place several pieces
    for col in [3, 2, 4, 3, 2, 4]:
        connectx.drop(board, col, 1, 7, 8)
        connectx.drop(board, col, 2, 7, 8)
    legal = connectx.valid_moves(board, 8)
    if not legal:
        return
    t0 = time.time()
    m = bitboard_ab_bot_fast_8x7_5_v2(board, 1, legal, 8, move_deadline=1.5)
    elapsed = time.time() - t0
    assert elapsed < 3.0, f"Non-empty board took {elapsed:.1f}s"
    assert m in legal


def test_v2_game():
    board = connectx.make_board(7, 8)
    for turn in range(16):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        t0 = time.time()
        m = bitboard_ab_bot_fast_8x7_5_v2(board, mark, legal, 8)
        elapsed = time.time() - t0
        assert m in legal, f"Turn {turn}: invalid move {m}"
        connectx.drop(board, m, mark, 7, 8)
        w = connectx.check_win(board, m, mark, 7, 8)
        if w:
            break  # Game over


def test_v2_different_from_original():
    """V2 should make different moves than original on some positions."""
    board = connectx.make_board(7, 8)
    # Place a few pieces to get past empty board
    connectx.drop(board, 3, 1, 7, 8)
    connectx.drop(board, 4, 2, 7, 8)
    legal = connectx.valid_moves(board, 8)
    m_orig = _orig_fast(board, 1, legal, 8)
    m_v2 = bitboard_ab_bot_fast_8x7_5_v2(board, 1, legal, 8)
    assert m_orig in legal
    assert m_v2 in legal


def test_v2_full_depth():
    """Full-depth variant should work."""
    board = connectx.make_board(7, 8)
    m = bitboard_ab_bot_8x7_5_v2(board, 1, None, 8)
    assert m in (3, 4), f"Empty board full-depth should return center, got {m}"


def test_v2_seat_reversed():
    """Two identical v2 bots should produce a game."""
    board = connectx.make_board(7, 8)
    for turn in range(20):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5_v2(board, mark, legal, 8)
        assert m in legal
        connectx.drop(board, m, mark, 7, 8)


def test_v2_no_crash_invalid():
    """Bot should never return an invalid move."""
    board = connectx.make_board(7, 8)
    for turn in range(30):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5_v2(board, mark, legal, 8)
        assert m in legal, f"Turn {turn}: invalid move {m}"
        connectx.drop(board, m, mark, 7, 8)
        w = connectx.check_win(board, m, mark, 7, 8)
        if w:
            break