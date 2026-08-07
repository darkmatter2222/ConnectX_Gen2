# Autonomous State — ConnectX Phase 2

**Session:** Cycle 4
**Date:** 2026-08-06

## What Was Last Completed

1. Repository audit, phase 2 control documents, Python env setup
2. **Core ConnectX 7×6/4 engine** with gravity, win detection, terminal detection, replay
3. **8 bots built and registered:**
   - `random_bot` — uniform random
   - `win_seek_block_bot` — priority tactical (win > block > center)
   - `shallow_minimax_bot` / `depth2_minimax_bot` — negamax depth 2/3
   - `bitboard_ab_bot` / `bitboard_ab_bot_fast` — negamax with TT, null-move, adaptive depth
   - `mcts_bot` / `mcts_bot_fast` — PUCT MCTS with tactical playouts
4. **Tournament system** with seat-aware win counting and leaderboard
5. **Comprehensive test suite:** 72/72 passing
6. **MCTS tactical rollout gravity bug fixed** — all drop() calls wrapped, valid_moves rechecked, empty moves handled

## Latest Tournament (10 games/pair, fast variants)

| Bot | W | L | D | Win% |
|-----|---|---|---|------|
| win_seek_block | 50 | 10 | 0 | 83.3% |
| bitboard_ab_fast | 76 | 24 | 0 | 76.0% |
| random | 38 | 20 | 2 | 63.3% |
| mcts_fast | 27 | 51 | 2 | 33.8% |
| depth2_minimax | 7 | 73 | 0 | 8.8% |
| shallow_minimax | 0 | 20 | 0 | 0.0% |

### Key pairwise results
- win_seek_block: **still dominant** (50/60) — beats mcts 20-0, ties bitboard 10-10
- bitboard_ab_fast: **major improvement** (30% -> 76% W) — beats mcts_fast 12-8, depth2 20-0
- mcts_fast: **dropped** (50% -> 34%) — bitboard's deeper search now dominates MCTS
- bitboard_ab vs win_seek_block: **10-10** — first time bitboard ties win_seek_block

## What Is Active

**Deeper search is the key insight.** Bitboard jumped from 30% to 76% by increasing search depth (5->7 for fast, 6-10+ for time-aware). Evaluation with fork/threat detection works well at depth 7+. Next: make bitboard_ab the primary contender, improve timing.

## What Failed

- Tournament win-counting bug (fixed)
- Research-only accumulation (fixed by building actual bots)
- MCTS tactical rollout crashes on full columns (fixed)
- MCTS v2 experiments: no improvement over v1 (abandoned)

## Next Highest-Value Unblocked Actions

1. **Improve bitboard_ab timing** — reduce evaluation cost, use iterative deepening
2. **Challenge win_seek_block** — increase search depth, add killer moves
3. **Profile timing** — ensure all bots meet the 1.75s strict promotion profile
4. **Run larger statistical tournaments** — 50+ games per pair
5. **Install PyTorch** — prepare for neural network bots
6. **Build opening book** for bitboard or MCTS