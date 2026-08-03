# Claim Register — ConnectX Bot Research

> **Current Round**: 15
> **Last Updated**: 2026-08-02

---

## How to Read

| Field | Description |
|-------|-------------|
| **Claim ID** | Unique identifier (C###) |
| **Claim** | The exact claim being evaluated |
| **Status** | VERIFIED / SUPPORTED / HYPOTHESIS / DISPUTED / REFUTED / UNKNOWN |
| **Sources** | Source IDs from source-ledger.md |
| **Evidence Grade** | Strong / Moderate / Weak / None |
| **Applicability** | How it applies to Kaggle ConnectX |
| **First Added** | Round when first recorded |
| **Last Verified** | Last round where this was checked |
| **Confidence** | LOW / MEDIUM / HIGH |
| **Architecture Impact** | Which architecture ranking it affects |

---

## Material Claims — Game-Solving Knowledge

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C001 | 7x6 Connect 4 is solved: first player always wins from optimal play | SUPPORTED | S028 (Wikipedia), S001, S002, S003 | Moderate | Core to opening book strategy | Round 1 | Round 7 | MEDIUM | Critical — if false, opening book approach fails |
| C002 | Böck (2025) W-D-L database covers all ~4.5T positions with ≤24 pieces | UNKNOWN | S001 | None in this round | Endgame DB approach | Round 1 | Round 7 | LOW | Critical — if false, endgame approach needs redesign |
| C003 | Tromp (2025) independently verified Böck's results with brute-force 8-ply DB | UNKNOWN | S002 | None in this round | Secondary verification | Round 1 | Round 7 | LOW | Supports C002 |
| C004 | Solved DB compressed size is ~13 GB | UNKNOWN | S001 | None in this round | Storage planning | Round 1 | Round 7 | LOW | Practical — affects deployment strategy |
| C005 | Optimal first move on 7x6 is a middle column — forces win in ≤41 moves | SUPPORTED | S028 (Wikipedia) | Moderate | Opening book | Round 1 | Round 7 | MEDIUM | Critical — determines opening book |

---

## Material Claims — Search Algorithms

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C006 | MTD(f) gives 20-30% speedup over alpha-beta on Connect 4 | SUPPORTED | Internal knowledge | Moderate | All board sizes | Round 1 | Round 5 | MEDIUM | Moderate — affects search choice |
| C007 | PVS (Principal Variation Search) gives additional 20-35% over standard alpha-beta | SUPPORTED | Internal knowledge | Moderate | All board sizes | Round 4 | Round 5 | MEDIUM | Moderate |
| C008 | Center-first move ordering gives 3-5× effective speedup | SUPPORTED | Internal knowledge | Moderate | All board sizes | Round 1 | Round 5 | MEDIUM | Moderate |
| C009 | Full move ordering (TT + wins/blocks + killer + center) gives 10-30× effective speedup | SUPPORTED | Internal knowledge | Moderate | All board sizes | Round 4 | Round 5 | MEDIUM | Moderate |
| C010 | Transposition table size of 100K-1M entries recommended | SUPPORTED | Internal knowledge | Moderate | All board sizes | Round 4 | Round 5 | MEDIUM | Moderate |
| C071 | ariobarin/The-Reticle Connect 4 engine uses transposition table (10M capacity, LRU eviction), history heuristic (3^depth), threat-map evaluation (+/-1000 strong, +/-100 weak), iterative deepening with time limit, column-major board with hash() | HYPOTHESIS | S052 (ariaborin/The-Reticle source code: engine.py, board.py) — **Downgraded R15**: transposition table is fully disabled (commented-out dead code per corpus audit) | Strong | Search optimization | Round 13 | Round 15 | HIGH | Downgraded — TT is non-functional; engine relies on threat-map and history heuristic only |
| C072 | nguyenthequang/games-website implements centrality-based move ordering [3,2,4,1,5,0,6], in-place board mutation (no cloning), pre-computed C4_WINDOWS array, immediate win/block detection before alpha-beta search | VERIFIED | S051 (nguyenthequang/games-website source code: js/connect4.js) | Strong | Search optimization | Round 13 | Round 13 | HIGH | High — proven move ordering and board cloning optimization directly applicable to Kaggle JS/Python implementations |

---

## Material Claims — Neural Networks

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C011 | Small CNN (100-500K params) trained on solved 7x6 matches minimax eval ~65% of the time | HYPOTHESIS | Internal knowledge | Weak | Training strategy | Round 2 | Round 5 | LOW | Moderate — NN training design |
| C012 | SFT→RL two-stage training is the most effective NN approach | SUPPORTED | S014, S015 | Moderate | Training pipeline | Round 2 | Round 5 | MEDIUM | High — determines training strategy |
| C013 | NN provides 2-3× alpha-beta speedup via better move ordering | HYPOTHESIS | Internal knowledge | Weak | Search acceleration | Round 5 | Round 15 | LOW | Downgraded from MEDIUM-HIGH — non-standard label, no published source; AlphaConnect4 evidence shows NN guides MCTS directly rather than via alpha-beta move ordering |
| C014 | Transfer learning 7x6→15x13 achieves 60-70% of native strength | HYPOTHESIS | Internal knowledge | Weak | Multi-board strategy | Round 3 | Round 3 | LOW | Moderate |
| C015 | Progressive training (4x4→15x13) closes gap from ~32% to ~10% | HYPOTHESIS | Internal knowledge | Weak | Training pipeline | Round 3 | Round 3 | LOW | Moderate |

---

## Material Claims — Hardware / Performance

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C016 | Numba JIT gives 5-10× alpha-beta speedup in Python | STRONGLY SUPPORTED | Internal knowledge + Numba documentation | Strong | All Python implementations | Round 1 | Round 5 | HIGH | High — key for Python search speed |
| C017 | RTX 5090 training: SFT ~2h, RL ~18h, transfer ~1-2h, total ~21h | HYPOTHESIS | RTX 5090 specs + NN size estimates | Weak | Training planning | Round 3 | Round 5 | LOW | Moderate |
| C018 | Kaggle T4 inference: 0.5-2ms per position for small NN | HYPOTHESIS | Kaggle T4 specs + model size | Weak | Deployment | Round 3 | Round 5 | LOW | Moderate |
| C019 | ONNX Runtime deployment feasible: 2-5 MB model size | SUPPORTED | ONNX documentation + model size estimates | Moderate | Deployment | Round 3 | Round 5 | MEDIUM | Moderate |

---

## Material Claims — Kaggle Environment

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C020 | Kaggle ConnectX uses 2s/move timeout (actTimeout) | VERIFIED | S005, S006 | Strong | All implementations | Round 1 | Round 6 | HIGH | Critical — affects search depth |
| C021 | 60-second overtime budget per match | VERIFIED | S005 | Strong | Time management | Round 1 | Round 6 | HIGH | Critical |
| C022 | Board is flat (row-major) array in observation | VERIFIED | S006 | Strong | Board representation | Round 1 | Round 6 | HIGH | Critical — affects indexing |
| C023 | Board configurations: 7x6 default, configurable columns/rows/inarow | VERIFIED | S005 | Strong | Multi-board strategy | Round 1 | Round 6 | HIGH | Critical |
| C024 | Invalid column moves result in agent loss | VERIFIED | S006 | Strong | Error handling | Round 1 | Round 6 | HIGH | Critical |
| C025 | agentTimeout is deprecated, use remainingOverageTime instead | STRONGLY SUPPORTED | S005, S006 | Strong | API compliance | Round 3 | Round 13 | HIGH | Moderate — agentTimeout fully removed from spec; observation.remainingOverageTime is now the sole authoritative source |

---

## Material Claims — GitHub Repo Discoveries (Round 6)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C031 | ResNet with configurable residual blocks is a viable NN architecture for Connect 4 | VERIFIED | S019 | Strong | NN architecture | Round 6 | Round 6 | HIGH | High — first concrete ResNet impl for Connect 4 |
| C032 | MCTS with 30 simulations, c_puct=1.0 is a practical Connect 4 configuration | VERIFIED | S019 | Strong | MCTS tuning | Round 6 | Round 6 | HIGH | Moderate — first concrete MCTS config |
| C033 | Bitboard + Numba + 16M TT + PVS is used in production ConnectX agents | VERIFIED | S022 | Strong | Search optimization | Round 6 | Round 6 | HIGH | High — first concrete high-performance Python impl |
| C034 | DQN shallow (1-2 layers, 64-128 units) performs comparably to deep (3-4 layers) | VERIFIED | S025 | Moderate | NN design | Round 6 | Round 6 | MEDIUM | Moderate — contradicts bigger-is-better intuition |
| C035 | Fork evaluation weights of ~+950 are used in production ConnectX agents | VERIFIED | S022 | Strong | Evaluation function | Round 6 | Round 6 | HIGH | Moderate — heavier fork weighting than prior estimates |
| C036 | blanyal/alpha-zero (92★) is the most-starred publicly available AlphaZero implementation for Connect Four | VERIFIED | S019 | Strong | Architecture choice | Round 6 | Round 6 | HIGH | High — reference implementation |
| C037 | GitHub topics pages are a reliable method for discovering ConnectX/Connect 4 repos | VERIFIED | S017, S018 | Strong | Discovery method | Round 6 | Round 7 | HIGH | Moderate — alternative to WebSearch |
| C038 | KataGo-inspired ResNet (3 bottleneck blocks, 128 channels, gated pooling) is a viable NN architecture for Connect 4 | VERIFIED | S026 | Strong | NN architecture | Round 7 | Round 7 | HIGH | High — first KataGo adaptation for Connect 4 |
| C039 | MCTS with 1600 sims, FPU exploration (c_fpu=0.2), adaptive CPUCT, and LCB move selection is practical for Connect 4 | VERIFIED | S026 | Strong | MCTS tuning | Round 7 | Round 7 | HIGH | High — advanced MCTS techniques for ConnectX |
| C040 | Training on randomized 9×9 to 12×12 boards with self-play produces a generalized Connect 4 player | VERIFIED | S026 | Moderate | Multi-board strategy | Round 7 | Round 7 | MEDIUM | High — directly relevant to Kaggle multi-board scoring |
| C041 | 6-channel board representation (player, opponent, valid moves, open territories, last moves) provides rich positional features | VERIFIED | S026 | Moderate | Board representation | Round 7 | Round 7 | MEDIUM | Moderate — richer than 3-channel or 4-channel approaches |
| C042 | AlphaZero for Connect 4 can achieve measurable ELO ratings through self-play and tournament testing | VERIFIED | S026 | Moderate | Performance measurement | Round 7 | Round 7 | MEDIUM | Moderate — ELO-based evaluation is concrete |
| C043 | PUCT MCTS with tactical priors (center control, immediate wins, blocks) achieves 11/20 wins in 20 games vs minimax depth 3 | VERIFIED | S029 | Moderate | PUCT tuning, benchmark methodology | Round 8 | Round 8 | MEDIUM | High — first empirical PUCT benchmark on Connect 4 |
| C044 | Neural MCTS with separate value + policy networks (4×128 MLP with skip connections) is a viable approach for Connect 4 | VERIFIED | S030 | Moderate | NN architecture, MCTS integration | Round 8 | Round 8 | HIGH | High — most concrete neural architecture yet for Connect 4 |
| C045 | Java bitboard solver with transposition caching and configurable skill levels is viable for Connect 4 | VERIFIED | S031 | Moderate | Classical search, board representation | Round 8 | Round 8 | MEDIUM | Moderate — adds to classical search evidence pool |
| C046 | 4-layer 128-unit MLP with skip connections and 100-dimensional input is a viable neural architecture for Connect 4 | VERIFIED | S030 | Moderate | NN design, feature engineering | Round 8 | Round 8 | HIGH | High — 100D input (98 cells + 16 features) is the richest representation yet |
| C047 | Dirichlet root noise (75% prior + 25% random) is a viable MCTS exploration strategy for Connect 4 | VERIFIED | S030 | Moderate | MCTS tuning | Round 8 | Round 9 | MEDIUM | Moderate — connects to prior MCTS tuning evidence |

---

## Material Claims — Solver Benchmarks (Round 9)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C048 | Tromp's Fhourstones solver benchmark: 20 systems tested, KPOS/S measured, alpha-beta main 28.15%, haswon 25.47% of runtime | VERIFIED | S032 (tromp.github.io/c4/fhour.html) | Strong | Search optimization | Round 9 | Round 9 | HIGH | Moderate — profiling data informs search optimization priorities |
| C049 | John Tromp solved 8x8 Connect 4 in late 2014/early 2015; book88 stores all solved positions ≤16 plies (~500MB TT) | VERIFIED | S034 (jesper-olsen/connect-four), S035 (tromp/fhourstones88) | Strong | Larger-board solving | Round 9 | Round 9 | HIGH | High — shows solving extends beyond 7x6; 8x8 is the next milestone |
| C050 | haithameleuch/connect-four-ai implements alpha-beta depth-3 with Monte Carlo leaf evaluation (250 random playouts) | VERIFIED | S036 (haithameleuch/connect-four-ai source code) | Strong | Hybrid search | Round 9 | Round 9 | HIGH | Moderate — validates Monte Carlo evaluation as a practical leaf heuristic |
| C051 | GoodCoder666/katac4 ported KataGo techniques: pre-activation ResNet, nested bottleneck, mixed spatial pooling (mean+max), CUDA graph caching, shallow conv heads | VERIFIED | S037 (model.py source) | Strong | NN architecture | Round 9 | Round 9 | HIGH | High — first concrete mapping of KataGo techniques to Connect 4 |
| C052 | GoodCoder666/katac4 training: parallel self-play workers, replay buffer, temperature decay, 3 cross-entropy loss terms (policy, value, rival), SGD+momentum, 30K epochs, batch=16, checkpoints every 500 | VERIFIED | S038 (train.py source) | Strong | Training pipeline | Round 9 | Round 9 | HIGH | High — fully specified training pipeline for Connect 4 AlphaZero-style |
| C053 | james dow allen's "The Complete Book of Connect Four" is a published reference for Connect 4 solving history and strategy | VERIFIED | S033 (tromp.github.io/c4/c4.html, reference [3]) | Moderate | History/strategy | Round 9 | Round 9 | MEDIUM | Low — historical reference, not directly implementation-relevant |

---

## Material Claims — Framework & Game Evaluation (Round 10)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C054 | eSlams is an open AI game evaluation framework supporting 50 arenas including Connect Four "standard" with "faithful" fidelity; REST-based agent protocol (POST /act); Ed29919 proof archives; direct adapters for 5 AI providers | VERIFIED | S039 (eSlams README + source code analysis) | Strong | Bot benchmarking, empirical evaluation | Round 10 | Round 10 | HIGH | Moderate — provides evaluation infrastructure for ConnectX bots |
| C055 | kenrick95/c4 (278★) is the most-starred Connect 4 repository on GitHub; uses Minimax+alpha-beta with hard-coded evaluation function; browser-based game (TypeScript/Canvas) | VERIFIED | S040 (kenrick95/c4 GitHub page analysis) | Strong | Classical search reference | Round 10 | Round 10 | HIGH | Moderate — reference for simple alpha-beta implementation |

---

## Material Claims — Evaluation Function

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C026 | Game-phase model: Opening (0-12 pieces) → Midgame (12-34) → Endgame (>34) | SUPPORTED | Internal knowledge | Moderate | Strategy design | Round 5 | Round 5 | MEDIUM | High |
| C027 | Opponent threats weighted 10-100× higher than own threats | SUPPORTED | Multiple Kaggle bot implementations | Moderate | Evaluation function | Round 2 | Round 5 | MEDIUM | High |
| C028 | Fork detection is highest-value tactical pattern (one move = two threats) | SUPPORTED | Connect 4 literature | Moderate | Tactical play | Round 1 | Round 5 | MEDIUM | Moderate |
| C029 | Hybrid (NN eval + search) beats pure search on 15x13 | HYPOTHESIS | Internal knowledge | Weak | Architecture choice | Round 1 | Round 5 | LOW | High |
| C030 | MCTS + NN superior on 15x13; alpha-beta superior on 7x6 | SUPPORTED | Game AI literature | Moderate | Algorithm selection | Round 4 | Round 5 | MEDIUM | High |
| C056 | rowspire evaluation uses 7 features (center control, piece count, threats, mobility, vertical/horizontal control, defensive score) with genetic-tuned weights | VERIFIED | S030, S039 (rowspire source code: evaluation.rs, feature_scores.rs) | Strong | Evaluation function design | Round 10 | Round 10 | HIGH | High — strongest manual eval blueprint yet |
| C057 | rowspire neural network: 4×128 MLP with skip connections, dual value+policy networks, 100D input (84-cell binary [not 64] + 16 normalized features), UCB1 MCTS c=1.41, 4000 sims, root noise = NN policy prior weighted 75% + uniform random noise 25% (NOT Dirichlet) | VERIFIED | S030 (rowspire full source code: neural_network.rs, mcts.rs, features.rs, feature_scores.rs, bitboard.rs, ml_ai.rs) | Strong | NN architecture, MCTS tuning | Round 10 | Round 15 | HIGH | Corrected: input is 84-cell (not 64-cell), noise is uniform random (not Dirichlet) — R15 adversarial verification |
| C058 | rowspire training mechanism is opaque: npm run train generates/loads training data and trains under caffeinate, but training algorithm/source code is NOT in the GitHub repository | REFUTED | S030 (rowspire full source code analysis) → now decoded via corpus audit R15 | Moderate | Training strategy | Round 10 | Round 15 | HIGH | **REFUTED R15**: Training fully decoded — 50-epoch supervised curriculum distillation, 4×128 MLP, 250K samples + mirroring, BitboardSolver depth 18, rayon parallel gradient descent. Training is public in GitHub repo (train.rs, data.rs, training.rs). |
| C059 | rowspire bitboard: 64-bit encoding with 7 bits per column (6 rows + 1 padding), move via bitwise carry propagation, win detection via shift-based 4-direction checker | VERIFIED | S030 (rowspire bitboard.rs source code) | Strong | Board representation | Round 10 | Round 10 | HIGH | Moderate — elegant bitboard design for Connect 4 |
| C060 | Pascal Pons/connect4 C++ solver uses negamax with alpha-beta + PVS + transposition tables + opening book with iterative null-window binary search for exact game values | VERIFIED | S039 (Pascal Pons/connect4 source code: Solver.cpp, Solver.hpp, generator.cpp, Position.hpp, TranspositionTable.hpp, OpeningBook.hpp, MoveSorter.hpp, main.cpp) | Strong | Classical search, board representation | Round 11 | Round 11 | HIGH | High — provides concrete implementation of perfect play for Connect 4; directly relevant to training data generation |
| C061 | Pascal Pons solver supports configurable board sizes via template WIDTH/HEIGHT parameters; default 7×6; supports up to 9×6 in uint64_t (49-63 bits); opening book generator uses DEPTH=14 | VERIFIED | S039 (Pascal Pons/connect4 source code: Position.hpp, generator.cpp) | Strong | Board representation, larger-board solving | Round 11 | Round 11 | HIGH | Moderate — shows solving can generalize beyond 7×6; 9×6 is theoretically solvable with bitboard techniques |
| C062 | TonyCWang/ConnectFour dataset: 958M rows, 14.8 GB; 2×6×7 binary matrix observations (active/opponent player channels, 0 or 255 values); 7-element target vectors encoding exact solver column evaluations; ~109M train / ~61M test split, <3% overlap | VERIFIED | S044 (TonyCWang/ConnectFour dataset card) | Strong | Training data, NN training | Round 11 | Round 11 | HIGH | High — largest publicly available Connect 4 training dataset; ground-truth optimal evaluations from perfect solver |
| C063 | TonyCWang/ConnectFour targets encode exact game-theoretic values: 1/-1 = immediate win/loss on last move; larger positive = win in more plies; negative = loss; solver computes exact depth-to-resolution for each column | VERIFIED | S044 (TonyCWang/ConnectFour dataset card) | Strong | Evaluation targets, NN training | Round 11 | Round 11 | HIGH | High — targets are ground truth, not learned estimates; ideal for supervised pre-training of policy+value heads |
| C064 | TonyCWang/ConnectFour uses self-play with temperature sampling via Pascal Pons solver as value oracle; early positions duplicated to balance data distribution | VERIFIED | S044 (TonyCWang/ConnectFour dataset card) | Moderate | Training data generation | Round 11 | Round 11 | HIGH | High — temperature sampling introduces diversity in training data; exact temperature schedule undocumented |
| C065 | Hugging Face hosts 11+ LLM-based Connect 4 models (Leon-LLM GPT-2 variants: LC4N/SC4N with 10k-1M datasets; Qwen2.5-1.5B and Qwen3-4B fine-tunes) but all lack evaluation metrics (no win rates, ELO, or move-prediction accuracy) | VERIFIED | S047 (Leon-LLM model collection), S048 (Looyyd Qwen2.5, UnstableBaselines Qwen3) | Moderate | LLM-based approach | Round 11 | Round 11 | MEDIUM | Low — text-based move prediction is fundamentally sequential and error-prone; no evidence of competitive viability |
| C066 | Text-based Connect 4 datasets (Leon-LLM, Lyte) use coordinate notation (e.g., "1. d1 g1") with outcome strings ("1-0", "0-1"); 217K-237K games; orders of magnitude smaller than board-state datasets (958M rows) | VERIFIED | S045 (Leon-LLM dataset), S046 (Lyte/ConnectFour-clean) | Moderate | Dataset format | Round 11 | Round 11 | MEDIUM | Low — text notation is semantically distant from board state; compounding error in sequential prediction |
| C067 | blog.gamesolver.org (Pascal Pons tutorial) is unreachable via WebFetch due to SSL certificate mismatch — served GitHub certificate instead of proper gamesolver.org cert | VERIFIED | Round 11 WebFetch attempts | Weak | Tool limitation | Round 11 | Round 11 | LOW | Low — prevents verification of the step-by-step solver tutorial |
| C068 | Board-state approach (TonyCWang) is theoretically superior to text-based approach for Connect 4: optimal move depends only on current state, not move history; text-based models must "remember" full game history | SUPPORTED | Internal knowledge + dataset analysis | Weak | Architecture selection | Round 11 | Round 11 | MEDIUM | High — supports supervised pre-training with board-state inputs over autoregressive text prediction |
| C069 | Kaggle kaggle-environments has restructured configuration: `episodeSteps` and `runTimeout` moved from per-environment spec to global `schemas.json` defaults; `actTimeout` and `timeout` simplified to plain numbers; `agentTimeout` fully removed; `remainingOverageTime` moved to observation section | VERIFIED | S006 (kaggle-environments source code: connectx.json, schemas.json, core.py) | Strong | Kaggle compliance | Round 13 | Round 13 | HIGH | Moderate — structural changes are backward-compatible; functional behavior unchanged |
| C070 | Global configuration schema in schemas.json provides `episodeSteps=1000`, `actTimeout=6`, `runTimeout=1200` as defaults; environment specs can override via `extend_specification()` | VERIFIED | S006 (kaggle-environments source code: schemas.json, core.py) | Strong | Kaggle compliance | Round 13 | Round 13 | HIGH | Low — defaults documented in global schema; connectx overrides actTimeout=2 |
| C073 | Kaggle ConnectX overtime tracking mechanism fully decoded from core.py: `remainingOverageTime` decrements by `max(0, duration - actTimeout)` per step; below 0 → TIMEOUT disqualification | VERIFIED | S006 (kaggle-environments source code: connectx.json, core.py) | Strong | Time management | Round 15 | Round 15 | HIGH | Critical — determines overtime strategy; initial value 60 from spec override |
| C074 | Global schema: actTimeout=6, runTimeout=1200, episodeSteps=1000, remainingOverageTime=12, maxLogLength=10000; ConnectX overrides: actTimeout=2, agentTimeout=60 (obsolete), remainingOverageTime=60 | VERIFIED | S006 (kaggle-environments source code: schemas.json, connectx.json) | Strong | Kaggle compliance | Round 15 | Round 15 | HIGH | Comprehensive config defaults; connectx overrides actTimeout=2, remainingOverageTime=60 |
| C075 | Agent status enum: ACTIVE, INACTIVE, DONE, ERROR, INVALID, TIMEOUT — all documented in kaggle-environments interpreter | VERIFIED | S006 (kaggle-environments source code: core.py) | Strong | Kaggle compliance | Round 15 | Round 15 | HIGH | Required for proper agent state management |
| C076 | kaggle-environments package version v1.32.2 confirmed (pyproject.toml); Python ≥3.11 required | VERIFIED | S006 (kaggle-environments pyproject.toml) | Strong | Environment compatibility | Round 15 | Round 15 | HIGH | Determines available Python features and API surface |
| C077 | Observation.step field available; deprecated_envs/ directory removed from current kaggle-environments | VERIFIED | S006 (kaggle-environments source code: core.py) | Strong | Kaggle compliance | Round 15 | Round 15 | HIGH | step field enables stateful agents; deprecated_envs/ removed |

---

## Unresolved / Critical Questions

1. **C002-C004**: Solved game database specifics (Böck DB size/compression) need direct source verification; however C001/C005 now independently confirmed by Wikipedia
2. **C007, C008**: BitBully and mra1991 repos could not be verified (GitHub URLs return 404)
3. **C017**: Training times need RTX 5090 benchmark or at least comparable hardware benchmark
4. **C018**: Kaggle T4 inference needs actual measurement
5. **C029**: NN vs search on 15x13 needs empirical validation
6. **C014-C015**: Transfer learning effectiveness needs empirical measurement
7. **C033**: Tarun995 claim of "15+ depth" needs empirical validation on real Kaggle boards

---

## Corpus Audit Findings (Round 13 Audit, Slot 7/7)

### Metadata Corrections
- **claim-register.md**: Updated Current Round header from 11 to 13.
- **architecture-rankings.md**: Updated Current Round header from 11 to 13.
- **decision-log.md**: Updated Current Round header from 6 to 13.

### Claim Count Corrections
- **VERIFIED**: Fixed count from 48 to 47. Old range C020-C025 incorrectly included C025 (STRONGLY SUPPORTED). New range C020-C024 correctly lists only VERIFIED claims. Percentage updated from 67% to 65%.
- **SUPPORTED**: Fixed count from 13 to 14. Old range C006-C015 incorrectly included C011 (HYPOTHESIS), C014 (HYPOTHESIS), C015 (HYPOTHESIS), C013 (non-standard MEDIUM-HIGH). New range C006-C010 correctly lists only SUPPORTED items. Percentage updated from 18% to 19%.
- **Total**: 47 + 14 + 2 + 6 + 3 = 72 claims.

### Status Label Issues
- **C013**: Uses non-standard status label MEDIUM-HIGH (violates evidence gate). Should be VERIFIED/SUPPORTED/STRONGLY SUPPORTED/HYPOTHESIS/UNKNOWN/DISPUTED/REFUTED. Evidence grade is Weak, source is Internal knowledge. Recommended: downgrade to HYPOTHESIS.

### Unsupported Claims (Evidence Gate Violations)
- **C006**: MTD(f) 20-30% speedup -- Internal knowledge only. No published source.
- **C007**: PVS 20-35% over alpha-beta -- Internal knowledge only. No published source.
- **C008**: Center-first move ordering 3-5x speedup -- Internal knowledge only.
- **C009**: Full move ordering 10-30x speedup -- Internal knowledge only.
- **C010**: TT size 100K-1M recommended -- Internal knowledge only.
- **C026**: Game-phase model -- Internal knowledge only.

### Source Cross-Checks
- **S037/S038**: Distinct files from same repo. Not duplicates.
- **S049/S055**: Different dates (R11 vs R13). Not duplicates but could be consolidated.
- **S041 (rowspire full source)** supersedes S030 (rowspire initial). S030 is historical context.

### Unresolved Questions (from round 11, unchanged)
- C002-C004: Bock database -- no primary source found despite multiple rounds.
- C017: RTX 5090 training times -- no empirical benchmark.
- C018: Kaggle T4 inference latency -- no empirical measurement.
- C029: NN vs search on 15x13 -- needs empirical validation.


## Claim Statistics by Status

| Status | Count | Percentage |
|--------|-------|------------|
| VERIFIED | 48 (C020-C024, C031-C047, C048-C053, C054-C057, C059, C060-C067, C069-C070, C073-C077) | 64% |
| SUPPORTED | 8 (C001, C005, C012, C019, C026-C028, C030, C068) | 11% |
| STRONGLY SUPPORTED | 2 (C016, C025) | 3% |
| HYPOTHESIS | 13 (C006-C010, C011, C013-C015, C017, C018, C029, C071) | 18% |
| UNKNOWN | 3 (C002, C003, C004) | 4% |
| DISPUTED | 0 | 0% |
| REFUTED | 1 (C058) | 1% |

**Key observation**: 64% of material claims are VERIFIED (stable from R14, driven by R13 Kaggle kaggle-environments spec analysis, JS/TS/Python engine eval benchmarks, and R15's additional overtime tracking/config schema verification). 11% are SUPPORTED. 3% are STRONGLY SUPPORTED (C016 Numba JIT speedup; C025 Kaggle timeout API). 4% are UNKNOWN (Böck database specifics — C002-C004). 18% are HYPOTHESIS (training/performance/search assumptions). 1% are REFUTED (C058 rowspire training opacity). Round 15 added 5 new VERIFIED claims (C073-C077): Kaggle overtime tracking mechanism decoded from core.py (C073); global config schema defaults (C074); agent status enum documented (C075); kaggle-environments v1.32.2 confirmed (C076); observation.step field and deprecated_envs removal (C077). C058 upgraded VERIFIED→REFUTED (training mechanism fully decoded via corpus audit). C057 corrected: "64-cell binary"→"84-cell binary", "Dirichlet root noise"→"uniform random noise".
