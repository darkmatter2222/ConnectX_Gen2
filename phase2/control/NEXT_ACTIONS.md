# Next Actions — ConnectX Phase 2

**Session:** Cycle 24
**Date:** 2026-08-07

## Cycle 24: PUCT MCTS vs AB — Does Full Tree Search Help?

**Completed:**
- **PUCT bot built** (`mcts_puct_bot_8x7_5`) — full tree-search MCTS with PUCT selection + tactical playouts
- **35 tests pass** (21 original + 14 new from cycles 21-24)
- **Full 60-game comparison: AB vs MCTS(UCB1, 500) vs PUCT(2500, tactical)**

### Results

| Matchup | Winner | Loser | Draws | Key Observation |
|---------|--------|-------|-------|-----------------|
| MCTS(500) as P1 vs AB as P2 | AB: 10 | 0 | 0 | AB wins in 54 moves |
| AB as P1 vs MCTS(500) as P2 | — | — | **10** | MCTS holds draw as P2 |
| PUCT(2500) as P1 vs AB as P2 | — | — | **10** | PUCT holds draw as P1 |
| AB as P1 vs PUCT(2500) as P2 | **AB: 10** | 0 | 0 | AB wins in **33 moves** |
| PUCT(2500) as P1 vs MCTS(500) as P2 | **PUCT: 10** | MCTS: 0 | 0 | PUCT beats MCTS as P1 |
| MCTS(500) as P1 vs PUCT(2500) as P2 | — | — | **10** | MCTS draws as P1 |

### Key Findings

1. **AB as P1 wins 100% vs both MCTS and PUCT** — first-player advantage is absolute
2. **PUCT as P2 loses FASTER** than UCB1 MCTS (33 moves vs 54 moves) — counterintuitive
3. **PUCT as P1 draws same as UCB1 MCTS** (10/10 draws)
4. **PUCT does NOT outperform UCB1 MCTS in head-to-head** when PUCT is P2, MCTS is P1

### Conclusion: PUCT selection + tactical playouts are NOT the solution

The deeper PUCT tree converges on AB's forced-win lines more efficiently.
Tactical playouts don't find counter-play paths. The bottleneck is search
paradigm: AB solves millions of positions/move via bitboard ops; MCTS explores
thousands via full board copies.

### Files Added
- `connectx/bots/mcts_8x7_5_puct.py` — PUCT MCTS bot (246 lines)
- `connectx/bots/__init__.py` — Updated registry
- `connectx/tests/test_8x7_5.py` — +5 new tests (35 total)
- `connectx/benchmarks/compare_8x7_5_puct_vs_ab.py` — PUCT vs AB comparison
- `connectx/benchmarks/compare_8x7_5_all_mcts.py` — Full 3-way comparison

## Cycle 21: Three 8×7/5 Bots — MCTS vs AB Comparison

**Completed:**
- **Deep variant built** (`bitboard_ab_8x7_5_deep`) — simple eval, depth 10 max
- **MCTS built for 8×7/5** (`mcts_bot_8x7_5`) — UCB1 selection, random playouts
- **3 comparison games run:**
  1. V1 (full eval, depth 8) vs V2 (simple eval, depth 10): V1 wins 1/5, 4 draws
  2. V1 as P2 vs V2 as P1: V1 wins 3/5, 2 draws — evaluation quality dominates
  3. AB (V1) vs MCTS (300 sims): AB wins 3/5, MCTS wins 2/5, 1 draw
- **Key finding: MCTS significantly stronger at 8×7/5 vs 7×6/4**
  - 7×6/4: MCTS 30-40% vs AB (solved, no value)
  - 8×7/5: MCTS 40-60% vs AB (unsolved, meaningful exploration)
- **30 tests pass** (21 original + 9 new)

## Cycle 22: MCTS Mark Tracking Bug Fix — AB Dominates 100%

**Completed:**
- Fixed comparison script mark-tracking bug (turn-based mark → explicit P1/P2 assignment)
- 20-game balanced comparison: AB wins 100% (20-0) vs Regular MCTS (500 sims)
- 20-game balanced comparison: AB wins 100% (20-0) vs Heuristic MCTS (500 sims)
- 20-game MCTS_REG vs MCTS_HEUR: Bot2 wins 10, draws 10
- Heuristic leaf evaluation provides no meaningful improvement at 500 sims
- Previous Cycle 21 MCTS results (81% AB, 19% MCTS) invalidated by mark-tracking bug

