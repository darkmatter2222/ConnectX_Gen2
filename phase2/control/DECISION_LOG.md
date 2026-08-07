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