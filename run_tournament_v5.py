"""Test v2 vs v5 at different time limits — eval speed matters under pressure."""
import sys
sys.path.insert(0, '.')
import time

from connectx.engine import make_board, valid_moves, check_win, drop
from connectx.bots.bitboard_ab_improved import (
    bitboard_ab_bot_v2, bitboard_ab_bot_fast_v2,
)
from connectx.bots.bitboard_ab_improved_v5 import (
    bitboard_ab_bot_v5, bitboard_ab_bot_fast_v5,
)


def timed_game(bot_a_fn, bot_b_fn, a_is_white, time_limit):
    board = make_board()
    a_mark = 1 if a_is_white else 2
    b_mark = 3 - a_mark
    total_a = 0.0
    total_b = 0.0
    moves = 0

    for move in range(1, 43):
        mark = a_mark if move % 2 == 1 else b_mark
        legal = valid_moves(board, 7)
        if not legal:
            return 0, total_a, total_b, moves

        if mark == a_mark:
            start = time.time()
            try:
                col = bot_a_fn(board, mark, list(legal), 7, move_deadline=time_limit)
            except Exception:
                col = legal[0]
            t = time.time() - start
            total_a += t
        else:
            start = time.time()
            try:
                col = bot_b_fn(board, mark, list(legal), 7, move_deadline=time_limit)
            except Exception:
                col = legal[0]
            t = time.time() - start
            total_b += t

        moves += 1
        drop(board, col, mark, 6, 7)
        if check_win(board, col, mark, 6, 7):
            return (1 if mark == a_mark else -1), total_a, total_b, moves

    return 0, total_a, total_b, moves


if __name__ == '__main__':
    print("=== Timing analysis: v2 vs v5 (3 games each) ===")
    for time_limit in [2.0, 1.0, 0.5, 0.25, 0.1]:
        print(f"\n  Time limit: {time_limit}s")
        for bot_name, bot_fn in [("v2", bitboard_ab_bot_v2), ("v5", bitboard_ab_bot_v5)]:
            total_move_time = 0.0
            total_moves = 0
            for _ in range(3):
                _, t_a, t_b, n = timed_game(bot_fn, bot_fn, True, time_limit)
                total_move_time += t_a
                total_moves += n
            avg = total_move_time / total_moves if total_moves else 0
            print(f"    {bot_name:>4}: avg={avg*1000:.1f}ms/move, total_game={total_move_time*1000:.0f}ms")