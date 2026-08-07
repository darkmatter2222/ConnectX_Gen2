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