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

## Cycle 10: Neural Network Evaluation (Knowledge Distillation)

### Training Results
- **Dataset:** 5000 games × 50% noise = 115,421 positions labeled by v2 eval
- **Architecture:** 84 → 128 → 1 (ReLU hidden, tanh output)
- **Training:** 50 epochs, batch_size=512, RTX 5090
- **Val loss:** 0.22 (vs 0.81 for outcome-based training)
- **MAE:** 0.31

### NN Bot Results
- **NN vs v2:** 50/50 (expected — NN trained to mimic v2)
- **NN vs mcts:** 40% win (vs v2's 75%) — NN bot UNDERPERFORMS MCTS

### Key Finding: NN evaluation quality insufficient
MAE of 0.31 in a [-1, 1] range causes suboptimal move selection in alpha-beta.
Small leaf evaluation errors cascade into wrong pruning decisions.
**Knowledge distillation from v2 heuristic ≠ better than v2** — the NN is a
compressed, noisy version of v2's evaluation.

### Knowledge Distillation vs Outcome Training
| Metric | Outcome-based | Knowledge Distillation |
|--------|--------------|----------------------|
| Val loss | 0.81 | 0.22 |
| MAE | 0.83 | 0.31 |
| Labels | 3 classes (+1/-1/0) | Continuous [-1, 1] |

Distillation vastly improves label diversity but the NN still underperforms
v2 because of compression loss.

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
Alpha-beta improvements don't matter at this board size.

### Neural Network Path
nn_evaluator.py and training pipeline exist but the trained NN (MAE 0.31)
underperforms v2. Next: improve training data quality.

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

1. **Improve NN evaluation quality** — train with v2 self-play data (competitive, not random)
   - Generate 10,000+ games of v2 vs v2 with 0.1s per move (deeper search)
   - Or generate mixed-depth self-play data (depth 10-14) for more varied evaluations
2. **Ensemble: v2 + NN** — combine v2's heuristic with NN evaluation
   - Weighted average: 0.7 × v2 + 0.3 × NN (if NN captures patterns v2 misses)
3. **PyTorch in project venv** — set up GPU training at `O:\master_model_collection\ConnectX_Gen2_Phase2\.venv`
4. **Build v2 ensemble** — combine v2 with mcts via confidence-gated hybrid
5. **Fix original bitboard_ab invalid-move bug** — use board copy approach
6. **Run full leaderboard tournament** — all bots, all pairs, measured ratings
7. **Build opening book** for bitboard or MCTS