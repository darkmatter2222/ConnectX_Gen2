"""Tests for the 8x7/5 AB-guided MCTS bot."""

from __future__ import annotations

import sys
sys.path.insert(0, ".")

import time
import connectx
from connectx.bots.mcts_8x7_5_ab import (
    mcts_ab_bot_8x7_5,
    mcts_ab_bot_fast_8x7_5,
)


def test_import():
    from connectx.bots.mcts_8x7_5_ab import (
        mcts_ab_bot_8x7_5,
        mcts_ab_bot_fast_8x7_5,
    )
    assert callable(mcts_ab_bot_8x7_5)
    assert callable(mcts_ab_bot_fast_8x7_5)


def test_from_package():
    from connectx.bots import mcts_ab_bot_8x7_5, mcts_ab_bot_fast_8x7_5
    assert callable(mcts_ab_bot_8x7_5)
    assert callable(mcts_ab_bot_fast_8x7_5)


def test_empty_board():
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    m = mcts_ab_bot_fast_8x7_5(board, 1, legal, 8)
    assert m in legal


def test_legal_moves():
    board = connectx.make_board(7, 8)
    for turn in range(16):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = mcts_ab_bot_fast_8x7_5(board, mark, legal, 8)
        assert m in legal, f"Turn {turn}: move {m} not in legal {legal}"
        connectx.drop(board, m, mark, 7, 8)


def test_timing():
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    t0 = time.time()
    m = mcts_ab_bot_fast_8x7_5(board, 1, legal, 8, move_deadline=1.5)
    elapsed = time.time() - t0
    assert elapsed < 5.0, f"AB-guided MCTS took {elapsed:.3f}s (expected < 5s)"
    assert m in legal


def test_timing_after_pieces():
    board = connectx.make_board(7, 8)
    for col in [3, 2, 4, 3, 2, 4]:
        connectx.drop(board, col, 1, 7, 8)
        connectx.drop(board, col, 2, 7, 8)
    legal = connectx.valid_moves(board, 8)
    if not legal:
        return
    t0 = time.time()
    m = mcts_ab_bot_fast_8x7_5(board, 1, legal, 8, move_deadline=1.5)
    elapsed = time.time() - t0
    assert elapsed < 3.0, f"AB-guided MCTS took {elapsed:.1f}s with pieces"
    assert m in legal


def test_game():
    board = connectx.make_board(7, 8)
    for turn in range(16):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = mcts_ab_bot_fast_8x7_5(board, mark, legal, 8)
        assert m in legal, f"Turn {turn}: invalid move {m}"
        connectx.drop(board, m, mark, 7, 8)
        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            break


def test_full_depth():
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    m = mcts_ab_bot_8x7_5(board, 1, legal, 8)
    assert m in legal, f"Full-depth bot returned {m} not in legal"


def test_seat_reversed():
    board = connectx.make_board(7, 8)
    for turn in range(20):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = mcts_ab_bot_fast_8x7_5(board, mark, legal, 8)
        assert m in legal
        connectx.drop(board, m, mark, 7, 8)


def test_no_crash_invalid():
    board = connectx.make_board(7, 8)
    for turn in range(30):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = mcts_ab_bot_fast_8x7_5(board, mark, legal, 8)
        assert m in legal, f"Turn {turn}: invalid move {m}"
        connectx.drop(board, m, mark, 7, 8)
        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            break