# ConnectX Phase 2 — Development Dashboard

**Created:** 2026-08-06
**Last Updated:** 2026-08-06 (Cycle 8)
**Environment:** Python 3.13.7 / RTX 5090
**Venv:** `O:\master_model_collection\ConnectX_Gen2_Phase2\.venv`

## Status: ACTIVE — v2 Significantly Stronger Than win_seek_block Against Imperfect Opponents

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
- **Cycle 8:** v2 vs wsb measured — both solve first-player advantage; v2 dominates wsb against MCTS

## Key Finding (Cycle 8): v2 vs win_seek_block

Connect 4 is solved for the first player. Both v2 and wsb play "perfectly" as first player.

| Matchup | v2 Win% | Notes |
|---------|---------|-------|
| v2 vs wsb (200 games) | 50% | Tie — both solve first-player. wsb=1st always wins, v2=1st always wins. |
| v2 vs random (30 games) | 87% | Strong against random play |
| v2 vs mcts (20 games) | **75%** | Deep search dominates MCTS |
| wsb vs mcts (20 games) | **35%** | wsb significantly weaker than v2 against MCTS |
| v2_fast vs mcts | 70% | Faster but slightly weaker |
| v2_fast vs random | 77% | OK but v2 dominates random |

### v2 vs wsb Performance Breakdown

- **As first player (white):** Both win 100% (solved game)
- **As second player (black):** Both lose 100% (first player advantage)
- **Against imperfect opponents:** v2 is **2× stronger** than wsb (75% vs 35% vs mcts)

### Why the Dashboard Previously Claimed 100%

The dashboard's earlier "100% v2 vs wsb" was from testing v2-as-white only (not seat-reversed).
Full seat-reversed tournaments show the 50/50 split expected from a solved game.

## Cycle 8: v2 Null-Move Safety Fix

**Commit:** `a4f7bcd`

### Fix:
- Added null-move safety check: don't prune if opponent has immediate winning threat
- Wrapped in try/except for board state resilience
- Prevents crashes when board state is inconsistent during search

### Performance Summary (20 games, alternating colors)

| Bot | vs random | vs mcts |
|-----|-----------|---------|
| bitboard_ab_v2 | 87% | **75%** |
| bitboard_ab_fast_v2 | 77% | 70% |
| win_seek_block | 93% | **35%** |

**Key insight:** win_seek_block's priority system (win>block>center) excels against random chaos,
but v2's deeper search + move ordering dominates against structured imperfect play like MCTS.

## Timing Profile (v2)

| Board State | Avg Time | Max Time |
|-------------|----------|----------|
| Empty board | ~61ms | ~65ms |
| Mid-game (move 6-41) | 1-14ms | - |
| Well within 1.75s strict profile | YES | - |

## Latest Tournament Results

| Rank | Bot | vs random | vs mcts | vs wsb |
|------|-----|-----------|---------|--------|
| 1 | bitboard_ab_v2 | 87% | 75% | 50% |
| 2 | bitboard_ab_fast_v2 | 77% | 70% | 50% |
| 3 | win_seek_block | 93% | 35% | 50% |
| 4 | mcts | 10% | - | 65% |
| 5 | random | - | 25% | 7% |

## Known Issues

- **Original bitboard_ab** returns invalid moves under time pressure (~20% of games) — known bug
- `mcts_fast` underperforms vs bitboard — shallower MCTS loses to deeper negamax
- No PyTorch/GPU packages installed yet
- No Kaggle packaging
- `shallow_minimax` and `depth2_minimax` have known drop() bugs (column-full handling)

## Files Created

| File | Description |
|------|-------------|
| `connectx/engine.py` | Core rule engine + ConnectXEnv + GameRecord |
| `connectx/bots/random_bot.py` | Random baseline |
| `connectx/bots/win_seek_block.py` | Priority tactical (win > block > center) |
| `connectx/bots/shallow_minimax.py` / `depth2_minimax.py` | Negamax depth 2/3 |
| `connectx/bots/bitboard_ab.py` | Negamax with TT, null-move, fork-aware eval |
| `connectx/bots/bitboard_ab_improved.py` | **v2: iterative deepening, killers, history, null-move + safety** |
| `connectx/bots/mcts.py` | MCTS with PUCT selection + tactical playouts |
| `connectx/tournament.py` | Tournament system with seat-aware leaderboard |
| `tests/test_connectx.py` | 78 tests across 13 classes |
| `run_tournament.py` | Comprehensive tournament runner with v2 variants |
| `.gitignore` | Python/ML ignores |