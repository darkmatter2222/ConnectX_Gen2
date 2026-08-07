"""Compare original 8x7/5 AB bot vs improved evaluation (v2).

Tests:
1. Original vs v2 (seat-reversed) — who wins?
2. v2 vs PUCT — does the stronger eval help?

Usage:
    python connectx/benchmarks/compare_8x7_5_v2_vs_original.py
"""

from __future__ import annotations

import sys
sys.path.insert(0, '.')

import time
import random

import connectx
from connectx.bots.bitboard_ab_8x7_5 import (
    bitboard_ab_bot_fast_8x7_5 as _ab_orig,
)
from connectx.bots.bitboard_ab_8x7_5_v2 import (
    bitboard_ab_bot_fast_8x7_5_v2 as _ab_v2,
)
from connectx.bots.mcts_8x7_5_puct import mcts_puct_bot_fast_8x7_5 as _puct

ROWS = 7
COLS = 8
INAROW = 5


def play_game(bot1, bot2, seed=None):
    """Play a game between two bots. bot1 is P1 (mark=1), bot2 is P2 (mark=2)."""
    board = connectx.make_board(ROWS, COLS)
    start = time.time()

    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, COLS)
        if not legal:
            break

        bot = bot1 if turn % 2 == 0 else bot2
        deadline = 2.0 - (time.time() - start)
        m = bot(board, mark, legal, COLS, move_deadline=deadline)

        assert m in legal, f"Invalid move: {m}"
        connectx.drop(board, m, mark, ROWS, COLS)

        w = connectx.check_win(board, m, mark, ROWS, COLS, INAROW)
        if w:
            return mark, time.time() - start, turn + 1

    # Draw (full board or no legal moves)
    return 0, time.time() - start, 56


def main():
    random.seed(42)
    n = 10

    print("=" * 60)
    print("Original 8x7/5 AB vs v2 (improved eval)")
    print("=" * 60)

    # Original as P1, v2 as P2
    wins_p1 = 0
    wins_p2 = 0
    draws = 0
    total_time_p1_p2 = 0
    total_time_p2_p1 = 0

    for i in range(n):
        # P1 = original, P2 = v2
        t0 = time.time()
        winner, elapsed, moves = play_game(_ab_orig, _ab_v2)
        total_time_p1_p2 += elapsed

        if winner == 1:
            wins_p1 += 1
        elif winner == 2:
            wins_p2 += 1
        else:
            draws += 1

        # Seat-reversed: P1 = v2, P2 = original
        t0 = time.time()
        winner2, elapsed2, moves2 = play_game(_ab_v2, _ab_orig)
        total_time_p2_p1 += elapsed2

        if winner2 == 2:
            wins_p1 += 1  # v2 wins as P1
        elif winner2 == 1:
            wins_p2 += 1  # original wins as P1
        else:
            draws += 1

        if (i + 1) % 5 == 0:
            print(f"  Game {i+1}: P1={'v2' if wins_p1 >= wins_p2 else 'orig'} {wins_p1}-{wins_p2} draws={draws}")

    avg_time_p1_p2 = total_time_p1_p2 / n
    avg_time_p2_p1 = total_time_p2_p1 / n
    avg_time = (avg_time_p1_p2 + avg_time_p2_p1) / 2

    print(f"\nResult ({n} games x 2 seats = {2*n} total):")
    print(f"  v2 as P1: {wins_p1} wins")
    print(f"  original as P1: {wins_p2} wins")
    print(f"  Draws: {draws}")
    print(f"  Avg time/game: {avg_time:.2f}s")

    print("\n" + "=" * 60)
    print("v2 vs PUCT")
    print("=" * 60)

    wins_v2 = 0
    wins_puct = 0
    draws = 0
    total_time = 0

    for i in range(n):
        t0 = time.time()
        winner, elapsed, moves = play_game(_ab_v2, _puct)
        total_time += elapsed

        if winner == 1:
            wins_v2 += 1
        elif winner == 2:
            wins_puct += 1
        else:
            draws += 1

        if (i + 1) % 5 == 0:
            print(f"  Game {i+1}: v2={wins_v2} puct={wins_puct} draws={draws}")

    avg_time2 = total_time / n
    print(f"\nResult ({n} games):")
    print(f"  v2: {wins_v2} wins")
    print(f"  PUCT: {wins_puct} wins")
    print(f"  Draws: {draws}")
    print(f"  Avg time/game: {avg_time2:.2f}s")


if __name__ == '__main__':
    main()