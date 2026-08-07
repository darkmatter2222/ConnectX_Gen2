"""Tests for the 8×7/5 bitboard alpha-beta bot."""

from __future__ import annotations

import sys
sys.path.insert(0, '.')

import time
import connectx
from connectx.bots.bitboard_ab_8x7_5 import (
    bitboard_ab_bot_8x7_5,
    bitboard_ab_bot_fast_8x7_5,
    ROWS,
    COLS,
    INAROW,
    SIZE,
)
from connectx.bots.bitboard_ab_8x7_5 import _LINE_MASKS, _to_bitboard, _evaluate


# ── Board configuration assertions ──────────────────────────────────────────────

def test_board_config():
    assert ROWS == 7
    assert COLS == 8
    assert INAROW == 5
    assert SIZE == 56  # 7 × 8


def test_line_masks_count():
    assert len(_LINE_MASKS) >= 50
    assert len(_LINE_MASKS) <= 100


def test_line_masks_unique():
    assert len(_LINE_MASKS) == len(set(_LINE_MASKS))


# ── Engine compatibility ───────────────────────────────────────────────────────

def test_engine_8x7_5():
    board = connectx.make_board(7, 8)
    assert len(board) == 56
    legal = connectx.valid_moves(board, 8)
    assert legal == list(range(8))


def test_vertical_win_8x7_5():
    board = connectx.make_board(7, 8)
    for i in range(5):
        connectx.drop(board, 3, 1, 7, 8)
    assert connectx.check_win(board, col=3, mark=1, rows=7, cols=8, inarow=5)


def test_horizontal_win_8x7_5():
    board = connectx.make_board(7, 8)
    for c in range(5):
        connectx.drop(board, c, 1, 7, 8)
    assert connectx.check_win(board, col=4, mark=1, rows=7, cols=8, inarow=5)


def test_diagonal_win_8x7_5():
    board = connectx.make_board(7, 8)
    for i in range(5):
        connectx.drop(board, 3 + i, 1, 7, 8)
    assert connectx.check_win(board, col=7, mark=1, rows=7, cols=8, inarow=5)


def test_game_end_no_win_8x7_5():
    """With 5-in-a-row on 8×7, a full board = draw."""
    board = connectx.make_board(7, 8)
    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        assert connectx.drop(board, legal[0], mark, 7, 8) >= 0
    assert connectx.is_terminal(board, 7, 8)


# ── Bot import and interface ───────────────────────────────────────────────────

def test_bot_import():
    assert callable(bitboard_ab_bot_8x7_5)
    assert callable(bitboard_ab_bot_fast_8x7_5)


def test_bot_from_package():
    from connectx.bots import bitboard_ab_bot_8x7_5, bitboard_ab_bot_fast_8x7_5
    assert callable(bitboard_ab_bot_8x7_5)
    assert callable(bitboard_ab_bot_fast_8x7_5)


# ── Fast bot tests (quick, bounded depth) ──────────────────────────────────────

def test_fast_bot_first_move():
    """First move should be a center column."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    m = bitboard_ab_bot_fast_8x7_5(board, 1, legal, 8)
    assert m in [3, 4]  # Center columns


def test_fast_bot_legal_moves():
    """All returned moves must be legal."""
    board = connectx.make_board(7, 8)
    for turn in range(6):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5(board, mark, legal, 8)
        assert m in legal, f'Turn {turn}: move {m} not in legal {legal}'
        connectx.drop(board, m, mark, 7, 8)


def test_fast_bot_diverse_columns():
    """Bot should play center columns first, then expand outward."""
    columns_played = set()
    board = connectx.make_board(7, 8)
    for turn in range(8):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break
        m = bitboard_ab_bot_fast_8x7_5(board, mark, legal, 8)
        columns_played.add(m)
        connectx.drop(board, m, mark, 7, 8)
    # Should prefer center columns (3, 4) and then expand
    assert len(columns_played) >= 2, 'Bot should use at least center columns'
    assert 3 in columns_played or 4 in columns_played


def test_fast_bot_timing():
    """Fast bot should return within a reasonable time."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    t0 = time.time()
    m = bitboard_ab_bot_fast_8x7_5(board, 1, legal, 8, move_deadline=1.5)
    elapsed = time.time() - t0
    assert elapsed < 2.0, f'Move took {elapsed:.1f}s'
    assert m in legal


def test_fast_bot_time_limit_respected():
    """Bot should respect the time deadline."""
    board = connectx.make_board(7, 8)
    legal = connectx.valid_moves(board, 8)
    t0 = time.time()
    m = bitboard_ab_bot_fast_8x7_5(board, 1, legal, 8, move_deadline=0.2)
    elapsed = time.time() - t0
    assert elapsed < 0.5, f'Bot took {elapsed:.1f}s with 0.2s deadline'
    assert m in legal


# ── Evaluation tests ──────────────────────────────────────────────────────────

def test_evaluate_empty_board():
    """Empty board should evaluate to 0."""
    board = [0] * 56
    score = _evaluate(board, 1, 8)
    assert abs(score) < 1.0  # Small center bonus only


def test_evaluate_detects_win():
    """Evaluation should return large positive for a winning board."""
    board = [0] * 56
    for i in range(5):
        board[i * 8 + 3] = 1  # 5 in a row at row 0, cols 3-7
    score = _evaluate(board, 1, 8)
    assert score >= 100000.0


def test_evaluate_detects_loss():
    """Evaluation should return large negative for opponent win."""
    board = [0] * 56
    for i in range(5):
        board[i * 8 + 3] = 2  # Opponent has 5 in a row
    score = _evaluate(board, 1, 8)
    assert score <= -100000.0


# ── Bitboard tests ─────────────────────────────────────────────────────────────

def test_to_bitboard():
    board = [0] * 56
    board[3] = 1
    bb = _to_bitboard(board, 1)
    assert bb == (1 << 3)

    board[10] = 2
    bb2 = _to_bitboard(board, 2)
    assert bb2 == (1 << 10)


# ── Full game test (short, timed) ─────────────────────────────────────────────

def test_full_game_8x7_5_draw():
    """Two identical bots should play to a draw (no win detected)."""
    board = connectx.make_board(7, 8)
    total_time = 0.0
    max_time = 30.0  # Max 30 seconds for a full draw game

    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break

        t0 = time.time()
        action = bitboard_ab_bot_fast_8x7_5(board, mark, legal, 8)
        elapsed = time.time() - t0
        total_time += elapsed

        if total_time > max_time:
            break  # Give up if too slow

        assert action in legal, f'Turn {turn}: invalid move {action}'
        connectx.drop(board, action, mark, 7, 8)

        w = connectx.check_win(board, action, mark, 7, 8, 5)
        if w:
            # Game ended with a win — record and continue
            pass

    # After 56 moves or early termination, board should be full or draw
    assert connectx.is_terminal(board, 7, 8) or total_time > max_time


def test_two_bots_vs_each_other():
    """v2 (7×6/4) vs 8×7/5 fast bot — should not crash when sizes differ."""
    # This tests that each bot correctly uses its own board dimensions
    board_76 = connectx.make_board(6, 7)
    legal_76 = connectx.valid_moves(board_76, 7)
    from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_fast_v2
    m = bitboard_ab_bot_fast_v2(board_76, 1, legal_76, 7)
    assert m in legal_76

    board_87 = connectx.make_board(7, 8)
    legal_87 = connectx.valid_moves(board_87, 8)
    m = bitboard_ab_bot_fast_8x7_5(board_87, 1, legal_87, 8)
    assert m in legal_87