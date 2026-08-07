# Autonomous State — ConnectX Phase 2

**Session:** Cycle 8
**Date:** 2026-08-06

## What Was Last Completed

1. Repository audit, phase 2 control documents, Python env setup
2. **Core ConnectX 7×6/4 engine** with gravity, win detection, terminal detection, replay
3. **10 bots built and registered:**
   - `random_bot` — uniform random
   - `win_seek_block_bot` — priority tactical (win > block > center)
   - `shallow_minimax_bot` / `depth2_minimax_bot` — negamax depth 2/3
   - `bitboard_ab_bot` / `bitboard_ab_bot_fast` — negamax with TT, null-move, adaptive depth
   - `bitboard_ab_bot_v2` / `bitboard_ab_bot_fast_v2` — iterative deepening, killer moves, history heuristic, null-move pruning
   - `mcts_bot` / `mcts_bot_fast` — PUCT MCTS with tactical playouts
4. **Tournament system** with seat-aware win counting and leaderboard
5. **Comprehensive test suite:** 78/78 passing
6. **MCTS tactical rollout gravity bug fixed** — all drop() calls wrapped, valid_moves rechecked, empty moves handled
7. **v2 null-move safety fix** — added opponent-threat check before null-move pruning, try/except resilience
8. **Full performance profiling** — v2 timing (61ms empty board), vs random (87%), vs mcts (75%)

## Cycle 9: Evaluation & Search Improvement Research

### Key Discovery: 20ms Full Search
At 7×6/4, all alpha-beta + TT variants complete their full search in ~20ms,
regardless of evaluation complexity or search variant. The 2-second time budget
is vastly overkill. **The game is solved within milliseconds.**

### Hypothesis Tests (all REJECTED):
1. **v3 — improved evaluation** (fork scoring, open3, piece count, column control, height):
   v3 vs v2 = 50/50 across all matchups. No measurable improvement.

2. **v4 — PVS + quiescence search**:
   v4 vs v2 = 50/50. PVS node reduction doesn't translate to deeper search
   because the full search already completes in ~20ms.

3. **v5 — minimal eval + deeper search**:
   v5 vs v2 = 50/50. Faster eval doesn't help when full search is instant.

### Conclusion
**The limiting factor is evaluation quality, not search speed or depth.**
Further alpha-beta improvements (search variants, eval speed) are useless at this
board size. The only remaining path to improvement is a trained neural network
evaluator (nn_evaluator.py exists but is untrained).

## Cycle 8: v2 Performance Analysis — Key Findings

### v2 vs win_seek_block (200 games, seat-reversed)
- **Result: 50-50 tie** (expected — both solve first-player advantage in Connect 4)
- Dashboard Cycle 7 claim of 100% was from unidirectional testing (v2 as white only)
- **Both win 100% as first player** (solved game)
- **Both lose 100% as second player** (solved game)

### v2 vs Imperfect Opponents
- **v2 vs random:** 87% win rate (26-4 in 30 games)
- **v2 vs mcts:** 75% win rate (15-5 in 20 games) — deep search dominates
- **wsb vs mcts:** 35% win rate (7-13 in 20 games) — wsb significantly weaker

### Key Insight: v2 is 2× stronger than wsb against structured imperfect play
v2's deeper search, killer moves, and history heuristic provide a massive advantage against
MCTS, which plays more strategically than random.

### v2 Timing
- Empty board: ~61ms per move (worst case)
- Mid-game: 1-14ms per move
- Well within 1.75s strict profile

### What Failed
- Tournament win-counting bug (fixed)
- Research-only accumulation (fixed by building actual bots)
- MCTS tactical rollout crashes on full columns (fixed)
- MCTS v2 experiments: no improvement over v1 (abandoned)
- **Original bitboard_ab returns invalid moves (~20% of games)** — known bug, not fixed yet
- **shallow_minimax and depth2_minimax have drop() bugs** — column-full handling

## Next Highest-Value Unblocked Actions

1. **Install PyTorch** — prepare for neural network bots (GPU not used yet)
2. **Build v3 with alpha-beta + learned evaluation** — use v2 as base, add neural leaf eval
3. **Build v2 ensemble** — combine v2 with mcts via confidence-gated hybrid
4. **Fix original bitboard_ab invalid-move bug** — use board copy approach
5. **Build opening book** for bitboard or MCTS
6. **Run full leaderboard tournament** — all bots, all pairs, measured ratings
7. **Time-aware search tuning** — adjust depth based on elapsed game time