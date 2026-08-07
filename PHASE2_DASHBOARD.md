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
| 4 | Deterministic replay & game records | COMPLETE (GameRecord, play_game) |
| 5 | Timing, overage, crash handling | PENDING |
| 6 | Tactical position tests | COMPLETE (via test suite) |
| 7 | Baseline bots | COMPLETE (random, win_seek_block, minimax x2, bitboard_ab x2) |
| 8 | Tournament scheduling & results | COMPLETE (with seat-aware win tracking) |
| 9 | Seat-reversed paired evaluation | COMPLETE (play_game_seated) |
| 10 | Measured leaderboards | COMPLETE (Leaderboard, BotStats) |

## Current Work

- **Tests passing:** 72/72
- **Core engine** with proper gravity, win detection, and terminal detection
- **5 bots:** random, win_seek_block, depth2_minimax, shallow_minimax, bitboard_ab_fast
- **Tournament system** with registry, matchmaking, seat-aware leaderboard
- **Comprehensive test suite** covering engine, bots, tournament, and end-to-end

## Latest Tournament (5 games/pair)

| Bot | W | L | D | Win% |
|-----|---|---|---|------|
| win_seek_block | 39 | 1 | 0 | 97.5% |
| random | 27 | 13 | 0 | 67.5% |
| depth2_minimax | 19 | 21 | 0 | 47.5% |
| bitboard_ab_fast | 15 | 25 | 0 | 37.5% |
| shallow_minimax | 0 | 40 | 0 | 0.0% |

## Key Decisions

- **Venv created** at `O:\master_model_collection\ConnectX_Gen2_Phase2\.venv`
- **Focus on 7×6/4:** Standard Kaggle ConnectX rules
- **PyTorch preferred** over TensorFlow
- **Storage:** Large data → `O:\master_data_collection\ConnectX_Gen2_Phase2`, models → `O:\master_model_collection\ConnectX_Gen2_Phase2`

## Files Created

- `connectx/__init__.py` — Package exports
- `connectx/engine.py` — Core rule engine (13 public functions + ConnectXEnv + GameRecord)
- `connectx/bots/__init__.py` — Bot registry
- `connectx/bots/random_bot.py` — Random baseline
- `connectx/bots/win_seek_block.py` — Priority tactical bot (win > block > center)
- `connectx/bots/shallow_minimax.py` — Negamax with alpha-beta (depth 2 & 3)
- `connectx/bots/bitboard_ab.py` — Negamax with TT, null-move pruning, adaptive depth
- `connectx/tournament.py` — Tournament system (BotRegistry, MatchResult, BotStats, Leaderboard, Tournament)
- `tests/test_connectx.py` — 72 test methods across 12 test classes
- `.gitignore` — Standard Python/ML ignores

## Known Issues

- Repository has extensive research docs but lots of orphaned files
- No GPU packages (PyTorch) installed yet — only pytest in venv
- No Kaggle-compatible packaging
- `win_seek_block` significantly outperforms tree-search bots — evaluation function tuning needed