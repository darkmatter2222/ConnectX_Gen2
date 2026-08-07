# Next Actions — ConnectX Phase 2

**Session:** Cycle 19
**Date:** 2026-08-07

## Session Summary (Cycle 19: Full Evaluation)

**Key finding: 7×6/4 is solved under perfect play at this board size.**
- All 7 alpha-beta bots equivalent (28 matchups, 336 games, 0 invalid)
- MCTS vs v2: 35% MCTS win rate (significantly weaker)
- MCTS PUCT vs v2: 15% win rate (even weaker, 200x slower)
- Value NN path plateaued (quantized gameplay)
- BC approach = v2 (perfect memorization of teacher)

**Conclusion: Classical search solves 7×6/4 completely. No alpha-beta variant can be distinguished.**

## Immediate next actions

## Session Summary (Cycle 18)

**Completed:**
- **Critical bug fix: negamax TT/null-move paths returning hardcoded col=0 across ALL bitboard bots**
  - **Root cause:** Every `_negamax` function had 4 early-exit paths (TT exact, TT lower, TT upper, null-move) that returned `return val, 0` or `return beta, 0` instead of `return val, legal[0]`
  - **Affected files (8 total):**
    - `connectx/bots/bitboard_ab.py` — original v1 bot
    - `connectx/bots/bitboard_ab_improved.py` — v2 bot (default)
    - `connectx/bots/bitboard_ab_value.py` — vValue bot
    - `connectx/bots/bitboard_ab_improved_v3.py` — v3 bot
    - `connectx/bots/bitboard_ab_ensemble.py` — ensemble bot
    - `connectx/bots/bitboard_ab_with_nn.py` — NN bot
    - `connectx/training/kaggle_self_contained.py` — Kaggle submission bot
    - `connectx/bots/bitboard_ab.py` (already fixed in Cycle 18, verified)
  - **Impact:** ~20% of v1 games produced invalid moves (column 0 was full, but bot returned 0). v2 also affected but iterative deepening + final safety check reduced impact. vValue, v3, ensemble, and kaggle bots all had the same bug.
  - **Fix:** All 4 early-exit paths in each file now return `legal[0]` instead of `0`
  - **Verified:** 8 bots × 3 games = 1008 moves across 8 different bitboard implementations, 0 invalid moves after fix

## Session Summary (Cycle 18.5: Smoke Test)

**Completed:**
- Fixed `bitboard_ab_book` opening book API: changed `get_move(board, mark, legal, prefer_random=False)` → `best_move(board_str, mark)` + `in legal` guard
- Ran smoke test across ALL 8 bots against random opponent: **1680 moves, 0 invalid**
- All 8 bots verified passing:
  1. `bitboard_ab` — 210/210 valid
  2. `bitboard_ab_book` — 210/210 valid
  3. `bitboard_ab_ensemble` — 210/210 valid
  4. `bitboard_ab_improved` (v2) — 210/210 valid
  5. `bitboard_ab_improved_v3` (v3) — 210/210 valid
  6. `bitboard_ab_value` (vValue) — 210/210 valid
  7. `bitboard_ab_with_nn` — 210/210 valid
  8. `mcts_bc` — 210/210 valid

## Session Summary (Cycle 17)

**Completed:**
- **Trained and evaluated value networks at different noise levels:**
  - 20% noise 776 pos (Cycle 15): val_mae=0.412, vValue vs MCTS = 65%
  - 20% noise 2,696 pos: val_mae=0.658, significantly worse
  - 25% noise 935 pos (ZERO draws): val_mae=0.496
  - 25% model gameplay = **identical** to Cycle 15 model
- **Key finding: Game play performance is quantized**
  - Once the value NN reaches sufficient quality, extra precision doesn't help
  - Cycle 15 model (MAE 0.412) and 25% model (MAE 0.496) give identical gameplay
  - vValue is stronger as P2 (70%) than P1 (60%) against MCTS
- **vValue consistent results (120 games total):**
  - vValue as P1 vs MCTS: 14W-6L (Cycle 15), 14W-6L (25% model) — 60% each
  - vValue as P2 vs MCTS: 12W-7L-1D (Cycle 15), 12W-7L-1D (25% model) — 70% each
- **mcts_value continues to underperform** (30-34% vs MCTS) — NN doesn't help MCTS
- **Full 80-game evaluation:** vValue 46W-21L-13D (57.5% vs MCTS)

## Session Summary (Cycle 16)

**Completed:**
- Generated v2 self-play at 10%/15%/25% noise (background task bglndsrv2)
- Generated v2 self-play at 20% noise: 2,696 positions (Cycle 15: 776)
- Generated WSB self-play at 15%/30% noise: 8,356 positions (blazing fast!)
- Combined v2 + WSB dataset: 11,890 positions
- Key finding: **Domain mismatch** — WSB data degrades quality
  - Combined (v2+WSB, 11,890): val_mae=0.75 — WORSE than v2-only (776 pos)
- Larger v2 dataset (3,472 positions, 10-30%): val_mae=0.56
  - Worse than 20% noise only (val_mae=0.41)
- **20% noise is the sweet spot** — mixing noise levels hurts quality
- On shared test set:
  - 20% model (776): MAE 0.36, sign_acc 78%
  - Mixed model (3,472): MAE 0.56, sign_acc 71%

