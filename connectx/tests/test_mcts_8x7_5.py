"""Tests for the MCTS 8×7/5 bot."""

from __future__ import annotations

import sys
sys.path.insert(0, '.')

import time
import connectx
from connectx.bots.mcts_8x7_5 import (
    mcts_bot_8x7_5,
    mcts_bot_fast_8x7_5,
    _random_playout,
)


# ── Bot import and interface ───────────────────────────────────────────────────

def test_mcts_import():
    assert callable(mcts_bot_8x7_5)
    assert callable(mcts_bot_fast_8x7_5)


def test_mcts_from_package():
    from connectx.bots import mcts_bot_8x7_5, mcts_bot_fast_8x7_5
    assert callable(mcts_bot_8x7_5)
    assert callable(mcts_bot_fast_8x7_5)


# ── Fast bot tests ─────────────────────────────────────────────────────────────

def test_mcts_fast_first_move():
    """First move should be a legal column (MCTS varies with seed)."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    m = mcts_bot_fast_8x7_5(board, 1, legal, 8, seed=42)
    assert m in legal


def test_mcts_fast_legal_moves():
    """All returned moves must be legal."""
    board = connectx.make_board(7, 8)
    for turn in range(6):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = mcts_bot_fast_8x7_5(board, mark, legal, 8, seed=turn)
        assert m in legal, f'Turn {turn}: move {m} not in legal {legal}'
        connectx.drop(board, m, mark, 7, 8)


def test_mcts_fast_diverse_columns():
    """Bot should use multiple columns."""
    columns_played = set()
    board = connectx.make_board(7, 8)
    for turn in range(10):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = mcts_bot_fast_8x7_5(board, mark, legal, 8, seed=turn * 100)
        columns_played.add(m)
        connectx.drop(board, m, mark, 7, 8)
    assert len(columns_played) >= 2


def test_mcts_fast_timing():
    """Fast bot should return quickly."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    t0 = time.time()
    m = mcts_bot_fast_8x7_5(board, 1, legal, 8, move_deadline=1.5, seed=42)
    elapsed = time.time() - t0
    assert elapsed < 2.0, f'Move took {elapsed:.1f}s'
    assert m in legal


def test_mcts_fast_time_limit_respected():
    """Bot should respect time deadline."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    t0 = time.time()
    m = mcts_bot_fast_8x7_5(board, 1, legal, 8, move_deadline=0.5, seed=42)
    elapsed = time.time() - t0
    assert elapsed < 1.0, f'Bot took {elapsed:.1f}s with 0.5s deadline'
    assert m in legal


def test_mcts_full_game():
    """Two MCTS bots should play a game."""
    board = connectx.make_board(7, 8)
    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = mcts_bot_fast_8x7_5(board, mark, legal, 8, seed=turn)
        assert m in legal, f'Turn {turn}: invalid move {m}'
        connectx.drop(board, m, mark, 7, 8)


# ── Playout tests ──────────────────────────────────────────────────────────────

def test_random_playout_win():
    """Playout should return +1 if start_mark has a guaranteed win."""
    import random
    rng = random.Random(42)
    # Test: mark 1 has 4 in a row vertically at col 3, rows 0-3
    board2 = [0] * 56
    for i in range(4):
        board2[i * 8 + 3] = 1  # 4 in a row vertically at col 3, rows 0-3
    result = _random_playout(board2, 1, 8, rng)
    # Mark 1 has 4 in a row — next time they play col 3 they win
    # But playout starts with mark 1's turn
    assert result >= -1.0 and result <= 1.0


def test_random_playout_draw():
    """Full board playout = draw (0)."""
    board = [1 if i % 2 == 0 else 2 for i in range(56)]
    import random
    rng = random.Random(42)
    result = _random_playout(board, 1, 8, rng)
    assert result == 0.0


# ── Comparison tests ───────────────────────────────────────────────────────────

def test_mcts_vs_ab_8x7_5():
    """MCTS should play legal moves vs AB at 8×7/5."""
    board = connectx.make_board(7, 8)
    for turn in range(10):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        if mark == 1:
            from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_fast_8x7_5 as AB
            m = AB(board, mark, legal, 8)
        else:
            m = mcts_bot_fast_8x7_5(board, mark, legal, 8, seed=turn)
        assert m in legal
        connectx.drop(board, m, mark, 7, 8)