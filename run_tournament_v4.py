"""Quick v4 tournament."""
import sys
sys.path.insert(0, '.')
import time

from connectx.engine import make_board, valid_moves, check_win, drop
from connectx.bots.bitboard_ab_improved import (
    bitboard_ab_bot_v2, bitboard_ab_bot_fast_v2,
)
from connectx.bots.bitboard_ab_improved_v3 import (
    bitboard_ab_bot_v3, bitboard_ab_bot_fast_v3,
)
from connectx.bots.bitboard_ab_improved_v4 import (
    bitboard_ab_bot_v4, bitboard_ab_bot_fast_v4,
)
from connectx.bots.win_seek_block import win_seek_block_bot
from connectx.bots.mcts import mcts_bot


def safe_call(fn, board, mark, legal, cols, time_limit=2.0):
    start = time.time()
    try:
        return fn(board, mark, list(legal), cols, move_deadline=time_limit), time.time() - start
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        try:
            return fn(board, mark, list(legal), cols), time.time() - start
        except Exception:
            return legal[0] if legal else 0, 0


def timed_game(bot_a_fn, bot_b_fn, a_is_white, name_a, name_b, time_limit=2.0):
    board = make_board()
    a_mark = 1 if a_is_white else 2
    b_mark = 3 - a_mark
    total_a = 0.0
    total_b = 0.0

    for move in range(1, 43):
        mark = a_mark if move % 2 == 1 else b_mark
        legal = valid_moves(board, 7)
        if not legal:
            return 0, total_a, total_b

        if mark == a_mark:
            col, t = safe_call(bot_a_fn, board, mark, legal, 7, time_limit)
            total_a += t
        else:
            col, t = safe_call(bot_b_fn, board, mark, legal, 7, time_limit)
            total_b += t

        drop(board, col, mark, 6, 7)
        if check_win(board, col, mark, 6, 7):
            return (1 if mark == a_mark else -1), total_a, total_b

    return 0, total_a, total_b


def matchup(bot_a_fn, bot_b_fn, name_a, name_b, games=10, time_limit=2.0):
    a_w = b_w = draws = 0
    times_a = []
    times_b = []

    for i in range(games // 2):
        r, t_a, t_b = timed_game(bot_a_fn, bot_b_fn, True, name_a, name_b, time_limit)
        if r == 1: a_w += 1
        elif r == -1: b_w += 1
        else: draws += 1
        times_a.append(t_a)
        times_b.append(t_b)

        r, t_a, t_b = timed_game(bot_a_fn, bot_b_fn, False, name_a, name_b, time_limit)
        if r == -1: a_w += 1
        elif r == 1: b_w += 1
        else: draws += 1
        times_a.append(t_a)
        times_b.append(t_b)

    avg_a = sum(times_a) / len(times_a) if times_a else 0
    avg_b = sum(times_b) / len(times_b) if times_b else 0
    total = a_w + b_w + draws
    print(f'{name_a} vs {name_b}: {name_a}={a_w}/{total} ({a_w/total*100:.0f}%) '
          f'avg_move: {name_a}={avg_a*1000:.0f}ms {name_b}={avg_b*1000:.0f}ms')
    return a_w, b_w, draws


if __name__ == '__main__':
    print("=== v4 vs v2 (10 games) ===")
    matchup(bitboard_ab_bot_v4, bitboard_ab_bot_v2, 'v4', 'v2', 10)

    print("\n=== v4 vs v3 (10 games) ===")
    matchup(bitboard_ab_bot_v4, bitboard_ab_bot_v3, 'v4', 'v3', 10)

    print("\n=== v4 vs mcts (10 games) ===")
    matchup(bitboard_ab_bot_v4, mcts_bot, 'v4', 'mcts', 10)

    print("\n=== v4_fast vs v2_fast (10 games) ===")
    matchup(bitboard_ab_bot_fast_v4, bitboard_ab_bot_fast_v2, 'v4f', 'v2f', 10)

    print("\n=== v4_fast vs mcts (10 games) ===")
    matchup(bitboard_ab_bot_fast_v4, mcts_bot, 'v4f', 'mcts', 10)

    print("\n=== Baseline: v2 vs mcts (10 games) ===")
    matchup(bitboard_ab_bot_v2, mcts_bot, 'v2', 'mcts', 10)