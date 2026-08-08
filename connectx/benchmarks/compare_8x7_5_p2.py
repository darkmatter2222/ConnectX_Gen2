"""Head-to-head comparison: P2-exploit bot vs v2 regular.

Measures how well the P2-exploit bot plays as P2 compared to v2.
"""

from __future__ import annotations

import sys
sys.path.insert(0, '.')

import random
import time
from typing import Sequence

import connectx
from connectx.bots.bitboard_ab_8x7_5_v2 import (
    bitboard_ab_bot_fast_8x7_5_v2 as V2_REGULAR,
)
from connectx.bots.bitboard_ab_8x7_5_p2 import (
    bitboard_ab_bot_fast_8x7_5_p2 as P2_BOT,
)

ACTIONS_BUDGET = 2.0
SEAT_REVERSES = 20


def play_game(p1_bot, p2_bot, rows=7, cols=8, inarow=5):
    """Play one game between two bots."""
    board = [0] * (rows * cols)
    turn = 0

    while True:
        legal = connectx.valid_moves(board, cols)
        if not legal:
            return 'DRAW'
        mark = 1 if turn % 2 == 0 else 2
        if turn % 2 == 0:
            m = p1_bot(board, mark, legal, cols)
        else:
            m = p2_bot(board, mark, legal, cols)
        if m not in legal:
            print(f"INVALID MOVE: {m} not in {legal}")
            continue
        connectx.drop(board, m, mark, rows, cols)
        w = connectx.check_win(board, m, mark, rows, cols, inarow)
        if w:
            return f'WIN:{mark}'
        turn += 1
        if len(board) == rows * cols:
            return 'DRAW'


def main():
    results = {'v2_p1': 0, 'p2_p1': 0, 'draws': 0}
    total = SEAT_REVERSES * 2

    for i in range(SEAT_REVERSES):
        seed = i * 1000
        rng = random.Random(seed)

        # Pair 1: v2(P1) vs P2(P2)
        v2_wins = 0
        p2_wins = 0
        draws = 0

        for _ in range(1):
            board = [0] * 56
            turn = 0
            while True:
                legal = connectx.valid_moves(board, 8)
                if not legal:
                    draws += 1
                    break
                mark = 1 if turn % 2 == 0 else 2
                if turn % 2 == 0:
                    m = V2_REGULAR(board, mark, legal, 8)
                else:
                    m = P2_BOT(board, mark, legal, 8, move_deadline=1.5)
                if m not in legal:
                    continue
                connectx.drop(board, m, mark, 7, 8)
                w = connectx.check_win(board, m, mark, 7, 8, 5)
                if w:
                    v2_wins += 1 if mark == 1 else 0
                    p2_wins += 1 if mark == 2 else 0
                    break
                turn += 1
                if len(board) == 56:
                    draws += 1
                    break

            # Swap seats
            board = [0] * 56
            turn = 0
            while True:
                legal = connectx.valid_moves(board, 8)
                if not legal:
                    draws += 1
                    break
                mark = 1 if turn % 2 == 0 else 2
                if turn % 2 == 0:
                    m = P2_BOT(board, mark, legal, 8, move_deadline=1.5)
                else:
                    m = V2_REGULAR(board, mark, legal, 8)
                if m not in legal:
                    continue
                connectx.drop(board, m, mark, 7, 8)
                w = connectx.check_win(board, m, mark, 7, 8, 5)
                if w:
                    p2_wins += 1 if mark == 1 else 0
                    v2_wins += 1 if mark == 2 else 0
                    break
                turn += 1
                if len(board) == 56:
                    draws += 1
                    break

        results['v2_p1'] += v2_wins
        results['p2_p1'] += p2_wins
        results['draws'] += draws

    # Print results
    print(f"v2 as P1 vs P2 as P2: {results['v2_p1']}/{total} wins for v2")
    print(f"P2 as P1 vs v2 as P2: {results['p2_p1']}/{total} wins for P2")
    print(f"Draws: {results['draws']}/{total}")
    print(f"P2 as P2 wins: {results['p2_p1']}/{total} (P2 as P2)")
    print(f"v2 as P2 wins: {results['v2_p1']}/{total} (v2 as P2)")


if __name__ == '__main__':
    main()