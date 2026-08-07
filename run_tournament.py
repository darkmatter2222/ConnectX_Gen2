"""Run tournament focusing on key matchups including v2 variants."""
import sys, time, json
from pathlib import Path
sys.path.insert(0, "C:/Users/ryans/source/repos/ConnectX_Gen2")

from connectx.bots import (
    random_bot,
    win_seek_block_bot,
    shallow_minimax_bot,
    depth2_minimax_bot,
    bitboard_ab_bot_fast,
    bitboard_ab_bot,
    bitboard_ab_bot_v2,
    bitboard_ab_bot_fast_v2,
    mcts_bot_fast,
    mcts_bot,
)
from connectx.tournament import BotRegistry, Tournament, Leaderboard

reg = BotRegistry()
reg.register("random", random_bot)
reg.register("win_seek_block", win_seek_block_bot)
reg.register("shallow_minimax", shallow_minimax_bot)
reg.register("depth2_minimax", depth2_minimax_bot)
reg.register("bitboard_ab_fast", bitboard_ab_bot_fast)
reg.register("bitboard_ab", bitboard_ab_bot)
reg.register("bitboard_ab_v2", bitboard_ab_bot_v2)
reg.register("bitboard_ab_fast_v2", bitboard_ab_bot_fast_v2)
reg.register("mcts_fast", mcts_bot_fast)
reg.register("mcts", mcts_bot)

names = reg.names()
print(f"Registered {len(names)} bots: {names}")
print()

# Tiered game counts: critical matchups get more games
GAMES_CRITICAL = 100  # v2 vs top contenders
GAMES_STANDARD = 50   # Standard matchups
GAMES_LIGHT = 20      # Weaker bots / quick checks

print(f"Running tournament...\n")
t0 = time.time()

lb = Leaderboard()
results = []

def run_pair(name_a, name_b, games, tier=""):
    tourney = Tournament(registry=reg, games_per_pair=games)
    r = tourney.run_pair(name_a, name_b)
    lb.add_match(r)
    elapsed = time.time() - t0
    total_games = sum(
        r2["games"] for r2 in results
    )
    line = f"  [{tier:>8}] {name_a} vs {name_b}: {r.summary()} [{elapsed:.0f}s, {total_games} total games]"
    print(line)
    results.append({
        "white": name_a, "black": name_b, "games": games, "tier": tier,
        "white_wins": r.bot_a_wins, "black_wins": r.bot_b_wins, "draws": r.draws,
        "elapsed": elapsed,
    })

# === CRITICAL: v2 vs everything (the new contender) ===
print("=== CRITICAL: bitboard_ab_v2 vs all ===")
critical_vs = ["win_seek_block", "random", "mcts", "mcts_fast", "bitboard_ab", "bitboard_ab_fast", "depth2_minimax", "shallow_minimax"]
for bot in critical_vs:
    run_pair("bitboard_ab_v2", bot, GAMES_CRITICAL, "CRITICAL")

# === CRITICAL: v2_fast vs everything ===
print("\n=== CRITICAL: bitboard_ab_fast_v2 vs all ===")
for bot in ["win_seek_block", "random", "mcts", "mcts_fast", "bitboard_ab", "bitboard_ab_fast", "depth2_minimax", "shallow_minimax"]:
    run_pair("bitboard_ab_fast_v2", bot, GAMES_CRITICAL, "CRITICAL")

# === STANDARD: bitboard_ab (original) vs top bots ===
print("\n=== STANDARD: bitboard_ab vs top bots ===")
for bot in ["win_seek_block", "random", "mcts", "bitboard_ab_fast"]:
    run_pair("bitboard_ab", bot, GAMES_STANDARD, "STANDARD")

# === STANDARD: MCTS variants ===
print("\n=== STANDARD: mcts vs remaining ===")
for bot in ["win_seek_block", "bitboard_ab_fast", "depth2_minimax"]:
    run_pair("mcts", bot, GAMES_STANDARD, "STANDARD")

# === LIGHT: weaker bots ===
print("\n=== LIGHT: weaker bot matchups ===")
light_matchups = [
    ("shallow_minimax", "depth2_minimax"),
    ("depth2_minimax", "random"),
    ("shallow_minimax", "win_seek_block"),
    ("mcts_fast", "bitboard_ab_fast"),
    ("mcts_fast", "win_seek_block"),
]
for a, b in light_matchups:
    run_pair(a, b, GAMES_LIGHT, "LIGHT")

total_time = time.time() - t0
total_games = sum(r2["games"] for r2 in results)
print(f"\nTotal time: {total_time:.0f}s, Total games: {total_games}")

print(f"\n{'Bot':<22} {'W':>5} {'L':>5} {'D':>5} {'GP':>5} {'Win%':>7} {'Pts':>6}")
print("-" * 56)
for name, stats in lb.ranked():
    print(f"{name:<22} {stats.wins:>5} {stats.losses:>5} {stats.draws:>5} {stats.games_played:>5} {stats.win_pct:>6.1f}% {stats.points:>6.1f}")

# Save results as JSON
results_path = Path("tournament_results.json")
with open(results_path, 'w') as f:
    json.dump({
        "date": "2026-08-06",
        "version": "Cycle 8",
        "games_per_pair": {"CRITICAL": GAMES_CRITICAL, "STANDARD": GAMES_STANDARD, "LIGHT": GAMES_LIGHT},
        "total_time": total_time,
        "total_games": total_games,
        "results": results,
    }, f, indent=2)
print(f"\nResults saved to {results_path}")