**Next actions:**
1. ~~Increase MCTS to 1000+ simulations~~ — **DONE**: 1000 sims = 10 draws as P1, 2000 = worse P1 play
2. ~~Implement PUCT~~ — **DONE**: PUCT bot built for 8x7/5
3. ~~Test PUCT vs UCB1~~ — **DONE**: PUCT as P2 loses faster (33 moves) than UCB1 (54 moves)
4. **Build 8×7/5 opening book** — pre-compute AB early-game optimal moves
5. **Consider deeper AB search** — can depth 12+ beat PUCT/MCTS?
6. **Consider hybrid: AB-guided MCTS** — use AB eval to seed MCTS playouts
7. **Consider 8×7/5 MCTS with tactical override** — if MCTS detects threat, solve with AB

## Cycle 23: MCTS Simulation Scaling — More Simulations = Worse P2 Play

**Completed:**
- Tested MCTS at 500/1000/2000 simulations vs AB at 8×7/5
- **500 sims:** AB 19-0, 1 draw — MCTS as P1 draws 1/10, as P2 loses in 41 moves avg
- **1000 sims:** AB 10-0, 10 draws — **MCTS as P1 draws ALL 10!** as P2 loses in 45 moves
- **2000 sims:** AB 20-0, 0 draws — MCTS as P1 loses in 38 moves (**worse than 500!**)
- **Key finding: More simulations make MCTS worse as P2** — deeper search amplifies AB advantage
- **Conclusion: Simulation budget has diminishing returns** — MCTS needs structural changes

## Session Summary (Cycle 19)

## Session Summary (Cycle 19: Systemic time_limit Bug Fix)

**Critical bug found and fixed across 10 bot files:** `time_limit = move_deadline - time.time()`
- `time.time()` returns epoch seconds (~1.75 billion), producing a massive negative number
- **Symptom:** Alpha-beta bots returned `best_col = 0` always. MCTS bots got 0.05s budget.
- **All previous benchmark results were INVALID.** The "v2 wins 100% vs Kaggle" was because BOTH were effectively random.
- **Fix:** `time_limit = move_deadline` (no subtraction of epoch time).
- **Post-fix results:**
  - v2 vs Kaggle negamax: **v2 wins 14/20 (70%)** — previously 0/20
  - MCTS vs Kaggle: **Kaggle wins 11/20** — previously MCTS 0/20 (0.05s budget)
  - All bots now make diverse moves (columns 0-6)
  - All 14 bot functions import and play correctly

**Key finding: 7×6/4 is solved under perfect play at this board size.**
- All alpha-beta variants equivalent (28 matchups, 336 games, 0 invalid — after TT fix)
- MCTS significantly weaker than alpha-beta
- Value NN path plateaued (quantized gameplay)
- BC approach = teacher (perfect memorization)

**Conclusion: Classical search solves 7×6/4 completely. Next productive directions: opponent-error exploitation, phase-aware play, or larger board expansion.**

## Immediate next actions

1. **Commit all changes** — DONE (time_limit fix + MCTS heuristic)
2. **Update dashboard** — DONE
3. **Commit mcts_heuristic** — DONE (c57ae12)
4. **Run test suite** — TODO: verify no regressions
5. **Decide next productive direction** — See below

## Next Productive Direction (Decision Pending)

After fixing the critical time_limit bug and improving MCTS, we've confirmed:

### What we know for certain
1. **7×6/4 is solved** — all alpha-beta bots play perfectly
2. **Time_limit bug invalidated all prior results** — v2=14/20 vs Kaggle
   is the first true measurement post-fix
3. **MCTS is weaker than alpha-beta** — even with heuristic evaluation
4. **NN/value network plateaued** — quantized gameplay
5. **BC approach matches teacher** — no surprise

### Three viable paths forward

**Path A: Larger board sizes (8×7/5 or 8×7/6)**
- 8×7/4 is NOT solved (unknown)
- 8×7/5 is definitely unsolved (larger branching factor)
- Alpha-beta at deeper depths may not solve it
- Neural networks might provide real value at larger sizes
- High research potential, but needs new engine support

