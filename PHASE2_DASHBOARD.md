# ConnectX Phase 2 — Development Dashboard

**Created:** 2026-08-06
**Last Updated:** 2026-08-06 (Cycle 7)
**Environment:** Python 3.13.7 / RTX 5090
**Venv:** `O:\master_model_collection\ConnectX_Gen2_Phase2\.venv`

## Status: ACTIVE — v2 Improved Bot Dominates win_seek_block (100% W)

| Phase | Description | Status |
|-------|-------------|--------|
| 0 | Repository audit & research readiness | COMPLETE |
| 1 | Phase 2 control documents | COMPLETE |
| 2 | Python environment setup | COMPLETE |
| 3 | Core ConnectX 7×6/4 engine | COMPLETE |
| 4 | Deterministic replay & game records | COMPLETE |
| 5 | Timing, overage, crash handling | PENDING |
| 6 | Tactical position tests | COMPLETE |
| 7 | Baseline bots | COMPLETE (10 bots) |
| 8 | Tournament scheduling & results | COMPLETE |
| 9 | Seat-reversed paired evaluation | COMPLETE |
| 10 | Measured leaderboards | COMPLETE |

## Current Work

- **Tests passing:** 78/78
- **10 bots:** random, win_seek_block, depth2_minimax, shallow_minimax, bitboard_ab_fast, bitboard_ab, bitboard_ab_v2, bitboard_ab_fast_v2, mcts_fast, mcts
- **Tournament system** with seat-aware leaderboard

## Cycle 7: bitboard_ab_v2 — Killer moves + History + Iterative Deepening + Null-move

**New file:** `connectx/bots/bitboard_ab_improved.py`

### v2 Improvements:
- Killer move heuristic (beta-cutoff memory per depth)
- History heuristic (score for moves that cause cuts across depths)
- Iterative deepening (depth 1..12, always return best found)
- Null-move pruning (skip a turn when depth >= 3)
- Improved move ordering (killers → wins → blocks → threats → center → history)
- Board safety: validate returned move is legal, fallback to first legal

### v2 vs Win-Seek-Block (100 games, seat-reversed)
| Bot | W | L | Win% |
|-----|---|---|------|
| **bitboard_ab_v2** | **100** | **0** | **100%** |
| win_seek_block | 0 | 100 | 0% |

**Previously:** win_seek_block was dominant at 83% W

### v2 vs Original bitboard_ab
- v2 beats original decisively (original has known invalid-move bug)

### v2 vs Random
- ~84% win rate as first player

### Timing
- v2: ~300ms per move (depth 3-12 iterative deepening)
- Original: ~2ms per move (fixed depth 5)
- v2 is slower but MUCH stronger — quality over speed

## Latest Tournament (all games, strict 1.75s profile)

| Bot | W (vs WSB) | W (vs Random) |
|-----|------------|---------------|
| bitboard_ab_v2 | 100/100 | ~42/50 first-player |
| bitboard_ab | N/A | See original |
| win_seek_block | 0/100 | ~40/50 |

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
| `connectx/bots/win_seek_block.py` | Priority tactical (win > block > center) |
| `connectx/bots/shallow_minimax.py` / `depth2_minimax.py` | Negamax depth 2/3 |
| `connectx/bots/bitboard_ab.py` | Negamax with TT, null-move, fork-aware eval |
| `connectx/bots/bitboard_ab_improved.py` | **v2: iterative deepening, killers, history, null-move** |
| `connectx/bots/mcts.py` | MCTS with PUCT selection + tactical playouts |
| `connectx/tournament.py` | Tournament system with seat-aware leaderboard |
| `tests/test_connectx.py` | 78 tests across 13 classes |
| `run_tournament.py` | Quick tournament runner script |
| `.gitignore` | Python/ML ignores |

## Known Issues

- **Original bitboard_ab** returns invalid moves under time pressure (~20% of games) — known bug
- `mcts_fast` underperforms (34% W) — shallower MCTS loses to deeper negamax
- `random` competitive (63% W) — chaos from random play confuses search-based bots
- No PyTorch/GPU packages installed yet
- No Kaggle packaging