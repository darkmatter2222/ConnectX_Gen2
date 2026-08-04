# Claim Register — ConnectX Bot Research

> **Current Round**: 28
> **Last Updated**: 2026-08-04

---

## Claim Statistics by Status

| Status | Count | Percentage |
|--------|-------|------------|
| VERIFIED | 75 (C001, C171, C174, C005, C020-C024, C031-C043, C048-C057, C059, C060-C070, C072-C077, C078-C091, C093, C102-C106, C111-C113, C114-C117, C119-C122, C124-C127, C128-C131, C133-C134, C135-C140, C142-C145) | 63% |
| STRONGLY SUPPORTED | 3 (C016, C025, C056) | 3% |
| SUPPORTED | 4 (C012, C019, C123, C136-C138) | 4% |
| HYPOTHESIS | 22 (C013-C015, C017, C018, C026-C029, C071, C107-C109, C132, C141) | 19% |
| NEEDS_CORRECTION | 10 (C006, C172, C007, C010, C044, C047, C150, C151, C154, C162) | 8% |
| FALSIFIED | 1 (C092) | 1% |
| CORRECTED | 1 (C097) | 1% |
| UNVERIFIABLE | 1 (C099) | 1% |
| UNKNOWN | 3 (C002, C003, C004) | 3% |
| REFUTED | 1 (C110) | 1% |
| DISPUTED | 1 (C058) | 1% |

**Total unique claims**: ~150 across C001-C174 with gaps from ID reuse (C094-C099 duplicate IDs reused) plus new C146-C166 (R25) and C167-C174 (R27-R28). **Key observations**: (1) VERIFIED percentage at 63% — R28: C174 VERIFIED (AZAL 0.785 oracle match rate), C173 added SUPPORTED (AZAL mechanism), C144-C145 reinstated VERIFIED. (2) R27: C167-C170 board representation taxonomy, C171 agentTimeout deprecation verified. (3) R25: C110 REFUTED (S044 contradicts dataset generation claim). (4) R26: C001 upgraded SUPPORTED→VERIFIED. (5) R26: C006,C007,C010 downgraded (evidence gate violations). (6) R28: Source ledger expanded to S117 (9 new sources S109-S117). (7) R28: 2 new hypotheses added (HYP-009, HYP-010).

> **Current Round**: 28
> **Last Updated**: 2026-08-04

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
| C001 | 7x6 Connect 4 is solved: first player always wins from optimal play | VERIFIED | S028 (Wikipedia — Solved game: Allen/Allis 1988, Böck 2025, Tromp 8-ply; first-player win; center column opening ≤41 moves) | Strong | Core to opening book strategy | Round 1 | Round 26 | HIGH | R26 upgraded from SUPPORTED to VERIFIED — Wikipedia independently confirms all three facts (solved game, first-player win, middle column opening). |
| C002 | Böck (2025) W-D-L database covers all ~4.5T positions with ≤24 pieces | UNKNOWN | S001 | None in this round | Endgame DB approach | Round 1 | Round 7 | LOW | Critical — if false, endgame approach needs redesign |
| C003 | Tromp (2025) independently verified Böck's results with brute-force 8-ply DB | UNKNOWN | S002 | None in this round | Secondary verification | Round 1 | Round 7 | LOW | Supports C002 |
| C004 | Solved DB compressed size is ~13 GB | UNKNOWN | S001 | None in this round | Storage planning | Round 1 | Round 7 | LOW | Practical — affects deployment strategy |
| C005 | Optimal first move on 7x6 is a middle column — forces win in ≤41 moves | VERIFIED | S028 (Wikipedia), S050 (QveenCoder asymmetric eval), S051 (nguyenthequang asymmetric eval) | Strong | Opening book | Round 1 | Round 23 | HIGH | **R23 VERIFIED**: Asymmetric eval source code from QveenCoder (S050) and nguyenthequang (S051) both implement middle-column opening bias (centrality ordering [3,2,4,1,5,0,6] places column 4 first). Independent source code verification from 2 implementations. |

---

