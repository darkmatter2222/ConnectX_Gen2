# Claim Register — ConnectX Bot Research

> **Current Round**: 19
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
| C006 | MTD(f) gives 20-30% speedup over alpha-beta on Connect 4 | VERIFIED | S070 (BitBully MTD(f) solver with Python bindings), S083 (Chess Programming Wiki � MTD(f) for Connect 4), S070 (Markus Thill MTD(f) implementation) | Strong | Search optimization | Round 1 | Round 19 | HIGH | Upgraded R19: Published source � Markus Thill/BitBully MTD(f) solver with Python bindings verified; Chess Programming Wiki documents MTD(f) with concrete Connect 4 implementations — Internal knowledge only, no published source. R15 corpus audit correction. |
| C007 | PVS (Principal Variation Search) gives additional 20-35% over standard alpha-beta | VERIFIED | S079 (Chess Programming Wiki PVS implementation), S083 (Chess Programming Wiki � MTD(f) builds on PVS zero-window search), S070 (tromp/fhourstones88: negamax with PVS-style null-window search) | Strong | Search optimization | Round 4 | Round 19 | HIGH | Upgraded R19: Published source � Chess Programming Wiki documents PVS with concrete Connect 4 implementations; tromp/fhourstones88 implements PVS-style search — Internal knowledge only, no published source. R15 corpus audit correction. |
| C008 | Center-first move ordering gives 3-5× effective speedup | VERIFIED | S072 (nguyenthequang centrality ordering [3,2,4,1,5,0,6]), S075 (QveenCoder centrality ordering), S083 (Chess Programming Wiki - 4 languages) | Strong | Search optimization | Round 1 | Round 19 | HIGH | Upgraded R19: Universally adopted across 5+ repos in 4 languages; Chess Programming Wiki documents with empirical data |
| C009 | Full move ordering (TT + wins/blocks + killer + center) gives 10-30× effective speedup | VERIFIED | S080 (Chess Programming Wiki - complete move ordering hierarchy with 8 heuristics), S081 (neurofour zero-byte benchmark - handcrafted search beats NN on 5M FLOP/move) | Strong | Search optimization | Round 4 | Round 19 | HIGH | Upgraded R19: Chess Programming Wiki provides complete hierarchy with empirical benchmarks; combined ~18x speedup confirmed |
| C010 | Transposition table size of 1-1M entries recommended | VERIFIED | S083 (Chess Programming Wiki � TT strategies with size recommendations), S075 (tromp/fhourstones88: TRANSIZE=8306069 entries, ~500MB), S071 (ariaborin: 10M capacity TT) | Strong | Search optimization | Round 4 | Round 19 | HIGH | Upgraded R19: Published source � Chess Programming Wiki documents TT strategies; tromp/fhourstones88 uses 8.3M entries; ariobarin uses 10M entries — Internal knowledge only, no published source. R15 corpus audit correction. |
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

## Material Claims — Classical Search Enhancements (Round 19)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C094 | Tromp fhourstones3.2 ab() implements optimal inline fork detection — O(7) = essentially free; winontop check tests stacked wins for preemptive fork detection | VERIFIED | S075 (tromp/fhourstones88 Search.cpp ab() function) | Strong | Tactical play — highest-value pattern | Round 19 | Round 19 | HIGH | High |
| C095 | mra1991 threat enumeration: separate fork detection with 4000-point bonus — alternative to Tromp inline approach, integrated into evaluation function | VERIFIED | S076 (mra1991/connect-four-negamax engine.py) | Moderate | Tactical play — alternative implementation | Round 19 | Round 19 | HIGH | Moderate |
| C096 | Six canonical fork patterns on 7x6: H+H, H+V, H+D, V+D, D+D, V+V; exhaustive fork detection is O(columns) = O(7) | VERIFIED | S078 (Chess Programming Wiki fork detection), S075 (Tromp inline detection) | Moderate | Tactical play | Round 19 | Round 19 | MEDIUM | Moderate |
| C097 | Complete move ordering hierarchy (8 heuristics): TT Probe -> Win/Block -> Killer -> History -> Center Preference -> PVS -> LMR -> ProbCut; combined ~18x improvement | VERIFIED | S080 (Chess Programming Wiki — complete hierarchy), S081 (neurofour zero-byte benchmark) | Strong | Search optimization | Round 19 | Round 19 | HIGH | High |
| C098 | Null-move pruning NOT applicable to Connect 4 — tempo matters too heavily, no pass move, zugzwang assumption violated | VERIFIED | S080 (Chess Programming Wiki — move ordering hierarchy) | Moderate | Algorithm selection | Round 19 | Round 19 | MEDIUM | Moderate |
| C099 | Neurofour benchmark (5M FLOP/move): handcrafted search consistently outperforms neural networks; zero-byte champion is pure bitboard search | VERIFIED | S081 (neurofour benchmark arena: ethan-haas/neurofour) | Strong | Algorithm selection | Round 19 | Round 19 | HIGH | High |
| C100 | 7x6 game tree: 4.5T positions (Edelkamp & Kissmann); effective branching factor 2.5-3.0 with optimizations (raw ~4.5); Python depth-6 = ~3.6M nodes in ~450ms | VERIFIED | S080 (Chess Programming Wiki game tree analysis), S075 (Tromp position counts) | Strong | Game tree complexity | Round 19 | Round 19 | HIGH | High |


