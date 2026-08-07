"""Compare booked v2 AB vs regular v2 AB vs PUCT MCTS at 8x7/5.

Benchmarks the v2 evaluation bot with and without opening book,
and compares against PUCT MCTS.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field

sys.path.insert(0, '.')

import connectx
from connectx.bots.bitboard_ab_8x7_5_v2 import (
    bitboard_ab_bot_8x7_5_v2 as v2_full,
    bitboard_ab_bot_fast_8x7_5_v2 as v2_fast,
)
from connectx.bots.bitboard_ab_8x7_5_v2_booked import (
    bitboard_ab_bot_8x7_5_v2_booked as v2_booked_full,
    bitboard_ab_bot_fast_8x7_5_v2_booked as v2_booked_fast,
)
from connectx.bots.mcts_8x7_5_puct import (
    mcts_puct_bot_8x7_5 as mcts_puct,
)


ROWS = 7
COLS = 8
INAROW = 5


def play_game(bot1, bot2, bot1_is_p1=True, max_moves=56):
    """Play one game between two bots.

    Args:
        bot1: Bot function (called first).
        bot2: Bot function (called second).
        bot1_is_p1: Whether bot1 plays as mark 1.
        max_moves: Maximum moves before forcing draw.

    Returns:
        (result, num_moves, bot1_wins_as_p1, bot1_wins_as_p2, total_time)
    """
    board = connectx.make_board(ROWS, COLS)
    total_time = 0.0
    bot1_moves = 0

    for turn in range(max_moves):
        mark = 1 if (turn % 2 == 0) else 2
        legal = connectx.valid_moves(board, COLS)
        if not legal:
            break

        t0 = time.time()
        if bot1_is_p1:
            current_bot = bot1 if mark == 1 else bot2
        else:
            current_bot = bot2 if mark == 1 else bot1

        m = current_bot(board, mark, legal, COLS, move_deadline=2.0)
        elapsed = time.time() - t0
        total_time += elapsed

        if m not in legal:
            return f"INVALID_{mark}", len(list(legal)), 0, 0, total_time

        if bot1_is_p1:
            if mark == 1 and bot1_is_p1:
                bot1_moves += 1
        connectx.drop(board, m, mark, ROWS, COLS)

        w = connectx.check_win(board, m, mark, ROWS, COLS, INAROW)
        if w:
            winner = mark if w == 1 else 3 - w
            bot1_wins_as_p1 = 1 if (bot1_is_p1 and winner == 1) else 0
            bot1_wins_as_p2 = 1 if (bot1_is_p1 and winner == 2) else 0
            # If bot1_is_p1 and bot1 plays as mark 1, bot1 wins as p1
            # If bot1_is_p1 and bot1 plays as mark 2, bot1 wins as p2
            if bot1_is_p1:
                bot1_wins_as_p1 = 1 if winner == 1 else 0
                bot1_wins_as_p2 = 1 if winner == 2 else 0
            else:
                bot1_wins_as_p1 = 1 if winner == 2 else 0
                bot1_wins_as_p2 = 1 if winner == 1 else 0
            return f"P{winner}_WINS", len(legal), bot1_wins_as_p1, bot1_wins_as_p2, total_time

    return f"DRAW_{max_moves}", len(legal), 0, 0, total_time


def run_comparison(bot1_name, bot1_fn, bot2_name, bot2_fn, n_games=20):
    """Run n_games of bot1 vs bot2, alternating P1/P2."""
    bot1_p1_wins = 0
    bot1_p2_wins = 0
    bot1_as_p1_wins = 0
    bot1_as_p2_wins = 0
    draws = 0
    invalid = 0
    total_time = 0.0

    for i in range(n_games):
        bot1_is_p1 = (i % 2 == 0)
        result, moves, p1_wins, p2_wins, game_time = play_game(
            bot1_fn, bot2_fn, bot1_is_p1=bot1_is_p1
        )

        total_time += game_time

        if result.startswith("INVALID"):
            invalid += 1
        elif result.startswith("DRAW"):
            draws += 1
        elif result.startswith("P1_WINS"):
            if bot1_is_p1:
                bot1_as_p1_wins += 1
                bot1_p1_wins += 1
            else:
                bot1_as_p2_wins += 1
                bot1_p2_wins += 1
        elif result.startswith("P2_WINS"):
            if bot1_is_p1:
                bot1_as_p2_wins += 1
                bot1_p2_wins += 1
            else:
                bot1_as_p1_wins += 1
                bot1_p1_wins += 1

    decisive = n_games - draws - invalid
    bot1_wins_total = bot1_as_p1_wins + bot1_as_p2_wins
    bot2_wins_total = decisive - bot1_wins_total

    return {
        "bot1": bot1_name,
        "bot2": bot2_name,
        "n_games": n_games,
        "bot1_as_p1_wins": bot1_as_p1_wins,
        "bot1_as_p2_wins": bot1_as_p2_wins,
        "bot1_wins_total": bot1_wins_total,
        "bot2_wins_total": bot2_wins_total,
        "draws": draws,
        "invalid": invalid,
        "bot1_p1_win_rate": f"{bot1_as_p1_wins}/{bot1_as_p1_wins + bot1_as_p2_wins}" if decisive > 0 else "0/0",
        "bot1_p2_win_rate": f"{bot1_as_p2_wins}/{bot1_as_p1_wins + bot1_as_p2_wins}" if decisive > 0 else "0/0",
        "total_time": round(total_time, 2),
    }


if __name__ == "__main__":
    n = 20  # 20 seat-reversed pairs = 40 games

    print("=" * 70)
    print("8x7/5 Bot Comparison — v2 Booked vs v2 vs PUCT")
    print("=" * 70)
    print(f"Games per comparison: {n} ({n * 2} total, alternating P1/P2)")
    print()

    results = []

    # Comparison 1: Booked v2 vs Regular v2
    print("=== Booked v2 vs Regular v2 ===")
    r1 = run_comparison(
        "v2_booked", v2_booked_fast,
        "v2_regular", v2_fast,
        n_games=n,
    )
    print(f"  {r1['bot1']} wins: {r1['bot1_wins_total']}/{n * 2}")
    print(f"  {r1['bot2']} wins: {r1['bot2_wins_total']}/{n * 2}")
    print(f"  Draws: {r1['draws']}, Invalid: {r1['invalid']}")
    results.append(r1)
    print()

    # Comparison 2: Booked v2 vs PUCT MCTS
    print("=== Booked v2 vs PUCT MCTS ===")
    r2 = run_comparison(
        "v2_booked", v2_booked_fast,
        "puct", mcts_puct,
        n_games=n,
    )
    print(f"  {r2['bot1']} wins: {r2['bot1_wins_total']}/{n * 2}")
    print(f"  {r2['bot2']} wins: {r2['bot2_wins_total']}/{n * 2}")
    print(f"  Draws: {r2['draws']}, Invalid: {r2['invalid']}")
    results.append(r2)
    print()

    # Comparison 3: Regular v2 vs PUCT MCTS
    print("=== Regular v2 vs PUCT MCTS ===")
    r3 = run_comparison(
        "v2_regular", v2_fast,
        "puct", mcts_puct,
        n_games=n,
    )
    print(f"  {r3['bot1']} wins: {r3['bot1_wins_total']}/{n * 2}")
    print(f"  {r3['bot2']} wins: {r3['bot2_wins_total']}/{n * 2}")
    print(f"  Draws: {r3['draws']}, Invalid: {r3['invalid']}")
    results.append(r3)
    print()

    # Save results
    summary = {
        "board": f"{COLS}x{ROWS}/{INAROW}",
        "n_games_per_pairing": n,
        "total_games": n * 6,
        "comparisons": results,
    }
    path = "compare_v2_booked_results.json"
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Results saved to {path}")
    print()
    print("Summary:")
    for r in results:
        print(f"  {r['bot1']} vs {r['bot2']}: "
              f"{r['bot1_wins_total']}W-{r['bot2_wins_total']}W-{r['draws']}D")