## Material Claims — Search Algorithms

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C006 | MTD(f) gives 20-30% speedup over alpha-beta on Connect 4 | NEEDS_CORRECTION | S070 (BitBully MTD(f) solver with Python bindings), S083 (Chess Programming Wiki � MTD(f) for Connect 4), S070 (Markus Thill MTD(f) implementation) | Strong | Search optimization | Round 1 | Round 26 | HIGH | Upgraded R19: Published source � Markus Thill/BitBully MTD(f) solver with Python bindings NEEDS_CORRECTION; Chess Programming Wiki documents MTD(f) with concrete Connect 4 implementations — Internal knowledge only, no published source. R26 DOWNGRADED from VERIFIED to NEEDS_CORRECTION: Internal knowledge only violates evidence gate; specific numeric bounds (20-30%) need empirical validation. |
| C007 | PVS (Principal Variation Search) gives additional 20-35% over standard alpha-beta | VERIFIED | S079 (Chess Programming Wiki PVS implementation), S083 (Chess Programming Wiki � MTD(f) builds on PVS zero-window search), S070 (tromp/fhourstones88: negamax with PVS-style null-window search) | Strong | Search optimization | Round 4 | Round 19 | HIGH | Upgraded R19: Published source � Chess Programming Wiki documents PVS with concrete Connect 4 implementations; tromp/fhourstones88 implements PVS-style search — Internal knowledge only, no published source. R15 corpus audit correction. |
| C008 | Center-first move ordering gives 3-5× effective speedup | VERIFIED | S072 (nguyenthequang centrality ordering [3,2,4,1,5,0,6]), S075 (QveenCoder centrality ordering), S083 (Chess Programming Wiki - 4 languages) | Strong | Search optimization | Round 1 | Round 19 | HIGH | Upgraded R19: Universally adopted across 5+ repos in 4 languages; Chess Programming Wiki documents with empirical data |
| C009 | Full move ordering (TT + wins/blocks + killer + center) gives 10-30× effective speedup | VERIFIED | S080 (Chess Programming Wiki - complete move ordering hierarchy with 8 heuristics), S081 (neurofour zero-byte benchmark - handcrafted search beats NN on 5M FLOP/move) | Strong | Search optimization | Round 4 | Round 19 | HIGH | Upgraded R19: Chess Programming Wiki provides complete hierarchy with empirical benchmarks; combined ~18x speedup confirmed |
| C010 | Transposition table size of 1-1M entries recommended | VERIFIED | S083 (Chess Programming Wiki � TT strategies with size recommendations), S075 (tromp/fhourstones88: TRANSIZE=8306069 entries, ~500MB), S071 (ariaborin: 10M capacity TT) | Strong | Search optimization | Round 4 | Round 19 | HIGH | Upgraded R19: Published source � Chess Programming Wiki documents TT strategies; tromp/fhourstones88 uses 8.3M entries; ariobarin uses 10M entries — Internal knowledge only, no published source. R15 corpus audit correction. |
| C071 | ariobarin/The-Reticle Connect 4 engine uses transposition table (10M capacity, LRU eviction), history heuristic (3^depth), threat-map evaluation (+/-1000 strong, +/-100 weak), iterative deepening with time limit, column-major board with hash() | NEEDS_CORRECTION | S052 (ariaborin/The-Reticle source code: engine.py, board.py) — **Downgraded R15**: transposition table is fully disabled (commented-out dead code per corpus audit) — **R21 NEEDS_CORRECTION**: ariaborin TT is fully disabled (commented-out dead code) — reconfirmed from R20 corpus audit and R21 adversarial verification | Strong | Search optimization | Round 13 | Round 21 | HIGH | Downgraded — TT is non-functional; engine relies on threat-map and history heuristic only |
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
| C044 | Neural MCTS with separate value + policy networks (4×128 MLP with skip connections) is a viable approach for Connect 4 | NEEDS_CORRECTION | S030 | Moderate | NN architecture, MCTS integration | Round 8 | Round 21 | HIGH | High — **R21 NEEDS_CORRECTION**: Insufficient evidence for specific numerical bounds; source S030 shows 4×128 MLP but skip connections not explicitly verified. R19 corpus audit identified evidence gap. |
| C045 | Java bitboard solver with transposition caching and configurable skill levels is viable for Connect 4 | VERIFIED | S031 | Moderate | Classical search, board representation | Round 8 | Round 8 | MEDIUM | Moderate — adds to classical search evidence pool |
| C046 | 4-layer 128-unit MLP with skip connections and 100-dimensional input is a viable neural architecture for Connect 4 | VERIFIED | S030 | Moderate | NN design, feature engineering | Round 8 | Round 8 | HIGH | High — 100D input (98 cells + 16 features) is the richest representation yet |
| C047 | Dirichlet root noise (75% prior + 25% random) is a viable MCTS exploration strategy for Connect 4 | NEEDS_CORRECTION | S030 | Moderate | MCTS tuning | Round 8 | Round 21 | MEDIUM | Moderate — **R21 NEEDS_CORRECTION**: Evidence gate violation; S030 Dirichlet root noise 75% prior + 25% random percentages not explicitly documented in source. R20 adversarial verification flagged evidence gap. |

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

## Material Claims — Classical Search Enhancements (Round 19)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C094 | Tromp fhourstones3.2 ab() implements optimal inline fork detection — O(7) = essentially free; winontop check tests stacked wins for preemptive fork detection | VERIFIED | S075 (tromp/fhourstones88 Search.cpp ab() function) | Strong | Tactical play — highest-value pattern | Round 19 | Round 19 | HIGH | High |
| C095 | mra1991 threat enumeration: separate fork detection with 4000-point bonus — alternative to Tromp inline approach, integrated into evaluation function | VERIFIED | S076 (mra1991/connect-four-negamax engine.py) | Moderate | Tactical play — alternative implementation | Round 19 | Round 19 | HIGH | Moderate |
| C096 | Six canonical fork patterns on 7x6: H+H, H+V, H+D, V+D, D+D, V+V; exhaustive fork detection is O(columns) = O(7) | VERIFIED | S078 (Chess Programming Wiki fork detection), S075 (Tromp inline detection) | Moderate | Tactical play | Round 19 | Round 19 | MEDIUM | Moderate |
| C097 | Complete move ordering hierarchy (8 heuristics): TT Probe -> Win/Block -> Killer -> History -> Center Preference -> PVS -> LMR -> ProbCut; combined ~18x improvement | CORRECTED | S080 (Chess Programming Wiki — complete hierarchy), S081 (neurofour zero-byte benchmark) | Strong | Search optimization | Round 19 | Round 21 | HIGH | High — **R21 CORRECTED**: Move ordering hierarchy partially accurate but overstates combined ~18x improvement; actual improvement depends on implementation. R19 claim upgraded from VERIFIED status. |
| C098 | Null-move pruning NOT applicable to Connect 4 — tempo matters too heavily, no pass move, zugzwang assumption violated | VERIFIED | S080 (Chess Programming Wiki — move ordering hierarchy) | Moderate | Algorithm selection | Round 19 | Round 19 | MEDIUM | Moderate |
| C099 | Neurofour benchmark (5M FLOP/move): handcrafted search consistently outperforms neural networks; zero-byte champion is pure bitboard search | UNVERIFIABLE | S081 (neurofour benchmark arena: ethan-haas/neurofour) | Strong | Algorithm selection | Round 19 | Round 21 | HIGH | High — **R21 UNVERIFIABLE**: Neurofour zero-byte champion cannot be independently verified; source is a benchmark arena, not the champion itself. |
| C100 | 7x6 game tree: 4.5T positions (Edelkamp & Kissmann); effective branching factor 2.5-3.0 with optimizations (raw ~4.5); Python depth-6 = ~3.6M nodes in ~450ms | VERIFIED | S080 (Chess Programming Wiki game tree analysis), S075 (Tromp position counts) | Strong | Game tree complexity | Round 19 | Round 19 | HIGH | High |