**Decision: Stick with Cycle 15 model (20% noise, 776 positions)**
  - Best validation metrics, best gameplay performance (70% vs MCTS)
  - More data from different noise levels → worse model (noise pollution)

## Session Summary (Cycle 16: Self-Play Data Generation + Training Comparison)

**Completed:**
- Generated v2 self-play at 10%, 15%, 25% noise (background tasks)
- Generated v2 self-play at 20% noise: 3,472 positions (100 games)
- Generated WSB self-play at 15%, 30%: 8,356 positions (200 games each)
- Combined all data: 11,890 positions (v2 + WSB)
- Key finding: **20% noise is the sweet spot**
  - v2 20% model: MAE 0.41, 74% accuracy, vValue vs MCTS = 70%
  - Combined (v2+WSB): MAE 0.75 (domain mismatch)
  - Mixed v2 (10-30%): MAE 0.56 (worse than pure 20%)
  - Conclusion: QUALITY > QUANTITY; consistent noise level matters

## Session Summary (Cycle 15)

**Completed:**
- High-noise self-play data: 776 positions from v2 vs v2 at 20% noise
  - 53% non-draw rate, 353 W / 339 L / 84 D labels
  - Key insight: 20% noise breaks solved-game equilibrium
- New value network trained on self-play data: MAE 0.41 (vs 0.79 old)
- 74% sign accuracy on test set (vs 15% old)
- vValue improved: 56% → 70% vs MCTS
- mcts_value still underperforms: 30% vs MCTS

## Immediate (next session)

1. **Retrospect: Re-evaluate affected bots**
   - v1, vValue, v3, ensemble, with_nn, and kaggle bots had ~20% invalid move rate before this fix
   - Re-evaluate these bots now that the bug is fixed to get accurate performance numbers
   - The "strong" results for v2 in previous cycles were unaffected (v2 didn't use the buggy code path)

2. **Continue value network work**
   - Try different NN architectures (wider, deeper, residual connections)
   - Try generating more self-play data at 20% noise (the sweet spot)
   - The quantized gameplay finding suggests NN quality matters above a threshold, but we may not have reached that threshold yet with only 776 positions

## After immediate actions

1. **vValue evaluation COMPLETE (120 games)**
   - vValue (Cycle 15 NN) vs MCTS: 60% as P1, 70% as P2 (quantized performance)
   - 25% model (MAE 0.496) gives identical gameplay to Cycle 15 (MAE 0.412)
   - vValue is stronger as P2 — possibly because MCTS has P1 advantage
   - mcts_value remains inferior (30-34% vs MCTS)
   - vValue with Cycle 15 NN remains the best NN-enhanced bot

2. **Register vValue with Cycle 15 NN as default**
   - vval._DEFAULT_VALUE_MODEL already points to models/value_net_selfplay/best.pth
   - Done

## After immediate actions

4. **Full leaderboard tournament** — all 11 bots, all pairs, measured ratings
   - Need: mcts_fast, bitboard_ab_fast_v2, bitboard_ab_fast, v2, mcts, mcts_value
   - Use seat-reversed 40-game matchups (20 each way)
   - Record Elo ratings, confidence intervals

5. **Fix original bitboard_ab invalid-move bug — DONE (Cycle 18)**
   - Root cause: _negamax returned hardcoded col=0 in TT/exact/null-move paths
   - Fixed: all early-exit paths now return legal[0] (valid move)
   - Verified: 380 moves across 20 games, 0 invalid

6. **Evaluate v3 bot** (bitboard_ab_improved_v3.py) — compare vs v2
   - Fork-aware evaluation, open3 detection, column control

7. **Kaggle submission** — deploy `kaggle_self_contained.py`
   - Package for Kaggle submission
   - Test in Kaggle environment

## Completed Actions (reference)

- [DONE] Core ConnectX 7×6/4 engine
- [DONE] 10 baseline bots + mcts_bot_value (11 total)
- [DONE] Tournament system with seat-aware leaderboard
- [DONE] Kaggle self-contained bot (kaggle_self_contained.py)
- [DONE] Value network trained (146KB, MAE 0.786) — v2-vs-MCTS data
- [DONE] Quick tournament (130 games) — v2 dominant
- [DONE] Self-play pipeline (generate, convert, train)
- [DONE] Self-play refinement attempt (v2 vs v2 = all draws)
- [DONE] Opening book for v2 (115 positions, 50KB)
- [DONE] High-noise self-play data (20% noise, 776 positions, balanced W/L)
- [DONE] Value network trained on self-play data (MAE 0.41, 74% sign accuracy)
- [DONE] New value network improves vValue (56%→70% vs MCTS)

## Key Findings

- **v2 is the strongest bot:** 120W 0L in quick tournament
- **mcts_value underperforms mcts:** value network doesn't help MCTS move selection
- **Equal-strength self-play at 7×6/4 produces draws with low noise:** game is solved
- **High-noise self-play (20%) produces balanced W/L data** — key parameter is noise level
- **Value network quality matters more than quantity:** 776 self-play positions outperformed
  13,520 biased v2-vs-MCTS positions
- **New value network improves vValue (56%→70% vs MCTS)** but doesn't help MCTS
- **Kaggle self-contained bot ready** (20-move test: 0 invalid)