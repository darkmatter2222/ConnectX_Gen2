"""Balanced MCTS comparisons at 8x7/5 with proper mark tracking.

P1 always gets mark=1, P2 always gets mark=2, regardless of which bot
plays which seat. Each game alternates which bot is P1 and which is P2.
"""

import time, sys
sys.path.insert(0, '.')
import connectx
from connectx.bots.bitboard_ab_8x7_5 import bitboard_ab_bot_8x7_5 as AB
from connectx.bots.mcts_8x7_5 import mcts_bot_8x7_5 as MCTS_REG
from connectx.bots.mcts_8x7_5 import mcts_bot_heuristic_8x7_5 as MCTS_HEUR


def play_game(bot1_bot_func, bot1_is_p1, bot2_bot_func, bot2_is_p1):
    """Play one game.

    Args:
        bot1_bot_func: callable for bot1's move selection
        bot1_is_p1: True if bot1 plays P1 (mark=1), else P2 (mark=2)
        bot2_bot_func: callable for bot2's move selection
        bot2_is_p1: True if bot2 plays P1 (mark=1), else P2 (mark=2)
    """
    bot1_mark = 1 if bot1_is_p1 else 2
    bot2_mark = 2 if bot1_is_p1 else 1

    board = connectx.make_board(7, 8)
    moves = []
    total_time = 0.0

    for turn in range(56):
        mark = 1 if turn % 2 == 0 else 2
        legal = connectx.valid_moves(board, 8)
        if not legal:
            break

        t0 = time.time()
        if mark == bot1_mark:
            m = bot1_bot_func(board, mark, legal, 8, move_deadline=2.0, seed=turn)
        else:
            m = bot2_bot_func(board, mark, legal, 8, move_deadline=2.0, seed=turn)
        elapsed = time.time() - t0
        total_time += elapsed

        if m not in legal:
            winner = 2 if mark == bot1_mark else 1
            return f"P{winner}_INVALID", len(moves), total_time, bot1_is_p1

        connectx.drop(board, m, mark, 7, 8)
        moves.append((turn + 1, mark, m, elapsed))

        w = connectx.check_win(board, m, mark, 7, 8, 5)
        if w:
            return f"P{mark}_WINS", len(moves), total_time, bot1_is_p1

    return f"DRAW_{len(moves)}", len(moves), total_time, bot1_is_p1


def run_comparison(name, bot1_func, bot2_func, n_games):
    """Run balanced comparison: alternating who is P1."""
    stats = {'bot1_win': 0, 'bot2_win': 0, 'draw': 0, 'invalid': 0}

    for i in range(n_games):
        bot1_is_p1 = (i % 2 == 0)
        bot2_is_p1 = not bot1_is_p1
        result, n, t, was_p1 = play_game(bot1_func, bot1_is_p1, bot2_func, bot2_is_p1)

        # Parse result
        if 'INVALID' in result:
            stats['invalid'] += 1
            # The bot playing the invalid move loses
            winner = 'bot2' if (was_p1 and 'INVALID_P2' in result) or (not was_p1 and 'INVALID_P1' in result) else 'bot1'
            stats['bot2_win' if winner == 'bot2' else 'bot1_win'] += 1
        elif 'WINS' in result:
            mark_won = int(result[1])
            # mark 1 wins: bot1 wins if bot1 is P1, bot2 wins if bot1 is P2
            if mark_won == 1:
                winner = 'bot1' if was_p1 else 'bot2'
            else:
                winner = 'bot2' if was_p1 else 'bot1'
            stats[f'{winner}_win'] += 1
        else:
            stats['draw'] += 1

        # Determine which side won for display
        if 'WINS' in result:
            mark_won = int(result[1])
            if mark_won == 1:
                winner_name = f'Bot1({name})' if was_p1 else 'Bot2'
            else:
                winner_name = 'Bot2' if was_p1 else f'Bot1({name})'
        else:
            winner_name = 'DRAW'

        print(f"  Game {i+1} ({'P1' if bot1_is_p1 else 'P2'}): {winner_name} | {n} moves | {t:.1f}s")

    b1 = stats['bot1_win']
    b2 = stats['bot2_win']
    d = stats['draw']
    dec = b1 + b2

    print(f"\n  {name} wins: {b1}, Bot2 wins: {b2}, Draws: {d}")
    if dec > 0:
        print(f"  {name} win rate: {b1/dec*100:.0f}%, Bot2 win rate: {b2/dec*100:.0f}%")
    print()

    return stats


if __name__ == '__main__':
    print("=== 8x7/5: Balanced MCTS Comparisons ===")
    print()

    n_games = 20

    # Test 1: Regular MCTS vs AB
    print("--- Regular MCTS (500 sims) vs AB ---")
    reg_vs_ab = run_comparison('MCTS_REG', MCTS_REG, AB, n_games)

    # Test 2: Heuristic MCTS vs AB
    print("--- Heuristic MCTS (500 sims) vs AB ---")
    heur_vs_ab = run_comparison('MCTS_HEUR', MCTS_HEUR, AB, n_games)

    # Test 3: Regular vs Heuristic MCTS
    print("--- Regular MCTS vs Heuristic MCTS ---")
    reg_vs_heur = run_comparison('MCTS_REG', MCTS_REG, MCTS_HEUR, n_games)

    # Summary
    print("=== Summary ===")
    for name, stats in [('MCTS_REG vs AB', reg_vs_ab),
                         ('MCTS_HEUR vs AB', heur_vs_ab),
                         ('MCTS_REG vs MCTS_HEUR', reg_vs_heur)]:
        b1 = stats['bot1_win']
        b2 = stats['bot2_win']
        d = stats['draw']
        dec = b1 + b2
        print(f"  {name}: Bot1={b1}, Bot2={b2}, Draw={d}" +
              (f" | Bot1={b1/dec*100:.0f}% Bot2={b2/dec*100:.0f}%" if dec > 0 else ""))