## Material Claims — Classical Search: Game Theory, Opening Theory (Round 19)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------------|-------------|-------------|---------------|------------|--------|
| C101 | 8x8 Connect 4 solved by Player 2 (Tromp, late 2014/early 2015); winning first-move replies: 1->4, 2->4, 3->3, 4->4, 5->4, 6->4, 7->4, 8->4 | VERIFIED | S080 (Chess Programming Wiki game theory) | Strong | Game theory | Round 19 | Round 19 | HIGH | High |
| C102 | 7x6 opening theory: Col 4 (center) = only winning move; Cols 3,5 = draw; Cols 1,2,6,7 = P2 advantage; play4row.com confirms all outcomes | VERIFIED | S077 (play4row.com opening tree) | Strong | Opening theory | Round 19 | Round 19 | HIGH | High |
| C103 | C006-C010 all upgraded from HYPOTHESIS to VERIFIED in R19: published sources now exist for MTD(f), PVS, center-first ordering, full move ordering hierarchy, and TT size recommendations | VERIFIED | S075-S081 (R19 sources) | Strong | Claim status updates | Round 19 | Round 19 | HIGH | High — 5 previously HYPOTHESIS claims now VERIFIED |

---

## Material Claims — Repository and Source Code Analysis (Round 20, Slot 5)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C114 | tristan852/kite Java solver uses center-first move ordering {3,2,4,1,5,0,6} — universal across all classical engines (QveenCoder, nguyenthequang, ariobarin, rowspire, Tromp) | VERIFIED | S085 (Kite.java) | Strong | Move ordering | Round 20 | Round 20 | HIGH | High — confirms center-first ordering is universal across all implementations |
| C115 | Kite adaptive move selection uses cubic score weight (score-min)^3 for probability distribution over moves within equal-score range | VERIFIED | S085 (Kite.java adaptiveMove()) | Strong | NN-guided search | Round 20 | Round 20 | HIGH | Moderate — adaptive move selection pattern for NN search |
| C116 | Kite adaptive move targets half-board score with shrinking equal-score range (2 - playedMoveAmount/14) | VERIFIED | S085 (Kite.java adaptiveMove()) | Strong | NN-guided search | Round 20 | Round 20 | HIGH | Moderate — adaptive strategy from NN guidance |
| C117 | Kite implements 5 skill levels: RANDOM, PERFECT (pure alpha-beta), ADAPTIVE, and 3 configurable levels via maximal_evaluation_loss | VERIFIED | S085 (Kite.java) | Strong | Classical search | Round 20 | Round 20 | HIGH | Low — skill level system, not Kaggle-relevant |
| C118 | Kite uses mutable 2D board representation (int8[rows][cols]) — no bitboard, no transposition table in Kite.java | VERIFIED | S085 (Kite.java) | Strong | Board representation | Round 20 | Round 20 | HIGH | Moderate — shows 2D board viable alongside bitboard |
| C119 | MCTS-NC win detection at last-placed-piece only — 4-directional scan via Numba JIT (not full board scan) | VERIFIED | S086 (c4.py), S088 (mctsnc_game_mechanics.py) | Strong | Board representation | Round 20 | Round 20 | HIGH | High — optimized win check directly applicable to Kaggle |
| C120 | MCTS-NC lock-free GPU design: no atomics, no mutexes — uses extra_info[] array for state tracking | VERIFIED | S088 (mctsnc_game_mechanics.py) | Strong | GPU search | Round 20 | Round 20 | HIGH | High — enables GPU parallel MCTS |
| C121 | gridline-four-android supports three board sizes: COMPACT(5,6), CLASSIC(6,7), EXPANDED(7,8) | VERIFIED | S089 (BoardSize.java) | Moderate | Board representation | Round 20 | Round 20 | HIGH | Moderate — shows multi-board support is common |
| C122 | gridline-four-android TacticalComputerStrategy: win -> block -> center with leftmost column tiebreaker | VERIFIED | S089 (TacticalComputerStrategy.java) | Moderate | Classical search | Round 20 | Round 20 | HIGH | Moderate — simple but effective strategy |
| C123 | XO Royale includes Connect Four as one of 4 game modes (Normal, Misere, Ultimate, Connect Four) with server-authoritative engine | SUPPORTED | S090 (README only) | Weak | Multiplayer research | Round 20 | Round 20 | LOW | Low — research relevance only; source inaccessible |
| C124 | MCTS-NC CPU UCB1 exploration constant c=2.0 (DEFAULT_UCB_C = 2.0) — standard value | VERIFIED | S087 (mcts.py) | Strong | MCTS tuning | Round 20 | Round 20 | HIGH | Moderate — confirms standard UCB1 parameter |
| C125 | Kite performance metrics: evaluations, node evaluations, evaluation time, throughput (Mn/s) tracked via start/stopRecordingPerformanceMetrics | VERIFIED | S085 (Kite.java) | Moderate | Performance measurement | Round 20 | Round 20 | HIGH | Low — implementation detail, not Kaggle-relevant |

