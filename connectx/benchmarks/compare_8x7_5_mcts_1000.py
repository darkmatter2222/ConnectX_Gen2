"""MCTS at 8x7/5 with increased sims — does more budget close the gap?"""

import time
import sys
sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5 as AB
from connectx.bots.mcts_8x7_5 import mcts_bot_8x7_5 as MCTS_BOT


def make_mcts(sims):
    """Return a bot function that calls MCTS with given simulations."""
    target_sims = sims
    def bot(board, mark, legal, cols, move_deadline=None, seed=None, **kw):
        return MCTS_BOT(board, mark, legal, cols, move_deadline,
                       seed=seed, num_simulations=target_sims)
    return bot


def play_game(p1_func, p1_mark, p2_func, p2_mark):
    """Play one game between two bots with fixed marks."""
    board = connectx.make_board(7, 8)
    moves = []
    total_time = 0.0

    for turn in range(56):
        mark = p1_mark if turn % 2 == 0 else p2_mark
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break

        t0 = time.time()
        if mark == p1_mark:
            m = p1_func(board, mark, legal, 8, move_deadline=2.0, seed=turn)
        else:
            m = p2_func(board, mark, legal, 8, move_deadline=2.0, seed=turn)
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


def run_comparison(b1_name, b1_func, b1_mark, b2_name, b2_func, b2_mark, n_games):
    """Run n_games between b1 (mark) and b2 (mark)."""
    b1_wins = 0
    b2_wins = 0
    draws = 0

    for i in range(n_games):
        result, n, t = play_game(b1_func, b1_mark, b2_func, b2_mark)

        if 'INVALID' in result:
            b2_wins += 1
            wname = b2_name
        elif 'WINS' in result:
            mark_won = int(result[1])
            if mark_won == b1_mark:
                b1_wins += 1
                wname = b1_name
            else:
                b2_wins += 1
                wname = b2_name
        else:
            draws += 1
            wname = 'DRAW'

        print(f"  Game {i+1}: {wname} | {n} moves | {t:.1f}s")

    dec = b1_wins + b2_wins
    print(f"\n  {b1_name}: {b1_wins}, {b2_name}: {b2_wins}, Draws: {draws}")
    if dec > 0:
        print(f"  {b1_name} win rate: {b1_wins/dec*100:.0f}%, {b2_name} win rate: {b2_wins/dec*100:.0f}%")
    print()
    return {'b1': b1_wins, 'b2': b2_wins, 'd': draws}


if __name__ == '__main__':
    print("=== 8x7/5: MCTS Simulation Scaling ===")
    print()

    results = {}

    for sims in [500, 1000, 2000]:
        mcts_bot = make_mcts(sims)
        label = f'MCTS_{sims}'

        print(f"--- {label} as P1(mark=1) vs AB as P2(mark=2) ---")
        r1 = run_comparison(label, mcts_bot, 1, 'AB', AB, 2, 10)

        print(f"--- AB as P1(mark=1) vs {label} as P2(mark=2) ---")
        r2 = run_comparison('AB', AB, 1, label, mcts_bot, 2, 10)

        # Combine
        mcts_total = r1['b1'] + r2['b2']
        ab_total = r1['b2'] + r2['b1']
        draw_total = (r1['d'] + r2['d']) // 2

        print(f"  Combined: {label}={mcts_total}, AB={ab_total}, Draws={draw_total}/20")
        if ab_total + mcts_total > 0:
            print(f"  {label} win rate: {mcts_total/(ab_total+mcts_total)*100:.0f}%")
        print()
        results[sims] = {'mcts': mcts_total, 'ab': ab_total, 'draws': draw_total}

    print("=== Summary ===")
    for sims, r in results.items():
        total = r['mcts'] + r['ab']
        print(f"  {sims} sims: MCTS={r['mcts']}, AB={r['ab']}, Draw={r['draws']}" +
              (f" | MCTS={r['mcts']/total*100:.0f}%" if total > 0 else ""))