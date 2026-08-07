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

## Immediate (next session)

1. **Combined dataset training — IN PROGRESS (Cycle 16)**
   - 11,890 positions from v2 (15%/20%/25% noise) + WSB (15%/30% noise)
   - Balanced: 5,863 W / 5,565 L / 462 D
   - Training on combined data now running

2. **Evaluate value model on combined data**
   - Compare vs Cycle 15 model (776 positions, 74% sign accuracy)
   - Expected: improved accuracy with 11,890 positions
   - Evaluate vValue and mcts_value with new model

3. **Register vValue with new NN in bot registry**
   - Currently old NN is default for vValue
   - New NN should be the default

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