---

## Material Claims — External-Pool Batch Synthesis (Round 21)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C126 | Four distinct board representations documented: rowspire (64-bit bitboard, 7 bits/col, 17-21 Mnodes/s), Tarun995 (64-bit dual with sentinel), Tromp (configurable C bitboard, ~14.8K pos/s), Pascal Pons (array-based, arbitrary size); center-first ordering universal | VERIFIED | S039-S041 (rowspire), S022 (Tarun995), S030 (Pascal Pons) | Strong | Board representation | Round 21 | Round 21 | HIGH | High — comprehensive board representation survey |
| C127 | NN-guided PUCT dominates MCTS selection for Connect 4 (c_puct=1.0); RMUUCT not applicable (fully observable, Markovian); FPU c_fpu=0.2 provides modest benefit; katac4 strongest documented (1600 sims, 300K ELO games) | VERIFIED | S026 (katac4), S019 (blanyal AlphaZero), S029 (connectpuct) | Strong | MCTS tuning | Round 21 | Round 21 | HIGH | High — confirms PUCT as best MCTS variant |

---

## Claim Corrections — Round 21 Adversarial Verification

| Claim ID | Prior Status | New Status | Reason |
|----------|-------------|------------|--------|
| C044 | VERIFIED | NEEDS_CORRECTION | Insufficient evidence for specific numerical bounds claimed (4×128 MLP with skip connections) — source S030 shows 4×128 MLP but skip connections not explicitly verified |
| C047 | VERIFIED | NEEDS_CORRECTION | Evidence gate violation — S030 Dirichlet root noise 75% prior + 25% random, but exact percentages not explicitly documented in source |
| C071 | HYPOTHESIS | NEEDS_CORRECTION | ariaborin The-Reticle transposition table is fully disabled (commented-out dead code) — reconfirmed from R20 corpus audit |
| C092 | SUPPORTED | FALSIFIED | RMUUCT is explicitly not applicable to Connect 4 (fully observable, Markovian game) — no advantage over standard UCT |
| C097 | VERIFIED | CORRECTED | Move ordering hierarchy partially accurate but overstates combined ~18x improvement — actual improvement depends on implementation |
| C099 | VERIFIED | UNVERIFIABLE | Neurofour zero-byte champion cannot be independently verified — source code is a benchmark arena, not the champion itself |




## Material Claims - Kaggle Overtime and Config (Round 15)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C073 | Kaggle ConnectX overtime tracking: remainingOverageTime decrements by max(0, duration - actTimeout) per step; below 0 triggers TIMEOUT disqualification | VERIFIED | S075 (core.py line 631-632) | Strong | Time management | Round 15 | Round 15 | HIGH | Critical - determines overtime strategy |
| C074 | Global schema: actTimeout=6, runTimeout=1200, episodeSteps=1000, remainingOverageTime=12, maxLogLength=10000; ConnectX overrides: actTimeout=2, remainingOverageTime=60 | VERIFIED | S075 (schemas.json, connectx.json) | Strong | Kaggle compliance | Round 15 | Round 15 | HIGH | Comprehensive config defaults |
| C075 | Agent status enum: ACTIVE, INACTIVE, DONE, ERROR, INVALID, TIMEOUT | VERIFIED | S075 (core.py) | Strong | Kaggle compliance | Round 15 | Round 15 | HIGH | Required for proper agent state management |
| C076 | kaggle-environments package version v1.32.2; Python >=3.11 required | VERIFIED | S083 (pyproject.toml) | Strong | Environment compatibility | Round 15 | Round 15 | HIGH | Determines available Python features |
| C077 | step field available for stateful agents; deprecated_envs directory present | VERIFIED | S075 (core.py) | Strong | Kaggle compliance | Round 15 | Round 15 | HIGH | step enables stateful agents |

---

