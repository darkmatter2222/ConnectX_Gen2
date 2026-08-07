"""Run tournament with FAST variants only — quick snapshot."""
import sys, time
sys.path.insert(0, "C:/Users/ryans/source/repos/ConnectX_Gen2")

from connectx.bots import (
    random_bot,
    win_seek_block_bot,
    shallow_minimax_bot,
    depth2_minimax_bot,
    bitboard_ab_bot_fast,
    bitboard_ab_bot,
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
reg.register("mcts_fast", mcts_bot_fast)
reg.register("mcts", mcts_bot)

names = reg.names()
print(f"Registered {len(names)} bots: {names}")
print(f"\nRunning tournament with {10} games per pair...\n")

t0 = time.time()

# Run specific matchups that matter
# Focus on top-4: win_seek_block, mcts, bitboard_ab, depth2_minimax
matchups = [
    ("mcts_fast", "bitboard_ab_fast"),
    ("mcts_fast", "depth2_minimax"),
    ("mcts_fast", "win_seek_block"),
    ("bitboard_ab_fast", "depth2_minimax"),
    ("bitboard_ab_fast", "win_seek_block"),
    ("mcts_fast", "random"),
    ("bitboard_ab_fast", "random"),
    ("depth2_minimax", "win_seek_block"),
    ("depth2_minimax", "random"),
    ("shallow_minimax", "bitboard_ab_fast"),
]

lb = Leaderboard()
for a, b in matchups:
    tourney = Tournament(registry=reg, games_per_pair=10)
    r = tourney.run_pair(a, b)
    lb.add_match(r)
    print(f"  {a} vs {b}: {r.summary()} [{time.time()-t0:.0f}s]")

print(f"\nTotal time: {time.time()-t0:.1f}s")
print(f"\n{'Bot':<20} {'W':>5} {'L':>5} {'D':>5} {'GP':>5} {'Win%':>7}")
print("-" * 48)
for name, stats in lb.ranked():
    print(f"{name:<20} {stats.wins:>5} {stats.losses:>5} {stats.draws:>5} {stats.games_played:>5} {stats.win_pct:>6.1f}%")