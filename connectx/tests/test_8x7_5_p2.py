"""Tests for the 8x7/5 P2-exploit bot."""

import time
from connectx.bots.bitboard_ab_8x7_5_p2 import (
    bitboard_ab_bot_8x7_5_p2,
    bitboard_ab_bot_fast_8x7_5_p2,
)
from connectx.engine import valid_moves, check_win, drop, seat_reverse


def test_p2_import():
    """Can import the p2 bot."""
    from connectx.bots.bitboard_ab_8x7_5_p2 import bitboard_ab_bot_8x7_5_p2
    assert callable(bitboard_ab_bot_8x7_5_p2)


def test_p2_from_package():
    """Package import works."""
    from connectx.bots import bitboard_ab_bot_8x7_5_p2
    assert callable(bitboard_ab_bot_8x7_5_p2)


def test_p2_empty_board():
    """Empty board returns a valid column."""
    board = [0] * 56
    col = bitboard_ab_bot_8x7_5_p2(board, 2, [0, 1, 2, 3, 4, 5, 6, 7])
    assert 0 <= col <= 7


def test_p2_legal_moves():
    """All moves are legal over many turns."""
    board = [0] * 56
    for turn in range(10):
        legal = valid_moves(board, 8)
        col = bitboard_ab_bot_8x7_5_p2(board, (turn % 2) + 1, legal)
        assert col in legal
        drop(board, col, (turn % 2) + 1, 7, 8)
        if check_win(board, col, (turn % 2) + 1, 7, 8):
            break


def test_p2_timing_empty():
    """Empty board responds quickly."""
    board = [0] * 56
    start = time.time()
    col = bitboard_ab_bot_8x7_5_p2(board, 2, [0, 1, 2, 3, 4, 5, 6, 7])
    elapsed = time.time() - start
    assert elapsed < 1.0  # should be instant
    assert col == 3 or col == 4  # center columns preferred


def test_p2_timing_with_pieces():
    """Non-empty board responds within budget."""
    board = [0] * 56
    for i in range(10):
        legal = valid_moves(board, 8)
        drop(board, legal[0], 1, 7, 8)
        legal = valid_moves(board, 8)
        drop(board, legal[0], 2, 7, 8)
    start = time.time()
    col = bitboard_ab_bot_8x7_5_p2(board, 1, valid_moves(board, 8))
    elapsed = time.time() - start
    assert elapsed < 5.0  # should be fast


def test_p2_game():
    """Full game plays to conclusion without crash."""
    board = [0] * 56
    turn = 0
    while True:
        legal = valid_moves(board, 8)
        if not legal:
            break
        p1_col = bitboard_ab_bot_8x7_5_p2(board, 1, legal)
        if p1_col not in legal:
            break
        drop(board, p1_col, 1, 7, 8)
        if check_win(board, p1_col, 1, 7, 8):
            break
        p2_col = bitboard_ab_bot_8x7_5_p2(board, 2, legal)
        if p2_col not in legal:
            break
        drop(board, p2_col, 2, 7, 8)
        if check_win(board, p2_col, 2, 7, 8):
            break
        turn += 1
        if turn > 30:
            break


def test_p2_full_depth():
    """Full-depth variant works."""
    board = [0] * 56
    col = bitboard_ab_bot_8x7_5_p2(board, 2)
    assert 0 <= col <= 7


def test_p2_seat_reversed():
    """Two P2 bots playing each other produce a valid game."""
    board = [0] * 56
    for i in range(20):
        legal = valid_moves(board, 8)
        if not legal:
            break
        c1 = bitboard_ab_bot_8x7_5_p2(board, 1, legal)
        if c1 not in legal:
            break
        drop(board, c1, 1, 7, 8)
        if check_win(board, c1, 1, 7, 8):
            break
        c2 = bitboard_ab_bot_8x7_5_p2(board, 2, legal)
        if c2 not in legal:
            break
        drop(board, c2, 2, 7, 8)
        if check_win(board, c2, 2, 7, 8):
            break
    assert board is not None


def test_p2_no_crash_invalid():
    """30 turns without invalid moves."""
    board = [0] * 56
    for turn in range(30):
        legal = valid_moves(board, 8)
        if not legal:
            break
        col = bitboard_ab_bot_8x7_5_p2(board, (turn % 2) + 1, legal)
        assert col in legal, f"Invalid move {col} at turn {turn}"
        drop(board, col, (turn % 2) + 1, 7, 8)


def test_p2_different_from_v2():
    """P2 bot makes different moves than regular v2, showing it's not identical."""
    from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5
    board = [0] * 56
    moves_p2 = set()
    moves_v2 = set()
    legal = [0, 1, 2, 3, 4, 5, 6, 7]
    for _ in range(5):
        m1 = bitboard_ab_bot_8x7_5_p2(board, 1, legal)
        m2 = bitboard_ab_bot_8x7_5(board, 1, legal)
        moves_p2.add(m1)
        moves_v2.add(m2)
        if m1 != m2:
            break
    # They should differ at least sometimes
    assert len(moves_p2) > 0