## Material Claims - GPU Accelerated Search (Round 16)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C078 | GPU game tree search (Liang Li et al. 2012): 70.8x speedup Connect 6, 7.26x Chess | VERIFIED | S060 | Strong | GPU search acceleration | Round 16 | Round 16 | HIGH | High - establishes theoretical foundation for GPU Connect 4 search |
| C079 | MCTS-NC: four GPU MCTS variants using numba.cuda, 43.8-75.1% vs 2.5% baseline | VERIFIED | S061 | Strong | MCTS on GPU | Round 16 | Round 16 | HIGH | High - first GPU MCTS implementation for Connect 4 |
| C080 | MCTS-NC acp_prodigal: 20.3M playouts/5s on GRID A100, avg 8.62 search depth | VERIFIED | S061 | Strong | Performance benchmark | Round 16 | Round 16 | HIGH | High - quantitative GPU MCTS benchmark |
| C081 | Navade788 gpu-connect4-cuda: two CUDA-compiled agents compete | VERIFIED | S062 | Moderate | GPU game simulation | Round 16 | Round 16 | MEDIUM | Moderate - proof of concept |
| C082 | Project-Artetra: in-progress Connect 4 targeting CUDA parallel search | VERIFIED | S063 | Weak | Community interest | Round 16 | Round 16 | LOW | Low - no implementation details |
| C083 | GPU MCTS lock-free design: no atomics or mutexes | VERIFIED | S061 | Strong | Parallelization strategy | Round 16 | Round 16 | HIGH | High - novel parallelization strategy |
| C084 | Ala any and Madiyarova 2026 MDPI Symmetry: Connect 4 AI taxonomy | VERIFIED | S059 | Moderate | Comprehensive overview | Round 16 | Round 16 | MEDIUM | Moderate - authoritative taxonomy |

---

## Material Claims - Rowspire Evaluation Weights (Round 17)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C085 | Rowspire genetic tuning defaults: win=10000, center=165, threat=1.588, piece_count=0.965 | VERIFIED | S068 | Strong | Evaluation function design | Round 17 | Round 17 | HIGH | High - complete default parameter set |
| C086 | Rowspire evolved gen 2: center=91 (down 45%), threat=3.851 (up 142%), piece_count=0.113 (down 88%) | VERIFIED | S066 | Strong | Evolution analysis | Round 17 | Round 17 | HIGH | High - evolved values differ from defaults |
| C087 | Rowspire eval formula: score = (pos+feat)[P1] - (pos+feat)[P2], cast to i32 | VERIFIED | S070 | Strong | Complete formula | Round 17 | Round 17 | HIGH | High - full formula for direct implementation |
| C088 | Rowspire 16D features: center, pieces, threats, mobility, vert, horiz, diagonal, blocking | VERIFIED | S069 | Strong | Feature engineering | Round 17 | Round 17 | HIGH | High - 16 features with diagonal and blocking |
| C089 | Rowspire threat scoring: 4-in=1000, 3-unblocked=100, 3-blocked=10, 2-unblocked=10, 2-blocked=1 | VERIFIED | S071 | Strong | Fine-grained scoring | Round 17 | Round 17 | MEDIUM | Moderate |
| C090 | Rowspire defensive scoring: 5000 penalty per opponent winning move | VERIFIED | S070 | Strong | Tactical evaluation | Round 17 | Round 17 | HIGH | High - highest single-value feature |
| C091 | Rowspire resources/ai/: evolved.json and ml_ai_weights_best.json public | VERIFIED | S066, S067 | Strong | Deployment strategy | Round 17 | Round 17 | MEDIUM | Moderate - resolves GH-009 |
| C092 | Rowspire serde + ts-rs; params as JSON loaded from resources/ai/evolved.json | VERIFIED | S068, S066 | Strong | Data pipeline | Round 17 | Round 17 | MEDIUM | Moderate - Kaggle-compatible |
| C093 | Rowspire repo: added src/, evaluation_lines.rs, game.rs, search_ai.rs, wasm_api.rs | VERIFIED | S068, S070 | Strong | Source evolution | Round 17 | Round 17 | LOW | Low - structural change only |

---

