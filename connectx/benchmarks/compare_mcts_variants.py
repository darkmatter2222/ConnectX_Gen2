"""Compare MCTS variants: standard PUCT vs tactical vs AB-guided.

Each bot plays each other bot in both seats.
Reports first-player and second-player win rates separately.
"""

from __future__ import annotations

import sys, time, json, random

sys.path.insert(0, ".")

import connectx
from connectx.bots.mcts_8x7_5_puct import mcts_puct_bot_8x7_5
from connectx.bots.mcts_8x7_5_tactical import mcts_tactical_bot_fast_8x7_5
from connectx.bots.mcts_8x7_5_ab import mcts_ab_bot_fast_8x7_5

BOTS = {
    "Tactical MCTS": mcts_tactical_bot_fast_8x7_5,
    "AB-guided MCTS": mcts_ab_bot_fast_8x7_5,
    "Standard PUCT": mcts_puct_bot_8x7_5,
}

PAIRINGS = [
    ("Tactical MCTS", "Standard PUCT"),
    ("AB-guided MCTS", "Standard PUCT"),
    ("Tactical MCTS", "AB-guided MCTS"),
]

NUM_GAMES = 20
TIME_LIMIT = 1.5


def play_one(bot_a_fn, bot_b_fn, mark_a, mark_b, seed_a, seed_b, time_limit):
    """Play one game. A is first player (mark_a), B is second (mark_b).

    Returns (winner_mark, time_a_ms, time_b_ms).
    """
    board = connectx.make_board(7, 8)
    random.seed(seed_a)
    t_a = 0.0
    t_b = 0.0
    turn = 0

    while True:
        legal = connectx.valid_moves(board, 8)
        if not legal:
            return 0, t_a, t_b

        mark = 1 if turn % 2 == 0 else 2
        is_a = (mark == mark_a)

        t0 = time.time()
        if is_a:
            move = bot_a_fn(board, mark_a, legal, 8, move_deadline=time_limit, seed=seed_a)
        else:
            move = bot_b_fn(board, mark_b, legal, 8, move_deadline=time_limit, seed=seed_b)
        elapsed_ms = (time.time() - t0) * 1000
        if is_a:
            t_a += elapsed_ms
        else:
            t_b += elapsed_ms

        if move not in legal:
            # Invalid move: opponent wins
            return (mark_b if is_a else mark_a), t_a, t_b

        connectx.drop(board, move, mark, 7, 8)
        turn += 1

        winner = connectx.check_win(board, move, mark, 7, 8, 5)
        if winner:
            return winner, t_a, t_b


def compare_pair(name_a, name_b, bot_a_fn, bot_b_fn, num_games):
    """Run num_games paired games with seat reversal.

    Returns stats dict: {name_a: {first_w, first_d, first_l, first_time,
                                   second_w, second_d, second_l, second_time},
                        name_b: {...}}
    """
    stats = {}
    for name in (name_a, name_b):
        stats[name] = {
            "first_w": 0, "first_d": 0, "first_l": 0, "first_time": 0.0,
            "second_w": 0, "second_d": 0, "second_l": 0, "second_time": 0.0,
        }

    for i in range(num_games):
        # Game 1: A is first player (mark=1), B is second (mark=2)
        w1, ta1, tb1 = play_one(bot_a_fn, bot_b_fn, 1, 2, i, i + 10000, TIME_LIMIT)
        if w1 == 1:
            stats[name_a]["first_w"] += 1
            stats[name_b]["first_l"] += 1
        elif w1 == 2:
            stats[name_a]["first_l"] += 1
            stats[name_b]["first_w"] += 1
        else:
            stats[name_a]["first_d"] += 1
            stats[name_b]["first_d"] += 1
        stats[name_a]["first_time"] += ta1
        stats[name_b]["first_time"] += tb1

        # Game 2: B is first player (mark=1), A is second (mark=2)
        w2, tb2, ta2 = play_one(bot_b_fn, bot_a_fn, 1, 2, i + 10000, i, TIME_LIMIT)
        if w2 == 1:
            stats[name_b]["first_w"] += 1
            stats[name_a]["first_l"] += 1
        elif w2 == 2:
            stats[name_b]["first_l"] += 1
            stats[name_a]["first_w"] += 1
        else:
            stats[name_b]["first_d"] += 1
            stats[name_a]["first_d"] += 1
        stats[name_b]["first_time"] += tb2
        stats[name_a]["first_time"] += ta2

        print(f"  [{name_a} vs {name_b}] {i+1}/{num_games} | "
              f"A: F={stats[name_a]['first_w']}W-{stats[name_a]['first_d']}D-{stats[name_a]['first_l']}L "
              f"B: F={stats[name_b]['first_w']}W-{stats[name_b]['first_d']}D-{stats[name_b]['first_l']}L",
              flush=True)

    return stats


def print_stats(title, s):
    f_w, f_d, f_l = s["first_w"], s["first_d"], s["first_l"]
    s_w, s_d, s_l = s["second_w"], s["second_d"], s["second_l"]
    f_total = f_w + f_d + f_l
    s_total = s_w + s_d + s_l
    f_win = f_w / f_total * 100 if f_total else 0
    s_win = s_w / s_total * 100 if s_total else 0
    f_avg = s["first_time"] / f_w if f_w else s["first_time"] / max(1, f_total)
    s_avg = s["second_time"] / s_w if s_w else s["second_time"] / max(1, s_total)
    print(f"    First ({f_total}): {f_w}W {f_d}D {f_l}L ({f_win:.0f}% win, {f_avg:.0f}ms/move)")
    print(f"    Second ({s_total}): {s_w}W {s_d}D {s_l}L ({s_win:.0f}% win, {s_avg:.0f}ms/move)")


def main():
    print("=" * 70)
    print("MCTS Variant Comparison — 8x7/5 Connect Four")
    print("=" * 70)
    print(f"  Games per pairing: {NUM_GAMES} each way")
    print(f"  Time limit: {TIME_LIMIT}s per move")
    print(f"  Bots: {', '.join(BOTS.keys())}")
    print()

    all_round_stats = {}

    for name_a, name_b in PAIRINGS:
        print(f"\n{'-' * 70}")
        print(f"  {name_a} vs {name_b}")
        print(f"{'-' * 70}")
        stats = compare_pair(name_a, name_b, BOTS[name_a], BOTS[name_b], NUM_GAMES)
        all_round_stats[f"{name_a}_vs_{name_b}"] = stats

    # Aggregate across all pairings
    agg = {name: {"first_w": 0, "first_d": 0, "first_l": 0, "first_time": 0.0,
                  "second_w": 0, "second_d": 0, "second_l": 0, "second_time": 0.0}
           for name in BOTS}

    for key, stats in all_round_stats.items():
        for name in BOTS:
            if name in stats:
                for field in stats[name]:
                    agg[name][field] += stats[name][field]

    print(f"\n{'=' * 70}")
    print("AGGREGATED RESULTS (across all pairings)")
    print(f"{'=' * 70}")
    for name in BOTS:
        print(f"\n  {name}:")
        print_stats(name, agg[name])

    # Save JSON
    output = {
        "params": {"num_games": NUM_GAMES, "time_limit": TIME_LIMIT},
        "rounds": {k: dict(v) for k, v in all_round_stats.items()},
        "aggregated": agg,
    }
    with open("connectx/benchmarks/mcts_comparison_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  Results saved to connectx/benchmarks/mcts_comparison_results.json")


if __name__ == "__main__":
    main()