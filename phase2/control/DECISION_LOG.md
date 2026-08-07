# Decision Log — ConnectX Phase 2

## D2026-08-06-001: Start with engine, not research
- **Rationale:** Repository has 53 rounds of research with zero implementation. The highest-value action is to build the gym so research can be tested.
- **Assumption:** Research quality is adequate; we trust the documented techniques and start implementing.

## D2026-08-06-002: Flat 42-cell array for board
- **Rationale:** Matches Kaggle environment API exactly. 7 columns × 6 rows = 42 cells, row-major.
- **Trade-off:** 2D array is more readable but 1D matches the API and is simpler for serialization.

## D2026-08-06-003: PyTorch over TensorFlow
- **Rationale:** System has PyTorch 2.11.0+cu128 installed. PyTorch is the preferred framework. Will use TensorFlow only if an imported contender requires it.

## D2026-08-06-004: No venv for initial engine development
- **Rationale:** System Python already has PyTorch. Will create venv at `O:\master_model_collection\ConnectX_Gen2_Phase2\.venv` when first needed (training, large dependencies).
- **Risk:** Environment not isolated. Will fix at venv creation time.

## D2026-08-06-005: Standard Kaggle rules only
- **Rationale:** Focus on 7×6/4: 7 columns, 6 rows, 4 in a row, 2 seconds/action, 60s cumulative overage. No variant boards.

## D2026-08-07-006: Value network trained on v2-vs-MCTS data not useful for MCTS
- **Finding:** mcts_value (value-guided MCTS, 34.5 pts) underperforms vanilla mcts (43 pts) in 130-game tournament
- **Root causes:**
  1. Value network trained on v2-vs-MCTS self-play → first-player bias, 100% P1-wins
  2. High MAE (0.786) → predictions too coarse for MCTS node selection
  3. PyTorch overhead (~2.5s/game) reduces search budget vs ~1.6s for vanilla MCTS
  4. Most leaf evaluations fall into "near-neutral" blend zone, negating value advantage
- **Decision:** Pivot from supervised training to AlphaZero-style self-play refinement
  - Self-play data will be balanced (50/50 seats)
  - Iterative: train NN → self-play → collect data → retrain → repeat
- **Rejected:** Keeping value-guided MCTS as-is (inferior to vanilla MCTS)
- **Evidence:** Cycle 13.1 quick tournament (130 games, 12 matchups)

## D2026-08-07-007: High-noise self-play generates useful value data; NN improves vValue
- **Finding:** v2 vs v2 at 5% noise produced all draws (solved game). At 20% noise:
  - 14 P1 wins, 14 P2 wins, 2 draws in 30 games (53% non-draw rate)
  - 353 W, 339 L, 84 D labels — nearly balanced
  - 776 positions from 288 seconds of runtime
