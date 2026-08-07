# Next Actions — ConnectX Phase 2

**Session:** Cycle 13.1
**Date:** 2026-08-07

## Immediate (next session)

1. **Neural network with self-play refinement loop** (AlphaZero-style)
   - Current value network trained on v2-vs-MCTS data, but value-guided MCTS underperforms vanilla MCTS (34.5 vs 43 pts)
   - Self-play data will be balanced (50/50 seats) — unlike v2-vs-MCTS which has first-player bias
   - Steps:
     a. Build MCTS with value-network-guided playouts (already have mcts_bot_value)
     b. Run v2-vs-value-MCTS self-play to generate balanced data
     c. Retrain value network on self-play data
     d. Evaluate new value-guided MCTS
     e. Iterate 5-10 times
   - Expected: Lower MAE, meaningful MCTS improvement, possible value-enhanced v2

2. **Build opening book** for v2
   - Pre-compute optimal moves for first ~20 ply
   - Could speed up early-game moves (already ~61ms, but book lookup is instant)
   - Useful for Kaggle submission (reduces cold-start latency)

## After immediate actions

3. **Full leaderboard tournament** — all 11 bots, all pairs, measured ratings
   - Need: mcts_fast, bitboard_ab_fast_v2, bitboard_ab_fast, v2, mcts, mcts_value
   - Use seat-reversed 40-game matchups (20 each way)
   - Record Elo ratings, confidence intervals

4. **Fix original bitboard_ab invalid-move bug** (~20% of games)
   - Root cause: board copy not preserved after search
   - Fix: use board copy approach

5. **Evaluate v3 bot** (bitboard_ab_improved_v3.py) — compare vs v2
   - Fork-aware evaluation, open3 detection, column control

6. **Adversarial position suite** — design tactical traps and edge cases
   - Fork traps, anti-forks, forced-defense positions
   - Test all bots against curated positions

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

## Blocked/Deferred

- **v2 self-play data**: 100% first-player wins → useless labels
- **Knowledge distillation from v2**: matches v2 but cannot exceed
- **Behavioral cloning**: perfectly memorizes v2, cannot exceed
- **Value network on v2-vs-MCTS data**: high MAE, underperforms vanilla MCTS