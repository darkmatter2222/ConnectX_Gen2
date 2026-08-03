# Claim Register — ConnectX Bot Research

> **Current Round**: 17
> **Last Updated**: 2026-08-03

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
| C006 | MTD(f) gives 20-30% speedup over alpha-beta on Connect 4 | HYPOTHESIS | Internal knowledge | Moderate | All board sizes | Round 1 | Round 17 | MEDIUM | Downgraded R17: Evidence gate violation — Internal knowledge only, no published source. R15 corpus audit correction. |
| C007 | PVS (Principal Variation Search) gives additional 20-35% over standard alpha-beta | HYPOTHESIS | Internal knowledge | Moderate | All board sizes | Round 4 | Round 17 | MEDIUM | Downgraded R17: Evidence gate violation — Internal knowledge only, no published source. R15 corpus audit correction. |
| C008 | Center-first move ordering gives 3-5× effective speedup | HYPOTHESIS | Internal knowledge | Moderate | All board sizes | Round 1 | Round 17 | MEDIUM | Downgraded R17: Evidence gate violation — Internal knowledge only, no published source. R15 corpus audit correction. |
| C009 | Full move ordering (TT + wins/blocks + killer + center) gives 10-30× effective speedup | HYPOTHESIS | Internal knowledge | Moderate | All board sizes | Round 4 | Round 17 | MEDIUM | Downgraded R17: Evidence gate violation — Internal knowledge only, no published source. R15 corpus audit correction. |
| C010 | Transposition table size of 1-1M entries recommended | HYPOTHESIS | Internal knowledge | Moderate | All board sizes | Round 4 | Round 17 | MEDIUM | Downgraded R17: Evidence gate violation — Internal knowledge only, no published source. R15 corpus audit correction. |
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
| C026 | Game-phase model: Opening (0-12 pieces) → Midgame (12-34) → Endgame (>34) | HYPOTHESIS | Internal knowledge | Moderate | Strategy design | Round 5 | Round 17 | MEDIUM | Downgraded R17: Evidence gate violation — Internal knowledge only, no published source. R15 corpus audit correction. |
| C027 | Opponent threats weighted 10-100× higher than own threats | SUPPORTED | Multiple Kaggle bot implementations | Moderate | Evaluation function | Round 2 | Round 5 | MEDIUM | High |
| C028 | Fork detection is highest-value tactical pattern (one move = two threats) | SUPPORTED | Connect 4 literature | Moderate | Tactical play | Round 1 | Round 5 | MEDIUM | Moderate |
| C029 | Hybrid (NN eval + search) beats pure search on 15x13 | HYPOTHESIS | Internal knowledge | Weak | Architecture choice | Round 1 | Round 5 | LOW | High |
| C030 | MCTS + NN superior on 15x13; alpha-beta superior on 7x6 | SUPPORTED | Game AI literature | Moderate | Algorithm selection | Round 4 | Round 5 | MEDIUM | High |
| C056 | rowspire evaluation uses 7 features (center control, piece count, threats, mobility, vertical/horizontal control, defensive score) with genetic-tuned weights | VERIFIED | S030, S039 (rowspire source code: evaluation.rs, feature_scores.rs) | Strong | Evaluation function design | Round 10 | Round 10 | HIGH | High — strongest manual eval blueprint yet |
| C057 | rowspire neural network: 4×128 MLP with skip connections, dual value+policy networks, 100D input (84-cell binary [not 64] + 16 normalized features), UCB1 MCTS c=1.41, 4000 sims, root noise = NN policy prior weighted 75% + uniform random noise 25% (NOT Dirichlet) | VERIFIED | S030 (rowspire full source code: neural_network.rs, mcts.rs, features.rs, feature_scores.rs, bitboard.rs, ml_ai.rs) | Strong | NN architecture, MCTS tuning | Round 10 | Round 15 | HIGH | Corrected: input is 84-cell (not 64-cell), noise is uniform random (not Dirichlet) — R15 adversarial verification |
| C058 | rowspire training mechanism is opaque: npm run train generates/loads training data and trains under caffeinate, but training algorithm/source code is NOT in the GitHub repository | REFUTED | S030 (rowspire full source code analysis) → now decoded via corpus audit R15 | Moderate | Training strategy | Round 10 | Round 15 | HIGH | **REFUTED R15**: Training fully decoded — 50-epoch supervised curriculum distillation, 4×128 MLP, 250K samples + mirroring, BitboardSolver depth 18, rayon parallel gradient descent. Training is public in GitHub repo (train.rs, data.rs, training.rs). |
| C059 | rowspire bitboard: 64-bit encoding with 7 bits per column (6 rows + 1 padding), move via bitwise carry propagation, win detection via shift-based 4-direction checker | VERIFIED | S030 (rowspire bitboard.rs source code) | Strong | Board representation | Round 10 | Round 10 | HIGH | Moderate — elegant bitboard design for Connect 4 |
| C060 | Pascal Pons/connect4 C++ solver uses negamax with alpha-beta (no PVS) + transposition tables + opening book with iterative null-window binary search for exact game values | VERIFIED | S039 (Pascal Pons/connect4 source code: Solver.cpp, Solver.hpp, generator.cpp, Position.hpp, TranspositionTable.hpp, OpeningBook.hpp, MoveSorter.hpp, main.cpp) | Strong | Classical search, board representation | Round 11 | Round 17 (corrected: PVS removed — solver uses alpha-beta only) | HIGH | High — provides concrete implementation of perfect play for Connect 4; directly relevant to training data generation |
| C061 | Pascal Pons solver supports configurable board sizes via static constexpr template WIDTH/HEIGHT defaults; default 7×6; supports up to 9×6 in uint64_t (49-63 bits); opening book generator uses DEPTH=14; board sizes are compile-time constants (static constexpr, not runtime-configurable) | VERIFIED | S039 (Pascal Pons/connect4 source code: Position.hpp, generator.cpp) | Strong | Board representation, larger-board solving | Round 11 | Round 17 (corrected: static constexpr board sizes, not runtime template parameters) | HIGH | Moderate — shows solving can generalize beyond 7×6; 9×6 is theoretically solvable with bitboard techniques |
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
 field available; deprecated_envs/ directory removed from current kaggle-environments | VERIFIED | S006 (kaggle-environments source code: core.py) | Strong | Kaggle compliance | Round 15 | Round 15 | HIGH | step field enables stateful agents; deprecated_envs/ removed |
