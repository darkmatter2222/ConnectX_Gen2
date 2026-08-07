# Next Actions — ConnectX Phase 2

**Session:** Cycle 13.2
**Date:** 2026-08-07

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
- [DONE] Value network trained (146KB, MAE 0.786)
- [DONE] Quick tournament (130 games) — v2 dominant
- [DONE] Self-play pipeline (generate, convert, train)
- [DONE] Self-play refinement attempt (v2 vs v2 = all draws)

## Key Findings

- **v2 is the strongest bot:** 120W 0L in quick tournament
- **mcts_value underperforms mcts:** value network too coarse for MCTS
- **Equal-strength self-play produces draws at 7×6/4:** game is solved
- **Need mixed-strength self-play** for useful W/L value network labels
- **Kaggle self-contained bot ready** (20-move test: 0 invalid)