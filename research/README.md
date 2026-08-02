# Research Repository — ConnectX Bot

> **Current Round**: 10 (2026-08-02)
> **Goal**: Build the world's best Kaggle ConnectX bot through iterative research

---

## Canonical Files (authoritative)

| File | Purpose |
|------|---------|
| `research-state.md` | Current research state, round tracking, tool availability, priority gaps |
| `research-trajectory.md` | Research plan, knowledge gaps, trajectory, iteration log |
| `final-conclusion.md` | Evolving final conclusion about what architecture to build |
| `claim-register.md` | All material claims with status, evidence grade, source |
| `architecture-rankings.md` | Ranked approaches with confidence scores |
| `decision-log.md` | Architecture, tool, and strategy decisions with evolution |
| `source-ledger.md` | All research sources: primary, secondary, verified, unverified |
| `research-gaps.md` | Knowledge gap catalog with priority and resolution status |

## Round Reports

| File | Round | Date | Summary |
|------|-------|------|---------|
| `iterations/round-001.md` | 1 | 2026-07-30 | Initial deep research audit — compendium created |
| `iterations/round-002.md` | 2 | 2026-07-30 | Web research, agent parallel — 5+ new docs |
| `iterations/round-003.md` | 3 | 2026-07-30 | Kaggle analysis, new repos |
| `iterations/round-004.md` | 4 | 2026-07-31 | GPU, MCTS, game theory, bots, search |
| `iterations/round-005.md` | 5 | 2026-08-02 | Game-phase, endgame, benchmarks, eval |
| `iterations/round-006.md` | 6 | 2026-08-02 | GitHub topics discovery; AlphaZero (blanyal 92★) fully analyzed; bitboard agent catalog; canonical files created |
| `iterations/round-007.md` | 7 | 2026-08-02 | GoodCoder666/katac4 (KataGo-inspired AlphaZero) fully analyzed; Wikipedia confirms solved game |
| `iterations/round-008.md` | 8 | 2026-08-02 | PUCT MCTS benchmark (11/20 vs minimax); rowspire neural MCTS + bitboard solver (Rust+WASM); Java bitboard solver |
| `iterations/round-009.md` | 9 | 2026-08-02 | Tromp Fhourstones benchmark (20 systems, KPOS/S); Tromp 8x8 solver (book88 ≤16 ply); katac4 full training pipeline; katac4 ResNet KataGo techniques; alpha-beta+MCTS hybrid; VERIFIED 55% |
| `iterations/round-010.md` | 10 | 2026-08-02 | rowspire FULL source decoded (14 files): 4×128 MLP, dual value+policy, 100D input, 7-feature eval, UCB1 MCTS; eSlams framework; kenrick95/c4; Wikipedia opening theory; VERIFIED 60% |

## Legacy Documents (evidence, preserved)

| File | Topic | Created |
|------|-------|---------|
| `00-comprehensive-report.md` | Initial comprehensive report | 2026-07-28 |
| `01-game-mechanics.md` | Game rules, board layout | 2026-07-28 |
| `02-connect4-ai-pipeline.md` | AI pipeline deep dive | 2026-07-28 |
| `03-deep-research-compendium.md` | Deep research compendium | 2026-07-30 |
| `04-environment-observations.md` | Live env inspection | 2026-07-28 |
| `05-bot-agent-interface-submission-format.md` | Agent interface docs | 2026-07-29 |
| `06-package-api-deep-dive.md` | Kaggle API deep dive | 2026-07-30 |
| `evaluation-function-design.md` | Eval features and weights | 2026-07-30 |
| `nn-architecture-research.md` | NN architecture | 2026-07-30 |
| `training-data-generation.md` | Training data strategies | 2026-07-30 |
| `neural_network_architectures_connectx.md` | NN hyperparameters, RTX timeline | 2026-07-30 |
| `transfer-learning-research.md` | Transfer learning findings | 2026-07-30 |
| `transfer-learning-domain-adaptation-connectx.md` | 7x6→15x13 transfer analysis | 2026-07-30 |
| `alpha_beta_optimizations_connect4.md` | Alpha-beta optimizations | 2026-07-30 |
| `gpu-research.md` | GPU hardware research | 2026-07-30 |
| `mcts-research.md` | MCTS research | 2026-07-30 |
| `advanced-search-research.md` | Advanced search research | 2026-07-30 |
| `opening-book-research.md` | Opening book research | 2026-07-30 |
| `gpu-research-iteration4.md` | GPU opportunities: inference, training, hybrid | 2026-07-31 |
| `mcts-research-iteration4.md` | MCTS variants: UCT, RAVE, Neural MCTS | 2026-07-31 |
| `game-theory-iteration4.md` | 7x6 SOLVED, opening book design, game transfer | 2026-07-31 |
| `open-source-bots-iteration4.md` | 10 repos cataloged | 2026-07-31 |
| `advanced-search-iteration4.md` | MTD(f), PVS, LMR, killer, JIT | 2026-07-31 |
| `iteration-2-findings.md` | Iteration 2 findings | 2026-07-30 |
| `iteration-3-findings.md` | Iteration 3 findings | 2026-07-30 |
| `iteration-4-findings.md` | Iteration 4 findings | 2026-07-31 |
| `iteration-5-findings.md` | Iteration 5 findings | 2026-08-02 |
| `benchmark_alpha_beta.py` | Alpha-beta benchmark script | 2026-07-30 |

## Test Files (evidence, preserved)

Test files from early development iterations (not executed):
`test_board_layout.py`, `test_bug.py`, `test_bug2.py`, `test_clean.py`, `test_final.py`, `test_full_game.py`, `test_renderer.py`, `test_win_trace.py`

---

## Research Summary

**Current Leading Approach**: Hybrid Neural + Classical Search (confidence: HIGH)

**Key Knowns**:
- 7x6 Connect 4 is SOLVED (first player wins from center)
- RTX 5090 available: 21,760 CUDA cores, 32GB GDDR7
- Kaggle: 2s/move, 60s overtime, arbitrary board sizes
- Game-phase strategy: Opening (book) → Midgame (search) → Endgame (tablebase)

**Key Unknowns**:
- Current Kaggle leaderboard (web search broken)
- Empirical benchmarks (NN training, inference speed)
- 15x13 first-player advantage
- Optimal NN architecture for ConnectX

**Tool Status**: WebSearch broken (Round 5+), WebFetch works, Bash/Read/Glob work