| C078 | Tromp (2015) 8x8 solver includes book88 — a binary database of all solved positions up to 16 plies, loaded at startup into BookMap hash table via read(bd, &bb, BBYTES) then read(bd, &rslt, sizeof(short)). C488 binary accepts positions via stdin and solves instantly from book. Positions with work >= BOOKWORK (24) dynamically added. ~500MB memory default (TRANSIZE=8306069). | VERIFIED | S066 (tromp/fhourstones88 source code: Book class in Search.cpp, book88 binary file) | Strong | Classical search, opening books | Round 16 | Round 16 | HIGH | High — first detailed binary opening book format found with complete source code and downloadable binary; demonstrates book generation at solving time and dynamic extension |
| C079 | Pascal Pons/connect4 OpeningBook.hpp + generator.cpp implements opening book generation at build time; DEPTH=14 for 7x6 board; configurable board sizes via template WIDTH/HEIGHT (up to 9x6 in uint64_t); AGPL v3 license | VERIFIED | S067 (Pascal Pons/connect4 source: OpeningBook.hpp, generator.cpp) | Strong | Classical search, opening books | Round 16 | Round 16 | HIGH | High — only open-source C++ opening book generator with configurable depth and board size; no binary book distributed |
| C080 | tristan852/kite Java solver implements 15-ply opening book as compiled cache (opening.cfc, 95.6 MB): 32 MiB bucket seeds (2^25 entries) + 58.9 MiB 6-bit packed scores (range -18 to +39, offset by -18); three-key mixed hash (0x9E3779B97F4A7C15L, 0xBF58476D1CE4E5B9L, 0x94D049BB133111EBL); lookup at filledCellAmount <= 15 | VERIFIED | S069 (kite source: OpeningBoardScoreCache.java, Board.java evaluate()) | Strong | Classical search, opening books | Round 16 | Round 16 | HIGH | High — most space-efficient opening book implementation: 95.6 MB compressed for all positions up to 15 ply vs ~500MB for Tromp 8x8; compiled cache format avoids runtime generation cost |
| C081 | Kite outperforms C++ (Fhourstones, Pascal Pons) and Rust (Ben Rall) solvers on Pascal Pons benchmark: endgame-easy 1.90us (vs 4.27-4.57), midgame-easy 22.22us (vs 32.20-137), midgame-medium 961us (vs 2.87-3.21ms), opening-easy 47.56us (vs 42us-150ms), opening-medium 716us (vs 7.44-96ms), opening-hard 22us (vs 1.40ms-5.5s); 17.84-20.72 Mnodes/s throughput | VERIFIED | S068 (kite README benchmark results) | Strong | Performance benchmark | Round 16 | Round 16 | HIGH | High — establishes current state-of-the-art in Connect 4 solver performance; opening-hard benchmark specifically demonstrates opening book effectiveness (22us vs 5.5s for Fhourstones without book) |
| C082 | Kite evaluates opening book positions at OPENING_SCORE_CACHE_MAXIMAL_DEPTH=15 ply using boardScore(mixedHash) as first-stage lookup before alpha-beta search; symmetry reduction applied before book lookup; boardScore returns 6-bit score offset by -18 (0=draw, 1-39=win, -18 to -1=loss) | VERIFIED | S069 (kite source: Board.java evaluate(), OpeningBoardScoreCache.java boardScore()) | Strong | Classical search, board representation | Round 16 | Round 16 | HIGH | Moderate — opening book is first-stage cache before search; score format compatible with alpha-beta; used only at depth 15 or less (positions with >15 pieces search normally) |

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
| VERIFIED | 56 (C020-C024, C031-C047, C048-C053, C054-C057, C059, C060-C067, C069-C070, C072, C073-C077, C078-C084) | 68% |
| SUPPORTED | 3 (C001, C005, C012, C019) — downgraded C006-C010 and C026 to HYPOTHESIS in R17 | 4% |
| STRONGLY SUPPORTED | 2 (C016, C025) | 2% |
| HYPOTHESIS | 19 (C006-C010, C011, C013-C015, C017, C018, C026, C029, C071) — R17: C006-C010 and C026 downgraded from SUPPORTED | 23% |
| UNKNOWN | 3 (C002, C003, C004) | 4% |
| DISPUTED | 0 | 0% |
| REFUTED | 1 (C058) | 1% |