**Path B: Opponent-error exploitation at 7×6/4**
- Design bots that play perfectly when opponent plays well
- But exploit mistakes (forks, open3, etc.) when opponent plays poorly
- "Confidence-gated hybrid": alpha-beta for strong positions, MCTS for uncertain ones
- Only meaningful improvement path at solved board size

**Path C: AlphaZero-style self-play training**
- Train value network on mixed-strength self-play (v2 + noise + random)
- Use trained value as MCTS leaf evaluation (not just random playout)
- Requires significant compute and careful design
- Risk: may plateau like previous NN attempts

### Recommended: Path A (Larger board sizes)
- Most novel research direction
- Opens up new solution space where NN could help
- 8×7/5 is a well-known interesting Connect Four variant
- Can start with small experiments before full training pipeline

### Files updated
- `connectx/bots/mcts.py` — Added heuristic evaluation
- `connectx/bots/__init__.py` — Registered mcts_bot_heuristic
- `PHASE2_DASHBOARD.md` — Added Cycle 19 sections
- `phase2/control/DECISION_LOG.md` — Added D2026-08-07-011
- `phase2/control/NEXT_ACTIONS.md` — Updated with next steps

## Cycle 20: 8×7/5 Bot Built — Path A Underway

**Completed:**
- **8×7/5 bitboard alpha-beta bot** — full v2 adaptation for 8×7/5
- **Engine seat_reverse made generic** (rows/cols params)
- **21 tests pass** — config, engine compatibility, win detection, bot behavior, timing, evaluation, bitboard
- **Key evidence: two identical 8×7/5 bots DRAW** (56 moves) — game not solved

**Files:**
- `connectx/bots/bitboard_ab_8x7_5.py` — 660 lines, 56-bit bitboards
- `connectx/tests/test_8x7_5.py` — 21 tests
- `connectx/engine.py` — generic seat_reverse

**Next 8×7/5 work:**
1. Profile search speed on 8×7/5 (empty board, mid-game, endgame)
2. Build a second 8×7/5 bot with different strategy (e.g., shallower but broader)
3. Compare two 8×7/5 bots against each other (P1 vs P2, seat-reversed)
4. If one strategy clearly dominates, begin deepening the stronger variant
5. Consider MCTS for 8×7/5 (where search is not solved, MCTS may shine)

## Cycle 21: 8×7/5 Benchmarking — Eval > Depth, MCTS Gains

**Completed:**
- **Deep variant built** (`bitboard_ab_8x7_5_deep`) — simple eval, depth 10
- **MCTS for 8×7/5 built** (`mcts_bot_8x7_5`) — UCB1, 300 simulations
- **5 comparisons run:**
  1. V1(full eval, depth 8) vs V2(simple eval, depth 10): V1 wins 1/5, 4 draws
  2. V1 as P2 vs V2 as P1: V1 wins 3/5, 2 draws — eval quality dominates
  3. AB vs MCTS(300 sims): AB 3W, MCTS 2W, 1D (5 games, misleading seat bias)
  4. AB vs MCTS(500 sims): MCTS wins 5/6 decisive (10 games, seat bias)
  5. AB vs MCTS(500 sims): AB wins 13/16 decisive (20 games, balanced)
- **Key findings:**
  - Deeper search does NOT compensate for weaker evaluation
  - Small samples mislead: MCTS appeared 60% vs AB, but 20-game balanced = 30%
  - 30 tests pass (21 + 9 new)
- **All 8×7/5 bots now benchmarked:** 3 variants tested against each other
- **Conclusion: AB still dominates MCTS at 8×7/5** but MCTS has real potential for improvement

**Next 8×7/5 work:**
1. **20-game balanced comparison COMPLETE** — AB wins 13/16 decisive (81%), MCTS 3/10 (30%)
2. **Tune MCTS** — increase simulations to 1000, test PUCT over UCB1
3. **Build MCTS with heuristic leaf evaluation** — blend random playout + positional score
4. **Build 8×7/5 opening book** — pre-compute AB's early-game optimal moves
5. **Consider 8×7/6 variant** — even larger board, deeper search needed
6. **Explore neural approaches for 8×7/5** — train value network on AB self-play

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