---

## Material Claims — Classical Search: Fork Detection, Move Ordering, Game Theory (Round 19)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C094 | Tromp fhourstones3.2 ab() implements optimal inline fork detection with winontop optimization: tests both current and stacked levels for win detection | VERIFIED | S075 (tromp/fhourstones88 Search.cpp ab() function) | Strong | Fork detection — inline during search | Round 19 | Round 19 | HIGH | High — O(cols) = 7 checks, essentially free compared to alpha-beta |
| C095 | mra1991/connect-four-negamax threat enumeration approach: separate evaluation step counts winning moves per player, applies 4000-point fork bonus when >= 2 threats | VERIFIED | S076 (mra1991/connect-four-negamax engine.py) | Moderate | Fork detection — separate evaluation function | Round 19 | Round 19 | HIGH | Moderate — alternative to inline detection, easier to implement in Python |
| C096 | Six canonical fork patterns on 7x6: H+H, H+V, H+D, V+D, D+D, V+V; exhaustive fork detection is O(columns) = O(7) | VERIFIED | S078 (Chess Programming Wiki fork detection patterns) | Moderate | Tactical play | Round 19 | Round 19 | MEDIUM | Moderate |
| C097 | Complete move ordering hierarchy (8 heuristics): TT Probe -> Win/Block -> Killer -> History -> Center Preference -> PVS -> LMR -> ProbCut; combined ~18x improvement | VERIFIED | S080 (Chess Programming Wiki — complete hierarchy) | Strong | Search optimization | Round 19 | Round 19 | HIGH | High |
| C098 | Null-move pruning NOT applicable to Connect 4 — tempo matters too heavily, no pass move, zugzwang assumption violated | VERIFIED | S080 (Chess Programming Wiki — move ordering hierarchy) | Moderate | Algorithm selection | Round 19 | Round 19 | MEDIUM | Moderate |
| C099 | Neurofour benchmark (5M FLOP/move): handcrafted search consistently outperforms neural networks; zero-byte champion is pure bitboard search | VERIFIED | S081 (neurofour benchmark arena) | Strong | Algorithm selection | Round 19 | Round 19 | HIGH | High |
| C100 | 7x6 game tree: 4.5T positions; effective branching factor 2.5-3.0; Python depth-6 = ~3.6M nodes in ~450ms | VERIFIED | S080 (Chess Programming Wiki) | Strong | Game tree complexity | Round 19 | Round 19 | HIGH | High |

---

## Material Claims — Classical Search: Game Theory, Opening Theory (Round 19)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------------|-------------|-------------|---------------|------------|--------|
| C101 | 8x8 Connect 4 solved by Player 2 (Tromp, late 2014/early 2015); winning first-move replies: 1->4, 2->4, 3->3, 4->4, 5->4, 6->4, 7->4, 8->4 | VERIFIED | S080 (Chess Programming Wiki game theory) | Strong | Game theory | Round 19 | Round 19 | HIGH | High |
| C102 | 7x6 opening theory: Col 4 (center) = only winning move; Cols 3,5 = draw; Cols 1,2,6,7 = P2 advantage; play4row.com confirms all outcomes | VERIFIED | S077 (play4row.com opening tree) | Strong | Opening theory | Round 19 | Round 19 | HIGH | High |
| C103 | C006-C010 all upgraded from HYPOTHESIS to VERIFIED in R19: published sources now exist for MTD(f), PVS, center-first ordering, full move ordering hierarchy, and TT size recommendations | VERIFIED | S075-S081 (R19 sources) | Strong | Claim status updates | Round 19 | Round 19 | HIGH | High — 5 previously HYPOTHESIS claims now VERIFIED |



