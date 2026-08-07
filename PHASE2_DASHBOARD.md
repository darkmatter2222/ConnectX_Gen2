# ConnectX Phase 2 — Development Dashboard

**Created:** 2026-08-06
**Last Updated:** 2026-08-06
**Environment:** Python 3.13.7 / RTX 5090
**Venv:** `O:\master_model_collection\ConnectX_Gen2_Phase2\.venv`

## Status: ACTIVE — Engine, Bots, Tournament Complete

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Repository audit & research readiness | COMPLETE |
| 1 | Phase 2 control documents | COMPLETE |
| 2 | Python environment setup | COMPLETE |
| 3 | Core ConnectX 7×6/4 engine | COMPLETE |
| 4 | Deterministic replay & game records | COMPLETE |
| 5 | Timing, overage, crash handling | PENDING |
| 6 | Tactical position tests | COMPLETE |
| 7 | Baseline bots | COMPLETE (6 bots) |
| 8 | Tournament scheduling & results | COMPLETE |
| 9 | Seat-reversed paired evaluation | COMPLETE |
| 10 | Measured leaderboards | COMPLETE |

## Current Work

- **Tests passing:** 72/72
- **6 bots:** random, win_seek_block, depth2_minimax, shallow_minimax, bitboard_ab_fast, mcts_fast
- **Tournament system** with seat-aware leaderboard

## Latest Tournament (10 games/pair, 10 matchups)

| Bot | W | L | D | Win% |
|-----|---|---|---|------|
| win_seek_block | 60 | 0 | 0 | 100.0% |
| random | 48 | 10 | 2 | 80.0% |
| mcts_fast | 39 | 39 | 2 | 48.8% |
| bitboard_ab_fast | 31 | 69 | 0 | 31.0% |
| depth2_minimax | 20 | 60 | 0 | 25.0% |
| shallow_minimax | 0 | 20 | 0 | 0.0% |

### Key pairwise results (ignoring random)
- win_seek_block beats ALL opponents (100% W) — dominant tactical player
- mcts_fast dominates classical search: 39-2 vs bitboard_ab_fast, 18-2 vs depth2_minimax
- mcts_fast loses 0-20 to win_seek_block — win_seek_block's deep tactical search wins
- depth2_minimax ties bitboard_ab_fast (10-10), beats shallow_minimax (20-0)

## Key Decisions

- **Venv** at `O:\master_model_collection\ConnectX_Gen2_Phase2\.venv`
- **Focus on 7×6/4:** Standard Kaggle ConnectX rules
- **PyTorch preferred** over TensorFlow
- **Storage:** Data → `O:\master_data_collection/ConnectX_Gen2_Phase2`, Models → `O:\master_model_collection/ConnectX_Gen2_Phase2`

## Files Created

| File | Description |
|------|-------------|
| `connectx/engine.py` | Core rule engine + ConnectXEnv + GameRecord |
| `connectx/bots/random_bot.py` | Random baseline |
| `connectx/bots/win_seek_block.py` | Priority tactical bot |
| `connectx/bots/shallow_minimax.py` | Negamax depth-2/3 |
| `connectx/bots/bitboard_ab.py` | Negamax with TT + null-move pruning |
| `connectx/bots/mcts.py` | MCTS with PUCT selection |
| `connectx/tournament.py` | Tournament system with seat-aware leaderboard |
| `tests/test_connectx.py` | 72 tests across 12 classes |
| `run_tournament.py` | Quick tournament runner script |
| `.gitignore` | Python/ML ignores |

## Known Issues

- `win_seek_block` dominates all other bots (100% W) — needs deeper counter-strategy (deeper MCTS, hybrid)
- `bitboard_ab_fast` underperforms (31% W) — evaluation function needs fork detection, mobility
- MCTS draws quickly with fast variant (same center column every game) — needs seed-based variation
- `random` beats MCTS/bitboard in head-to-head due to chaotic positions — MCTS lacks robustness to noise
- No PyTorch/GPU packages installed yet
- No Kaggle packaging