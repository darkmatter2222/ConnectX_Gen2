"""
Tournament: ensemble vs v2 vs nn vs mcts vs wsb vs random.

Proper seat-reversed paired evaluation.
"""

import sys
import time
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import connectx
from connectx import ConnectXEnv
from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2
from connectx.bots.bitboard_ab_with_nn import bitboard_ab_nn_bot
from connectx.bots.bitboard_ab_ensemble import bitboard_ab_ensemble_bot
from connectx.bots.mcts import mcts_bot, mcts_bot_fast
from connectx.bots.win_seek_block import win_seek_block_bot
from connectx.bots.random_bot import random_bot
from connectx.engine import valid_moves


BOTS = {
    'random': random_bot,
    'wsb': win_seek_block_bot,
    'v2': bitboard_ab_bot_v2,
    'mcts': mcts_bot,
    'mcts_fast': mcts_bot_fast,
    'nn': bitboard_ab_nn_bot,
    'ensemble': bitboard_ab_ensemble_bot,
}


def run_pair(bot_a_name, bot_b_name, n_games=40, cols=7, time_per_move=2.0):
    """Seat-reversed: half with bot_a as mark=1 (first), half as mark=2.

    Returns: dict with wins for each bot.
    """
    bot_a_fn = BOTS[bot_a_name]
    bot_b_fn = BOTS[bot_b_name]

    bot_a_wins = 0
    bot_b_wins = 0

    for game in range(n_games):
        is_a_first = (game % 2 == 0)

        env = ConnectXEnv(cols=cols)
        board = env.reset()

        for step in range(42):
            deadline = time.time() + time_per_move
            legal = valid_moves(board, cols)

            if not legal:
                break

            # Determine whose turn it is and what mark they play
            # Player 0 = mark 1, Player 1 = mark 2
            mark = env._player

            # Which bot moves?
            if is_a_first:
                # Bot A plays mark=1 (first player), Bot B plays mark=2
                bot_fn = bot_a_fn if mark == 1 else bot_b_fn
            else:
                # Bot A plays mark=2, Bot B plays mark=1
                bot_fn = bot_b_fn if mark == 1 else bot_a_fn

            try:
                move = bot_fn(board, mark, legal, cols,
                             move_deadline=deadline, remaining_overage=0.0)
            except Exception:
                # Bot crashed
                if mark == 1:
                    bot_b_wins += 1  # mark=1 lost
                else:
                    bot_a_wins += 1  # mark=2 lost
                board = env.reset()
                break

            if move not in legal:
                if mark == 1:
                    bot_b_wins += 1
                else:
                    bot_a_wins += 1
                board = env.reset()
                break

            result = env.step(move)
            board = result['board']

            if result['done']:
                # result['winner'] = 1 if mark=1 wins, 2 if mark=2 wins, 0 if draw
                winner = result['winner']
                if winner == 1:
                    # mark=1 won
                    if is_a_first:
                        bot_a_wins += 1  # bot_a played mark=1
                    else:
                        bot_b_wins += 1  # bot_b played mark=1
                elif winner == 2:
                    # mark=2 won
                    if is_a_first:
                        bot_b_wins += 1  # bot_b played mark=2
                    else:
                        bot_a_wins += 1  # bot_a played mark=2
                # draws are impossible in Connect 4 with optimal play
                break

    total = bot_a_wins + bot_b_wins
    return {
        'bot_a_wins': bot_a_wins,
        'bot_b_wins': bot_b_wins,
        'total': total,
        f'{bot_a_name}_wins': bot_a_wins,
        f'{bot_b_name}_wins': bot_b_wins,
        f'{bot_a_name}_win_pct': round(bot_a_wins / total * 100, 1) if total else 0,
        f'{bot_b_name}_win_pct': round(bot_b_wins / total * 100, 1) if total else 0,
    }


def main():
    matchups = [
        ('ensemble', 'v2'),
        ('ensemble', 'nn'),
        ('nn', 'v2'),
        ('ensemble', 'mcts'),
        ('v2', 'mcts'),
        ('nn', 'mcts'),
        ('ensemble', 'wsb'),
        ('v2', 'wsb'),
        ('nn', 'wsb'),
    ]

    results = {}
    for bot_a, bot_b in matchups:
        print(f"\n{'=' * 60}")
        print(f"  {bot_a} vs {bot_b}")
        print(f"{'=' * 60}")

        t0 = time.time()
        result = run_pair(bot_a, bot_b, n_games=40, time_per_move=2.0)
        elapsed = time.time() - t0

        key = f'{bot_a} vs {bot_b}'
        results[key] = result
        a_pct = result[f'{bot_a}_win_pct']
        b_pct = result[f'{bot_b}_win_pct']
        print(f"  {bot_a} wins: {result['bot_a_wins']:.0f} ({a_pct}%)")
        print(f"  {bot_b} wins: {result['bot_b_wins']:.0f} ({b_pct}%)")
        print(f"  Time: {elapsed:.1f}s")

    output = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'bots': list(BOTS.keys()),
        'matchups': results,
    }

    path = Path('tournament_ensemble_results.json')
    path.write_text(json.dumps(output, indent=2))
    print(f"\nResults saved to {path}")


if __name__ == '__main__':
    main()