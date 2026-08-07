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
| win_seek_block | 97 | 3 | 0 | 97.0% |
| random | 69 | 26 | 5 | 69.0% |
| mcts_fast | 59 | 36 | 5 | 59.0% |
| depth2_minimax | 40 | 60 | 0 | 40.0% |
| bitboard_ab_fast | 30 | 70 | 0 | 30.0% |
| shallow_minimax | 0 | 100 | 0 | 0.0% |

### Key pairwise results (ignoring random)
- win_seek_block beats ALL opponents (100% W)
- mcts_fast beats ALL opponents except win_seek_block (100% W vs depth2/minimax/bitboard)
- depth2_minimax beats shallow_minimax (100%) and ties bitboard (50%)

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
| `.gitignore` | Python/ML ignores |

## Known Issues

- `win_seek_block` dominates all other bots — evaluation needs work for deeper bots
- No PyTorch/GPU packages installed yet
- No Kaggle packaging
- MCTS vs bitboard_ab: MCTS wins 100%, suggesting evaluation function is weak vs search-based approaches