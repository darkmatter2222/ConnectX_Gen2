# Autonomous State — ConnectX Phase 2

**Session:** Cycle 2
**Date:** 2026-08-06

## What Was Last Completed

1. Repository audit: researched the current state
   - 53 rounds of research dossier expansion (rounds 041-053)
   - Research documents cover: MCTS, NNUE, bitboards, ensembles, Kaggle agents, governance
   - No actual gym/bot code has been written yet

2. Phase 2 control documents established (dashboard, decision log, risk register, next actions)

3. Python environment created at `O:\master_model_collection\ConnectX_Gen2_Phase2\.venv`

4. **Core ConnectX 7×6/4 engine built and tested:**
   - `connectx/engine.py` — full rule engine with gravity, win detection, terminal detection
   - `ConnectXEnv` class — turn-based environment
   - `GameRecord` dataclass — replay-capable game records
   - `play_game()` / `play_game_seated()` — bot vs bot game simulation

5. **Baseline bots built:**
   - `random_bot` — uniform random legal moves
   - `win_seek_block_bot` — priority tactical: win > block > center bias
   - `shallow_minimax_bot` (depth 3) / `depth2_minimax_bot` (depth 2) — negamax with alpha-beta

6. **Tournament system built and debugged:**
   - `BotRegistry` — register and lookup bots by name
   - `MatchResult` / `BotStats` — track match and bot performance
   - `Leaderboard` — rank bots by performance
   - `Tournament` — pairwise match scheduling with seat-aware win counting

7. **Comprehensive test suite:** 72/72 tests passing
   - 12 test classes covering: board ops, legal moves, drop/undrop, win detection, draw, env, paired play, baseline bots, tournament, edge cases, end-to-end, win-seek-block tactics

8. **Bitboard alpha-beta bot built:**
   - `connectx/bots/bitboard_ab.py` — negamax with TT, null-move pruning, adaptive depth
   - Zobrist hashing for transposition table
   - Bitboard-based evaluation with open-end bonus
   - Time management: depth-adaptive based on deadline

9. **Initial tournament run with 5 bots:**
   - `win_seek_block` dominates (97.5% win rate)
   - `bitboard_ab_fast` beats all bots except `win_seek_block`
   - `shallow_minimax` is weakest (0% win rate)

## What Is Active

**All foundational work + bitboard bot complete.** Next: fix evaluation function for bitboard bot to improve against `win_seek_block`.

## What Failed

- Multiple prior attempts to scaffold phase2 infrastructure via .ps1 scripts (all in orphaned files)
- Research-only accumulation without moving to implementation
- Tournament win-counting (fixed: seat-aware tracking in `run_pair` and `Leaderboard.add_match`)

## Next Highest-Value Unblocked Actions

1. **Tune bitboard evaluation function** — the `win_seek_block` bot is significantly stronger; need to understand why
2. **Build MCTS baseline** — pure Monte Carlo tree search for comparison with tree-search approaches
3. **Run larger tournament** — compare all bots with more games per pair (10+)
4. **Profile timing** — ensure bots meet Kaggle's 2-second action budget
5. **Build PUCT MCTS** — for comparison with classical tree search
6. **Install PyTorch** — GPU packages not yet installed in venv