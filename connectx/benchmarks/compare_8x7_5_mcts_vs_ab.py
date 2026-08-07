"""Compare UCB1 MCTS (500 sims) vs AB at 8x7/5 — baseline for PUCT comparison."""

import time
import sys
sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5 as AB
from connectx.bots.mcts_8x7_5 import mcts_bot_fast_8x7_5 as MCTS


def run_comparison(name, bot1_func, bot2_func, n_games):
    b1_wins = 0
    b2_wins = 0
    draws = 0

    for i in range(n_games):
        if i % 2 == 0:
            b1m, b2m = 1, 2
        else:
            b1m, b2m = 2, 1

        result, n, t = play_game(b1m, bot1_func, b2m, bot2_func)

        if 'INVALID' in result:
            b2_wins += 1
            wname = f'INVALID({name})'
        elif 'WINS' in result:
            mark_won = int(result[1])
            if mark_won == b1m:
                b1_wins += 1
                wname = name
            else:
                b2_wins += 1
                wname = bot2_func.__name__ if hasattr(bot2_func, '__name__') else 'AB'
        else:
            draws += 1
            wname = 'DRAW'

        print(f"  Game {i+1}: {wname} | {n} moves | {t:.1f}s")

    dec = b1_wins + b2_wins
    print(f"\n  {name}: {b1_wins}, AB: {b2_wins}, Draws: {draws}")
    if dec > 0:
        print(f"  {name} win rate: {b1_wins/dec*100:.0f}%, AB win rate: {b2_wins/dec*100:.0f}%")
    print()
    return {'b1': b1_wins, 'b2': b2_wins, 'd': draws}


def play_game(b1_mark, b1_func, b2_mark, b2_func):
    board = connectx.make_board(7, 8)
    moves = []
    total_time = 0.0

    for turn in range(56):
        mark = b1_mark if turn % 2 == 0 else b2_mark
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break

        t0 = time.time()
        if mark == b1_mark:
            m = b1_func(board, mark, legal, 8, move_deadline=2.0, seed=turn)
        else:
            m = b2_func(board, mark, legal, 8, move_deadline=2.0, seed=turn)
        elapsed = time.time() - t0
        total_time += elapsed

        if m not in legal:
            return f'INVALID', len(moves), total_time

        connectx.drop(board, m, mark, 7, 8)
        moves.append((turn + 1, mark, m, elapsed))

        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            return f'P{mark}_WINS', len(moves), total_time

    return f'DRAW_{len(moves)}', len(moves), total_time


if __name__ == '__main__':
    print("=== 8x7/5: UCB1 MCTS (500) vs AB ===\n")

    print("--- MCTS (500 sims) as P1(mark=1) vs AB as P2(mark=2) ---")
    r1 = run_comparison('MCTS_500', MCTS, AB, 10)

    print("--- AB as P1(mark=1) vs MCTS (500 sims) as P2(mark=2) ---")
    r2 = run_comparison('MCTS_500', AB, MCTS, 10)

    mcts_total = r1['b1'] + r2['b2']
    ab_total = r1['b2'] + r2['b1']
    draw_total = (r1['d'] + r2['d']) // 2

    print("=== Summary ===")
    total = mcts_total + ab_total
    print(f"  MCTS: {mcts_total}, AB: {ab_total}, Draw: {draw_total}/{20}" +
          (f" | MCTS={mcts_total/total*100:.0f}%" if total > 0 else ""))