**Key observation**: 68% of material claims are VERIFIED (R16: +7 GPU claims C078-C084, +7 sources S059-S065; R17: R15 evidence gate violations corrected — C006-C010 and C026 downgraded from SUPPORTED to HYPOTHESIS). 4% are SUPPORTED (C001 Wikipedia, C005 Wikipedia, C012 SFT→RL training, C019 ONNX deployment). 2% are STRONGLY SUPPORTED (C016 Numba JIT; C025 Kaggle timeout API). 23% are HYPOTHESIS (up from 15% after R17 downgrades). 4% are UNKNOWN (Böck database specifics — C002-C004). 1% are REFUTED (C058 rowspire training opacity — R15 decoded, R17 cleaned up unverified details). Total: 82 claims (C001-C084, minus C012/SUPPORTED and C013/HYPOTHESIS misclassification). R17 corpus audit corrections: 6 claims downgraded from SUPPORTED to HYPOTHESIS per evidence gate requirements (Internal knowledge only, no published external source). VERIFIED claims C078-C084 from R16 GPU/Parallel Search lane (Liang Li et al. 2012, MCTS-NC Klęsk, Navade788, Project-Artetra, Ala'anzy 2026 taxonomy).

---

## Material Claims — GPU Accelerated Search (Round 16)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C078 | GPU-accelerated Connect 6 game tree search (Liang Li et al. 2012) achieves 70.8× speedup without pruning, 10.58× with pruning; 7.26× on Chess — proving GPUs are a feasible way to accelerate game tree algorithms | VERIFIED | S060 (Liang Li et al. 2012 conference paper) | Strong | GPU search acceleration; techniques transferable to Connect 4/ConnectX | Round 16 | Round 16 | HIGH | High — establishes theoretical foundation for GPU-based Connect 4 search acceleration; speedup factors are empirically measured |
| C079 | MCTS-NC (Klęsk) implements four GPU-accelerated MCTS variants for Connect 4 using numba.cuda: ocp_thrifty, ocp_prodigal, acp_thrifty, acp_prodigal — all variants significantly outperform vanilla MCTS (2.5-2.875% avg score baseline vs 43.8-75.1% for GPU variants) | VERIFIED | S061 (pklesk/mcts_numba_cuda GitHub + paper) | Strong | MCTS on GPU; directly applicable to ConnectX if MCTS approach chosen | Round 16 | Round 16 | HIGH | High — provides first concrete open-source GPU MCTS implementation for Connect 4 with benchmarked performance |
| C080 | MCTS-NC acp_prodigal variant achieves 20.3M playouts in 5 seconds on AMD EPYC + NVIDIA GRID A100, averaging 8.62 search depth (max 17.54) — demonstrates GPU throughput orders of magnitude higher than CPU-only MCTS | VERIFIED | S061 (pklesk/mcts_numba_cuda performance benchmarks) | Strong | Performance planning; shows GPU MCTS feasibility for Kaggle T4 (lower spec than GRID A100) | Round 16 | Round 16 | HIGH | High — quantitative performance benchmark for GPU MCTS on Connect 4; informs time-budget allocation |
| C081 | Navade788/gpu-connect4-cuda demonstrates independent GPU-player architecture: two CUDA-compiled agents compete with one using random moves and one using pattern-analysis; board state transfers between host/device memory after each turn | VERIFIED | S062 (Navade788/gpu-connect4-cuda GitHub repo) | Moderate | GPU-based game simulation architecture; demonstrates feasibility but lacks sophisticated search | Round 16 | Round 16 | MEDIUM | Moderate — proof-of-concept for GPU Connect 4; not competitive but demonstrates CUDA feasibility |
| C082 | Project-Artetra (brightonanc) is an in-progress Connect 4 AI targeting CUDA parallel search with alpha-beta, negamax, and PVS — source code incomplete (only directory structure visible, no .cu/.cpp files committed) | VERIFIED | S063 (brightonanc/Project-Artetra GitHub repo) | Weak | Indicates community interest in GPU Connect 4 search; not yet useful for benchmarking | Round 16 | Round 16 | LOW | Low — work-in-progress, no implementation details available |
| C083 | GPU-accelerated MCTS (MCTS-NC) using lock-free design with no atomics or mutexes is possible: OCP evaluates one random child per expanded leaf; ACP evaluates all children — two execution models × two memory modes = four variants | VERIFIED | S061 (MCTS-NC implementation documentation) | Strong | Parallelization strategy for GPU search; applicable to both MCTS and alpha-beta on GPU | Round 16 | Round 16 | HIGH | High — novel parallelization strategy avoids GPU synchronization overhead, enabling higher throughput |
| C084 | Ala'anzy & Madiyarova (2026) published peer-reviewed taxonomy paper in MDPI Symmetry covering all Connect 4 AI methods: game theory, classical search (alpha-beta, MTD(f)), MCTS, RL, XAI, and formal verification — reviewer recommended more combinatorial game theory examples | VERIFIED | S059 (MDPI Symmetry 18(2)293; Semantic Scholar metadata) | Moderate | Comprehensive overview of Connect 4 AI landscape; validates GPU as one of many explored approaches | Round 16 | Round 16 | MEDIUM | Moderate — provides authoritative taxonomy of all Connect 4 AI approaches, including GPU acceleration |


## Material Claims — Rowsire Evaluation Weights (Round 17)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C085 | Rowspire genetic tuning default parameters (genetic_params.rs): win_score=10000, loss_score=-10000, center_column=165, adjacent_center=97, outer_column=17, edge_column=6, row_height_weight=1.798, center_control_weight=2.022, piece_count_weight=0.965, threat_weight=1.588, mobility_weight=1.453, vertical_control_weight=2.862, horizontal_control_weight=1.344, defensive_weight=1.372 | VERIFIED | S068 (genetic_params.rs default impl) | Strong | Evaluation function design — default starting values for genetic tuning | Round 17 | Round 17 | HIGH | High — complete default parameter set for rowspire's 7-feature evaluation |
| C086 | Rowspire evolved genetic parameters (generation 2, evolved.json): center=91 (↓45% from default 165), adjacent=30 (↓69%), threat_weight=3.851 (↑142%), horizontal_control=2.840 (↑112%), vertical_control=1.335 (↓53%), piece_count=0.113 (↓88%), defensive=0.992 (↓28%). Evolution converges toward threat-focused, horizontally-aware evaluation. | VERIFIED | S066 (evolved.json) | Strong | Evaluation function design — evolved optimal values | Round 17 | Round 17 | HIGH | High — actual evolved values differ significantly from defaults; threat_weight is the highest-weighted feature post-evolution |
| C087 | Rowspire evaluation formula: score = (positional_score(P1) + weighted_feature_score(P1)) − (positional_score(P2) + weighted_feature_score(P2)); positional_score = Σ(column_value × row_height × row_height_weight); weighted_feature_score = Σ(feature_score × feature_weight) cast to i32 | VERIFIED | S070 (evaluation.rs) | Strong | Evaluation function — complete formula | Round 17 | Round 17 | HIGH | High — full formula available for direct implementation |
| C088 | Rowspire 16D feature encoding (feature_scores.rs): center, pieces, threats, mobility, vertical, horizontal, diagonal, blocking — with opponent mirroring for 14 features + player indicator ±1 | VERIFIED | S069 (feature_scores.rs) | Strong | Board representation — feature engineering | Round 17 | Round 17 | HIGH | High — 16 features is richer than R10's 16 normalized features; includes diagonal and blocking not in R10 |
| C089 | Rowspire evaluation_lines.rs extends threat scoring: 4-in-row=1000, 3-unblocked=100, 3-blocked=10, 2-unblocked=10, 2-blocked=1, 1-unblocked=1 (new: +1 for single piece in open line), else 0 | VERIFIED | S071 (evaluation_lines.rs) | Strong | Evaluation function — fine-grained scoring | Round 17 | Round 17 | MEDIUM | Moderate — the 1-unblocked=1 is new vs R10; captures positional value of isolated pieces |
| C090 | Rowspire defensive scoring: counts opponent's winning moves if they play next; each = 5000 points penalty | VERIFIED | S070 (evaluation.rs defensive_score()) | Strong | Tactical evaluation — opponent threat prevention | Round 17 | Round 17 | HIGH | High — defensive move detection is the highest single-value tactical feature (5000 per move); evolved weight 0.992 makes it ~5000 per threat |
| C091 | Rowspire resources/ai/ directory contains two files: evolved.json (generation 2 genetic parameters) and ml_ai_weights_best.json (best neural network weights). Both are public data files. | VERIFIED | S066, S067 | Strong | Deployment strategy — weights are public, not hidden | Round 17 | Round 17 | MEDIUM | Moderate — confirms weights/resources are publicly accessible, resolves GH-009 |
| C092 | Rowspire genetic_params.rs uses serde (Serialize/Deserialize) + ts-rs (TypeScript export via #[ts(export)]); parameters are persisted as JSON and loaded from resources/ai/evolved.json | VERIFIED | S068 (genetic_params.rs), S066 (evolved.json) | Strong | Data pipeline — JSON-based parameter transfer | Round 17 | Round 17 | MEDIUM | Moderate — confirms JSON format is the parameter exchange mechanism; Kaggle-compatible |
| C093 | Rowspire repository structure has changed significantly since R16: added src/ (top-level), evaluation_lines.rs, features_tests.rs, genetic_params.rs, game.rs, network_training.rs, rules.rs, search_ai.rs, wasm_api.rs, ml_ai_tests.rs, ml_types.rs, network_layer.rs, neural_network_tests.rs, mcts_tests.rs, bin/ subdirectory | VERIFIED | S068, S070 | Strong | Source code evolution tracking | Round 17 | Round 17 | LOW | Low — structural change only; no functional impact on existing findings |