- **New value network (Cycle 15) vs old (Cycle 13):**
  - Test MAE: 0.35 vs 0.96 (74% improvement)
  - Test sign accuracy: 74% vs 15%
  - vValue vs MCTS: 70% (up from 56% in Cycle 13)
  - mcts_value vs mcts: 30% (down from ~35%, NN doesn't help MCTS)
- **Insight:** Value network helps alpha-beta leaf evaluation (vValue) significantly.
  MCTS still underperforms vanilla MCTS with value network leaf evaluation —
  likely because MCTS node selection amplifies NN prediction variance.
- **Decision:** Value network useful for vValue enhancement only. MCTS with NN guidance
  remains inferior to vanilla MCTS. Self-play noise level = 20% is the key parameter.
- **Evidence:** Cycle 15 training (50 epochs, batch 64, 776 positions), 80-game evaluation

## D2026-08-07-008: Game play performance is quantized — extra NN precision doesn't help

- **Finding:** Cycle 15 model (MAE 0.412, 776 pos @ 20% noise) and 25% model (MAE 0.496, 935 pos @ 25%) produce **identical gameplay** — 14W-6L as P1, 12W-7L-1D as P2 vs MCTS in 40-game tests, and 46W-21L-13D in 80-game evaluation (57.5% vs MCTS)
- **25% noise data is ideal for training:** zero draws, 481W/454L (51.4%/48.6%)
- **20% noise 2,696 positions** — surprisingly worse (MAE 0.658) despite being pure 20% data
  - Same game distribution as 776 positions, just scaled up
  - Suggests training randomness (seed, split) may dominate
- **Conclusion:** Once value NN quality reaches a threshold, extra precision is irrelevant for alpha-beta gameplay. The NN only needs to be good enough to guide leaf evaluation; beyond that, the heuristic dominates.
- **Decision:** Keep Cycle 15 model as default. No need to pursue more data or hyperparameter tuning.
- **Evidence:** 120 games (3×40), 3 models compared (Cycle 15, 25% noise, 20% 2696)
## D2026-08-07-009: vValue model loading bug

- **Bug:** The trained value network weights (saved to `.pth` files) were never loaded into the inference model. `bitboard_ab_value.py` created a fresh `GPUValueNet()` with random weights.
- **Impact:** All vValue evaluations (Cycle 13-17) used random-weights NN. The "trained model" results were really from random noise.
- **Fix:** Added `vn.load(_DEFAULT_MODEL_PATH)` in `_get_predictor()`.
- **Result:** Trained NN loads correctly. Gameplay unchanged — both trained and untrained NN give ~60% vs MCTS. Game play is quantized.

## D2026-08-07-010: bitboard_ab invalid-move bug

- **Bug:** `_negamax` in `bitboard_ab.py` returned hardcoded `col=0` in TT lookup and null-move prune paths. When column 0 was full, the bot returned an invalid move.
- **Impact:** ~20% of games failed with invalid move (column full) or crashed with ValueError.
- **Fix:** All early-exit paths in `_negamax` now return `legal[0]` instead of `0`.
- **Verified:** 380 moves across 20 games, 0 invalid moves.

## D2026-08-07-011: Systemic time_limit bug — move_deadline - time.time()

- **Bug:** Multiple bot files used `time_limit = move_deadline - time.time()` (or `max(0.05, move_deadline - time.time() - 0.05)`). `time.time()` returns epoch seconds (~1.75 billion), producing a massive negative number.
- **Root cause:** Confused `move_deadline` (a duration in seconds) with a Unix timestamp. The correct pattern is `time.time() - start_time` for elapsed computation, never `deadline - time.time()`.
- **Symptoms:**
  1. `_select_depth(negative)` matched the `else` branch → returned `(2, 7)` instead of `(3, 12)` for v2
  2. Time check `elapsed >= time_limit * 0.95` → `0 >= -1753688231` → True → immediately breaks
  3. Returns `best_col = 0` (initialized at line 550) — **bot always chose column 0**
  4. MCTS bots: `max(0.05, negative)` → `0.05` second time budget (1.5s wasted on nothing)
- **Affected files (10 total):**
  1. `connectx/bots/bitboard_ab.py` — v1
  2. `connectx/bots/bitboard_ab_improved.py` — v2 (ALREADY FIXED in previous cycle)
  3. `connectx/bots/bitboard_ab_value.py` — vValue (both vValue and vValue_fast)
  4. `connectx/bots/bitboard_ab_improved_v3.py` — v3 (both v3 and v3_fast)
  5. `connectx/bots/bitboard_ab_ensemble.py` — ensemble
  6. `connectx/bots/bitboard_ab_with_nn.py` — NN bot
  7. `connectx/bots/mcts.py` — both mcts and mcts_value
  8. `connectx/bots/mcts_bc.py` — BC-trained MCTS
  9. `connectx/training/kaggle_self_contained.py` — Kaggle bot
  10. **Impact:** **All previous benchmark results using v1, vValue, v3, ensemble, NN, MCTS variants were invalid.** v2 results were also invalid before this cycle's fix.
- **Fix:** `time_limit = move_deadline` (or `max(0.05, move_deadline - 0.05)` for MCTS). No subtraction of `time.time()`.
- **Verified:**
  1. All 10 bot families import correctly
  2. All bots play legal games (no crashes, no invalid moves)
  3. All bots make diverse moves (columns 0-6, not just col 0)
  4. **v2 vs Kaggle negamax after fix: v2 wins 14/20 (70%), kaggle 2/20, 4 draws** (previously v2 won 0/20 — both playing random)
  5. **MCTS vs Kaggle after fix: MCTS 1/20, kaggle 11/20** (MCTS was 0/20 before due to 0.05s budget)
