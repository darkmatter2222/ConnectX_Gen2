# Next Actions — ConnectX Phase 2

**Session:** Cycle 16
**Date:** 2026-08-07

## Session Summary (Cycle 15)

**Completed:**
- High-noise self-play data: 776 positions from v2 vs v2 at 20% noise
  - 53% non-draw rate, 353 W / 339 L / 84 D labels
  - Key insight: 20% noise breaks solved-game equilibrium
- New value network trained on self-play data: MAE 0.41 (vs 0.79 old)
- 74% sign accuracy on test set (vs 15% old)
- vValue improved: 56% → 70% vs MCTS
- mcts_value still underperforms: 30% vs MCTS

**Immediate (next session)

## Immediate (next session)

1. **Build opening book** for v2
   - Pre-compute optimal moves for first ~20 ply using v2 search
   - Already takes ~61ms for empty board, book lookup is instant
   - Useful for Kaggle submission (reduces cold-start latency)
   - Format: dict mapping (board_state_string) → best_col

2. **Neural network with mixed-strength self-play**
   - Previous equal-strength self-play (v2 vs v2) produced all draws → useless labels
   - **New approach:** v2 vs MCTS with varying noise levels for both players
   - This produces W/L/D labels from both perspectives
   - Pipeline already built: selfplay_generate.py → CSV → NPZ → train_value_net
   - Expected: value network learns positional advantage patterns

3. **Evaluate value-enhanced v2 vs vanilla v2**
   - Test whether the new value network (trained on mixed data) can improve v2
   - If MAE drops below 0.5, the network may be useful for alpha-beta leaf evaluation
   - Re-evaluate vValue (v2 + NN guidance) with new model

## After immediate actions

4. **Full leaderboard tournament** — all 11 bots, all pairs, measured ratings
   - Need: mcts_fast, bitboard_ab_fast_v2, bitboard_ab_fast, v2, mcts, mcts_value
   - Use seat-reversed 40-game matchups (20 each way)
   - Record Elo ratings, confidence intervals

5. **Fix original bitboard_ab invalid-move bug** (~20% of games)
   - Root cause: board copy not preserved after search
   - Fix: use board copy approach
   - Or: fix valid_moves to check bottom row instead of top row

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