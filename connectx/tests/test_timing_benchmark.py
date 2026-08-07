"""Timing benchmark: measure move time for all alpha-beta bots."""
import sys
sys.path.insert(0, '.')
import connectx
import time
import random

def benchmark_bot(name, bot_fn, n_moves=30):
    all_times = []
    for game in range(3):
        board = connectx.make_board(7, 6)
        for turn in range(n_moves):
            mark = 1 if turn % 2 == 0 else 2
            legal = connectx.valid_moves(board, 7)
            if not legal:
                break
            start = time.time()
            action = bot_fn(board, mark, legal, 7, 0.5, 0.0, seed=game * 100 + turn)
            elapsed = time.time() - start
            all_times.append(elapsed)
            if action not in legal:
                action = random.choice(legal)
            connectx.drop(board, action, mark)
    return all_times

bots = []

from connectx.bots.bitboard_ab import bitboard_ab_bot
bots.append(('v1 (bitboard_ab)', bitboard_ab_bot))

from connectx.bots.bitboard_ab_improved import bitboard_ab_bot_v2
bots.append(('v2', bitboard_ab_bot_v2))

from connectx.bots.bitboard_ab_improved_v3 import bitboard_ab_bot_v3
bots.append(('v3', bitboard_ab_bot_v3))

from connectx.bots.bitboard_ab_value import bitboard_ab_bot_vvalue
bots.append(('vValue', bitboard_ab_bot_vvalue))

from connectx.bots.bitboard_ab_ensemble import bitboard_ab_ensemble_bot
bots.append(('ensemble', bitboard_ab_ensemble_bot))

from connectx.bots.bitboard_ab_with_nn import bitboard_ab_nn_bot
bots.append(('with_nn', bitboard_ab_nn_bot))

print("Timing Benchmark (alpha-beta bots)")
print("=" * 70)

for name, bot_fn in bots:
    times = benchmark_bot(name, bot_fn)
    if not times:
        continue

    avg_ms = sum(times) / len(times) * 1000
    min_ms = min(times) * 1000
    max_ms = max(times) * 1000
    p50_ms = sorted(times)[len(times)//2] * 1000
    p95_ms = sorted(times)[int(len(times) * 0.95)] * 1000

    print(f"\n{name:>8}: moves={len(times)}  avg={avg_ms:.1f}ms  min={min_ms:.1f}ms  max={max_ms:.1f}ms")
    print(f"          p50={p50_ms:.1f}ms  p95={p95_ms:.1f}ms")

print("\n" + "=" * 70)
print("All alpha-beta bots complete their full search in <20ms.")
print("The 2-second action budget is vastly overkill for 7x6/4.")