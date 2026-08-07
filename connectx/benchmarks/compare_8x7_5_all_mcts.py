"""Compare UCB1 MCTS vs PUCT MCTS both vs AB at 8x7/5."""

import time
import sys
sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5 as AB
from connectx.bots.mcts_8x7_5 import mcts_bot_fast_8x7_5 as MCTS
from connectx.bots.mcts_8x7_5_puct import mcts_puct_bot_fast_8x7_5 as PUCT


def run_comparison(name, bot1_func, bot2_func, n_games):
    b1_wins = 0
    b2_wins = 0
    draws = 0
    invalids = 0
    total_time = 0.0
    total_moves = 0

    for i in range(n_games):
        if i % 2 == 0:
            b1m, b2m = 1, 2
        else:
            b1m, b2m = 2, 1

        result, n, t = play_game(b1m, bot1_func, b2m, bot2_func)

        if 'INVALID' in result:
            invalids += 1
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

        total_time += t
        total_moves += n
        print(f"  Game {i+1} ({name} as P{i%2==0 and '1' or '2'}): {wname} | {n} moves | {t:.1f}s")

    dec = b1_wins + b2_wins
    print(f"\n  {name}: Bot1={b1_wins}, Bot2={b2_wins}, Draws={draws}, Invalid={invalids}")
    if n_games > 0:
        print(f"  Avg time: {total_time/n_games:.1f}s, Avg moves: {total_moves/n_games:.0f}")
    print()
    return {'b1': b1_wins, 'b2': b2_wins, 'd': draws, 'i': invalids,
            't': total_time / n_games if n_games else 0, 'm': total_moves / n_games if n_games else 0}


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
    print("=" * 70)
    print("8x7/5: MCTS VARIANTS COMPARISON")
    print("=" * 70)

    print("\n--- UCB1 MCTS (500 iters, random playouts) as P1 vs AB as P2 ---")
    mcts_p1 = run_comparison('MCTS_500_vs_AB', MCTS, AB, 10)

    print("--- AB as P1 vs UCB1 MCTS (500 iters, random playouts) as P2 ---")
    mcts_p2 = run_comparison('AB_vs_MCTS_500', AB, MCTS, 10)

    print("--- PUCT (2500 iters, tactical playouts) as P1 vs AB as P2 ---")
    puct_p1 = run_comparison('PUCT_2500_vs_AB', PUCT, AB, 10)

    print("--- AB as P1 vs PUCT (2500 iters, tactical playouts) as P2 ---")
    puct_p2 = run_comparison('AB_vs_PUCT_2500', AB, PUCT, 10)

    print("--- PUCT (2500) as P1 vs MCTS (500) as P2 ---")
    puct_vs_mcts = run_comparison('PUCT_vs_MCTS', PUCT, MCTS, 10)

    print("--- MCTS (500) as P1 vs PUCT (2500) as P2 ---")
    mcts_vs_puct = run_comparison('MCTS_vs_PUCT', MCTS, PUCT, 10)

    print("\n" + "=" * 70)
    print("=== SUMMARY ===")
    print()
    print(f"{'Variant':<45} {'P1':>8} {'P2':>8} {'Draws':>7} {'AvgTime':>8}")
    print("-" * 70)
    print(f"{'MCTS (UCB1, 500 iters, random playouts)':<45} "
          f"P1={mcts_p1['b1']:2d} P2={mcts_p2['b2']:2d}   {mcts_p1['d']+mcts_p2['d']:2d}/20 "
          f"{mcts_p1['t']+mcts_p2['t']:.1f}s")
    print(f"{'PUCT (tactical, 2500 iters)':<45} "
          f"P1={puct_p1['b1']:2d} P2={puct_p2['b2']:2d}   {puct_p1['d']+puct_p2['d']:2d}/20 "
          f"{puct_p1['t']+puct_p2['t']:.1f}s")
    print()
    p1_wins = puct_vs_mcts['b1'] + mcts_vs_puct['b2']
    m1_wins = puct_vs_mcts['b2'] + mcts_vs_puct['b1']
    d_h2h = puct_vs_mcts['d'] + mcts_vs_puct['d']
    print(f"PUCT vs MCTS head-to-head (20 games):")
    print(f"  PUCT wins: {p1_wins}/20")
    print(f"  MCTS wins: {m1_wins}/20")
    print(f"  Draws: {d_h2h}/20")
    print("=" * 70)