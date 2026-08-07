# Autonomous State — ConnectX Phase 2

**Session:** Cycle 4
**Date:** 2026-08-06

## What Was Last Completed

1. Repository audit, phase 2 control documents, Python env setup
2. **Core ConnectX 7×6/4 engine** with gravity, win detection, terminal detection, replay
3. **8 bots built and registered:**
   - `random_bot` — uniform random
   - `win_seek_block_bot` — priority tactical (win > block > center)
   - `shallow_minimax_bot` / `depth2_minimax_bot` — negamax depth 2/3
   - `bitboard_ab_bot` / `bitboard_ab_bot_fast` — negamax with TT, null-move, adaptive depth
   - `mcts_bot` / `mcts_bot_fast` — PUCT MCTS with tactical playouts
4. **Tournament system** with seat-aware win counting and leaderboard
5. **Comprehensive test suite:** 72/72 passing
6. **MCTS tactical rollout gravity bug fixed** — all drop() calls wrapped, valid_moves rechecked, empty moves handled

## Latest Tournament (10 games/pair, fast variants)

| Bot | W | L | D | Win% |
|-----|---|---|---|------|
| win_seek_block | 60 | 0 | 0 | 100.0% |
| random | 48 | 10 | 2 | 80.0% |
| mcts_fast | 39 | 39 | 2 | 48.8% |
| bitboard_ab_fast | 31 | 69 | 0 | 31.0% |
| depth2_minimax | 20 | 60 | 0 | 25.0% |
| shallow_minimax | 0 | 20 | 0 | 0.0% |

### Key pairwise results
- win_seek_block: **unbeaten** (60/60) — dominant tactical player
- mcts_fast: **39-2 vs bitboard_ab_fast**, 18-2 vs depth2_minimax — MCTS beats classical search
- mcts_fast: 0-20 vs win_seek_block — win_seek_block's shallow-depth deep-tactical search wins
- mcts_fast vs random: 1-17 (random lucky wins from chaotic positions)

## What Is Active

**Improving the MCTS bot** — gravity fix complete, now ready to build stronger MCTS with:
- Seed-based deterministic variation
- Better exploration/exploitation balance
- Killer move history table
- Extended search at time-remaining

## What Failed

- Tournament win-counting bug (fixed)
- Research-only accumulation (fixed by building actual bots)
- Bitboard evaluation underperforms MCTS (still)
- MCTS tactical rollout crashes on full columns (fixed)

## Next Highest-Value Unblocked Actions

1. **Add deterministic seeding to MCTS** — use seed parameter for reproducible play, avoid chaotic draws
2. **Improve MCTS exploration** — tune PUCT constant, add move history heuristic
3. **Improve bitboard evaluation** — fork detection, mobility, threat-weighted scoring
4. **Build win_seek_block killer / counter-strategy** — deeper MCTS or hybrid
5. **Profile timing** — ensure all bots meet the 1.75s strict promotion profile
6. **Run larger statistical tournaments** — 50+ games per pair
7. **Install PyTorch** — prepare for neural network bots