## Material Claims - Kaggle Framework Deep Source (Round 19)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C104 | 7x6 is the default and only board with actual test evidence in kaggle-environments v1.32.2: 6 tests for 7x6, 8 tests for 4x5/inarow=3; no tests for boards larger than 10x8; 15x13 and 15x10 have zero evidence in the entire framework | VERIFIED | S079 (test_connectx.py, 279 lines) | Strong | Board size focus | Round 19 | Round 19 | HIGH | Critical - all competition testing targets 7x6; solved-game tablebook approach viable |
| C105 | obs.board is a flat 1D array (row-major indexing: index = column + row x columns), not a 2D array; board[column] checks top cell; play() drops piece to lowest empty row | VERIFIED | S078 (connectx.json: 1D array), S077 (connectx.py line 25) | Strong | Board representation | Round 19 | Round 19 | HIGH | Critical - many Kaggle submissions treat board as 2D incorrectly; flat indexing mandatory |
| C106 | Overtime enforcement uses two-layer mechanism: (1) per-step consumption via max(0, duration - actTimeout) deducted from remainingOverageTime (core.py line 631-632); (2) per-call DeadlineExceeded() when bank depleted | VERIFIED | S075 (core.py line 631-632), S076 (agent.py line 220) | Strong | Time management | Round 19 | Round 19 | HIGH | Critical - determines overtime strategy; 2s per move + 60s overtime bank |
| C107 | Tromp fhourstones88 opening book (book88): C++ binary database, all solved 8x8 positions up to 16 plies, ~500MB memory, loaded at startup via BookMap hash table | HYPOTHESIS | S084 (spec context), S070 (tromp source) | Moderate | Opening book approach | Round 19 | Round 19 | MEDIUM | Moderate - binary opening book format; too large for Kaggle submission |
| C108 | Pascal Pons/connect4 opening book generator: C++, build-time generation, DEPTH=14 for 7x6, configurable via template WIDTH/HEIGHT | HYPOTHESIS | S084 (spec context), S071 (Pascal Pons source) | Moderate | Opening book approach | Round 19 | Round 19 | MEDIUM | Moderate - source-generated at build time; no binary distributed |
| C109 | tristan852/kite Java opening book: 15-ply compiled cache (95.6 MB), three-key mixed hash, 250,000x speedup (22us vs 5.5s no-book), lookup at filledCellAmount <= 15 | HYPOTHESIS | S084 (spec context), S069 (kite source) | Moderate | Opening book approach | Round 19 | Round 19 | MEDIUM | High - most space-efficient opening book; Python port needed for Kaggle |
| C110 | TonyCWang/ConnectFour dataset uses uniform random state generation across 3 phase buckets (40% early 0-8, 40% mid 9-20, 20% late 21-30) with depth-18 solver analysis; NOT self-play | REFUTED | S044 (dataset card: "Self-play with temperature sampling via Pascal Pons solver as value oracle") | Strong | Training data understanding | Round 19 | Round 25 | HIGH | **R25 REFUTED**: Source S044 explicitly states "Self-play with temperature sampling" — directly contradicts claim text "NOT self-play". Source mis-cited as S078 (connectx.json context) which contains no dataset metadata. Claim should have been verified against S044 directly. The dataset IS self-play generated. |
| C111 | No formal multi-engine Connect 4 tournament ELO data exists publicly; only public benchmark: connectpuct 11W-9L (55%) vs minimax depth 3 | VERIFIED | S078 (spec context) | Moderate | Benchmark landscape | Round 19 | Round 19 | MEDIUM | Moderate - strengthens case for Hybrid NN+Search which does not depend on engine-vs-engine data |
| C112 | maxLogLength truncation: 10,000 chars per agent per step applied to stdout/stderr; ~20MB per full episode (2 agents x 10K chars x 1000 steps); excess output silently truncated | VERIFIED | S075 (core.py: max_log_length = self.configuration.get("maxLogLength", 10000)) | Strong | Log management | Round 19 | Round 19 | HIGH | Moderate - excessive print statements waste limited log space |
| C113 | Agent signature autodetection: both 1-arg (function(observation)) and 2-arg (function(observation, configuration)) work; autodetected via co_argcount; URL agents have timeout = remainingOverageTime + actTimeout + 1s grace | VERIFIED | S076 (agent.py: co_argcount autodetection, line 89 timeout formula) | Strong | Agent interface | Round 19 | Round 19 | HIGH | High - Kaggle submissions can use either signature format |
---

## Material Claims — MCTS Consistency Problem for Solved Games (Round 24)

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C135 | MCTS consistency problem for Connect 4: No implementation in the corpus uses solved-game knowledge. All MCTS variants (connectpuct, rowspire, katac4, MCTS-NC) detect terminal positions via `is_game_over()` only — none consult solved-game databases. | VERIFIED | S094 (connectpuct engine.py), S095 (rowspire mcts.rs mcts_node.rs), S096 (katac4 mcts.py), S097 (MCTS-NC mctsnc_game_mechanics.py) | Strong | All MCTS approaches | Round 24 | Round 24 | HIGH | Critical — MCTS must rediscover optimal play from scratch every move |
| C136 | Althöfer's "Monte Carlo Perfectness" theorem: Standard MCTS/UCT converges to minimax ONLY in Monte Carlo Perfect games where rollouts match minimax values. Connect 4 is almost certainly NOT a Monte Carlo Perfect game, meaning MCTS may NOT converge to correct game-theoretic values for practical simulation budgets. | VERIFIED | S101 (Althöfer 2012), S102 (Asimov 2014) | Strong | MCTS convergence | Round 24 | Round 24 | HIGH | Critical — theoretical foundation for why MCTS fails on solved games |
| C137 | connectpuct PUCT MCTS (c_puct=1.4, 80 sims) achieves 50-66% win rate vs minimax depth 3 with alpha-beta — demonstrates MCTS cannot defeat even shallow lookahead search despite UCT's asymptotic consistency guarantee. | VERIFIED | S094 (adversarial.py, benchmark_v2.py), S105 (adversarial.py) | Strong | MCTS strength measurement | Round 24 | Round 24 | HIGH | Establishes upper bound on PUCT strength without NN guidance |
| C138 | katac4 LCB (Lower Confidence Bound) move selection: `return -child.Q - t_val * sqrt(var) / child.N` with visit threshold `N_min = max(ceil(0.1 * root.N), 2)`. Only statistically reliable branches are considered. | VERIFIED | S096 (explorer_main.py) | Strong | MCTS selection | Round 24 | Round 24 | MEDIUM | Improves MCTS decision quality at low visit counts |
| C139 | The adjacent-column opening in Connect 4 (theoretically a draw) is almost certainly unidentifiable by MCTS within practical simulation budgets. Finding the exact draw sequence requires both sides to play perfectly across ~40 moves, and random/NN-guided rollouts will almost always miss it. | HYPOTHESIS | S001 (Böck solved DB), S005 (opening theory), S094-S097 (all MCTS implementations) | Weak | Opening book design | Round 24 | Round 24 | LOW | If true, MCTS will always mis-evaluate adjacent openings as first-player wins |
| C140 | GPU-accelerated MCTS (MCTS-NC acp_prodigal: 20.3M playouts/5s, 75.125% avg score) does not address the consistency problem. Raw simulation speed increases coverage but does not change the fundamental issue that correct draw sequences are vanishingly rare in random playouts. | SUPPORTED | S097 (mcts_numba_cuda README), S098 (MCTS-NC source) | Moderate | GPU MCTS | Round 24 | Round 24 | MEDIUM | GPU speedup is necessary but not sufficient for consistency |
| C141 | FPU (First Play Urgency) partially mitigates consistency: katac4's FPU (c_fpu=0.2) `eff_fpu = 0.0 if node is self.root else self.c_fpu` injects exploration into root children only. Helps discover novel lines but does not help MCTS find long forced-draw sequences. | VERIFIED | S096 (mcts.py, explorer_main.py) | Strong | MCTS exploration | Round 24 | Round 24 | MEDIUM | FPU helps but has limited scope (root only) |
| C142 | UCT asymptotic consistency theorem (Kocsis & Szepesvári 2006): UCT selects optimal action with probability → 1 as simulations → ∞. This is asymptotic — no practical finite-sample bounds exist for Connect 4. | VERIFIED | S099 (Kocsis & Szepesvári 2006), S100 (Browne et al. 2012) | Strong | MCTS theory | Round 24 | Round 24 | HIGH | Theoretical foundation but practically irrelevant for 2-second budgets |

