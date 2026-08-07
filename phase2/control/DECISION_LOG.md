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