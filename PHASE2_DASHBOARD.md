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
| 7 | Baseline bots | COMPLETE (8 bots) |
| 8 | Tournament scheduling & results | COMPLETE |
| 9 | Seat-reversed paired evaluation | COMPLETE |
| 10 | Measured leaderboards | COMPLETE |

## Current Work

- **Tests passing:** 72/72
- **8 bots:** random, win_seek_block, depth2_minimax, shallow_minimax, bitboard_ab_fast, mcts_fast, bitboard_ab, mcts
- **Tournament system** with seat-aware leaderboard

## Latest Tournament (10 games/pair, 10 matchups)

| Bot | W | L | D | Win% |
|-----|---|---|---|------|
| win_seek_block | 50 | 10 | 0 | 83.3% |
| bitboard_ab_fast | 76 | 24 | 0 | 76.0% |
| random | 38 | 20 | 2 | 63.3% |
| mcts_fast | 27 | 51 | 2 | 33.8% |
| depth2_minimax | 7 | 73 | 0 | 8.8% |
| shallow_minimax | 0 | 20 | 0 | 0.0% |

### Key pairwise results (ignoring random)
- win_seek_block beats ALL opponents (83% W) — dominant tactical player
- **bitboard_ab_fast major improvement**: 30% -> 76% W (deeper search: depth 5->7 fast, 6-10+ time-aware)
- **bitboard_ab_fast ties win_seek_block 10-10** — first time bitboard competes!
- bitboard_ab_fast beats mcts_fast 12-8 — deeper negamax beats shallower MCTS
- bitboard_ab_fast crushes depth2_minimax 20-0
- mcts_fast beats depth2_minimax 17-3

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
| `connectx/bots/bitboard_ab.py` | Negamax with TT + null-move + fork-aware evaluation |
| `connectx/bots/mcts.py` | MCTS with PUCT selection + tactical playouts |
| `connectx/tournament.py` | Tournament system with seat-aware leaderboard |
| `tests/test_connectx.py` | 72 tests across 12 classes |
| `run_tournament.py` | Quick tournament runner script |
| `.gitignore` | Python/ML ignores |

## Known Issues

- **`win_seek_block` still strongest** (83% W) — need deeper search or hybrid strategy
- `mcts_fast` underperforms (34% W) — shallower MCTS loses to deeper negamax
- `random` competitive (63% W) — chaos from random play confuses search-based bots
- No PyTorch/GPU packages installed yet
- No Kaggle packaging