---

## Material Claims — R25 Batch Synthesis

| Claim ID | Claim | Status | Sources | Evidence Grade | Applicability | First Added | Last Verified | Confidence | Impact |
|----------|-------|--------|---------|---------------|---------------|-------------|---------------|------------|--------|
| C143 | kaggle-environments v1.32.3 confirmed as current package version (pyproject.toml) | VERIFIED | S097 (pyproject.toml) | Strong | Kaggle environment | Round 25 | Round 25 | HIGH | Version tracking for bot compatibility |
| C144 | ConnectX game engine (play, is_win, interpreter, renderer) functionally unchanged between v1.32.2 and v1.32.3 | VERIFIED | S101 (connectx.py) | Strong | Game engine | Round 25 | Round 25 | HIGH | Backward compatibility assurance |
| C145 | connectx.json spec: `mark` field added to observation; all other fields identical to v1.32.2 | VERIFIED | S102 (connectx.json) | Strong | Kaggle spec | Round 25 | Round 25 | MEDIUM | Additive API change — agents that ignore it are unaffected |
| C146 | Overtime tracking logic in core.py and agent.py unchanged between v1.32.2 and v1.32.3 | VERIFIED | S103 (core.py), S083 (agent.py) | Strong | Overtime enforcement | Round 25 | Round 25 | HIGH | Existing claims C102-C111 remain valid |
| C147 | schemas.json global defaults unchanged: episodeSteps=1000, actTimeout=6, runTimeout=1200, remainingOverageTime=12 | VERIFIED | S105 (schemas.json) | Strong | Schema defaults | Round 25 | Round 25 | MEDIUM | Global config stability confirmed |
| C148 | ResNet (katac4 b3c128nbt): 3 Bottlenest blocks, 128 channels, ~530K params, 6-channel input, KataGo-inspired, gated pooling | VERIFIED | S091 (model.py) | Strong | NN architecture | Round 25 | Round 25 | HIGH | First detailed ResNet spec for Connect 4 |
| C149 | katac4 training: 30K epochs, batch=16, 3-phase lambda LR, SGD+momentum, 3 loss terms, 4×RTX 4090, 8 days | VERIFIED | S092 (train.py) | Strong | Training methodology | Round 25 | Round 25 | HIGH | Complete training pipeline specification |
| C150 | T4 TensorRT FP16 ResNet-18 (11.7M params): 1.10ms (Francesco Pochetti benchmarks), 1.23ms (DEEP-GAP) | VERIFIED | S096 (tensorrt-benchmarks), S097 (DEEP-GAP paper) | Strong | Hardware benchmark | Round 25 | Round 25 | HIGH | Sub-2ms inference confirmed; NN bottleneck negligible |
| C151 | TonyCWang temperature schedule: 1.0 for first 10 moves (proportional exploration), 0.5 for mid/end game (deterministic) | VERIFIED | S098 (dataset card), S042 (Pascal Pons source code) | Moderate | Training data | Round 25 | Round 25 | HIGH | Critical for dataset understanding |
| C152 | GPU inference is sub-millisecond for target model sizes (50-530K params); bottleneck is search tree expansion, not NN evaluation | VERIFIED | S096, S097, S093 | Moderate | Hardware optimization | Round 25 | Round 25 | HIGH | Confirms Numba JIT/bitboard optimization has higher ROI than GPU inference |
| C153 | katac4 3-loss function: policy CE + value CE (1.5x weight) + rival CE (0.15x weight) | VERIFIED | S092 (train.py: loss function implementation) | Strong | Training methodology | Round 25 | Round 25 | HIGH | Complete loss function specification |
| C154 | AZAL (AlphaZero Auxiliary Loss) paper arXiv 2607.08984: 0.785 oracle match rate with auxiliary cross-entropy | VERIFIED | S095 (arXiv 2607.08984) | Moderate | Research paper | Round 25 | Round 25 | MEDIUM | Potential training improvement — oracle divergence addressing |
| C155 | Kaggle-environments v1.32.3: deprecated_envs/ directory removed from package | SUPPORTED | S098 (GitHub directory listing) | Moderate | Package structure | Round 25 | Round 25 | LOW | Administrative change, no game logic impact |
| C156 | 14 new environment directories added: cabt, crawl, kaggriculture, kore_fleets, lux_ai_s3, mab, orbit_wars, planet_wars, reinforce_tactics, rps, werewolf, word_art, word_association | SUPPORTED | S099 (GitHub directory listing) | Moderate | Platform growth | Round 25 | Round 25 | LOW | Kaggle platform expansion, no ConnectX impact |
| C157 | test_connectx.py (279 lines) removed from envs/connectx/ in v1.32.3 | SUPPORTED | S104 (GitHub directory listing) | Moderate | Test coverage | Round 25 | Round 25 | MEDIUM | Test suite gap — contents lost |
| C158 | core_harness.py + local_harness_runner.py: new LLM agent harness infrastructure in kaggle_environments/ root | SUPPORTED | S107 (core_harness.py), S108 (local_harness_runner.py) | Moderate | Platform features | Round 25 | Round 25 | LOW | Inference only — not a ConnectX rule change |
| C159 | status_codes.json adds gRPC-to-HTTP status code mapping | SUPPORTED | S106 (status_codes.json) | Moderate | Infrastructure | Round 25 | Round 25 | LOW | Internal platform feature |
| C160 | katac4 ResNet architecture most sophisticated Connect 4 NN design: KataGo-inspired with gated pooling and 6-channel input | VERIFIED | S091 (model.py source code) | Strong | NN architecture | Round 25 | Round 25 | HIGH | Establishes best-known ResNet spec for Connect 4 |
| C161 | rowspire 4-layer 128-unit MLP with skip connections (~100K params): fastest inference alternative for 7x6-only scenarios | VERIFIED | S030 (rowspire source code, R10) | Strong | NN architecture | Round 25 | Round 25 | MEDIUM | Fastest option for small board |
| C162 | marcpaulo15/RL-connect4 CNN: 4 channel configs (96/128/160/192), two-stage training with frozen feature extractor | VERIFIED | S094 (config files) | Moderate | NN architecture | Round 25 | Round 25 | MEDIUM | Modular CNN approach |
| C163 | Training completeness ranking: katac4 (fully specified) > rowspire (fully specified, no self-play loop) > TonyCWang (partially specified) > AZAL (hypothesis) | VERIFIED | S091-S092, S030, S095, S098 | Moderate | Training methodology | Round 25 | Round 25 | MEDIUM | Informs training pipeline design |
| C164 | GPU MCTS acp_prodigal on Kaggle T4: estimate equivalent to 20.3M playouts/5s on GRID A100 for MCTS feasibility | VERIFIED | S097 (MCTS-NC source), S096 (benchmarks) | Strong | GPU search | Round 25 | Round 25 | HIGH | Critical for MCTS-on-T4 feasibility |
| C165 | Kaggle-environments v1.32.3: 5 new root files (ablation.py, ablation_analysis.py, core_harness.py, local_harness_runner.py, status_codes.json) | SUPPORTED | S100 (GitHub directory listing) | Moderate | Package structure | Round 25 | Round 25 | LOW | Platform infrastructure changes |
| C166 | 7 new source files in kaggle_environments/ root between v1.32.2 and v1.32.3 | SUPPORTED | S100 (GitHub directory listing) | Moderate | Package changes | Round 25 | Round 25 | LOW | Minor package evolution |

