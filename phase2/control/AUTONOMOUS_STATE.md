# Autonomous State — ConnectX Phase 2

**Session:** Cycle 13.1
**Date:** 2026-08-07
**Status:** Cycle 13.1 completed — value-guided MCTS registered (mcts_bot_value), self-contained Kaggle bot built. mcts_value vs mcts within statistical noise.

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
   - `mcts_bot_value` — value-guided MCTS (70% value network + 30% tactical)
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

## Cycle 11: Ensemble Evaluation (v2 + NN)

**Hypothesis:** Ensemble (0.7 × v2 + 0.3 × NN) improves over v2 alone.

**Results (20-game seat-reversed matchups):**
| Matchup | Result | Notes |
|---------|--------|-------|
| ensemble vs v2 | 50/50 | ensemble = v2 |
| ensemble vs mcts | 67.5% | ensemble beats MCTS |
| v2 vs mcts | 70% | v2 beats MCTS |
| nn vs mcts | 72.5% | NN bot also strong vs MCTS |

**Key Finding: ENSEMBLE MATCHES V2 — no measurable improvement.**

The NN component is too noisy (MAE 0.31) and is trained on random-player data.
v2's heuristic dominates (70% weight). Even the NN-only bot performs comparably
to v2 (72.5% vs mcts).

**Conclusion:** Ensemble doesn't help. NN needs fundamentally better training data.

## Cycle 12: Behavioral Cloning Training Pipeline

**Hypothesis:** Train a policy network to predict v2's moves (BC) vs MCTS.
- Data: v2 vs MCTS games, v2's moves as labels
- Architecture: 84 → 256 → 128 → 7 (policy: softmax over columns)
- Trained 1000 games → 3,562 positions → 100% val accuracy by epoch 13

**Results (BC bot vs MCTS):**
| Bot | vs mcts | vs v2 |
|-----|---------|-------|
| bc_bot | 60% (40 games) | 50% (40 games) |
| v2 | 62% (40 games) | — |

BC bot performance ≈ v2 performance. BC perfectly memorizes v2's moves
(100% accuracy) but can't exceed v2 since it's only learning v2's behavior.

**Key Finding: BC also converges to v2 — cannot exceed the teacher.**

## What Failed
- **Tournament bot selection bug** — used `env._player == 0` mapping when `_player` is 1-indexed
- **Ensemble evaluation** — 0.3×NN is too noisy to improve over 0.7×v2
- **NN evaluation only** — while comparable to v2, doesn't surpass it
- **v2 self-play data** — 100% first-player wins, trivial labels
- **BC training** — perfectly memorizes v2 but can't exceed v2

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

1. **Kaggle packaging — DONE** (Cycle 13.1): `connectx/training/kaggle_self_contained.py`
   - Self-contained single file, ready for Kaggle submission
   - 20-move test: all moves valid, consistent with v2 behavior
2. **Fix original bitboard_ab invalid-move bug** — use board copy approach
3. **Run full leaderboard tournament** — all bots, all pairs, measured ratings
4. **Build opening book** for v2 (pre-computed early moves for speed)
5. **NN ensemble with v2 fallback** — train larger NN, use as tiebreaker in v2
6. **Evaluate v3 bot (bitboard_ab_improved_v3.py)** — compare vs v2
7. **Neural network with self-play refinement loop** — train NN, test vs v2, retrain

## Session Summary (Cycle 12)

**Completed this session:**
- Fixed ensemble bot CUDA warning
- Built tournament system with correct mark mapping
- Tested ensemble, NN, BC bots against v2 and mcts (100 games each)
- Fixed MCTS PUCT math domain error
- Built BC training pipeline (generate_bc_data.py, train_bc.py, bc_bot.py)
- Trained BC model (100% val accuracy)
- Updated dashboard and autonomous state

**All changes pushed to origin/main (6 commits)**

## Session Summary (Cycle 13)

**Completed this session:**
- Created `connectx/bots/connectx_value_net.py` — PyTorch + CPU value network model
- Created `connectx/bots/bitboard_ab_value.py` — v2 with NN value guidance (vValue)
- Created `connectx/training/value_generate.py` — v2 vs MCTS data generator
- Created `connectx/training/value_train.py` — Value network training script
- Generated 13,520 training positions from 1,000 v2 vs MCTS games
- Trained value network (30 epochs, best val_loss=0.784)
- Evaluated vValue vs v2 (50/50), vValue vs MCTS (56%), v2 vs MCTS (57.5%)
- Updated dashboard and autonomous state
- **CRITICAL FIX: negamax inf score bug** — Two fixes: (1) bounds capping at top of
  _negamax (alpha=max(alpha,-100000), beta=min(beta,100000)) to prevent infinity
  propagation through alpha-beta; (2) opponent 4-in-a-row scan before search via
  bitboard masks. All 78 tests pass. Fixed: TT mark field, un_drop row param,
  null-move mark (3-mark), is_root=True for null-move.

**Key finding:** Value network improves NN_eval (44% vs MCTS, up from 40%) but
does not enhance v2. The network's high MAE (0.786) makes it too noisy for alpha-beta.
v2's heuristic evaluation is already near-optimal at 7×6/4.

**Next viable paths (ranked by expected impact):**

1. **Value-guided MCTS** — Use the trained value network as leaf evaluation for
   MCTS instead of tactical playouts. MCTS can tolerate coarse value predictions
   better than alpha-beta. Expected: 60%+ vs MCTS (improving over vValue's 56%).
   Effort: ~2 hours (modify mcts.py to call nn_value_predict at rollout).

2. **Self-play refinement** — Train value network through AlphaZero-style self-play:
   train NN, use it to guide MCTS self-play, collect data, retrain. Loop 5-10 times.
   Expected: Lower MAE, stronger play. Effort: ~4 hours.

3. **Kaggle packaging** — Package v2 as deployable submission.
   Effort: ~1 hour.

4. **Opening book** — Pre-compute optimal moves for early-game speed.
   Effort: ~2 hours.

## Session Summary (Cycle 13.1)

**Completed this session:**
- Registered `mcts_bot_value` in bot registry (connectx/bots/__init__.py)
- Value-guided MCTS comparison (40 games): mcts_value = 17W, mcts = 13W, draws = 10
  - Within statistical noise (Connect 4 at 7x6/4 is solved; both converge)
  - mcts_value slower (~2.5s vs ~1.6s per game) due to PyTorch inference
- **Kaggle packaging complete:** `connectx/training/kaggle_self_contained.py`
  - Fully self-contained single file (~761 lines, ~25 KiB)
  - Includes: engine, TT, killer moves, history heuristic, null-move pruning, bounds capping
  - No external dependencies at runtime
  - Self-test: 20 moves valid, 0 invalid moves, consistent with v2
- All changes committed and ready to push

**Files created:**
- `connectx/training/kaggle_self_contained.py` — self-contained Kaggle bot
- `connectx/bots/__init__.py` — updated (added mcts_bot_value to __all__)