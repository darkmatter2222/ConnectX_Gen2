"""Cycle 13.1 Quick Comparison: key matchups only, 10 games each."""
import sys, time, json
from pathlib import Path
sys.path.insert(0, ".")

from connectx.bots import (
    random_bot,
    win_seek_block_bot,
    bitboard_ab_bot_fast_v2,
    bitboard_ab_bot,
    bitboard_ab_bot_fast,
    mcts_bot,
    mcts_bot_value,
)
from connectx.tournament import BotRegistry, Tournament, Leaderboard

reg = BotRegistry()
for name, fn in [
    ("random", random_bot),
    ("win_seek_block", win_seek_block_bot),
    ("bitboard_ab_fast_v2", bitboard_ab_bot_fast_v2),
    ("bitboard_ab", bitboard_ab_bot),
    ("bitboard_ab_fast", bitboard_ab_bot_fast),
    ("mcts", mcts_bot),
    ("mcts_value", mcts_bot_value),
]:
    reg.register(name, fn)

GAMES = 10

t0 = time.time()
lb = Leaderboard()
results = []

def run_pair(name_a, name_b, tier=""):
    tourney = Tournament(registry=reg, games_per_pair=GAMES)
    r = tourney.run_pair(name_a, name_b)
    lb.add_match(r)
    elapsed = time.time() - t0
    total_games = sum(r2["games"] for r2 in results)
    print(f"  [{tier:>6}] {name_a} vs {name_b}: {r.summary()} [{elapsed:.0f}s, {total_games} games]")
    results.append({
        "white": name_a, "black": name_b, "games": GAMES, "tier": tier,
        "white_wins": r.bot_a_wins, "black_wins": r.bot_b_wins, "draws": r.draws,
        "elapsed": elapsed,
    })

# Key matchups
print("=== Key matchups ===")
run_pair("bitboard_ab_fast_v2", "mcts", "KEY")
run_pair("bitboard_ab_fast_v2", "mcts_value", "KEY")
run_pair("mcts", "mcts_value", "KEY")
run_pair("bitboard_ab_fast_v2", "win_seek_block", "KEY")
run_pair("bitboard_ab", "mcts", "KEY")
run_pair("mcts", "win_seek_block", "KEY")
run_pair("bitboard_ab_fast_v2", "bitboard_ab", "KEY")
run_pair("mcts_value", "win_seek_block", "KEY")
run_pair("mcts_value", "bitboard_ab_fast_v2", "KEY")
run_pair("mcts", "random", "KEY")
run_pair("mcts_value", "random", "KEY")
run_pair("bitboard_ab_fast_v2", "random", "KEY")
run_pair("win_seek_block", "random", "KEY")

total_time = time.time() - t0
total_games = sum(r2["games"] for r2 in results)
print(f"\nTotal time: {total_time:.0f}s, Total games: {total_games}")

print(f"\n{'Bot':<22} {'W':>5} {'L':>5} {'D':>5} {'GP':>5} {'Win%':>7} {'Pts':>6}")
print("-" * 60)
for name, stats in lb.ranked():
    points = stats.wins + 0.5 * stats.draws
    print(f"{name:<22} {stats.wins:>5} {stats.losses:>5} {stats.draws:>5} {stats.games_played:>5} {stats.win_pct:>6.1f}% {points:>6.1f}")

results_path = Path("tournament_results.json")
with open(results_path, 'w') as f:
    json.dump({
        "date": "2026-08-07",
        "cycle": "13.1-quick",
        "bots": reg.names(),
        "games_per_pair": GAMES,
        "total_time": total_time,
        "total_games": total_games,
        "results": results,
    }, f, indent=2)
print(f"\nResults saved to {results_path}")