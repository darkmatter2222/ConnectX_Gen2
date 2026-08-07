# Autonomous State — ConnectX Phase 2

**Session:** Cycle 7
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
5. **Comprehensive test suite:** 78/78 passing (6 new v2 tests)
6. **MCTS tactical rollout gravity bug fixed** — all drop() calls wrapped, valid_moves rechecked, empty moves handled

## Cycle 7: v2 Completely Dominates win_seek_block

### v2 Improvements:
- Killer move heuristic (beta-cutoff memory per depth)
- History heuristic (score for moves that cause cuts across depths)
- Iterative deepening (depth 1..12, always return best found)
- Null-move pruning (skip a turn when depth >= 3)
- Improved move ordering (killers → wins → blocks → threats → center → history)
- Board safety: validate returned move is legal, fallback to first legal

### v2 vs win_seek_block (100 games, seat-reversed):
- **v2 wins: 100, WSB wins: 0, Draws: 0**
- Previously: win_seek_block was dominant (83% W)

### v2 vs random: ~84% win rate as first player
### v2 timing: ~300ms per move (vs ~2ms for original bitboard_ab)

## Previous Tournament (Cycle 5, 10 games/pair, fast variants)

| Bot | W | L | D | Win% |
|-----|---|---|---|------|
| win_seek_block | 50 | 10 | 0 | 83.3% |
| bitboard_ab_fast | 76 | 24 | 0 | 76.0% |
| random | 38 | 20 | 2 | 63.3% |
| mcts_fast | 27 | 51 | 2 | 33.8% |
| depth2_minimax | 7 | 73 | 0 | 8.8% |
| shallow_minimax | 0 | 20 | 0 | 0.0% |

### Key pairwise results (ignoring random)
- win_seek_block beats ALL opponents (83% W) — dominant tactical player
- **bitboard_ab_fast major improvement**: 30% -> 76% W (deeper search: depth 5->7 fast, 6-10+ time-aware)
- **bitboard_ab_fast ties win_seek_block 10-10** — first time bitboard competes!
- bitboard_ab_fast beats mcts_fast 12-8 — deeper negamax beats shallower MCTS
- bitboard_ab_fast crushes depth2_minimax 20-0
- mcts_fast beats depth2_minimax 17-3

## What Is Active

**Deeper search + move ordering = overwhelming strength.** v2 beat win_seek_block 100% by combining iterative deepening, killer moves, history heuristic, and null-move pruning.

## What Failed

- Tournament win-counting bug (fixed)
- Research-only accumulation (fixed by building actual bots)
- MCTS tactical rollout crashes on full columns (fixed)
- MCTS v2 experiments: no improvement over v1 (abandoned)
- **Original bitboard_ab returns invalid moves (~20% of games)** — known bug, not fixed yet

## Next Highest-Value Unblocked Actions

1. **Optimize v2 evaluation** — reduce per-node cost while maintaining depth
2. **Run full tournament** with v2 against ALL bots
3. **Profile timing** — ensure v2 meets 1.75s strict profile
4. **Install PyTorch** — prepare for neural network bots
5. **Build opening book** for bitboard or MCTS
6. **Fix original bitboard_ab invalid-move bug** — use board copy approach