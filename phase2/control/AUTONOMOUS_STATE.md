# Autonomous State — ConnectX Phase 2

**Session:** Cycle 3
**Date:** 2026-08-06

## What Was Last Completed

1. Repository audit, phase 2 control documents, Python env setup
2. **Core ConnectX 7×6/4 engine** with gravity, win detection, terminal detection, replay
3. **6 bots built and registered:**
   - `random_bot` — uniform random
   - `win_seek_block_bot` — priority tactical (win > block > center)
   - `shallow_minimax_bot` / `depth2_minimax_bot` — negamax depth 2/3
   - `bitboard_ab_bot` / `bitboard_ab_bot_fast` — negamax with TT, null-move, adaptive depth
   - `mcts_bot` / `mcts_bot_fast` — PUCT MCTS with random rollouts
4. **Tournament system** with seat-aware win counting and leaderboard
5. **Comprehensive test suite:** 72/72 passing

## Latest Tournament (10 games/pair)

| Bot | W | L | D | Win% |
|-----|---|---|---|------|
| win_seek_block | 97 | 3 | 0 | 97.0% |
| random | 69 | 26 | 5 | 69.0% |
| mcts_fast | 59 | 36 | 5 | 59.0% |
| depth2_minimax | 40 | 60 | 0 | 40.0% |
| bitboard_ab_fast | 30 | 70 | 0 | 30.0% |
| shallow_minimax | 0 | 100 | 0 | 0.0% |

MCTS is the 2nd strongest bot, beating all opponents except win_seek_block. The bitboard bot underperforms — evaluation function needs tuning.

## What Is Active

**Building and comparing bot families.** MCTS outperforms classical tree search (except win_seek_block), confirming that simulation-based approaches are strong for ConnectX. Next: improve bitboard evaluation, build stronger MCTS.

## What Failed

- Tournament win-counting bug (fixed)
- Research-only accumulation (fixed by building actual bots)
- Bitboard evaluation underperforms MCTS

## Next Highest-Value Unblocked Actions

1. **Improve bitboard evaluation** — add threat-weighted scoring, opponent-threat priority
2. **Build PUCT MCTS with better playouts** — replace random rollouts with shallow tactical play
3. **Build opening book** for win_seek_block or MCTS
4. **Profile timing** — ensure all bots meet the 1.75s strict promotion profile
5. **Run statistical tournaments** — 50+ games per pair with confidence intervals
6. **Install PyTorch** — prepare for neural network bots