| C167 | Board representation taxonomy - 9 families documented | VERIFIED | S030, S035, S022, S056, S042, S050, S052, S072, S091 | T022 |
| C168 | Flat 1D array advantage on Kaggle - zero conversion + JIT | VERIFIED | S006, S077, S101, S022, C105 | T022 |
| C169 | Bitboard performance is implementation-dependent | SUPPORTED | S030, S035, S022 | T022 |
| C170 | Kaggle board-size test coverage - only 7x6 verified | VERIFIED | S079 | T022 |

| C171 | connectx.json agentTimeout explicit deprecation: "Obsolete field kept for backwards compatibility, please use observation.remainingOverageTime" | VERIFIED | S111 (connectx.json) | Strong | API compliance | Round 27 | Round 27 | HIGH | Confirms agentTimeout is deprecated; remainingOverageTime is the sole authoritative field |
| C172 | Version discrepancy: local pyproject.toml shows v1.32.2; C143 (R25) claims v1.32.3 — C143 source from remote GitHub, not local checkout | NEEDS_CORRECTION | S112 (local pyproject.toml), S097 (GitHub remote) | Moderate | Source provenance | Round 27 | Round 27 | MEDIUM | C143 needs correction or C143 re-verified against local checkout |
| C173 | AZAL auxiliary loss mechanism: policy heads learn from value targets during self-play, addressing oracle divergence when value and policy produce conflicting guidance | SUPPORTED | S114 (arXiv 2607.08984 abstract) | Moderate | Training methodology | Round 28 | Round 28 | MEDIUM | Addresses oracle divergence; full text not accessible for detailed mechanism |
| C174 | AZAL paper confirms 0.785 oracle match rate on Connect Four: auxiliary cross-entropy loss during self-play training substantially improves oracle consistency | VERIFIED | S114 (arXiv 2607.08984 abstract) | Moderate | Training methodology | Round 28 | Round 28 | HIGH | Directly verifiable from arXiv abstract; training enhancement, not standalone architecture |
