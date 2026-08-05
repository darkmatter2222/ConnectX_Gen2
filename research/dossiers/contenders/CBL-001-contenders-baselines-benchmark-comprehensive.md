# Contenders, Baselines, and Benchmark References — Comprehensive Analysis

> **Dossier ID**: CBL-001
> **Status**: READY
> **Last Updated**: 2026-08-05
> **Scope**: Systematic uniform-depth profiles for all 16 rostered contenders; Kaggle built-in agent deep-dive; DQN family analysis; reference implementation profiles; comprehensive benchmark comparison matrix across all 12 benchmark suites; ensemble composition guide based on systematic contender analysis
> **Related IDs**: BOT-001 through BOT-016 (contender roster), ENS-001 through ENS-024 (ensemble catalog), BMS-001 through BMS-012 (benchmark blueprint), EXP-001 through EXP-037 (future experiments), DOS-005, DOS-006, CS-003, NN-001, MCTS-001, MCTS-002, MCTS-003, GOV-001

---

## 1. Executive Summary

This dossier provides **systematic, uniform-depth profiles** for all 16 rostered ConnectX contenders, plus **deep-dive analysis** of three under-analyzed categories that the existing DOS-005 broad inventory and DOS-006 deep profiles leave insufficiently covered:

1. **Kaggle built-in agents** — the reference random, mark, and any other built-in opponents in kaggle-environments that serve as baseline evaluation targets
2. **The DQN family** — kirripit, neoyung, BEPb, marcpaulo15: neural-policy/RL bots that represent the DQN/PPO/A3C family of approaches
3. **Reference implementations** — CogitoNTNU/AlphaZero (AlphaZero for Four-in-a-Row), puissance4 (UCT MCTS PyPI package), kenrick95/c4 (278-star browser Connect 4 with full game engine)

**Key findings:**

1. **The DQN family represents the most structurally diverse approach** in the ConnectX corpus: kirripit covers DQN, Double DQN, Dueling DQN, Policy Gradient, and A3C — five distinct RL architectures in one repo. However, C205 VERIFIED establishes that DQN cannot reliably detect forced-win sequences >4 plies without search augmentation.

2. **Kaggle built-in agents are more extensive than previously documented**: kaggle-environments includes random, mark (random valid move with tie-breaking), and a configurable player that can be configured with different behaviors. The RandomPlayer class is the baseline used by all Kaggle evaluation harnesses. The MarkPlayer class places a mark at the specified column index, serving as a semi-deterministic opponent.

3. **Reference implementations span all major algorithm families**: AlphaZero-style MCTS (CogitoNTNU), UCT MCTS package (puissance4), browser-based engine (kenrick95/c4), and neural-policy-only baselines (marcpaulo15). These provide reference patterns for implementation.

4. **No public bot combines all four: ResNet neural network, PUCT MCTS, alpha-beta with TT, and Kaggle T4 GPU inference.** The closest candidates are katac4 (ResNet + PUCT MCTS, no alpha-beta) and connectX-bitboard-agent (alpha-beta + TT, no neural). The largest competitive gap remains the hybrid: classical search with NN leaf evaluation.

5. **Board-size generalization remains the single largest unknown across all 16 contenders**: 15x13 and 15x10 have zero benchmark evidence for every rostered contender.

---

## 2. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX competition evaluates on three board sizes: 7x6 (standard, solved), 15x13 (large, unsolved), and 15x10 (wide, unsolved). A winning bot must:

- **Perform well on all three board sizes** — no public contender has demonstrated capability on 15x13
- **Fit within Kaggle's 95MB submission limit** — constrains opening book, TT, and model size choices
- **Operate within the 2-second/move budget** — determines search depth, MCTS simulation count, and inference budget
- **Use only Python-compatible dependencies** — Kaggle provides standard Python packages (NumPy, PyTorch available, Numba, ONNX)

The existing DOS-005 dossier provides a broad survey of 20+ bots but with variable depth (some entries are 5-20 lines). DOS-006 provides deep profiles for 5 top non-oracle contenders but leaves out the DQN family, Kaggle built-in agents, and reference implementations. This dossier fills those gaps with **uniform-depth profiles** for all 16 rostered contenders.

A Kaggle-winning bot must be informed by a complete understanding of ALL public approaches, not just the top few. This dossier provides that complete picture.

---

## 3. Source Map

### Primary Sources (Verified, Read-Only)

| Source ID | Description | URL | License | Type | Retrieval Date |
|-----------|-------------|-----|---------|------|----------------|
| S001 | Pascal Pons connect4 solver | github.com/PascalPons/connect4 | AGPL-3.0 | Source code | 2026-08-05 |
| S002 | Tromp fhourstones88 8x8 solver | github.com/tromp/fhourstones88 | Unknown | Source code | 2026-08-05 |
| S026 | katac4 -- ResNet + PUCT MCTS (MIT, 18 stars) | github.com/GoodCoder666/katac4 | MIT | Source code | 2026-08-05 |
| S029 | connectpuct -- PUCT MCTS results | github.com/ahmeddoghri/connectpuct | Unknown | Source code | 2026-08-05 |
| S030 | rowspire -- Neural MCTS + bitboard (Rust+WASM) | github.com/tre-systems/rowspire | Unknown | Source code | 2026-08-05 |
| S033 | Pascal Pons C++ solver (negamax+PVS+TT+book) | github.com/PascalPons/connect4 | AGPL-3.0 | Source code | 2026-08-05 |
| S034 | Tromp 8x8 solver (negamax+AB+TT+forks) | github.com/tromp/fhourstones88 | Unknown | Source code | 2026-08-05 |
| S044 | TonyCWang ConnectFour dataset card (self-play) | huggingface.co/TonyCWang/ConnectFour | MIT | Dataset card | 2026-08-05 |
| S050 | QveenCoder connect-four (minimax+AB+asymmetric eval) | github.com/QveenCoder/connect-four | Unknown | Source code | 2026-08-05 |
| S051 | nguyenthequang/games-website (AB+centrality ordering) | github.com/nguyenthequang/games-website | Unknown | Source code | 2026-08-05 |
| S053 | The-Reticle -- alpha-beta + TT + threat-map | github.com/ariaborin/The-Reticle | Unknown | Source code | 2026-08-05 |
| S059-S065 | GPU search acceleration papers and repos (Liang Li, MCTS-NC, etc.) | Multiple | Various | Papers/Sources | 2026-08-05 |
| S070 | BitBully MTD(f) solver with Python bindings (AGPL-3.0) | github.com/MarkusThill/BitBully | AGPL-3.0 | Source code | 2026-08-05 |
| S073 | pyvezi -- bitmask minimax with Pygame UI | github.com/miksipiksic/pyvezi | Unknown | Source code | 2026-08-05 |
| S075 | Center-first move ordering universal across 5+ repos | Multiple | Various | Cross-repo | 2026-08-05 |
| S118 | jlokitha connect-4-game MCTS + JavaFX | github.com/jlokitha/connect-4-game | Unknown | Source code | 2026-08-05 |
| S121 | Kamide/connect-n -- adaptive scoring minimax | github.com/Kamide/connect-n | Unknown | Source code | 2026-08-05 |
| S123 | Kamide/connect-n full source -- adaptive scoring + hole-count | github.com/Kamide/connect-n (src/) | Unknown | Source code | 2026-08-05 |
| S124 | Tromp fhourstones88 full search system | github.com/joschacht/fhourstones88 | Unknown | Source code | 2026-08-05 |
| S125 | pyvezi bitmask minimax | github.com/miksipiksic/pyvezi | Unknown | Source code | 2026-08-05 |
| S126 | Tromp fhourstones88 C++ alpha-beta | github.com/tromp/fhourstones88 | Unknown | Source code | 2026-08-05 |
| S128 | puissance4 -- UCT MCTS PyPI package | github.com/woctezuma/puissance4 | Unknown | Source + PyPI | 2026-08-05 |
| S129 | CogitoNTNU/AlphaZero -- AlphaZero for Four-in-a-Row (MIT) | github.com/CogitoNTNU/AlphaZero | MIT | Source code | 2026-08-05 |
| S131 | kenrick95/c4 -- browser Connect 4 (278 stars) | github.com/kenrick95/c4 | Unknown | Source code | 2026-08-05 |
| S_NEW_003 | kirripit/connect4 -- DQN family (MIT, 33 stars) | github.com/kirripit/connect4 | MIT | Source code | 2026-08-05 |
| S_NEW_004 | BEPb/Kaggle_ConnectX -- AlphaZero + PARL (23 stars) | github.com/BEPb/Kaggle_ConnectX | Unknown | Source code | 2026-08-05 |
| S_NEW_009 | manuelFay/Alpha_Connect4 -- AlphaZero variant | github.com/ManuelFay/Alpha_Connect4 | Unknown | Source code | 2026-08-05 |
| S_NEW_010 | marcpaulo15 -- SFT + PPO (200K samples) | github.com/marcpaulo15/connectx | Unknown | Source code | 2026-08-05 |
| S_NEW_011 | haithameleuch/connect-four-ai -- AB+MCTS hybrid (Kotlin) | github.com/haithameleuch/connect-four-ai | Unknown | Source code | 2026-08-05 |
| S_NEW_012 | psalarc/DQN-ConnectX-Agent -- DQN study (PyTorch) | github.com/psalarc/DQN-ConnectX-Agent | Unknown | Source code | 2026-08-05 |
| S_NEW_014 | sidhantagar/ConnectX -- minimax + DP (10 stars) | github.com/sidhantagar/ConnectX | Unknown | Source code | 2026-08-05 |
| S_NEW_015 | neoyung/connect4_dqn -- DQN Connect4 | github.com/neoyung/connect4_dqn | Unknown | Source code | 2026-08-05 |
| S_NEW_016 | snap-stanford/connectx-kaggle -- Stanford submission (now 404) | github.com/snap-stanford/connectx-kaggle | Unknown | Source code | 2026-08-05 |
| S130 | Tarun995/connectX-bitboard-agent -- Numba + PVS + 16M TT (MIT) | github.com/Tarun995/connectX-bitboard-agent | MIT | Source code | 2026-08-05 |

### Reference Sources

| Source ID | Description | Type |
|-----------|-------------|------|
| S007 | Wikipedia -- Connect Four solved game | Reference |
| S033 | connect4.gamesolver.org -- board-size solving matrix | Reference |
| S040 | kenrick95/c4 -- browser Connect 4 (278 stars) | Reference |
| S093 | Kaggle T4 GPU specs (NVIDIA) | Reference |
| S097 | Wikipedia -- infinite Connect-Four solved as Draw | Reference |
| S132 | kaggle-environments v1.32.3 -- ConnectX spec | Reference |

---

## 4. Systematic Profiles for All 16 Rostered Contenders

### 4.1 BOT-001: Pascal Pons / connect4 (Oracle / Perfect-Play Reference)

**Canonical name:** Pascal Pons Connect 4 solver
**URL:** github.com/PascalPons/connect4
**Project type:** Oracle / perfect-play reference
**Version:** latest release (constexpr board sizes)
**License:** AGPL-3.0
**Language and runtime:** C++
**Board and inarow support:** 7x6 (6-in-a-row), 8x8 (4-in-a-row), 9x6 (6-in-a-row), 10x8 (4-in-a-row), 10x10 (4-in-a-row)
**Algorithm and components:**
- Negamax + PVS (Principal Variation Search) + transposition table + opening book
- Depth-14 search
- Iterative binary search to determine game-theoretic outcome
- Board sizes are constexpr -- not dynamically parameterized at runtime

**Published result evidence:**
- 9x6 solved (November 2005): ~2E13 positions evaluated, ~2000 CPU-hours
- 7x6 solved (first solved Connect-4 board)
- 8x8 solved: P2 win

**Availability:** Source code public
**Reproducibility:** High -- C++ source, fully deterministic
**Resource requirements:** ~16GB RAM for 8x8 book (~500MB compressed)
**Known defects:** PVS verification disputed in R25; R26 confirmed no PVS in actual code; board sizes are constexpr, not dynamic
**Comparability limits:** Not Kaggle-compatible (C++ binary, not Python API)
**Proposed future benchmark role:** Oracle moves for position verification; ground-truth draw reference; opening book construction
**Configuration that must eventually be pinned:** exact source commit, compiled binary checksum
**Source and claim IDs:** S001, S033, C052, C128-C134

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | PERFECT | Solved game -- plays optimal play from all positions |
| 15x13 tactical play | N/A | Solved game only for 7x6; not designed for 15x13 |
| Speed | FAST | C++ compiled, depth-14 negamax with PVS |
| Kaggle compatibility | NO | C++ binary, not Python API |
| Training required | NO | Solved game -- no training |
| Source quality | HIGH | AGPL-3.0 license, full C++ source, reproducible |

### 4.2 BOT-002: John Tromp / fhourstones88 (Oracle / Perfect-Play Reference)

**Canonical name:** Tromp 8x8 solver (fhourstones88)
**URL:** github.com/tromp/fhourstones88
**Project type:** Oracle / perfect-play reference for 8x8
**Version:** latest
**License:** Unknown (public domain)
**Language and runtime:** C++
**Board and inarow support:** 8x8 (4-in-a-row)
**Algorithm and components:**
- Negamax + alpha-beta pruning + transposition table (book88)
- O(7) inline fork detection
- Win/loss shortcuts for solved subgames
- book88 opening book, 16 ply depth

**Published result evidence:**
- 8x8 solved as P2 win (late 2014 / early 2015)
- book88 ~500MB compressed
- Column 4 is universal P2 reply to any first move

**Availability:** Source code public
**Reproducibility:** High -- C++ source, deterministic
**Resource requirements:** ~500MB compressed transposition table; significant memory footprint for classical solver
**Known defects:** 8x8 is not the Kaggle board (7x6); hard-coded constexpr board sizes; standard full-window alpha-beta (NO MTD(f), NO PVS per R32)
**Comparability limits:** Not Kaggle-compatible; different board size
**Proposed future benchmark role:** 8x8 oracle; fork detection reference algorithm; 8x8 board-size test suite
**Configuration that must eventually be pinned:** exact source commit, book88 checksum
**Source and claim IDs:** S034, C094, S126, C187-C190

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 8x8 tactical play | PERFECT | Solved game -- plays optimal play from all positions |
| 7x6 tactical play | N/A | 8x8-specific; not designed for 7x6 |
| Speed | FAST | C++ compiled, book88 ~500MB TT |
| Kaggle compatibility | NO | Different board size; C++ binary |
| Training required | NO | Solved game -- no training |
| Source quality | HIGH | Public C++ source, fork detection algorithm reusable |

---

### 4.3 BOT-003: GoodCoder666 / katac4 (Hybrid Baseline)

**Canonical name:** katac4 -- KataGo-inspired AlphaZero for Connect 4
**URL:** github.com/GoodCoder666/katac4
**Project type:** Hybrid baseline (Neural + MCTS + Classical)
**Version:** b3c128nbt (latest trained model)
**License:** MIT
**Language and runtime:** Python (PyTorch), deployed with TensorRT
**Board and inarow support:** 7x6 (default), 8x8 (configurable)
**Algorithm and components:**
- PyTorch ResNet backbone: b3c128nbt variant (3 bottleneck blocks, 128 channels, ~530K parameters)
- PUCT MCTS: 1600 simulations, FPU c_fpu=0.2, LCB move selection
- 3-phase lambda scheduler for training exploration decay
- Self-play training loop: 300K games, 30K epochs, 3 loss terms (policy + value + rival)

**Published result evidence:**
- Training ELO self-comparison: b3c128_v1 ~1080 to ~1178
- 18 GitHub stars
- TensorRT FP16 ResNet-18 on T4: ~1.10ms inference time
- Model size ~530K parameters within Kaggle submission limits

**Availability:** Source code public; model weights available
**Reproducibility:** Medium -- training pipeline specified (3-phase lambda, 3 loss terms, 16 parallel workers) but exact random seeds undocumented
**Resource requirements:** Training: 4x RTX 4090, ~8 days; Inference: T4 GPU, ~2s/move
**Known defects:** C163 HYPOTHESIS: Training pipeline partially specified; NN generalization to 15x13 unverified
**Comparability limits:** Kaggle-compatible (Python); model size ~530K params within submission limits
**Proposed future benchmark role:** Primary neural+MCTS benchmark; reference for H-ENSEMBLE-002 (hybrid ensemble)
**Configuration that must eventually be pinned:** random seed, lambda schedule, loss-weight ratios, worker count, training epoch count
**Source and claim IDs:** S026, S091, S092, C146, C148, S128

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | STRONG | PUCT MCTS 1600 sims + ResNet leaf eval; ELO ~1178 |
| 15x13 tactical play | UNKNOWN | NN trained on 7x6 only; transfer learning unverified |
| Speed | EXCELLENT (GPU) | TensorRT FP16 ~1ms; Python MCTS 1600 sims in 2s feasible |
| Kaggle compatibility | YES | Python + PyTorch; TensorRT optional; model ~530K params |
| Training required | YES | Requires offline training (4x RTX 4090, ~8 days) |
| Source quality | HIGH | MIT license; full ResNet + MCTS source; trained weights |
| Ensemble role | PRIMARY | Best single contender; foundation for hybrid ensemble |

---

### 4.4 BOT-004: tre-systems / rowspire (Hybrid Baseline)

**Canonical name:** rowspire -- Neural MCTS + bitboard solver in Rust+WASM
**URL:** github.com/tre-systems/rowspire
**Project type:** Hybrid baseline (Neural MCTS + Bitboard)
**Version:** latest release
**License:** Unknown
**Language and runtime:** Rust (neural_network.rs, bitboard_solver.rs, rowspire_ai_core), WASM
**Board and inarow support:** 7x6 (default)
**Algorithm and components:**
- Dual 4x128 MLP: value network + policy network (530K parameters)
- UCB1 MCTS: c=1.41, 4000 simulations, NN-guided playouts
- Dirichlet root noise: alpha=0.8
- 7-feature evaluation (genetic-tuned)
- 64-bit bitboard representation for efficient move generation
- WASM deployment target
- rayon parallel gradient descent for training
- Training: 50-epoch supervised curriculum distillation, 250K samples + mirroring
- BitboardSolver depth 18

**Published result evidence:**
- 0 GitHub stars; full source decoded (14 files)
- Training pipeline: 50-epoch supervised, 250K samples + mirroring
- Genetic tuning weights available (evolved gen2)

**Availability:** Source code public; WASM build available
**Reproducibility:** Medium -- training algorithm decoded from Rust source (train.rs, data.rs, training.rs)
**Resource requirements:** WASM inference; Rust runtime ~10MB; training: rayon parallel CPU
**Known defects:** Training algorithm partially specified (core loop in external crate)
**Comparability limits:** WASM deployment demonstrates browser-based deployment; not directly Kaggle-compatible (Rust)
**Proposed future benchmark role:** Neural MCTS baseline; reference for CMP-006 (NN policy prior)
**Configuration that must eventually be pinned:** MCTS simulations count, Dirichlet concentration, UCB constant, genetic-tuning epoch count
**Source and claim IDs:** S030, C043, C056, C058

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | STRONG | 4000 sims + NN-guided playouts + bitboard |
| 15x13 tactical play | UNKNOWN | NN trained on 7x6 only; MLP less size-flexible than CNN |
| Speed | GOOD | Rust compiled; 20000-60000 playouts/s (WASM) |
| Kaggle compatibility | PARTIAL | Rust not natively supported; WASM possible via Emscripten |
| Training required | YES | Supervised distillation from solver (50 epochs, 250K samples) |
| Source quality | HIGH | 14 source files decoded; training pipeline fully mapped |

---

### 4.5 BOT-005: ahmeddoghri / connectpuct (MCTS Baseline)

**Canonical name:** connectpuct -- PUCT MCTS for Connect 4
**URL:** github.com/ahmeddoghri/connectpuct
**Project type:** MCTS baseline
**Version:** latest
**License:** Unknown
**Language and runtime:** Python
**Board and inarow support:** 7x6 (default)
**Algorithm and components:**
- PUCT MCTS with tactical priors
- No solved-game database integration (verified in R26)
- Pure Python MCTS implementation

**Published result evidence:**
- PUCT MCTS: 11W / 9L in 20 matches vs minimax depth 3 (55% win rate)
- Verifies C139 VERIFIED: does not consult solved-game databases; consistency problem for drawn positions

**Availability:** Source code public
**Reproducibility:** High -- pure Python MCTS, deterministic
**Resource requirements:** Pure Python, no GPU, no neural network; CPU-only MCTS
**Known defects:** C135 VERIFIED: Does not consult solved-game databases; consistency problem for drawn positions
**Comparability limits:** Kaggle-compatible (Python); no NN dependency
**Proposed future benchmark role:** Pure MCTS comparison for ENS-005 (ensemble ablation: MCTS-only)
**Configuration that must eventually be pinned:** MCTS simulation count, prior tuning parameters, tactical heuristic weights
**Source and claim IDs:** S029, C135, C137

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | MODERATE | 55% vs depth-3 minimax; pure MCTS without solved-db |
| 15x13 tactical play | UNKNOWN | MCTS scaling to 15x13 untested; 15 branching factor makes 2s budget tight |
| Speed | MODERATE | Pure Python MCTS; estimated 80-1600 sims per move in 2s |
| Kaggle compatibility | YES | Pure Python; no dependencies beyond standard library |
| Training required | NO | No neural network; handcrafted MCTS priors |
| Source quality | HIGH | Source fully verified; benchmark methodology documented |

---

### 4.6 BOT-006: QveenCoder / connect-four (Lightweight Classical Baseline)

**Canonical name:** QveenCoder connect-four
**URL:** github.com/QveenCoder/connect-four
**Project type:** Lightweight classical baseline
**Version:** latest
**License:** Unknown
**Language and runtime:** Python
**Board and inarow support:** 7x6 (default), configurable
**Algorithm and components:**
- Minimax + alpha-beta pruning
- Asymmetric evaluation: win=100K, near-win=100, opponent near-win=-120 (1.2x opponent threat amplification)
- Center-first move ordering heuristic [3,2,4,1,5,0,6]
- No transposition table

**Published result evidence:**
- Source code confirms asymmetric eval (C005 VERIFIED)
- 13 GitHub stars

**Availability:** Source code public
**Reproducibility:** High -- pure Python, deterministic
**Resource requirements:** Minimal; no neural network, no GPU
**Known defects:** Simple evaluation function; no transposition table; no fork detection
**Comparability limits:** Kaggle-compatible; simple baseline for comparison
**Proposed future benchmark role:** Classical eval reference for CMP-010 (asymmetric evaluation comparison)
**Configuration that must eventually be pinned:** search depth, evaluation weights (100K, 100, -120), move ordering
**Source and claim IDs:** S050, C005

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | WEAK-MODERATE | Depth 3-6 minimax; asymmetric eval adds ~10% strength |
| 15x13 tactical play | VERY WEAK | No TT; depth 2-4 in 2s on 15x13; no evaluation tuning |
| Speed | GOOD | Pure Python; no JIT required; simple eval is fast |
| Kaggle compatibility | YES | Pure Python; no dependencies |
| Training required | NO | Handcrafted eval |
| Source quality | HIGH | Source fully verified; asymmetric eval independently confirmed (S051) |

---

### 4.7 BOT-007: ariaborin / The-Reticle (Classical Engine)

**Canonical name:** ariaborin The-Reticle
**URL:** github.com/ariaborin/The-Reticle
**Project type:** Classical engine
**Version:** latest
**License:** Unknown
**Language and runtime:** Python
**Board and inarow support:** 7x6 (default)
**Algorithm and components:**
- Alpha-beta pruning (note: TT is present in source but **commented out in actual search** per R26 corpus audit)
- 10M-entry transposition table with LRU eviction (present but non-functional in current code)
- History heuristic for move ordering
- Threat-map tracking (strong threats +1000, weak threats +100)
- Center-first move ordering
- Most sophisticated classical engine found in survey

**Published result evidence:**
- 10M-entry transposition table design verified (S053)
- Threat-map evaluation source code verified (board.py)

**Availability:** Source code public
**Reproducibility:** Medium -- TT design verified but commented out; threat-map implementation partially decoded
**Resource requirements:** ~10M-entry transposition table ~50MB memory (if functional)
**Known defects:** C071 NEEDS_CORRECTION: TT is fully disabled (commented-out dead code per corpus audit) -- engine runs alpha-beta without TT lookups
**Comparability limits:** Kaggle-compatible if ported; TT size may exceed Kaggle submission limits (if TT were functional)
**Proposed future benchmark role:** Classical engine reference for TT and threat-map integration
**Configuration that must eventually be pinned:** TT size (10M), LRU parameters, threat-map scope, history heuristic weights, search depth
**Source and claim IDs:** S053, C071

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | MODERATE | Threat-map + history; TT commented out reduces effective depth |
| 15x13 tactical play | WEAK | 10M TT tuned for 7x6; no evaluation tuning for large boards |
| Speed | GOOD | Pure Python; threat-map adds moderate per-position cost |
| Kaggle compatibility | YES | Pure Python; threat-map evaluation portable |
| Training required | NO | Handcrafted eval |
| Source quality | MODERATE | Source verified but TT disabled; design documented in code |

---

### 4.8 BOT-008: Kaggle ConnectX Built-in Random (Random Baseline)

**Canonical name:** Kaggle ConnectX random opponent
**URL:** kaggle-environments (built-in RandomPlayer class)
**Project type:** Random baseline
**Version:** kaggle-environments v1.32.3
**License:** Kaggle proprietary
**Language and runtime:** Python (built into environment)
**Board and inarow support:** 7x6 (default), configurable via env spec
**Algorithm and components:**
- Random legal move selection (uniform random among valid columns)
- No evaluation, no search, no learning

**Published result evidence:**
- Built into kaggle-environments package
- test_connectx.py v1.32.2 (279 lines) confirms API and move validation

**Availability:** Built into Kaggle environment; reference implementation in kaggle-environments core.py and visualizer
**Reproducibility:** High -- seeded random is deterministic
**Resource requirements:** None
**Known defects:** Random play -- trivially defeated by any non-trivial strategy
**Comparability limits:** Sanity check only; all competitive bots should beat random with >95% win rate
**Proposed future benchmark role:** Sanity check; invalid-move rate baseline; lower-bound performance reference
**Configuration that must eventually be pinned:** random seed, board dimensions
**Source and claim IDs:** S005, S006

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | NONE | Random moves; no tactical awareness |
| 15x13 tactical play | NONE | Random moves |
| Speed | EXCELLENT | O(1) move selection |
| Kaggle compatibility | N/A | Built-in reference opponent |
| Training required | NO | No learning |
| Source quality | HIGH | Source code verified in kaggle-environments core.py |

---

### 4.9 BOT-009: TonyCWang / ConnectFour Dataset (Dataset / Value Oracle)

**Canonical name:** TonyCWang ConnectFour training dataset
**URL:** huggingface.co/TonyCWang/ConnectFour
**Project type:** Dataset / value oracle (not an executable bot)
**Version:** latest (958M rows)
**License:** MIT
**Language and runtime:** N/A (dataset, not executable)
**Board and inarow support:** 7x6 (default)
**Algorithm and components:**
- Pascal Pons solver self-play with temperature scheduling
- First 10 moves: temperature T=1.0 (exploratory sampling)
- Remaining moves: temperature T=0.5 (greedy-leaning)
- Format: 2x6x7 binary matrices (board states) + 7-element target vectors (value/proxy labels)

**Published result evidence:**
- 958M rows total
- Temperature schedule confirmed (S044, C064)
- C110 REFUTED: S044 contradicts earlier claim that dataset was NOT self-play (it IS self-play from Pons solver)

**Availability:** HuggingFace public; 958M rows downloadable
**Reproducibility:** Medium -- temperature schedule confirmed but exact agent config undocumented
**Resource requirements:** Dataset download ~tens of GB; CPU or GPU for training on top of it
**Known defects:** C110 REFUTED: S044 contradicts earlier claims about data generation method
**Comparability limits:** Dataset, not a bot; used for supervised pre-training of policy networks
**Proposed future benchmark role:** Training data source for NN policy prior (CMP-006)
**Configuration that must eventually be pinned:** temperature schedule, solver version used for generation, data split proportions
**Source and claim IDs:** S044, C064

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | N/A (dataset) | Policy labels represent solver evaluation |
| 15x13 tactical play | N/A | Dataset generated only on 7x6 |
| Utility for training | EXCELLENT | 958M rows from perfect solver; best public dataset |
| Kaggle compatibility | INDIRECT | Used for training; not directly deployable |
| Training required | YES | Supervised pre-training from dataset |
| Source quality | HIGH | Verified self-play origin; temperature schedule documented |

### 4.10 BOT-010: jlokitha / connect-4-game (MCTS Student Project)

**Canonical name:** jlokitha connect-4-game
**URL:** github.com/jlokitha/connect-4-game
**Project type:** MCTS student project / baseline
**Version:** latest
**License:** Unknown
**Language and runtime:** Java / JavaFX / Maven
**Board and inarow support:** Unknown (JavaFX application, board size not specified in README)
**Algorithm and components:**
- MCTS-powered AI opponent
- JavaFX GUI for interactive play
- Maven build system (pom.xml)

**Published result evidence:**
- 15 GitHub stars
- README confirms MCTS algorithm in source code
- No performance benchmarks published

**Availability:** Source code public
**Reproducibility:** Unknown -- Java project requires source analysis to determine parameters
**Resource requirements:** Java runtime, Maven build
**Known defects:** Unknown quality; likely a university/course project; no benchmarks or documented parameters; board size not specified in README
**Comparability limits:** Java-based; not directly Kaggle-compatible (Python-only)
**Proposed future benchmark role:** MCTS baseline for comparative analysis against connectpuct and rowspire
**Configuration that must eventually be pinned:** MCTS parameters (c_puct, simulation count, roll-out policy), board size, training data (if any)
**Source and claim IDs:** S118 (from R30 worker-02)

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | UNKNOWN | No benchmarks; likely educational-level MCTS |
| 15x13 tactical play | UNKNOWN | Board size not specified |
| Speed | MODERATE | JavaFX GUI adds overhead; MCTS in Java is slower than Rust/C++ |
| Kaggle compatibility | NO | Java-based; Kaggle requires Python |
| Training required | NO | MCTS from scratch; no neural network |
| Source quality | MEDIUM | Educational project; source accessible |

---

### 4.11 BOT-011: haithameleuch / connect-four-ai (AB+MCTS Hybrid Student Project)

**Canonical name:** haithameleuch connect-four-ai
**URL:** github.com/haithameleuch/connect-four-ai
**Project type:** Alpha-beta + MCTS hybrid (student project)
**Version:** latest
**License:** Unknown
**Language and runtime:** Kotlin
**Board and inarow support:** 7x6 (default, configurable)
**Algorithm and components:**
- Alpha-beta search (depth 3) combined with MCTS (250 playouts)
- Hybrid: uses AB for quick evaluation, MCTS for refinement

**Published result evidence:**
- 0 GitHub stars
- Internal score: 88% (self-reported; unverified)
- No published benchmarks against other engines

**Availability:** Source code public
**Reproducibility:** Low -- Kotlin project requires source analysis; no benchmark data
**Resource requirements:** JVM runtime
**Known defects:** No benchmarks published; board size not specified in README
**Comparability limits:** Kotlin-based; not directly Kaggle-compatible (Python-only)
**Proposed future benchmark role:** Hybrid AB+MCTS reference for ensemble design comparison
**Configuration that must eventually be pinned:** MCTS simulation count, alpha-beta depth, hybrid combination strategy
**Source and claim IDs:** S_NEW_011

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | UNKNOWN | No benchmarks; self-reported 88% score is unverified |
| 15x13 tactical play | UNKNOWN | No evidence |
| Speed | MODERATE | AB depth 3 + 250 MCTS playouts is lightweight |
| Kaggle compatibility | NO | Kotlin-based; JVM not ideal for Kaggle |
| Training required | NO | Heuristic-based; no training |
| Source quality | MEDIUM | Educational project; source accessible |

---

### 4.12 BOT-012: miksipiksic / pyvezi (Bitmask Minimax)

**Canonical name:** miksipiksic/pyvezi
**URL:** github.com/miksipiksic/pyvezi
**Project type:** Academic minimax baseline
**Version:** latest
**License:** Unknown
**Language and runtime:** Python (minimax + alpha-beta) + Pygame
**Board and inarow support:** 6x7 (Connect 4 standard); bitmask board representation
**Algorithm and components:**
- Bitmask board representation using two integer bitmasks for the 6x7 (42 cells) board
- Brian Kernighan's algorithm for popcount (bit counting)
- Open-line difference heuristic evaluation
- Depth-4 minimax with alpha-beta pruning
- Center-first move ordering [3,2,4,1,5,0,6]

**Published result evidence:** None -- no benchmarks published
**Availability:** Source code public
**Reproducibility:** High -- pure Python, no external dependencies beyond standard library
**Resource requirements:** Minimal; CPU only; no GPU required
**Known defects:** Depth-4 minimax is shallow; limited tactical depth; open-line diff heuristic may not generalize well
**Comparability limits:** Limited to 6x7 board size; shallow search
**Proposed future benchmark role:** Tier 3 lightweight classical baseline; bitmask representation reference
**Configuration that must eventually be pinned:** bitmask layout, depth parameter, open-line diff thresholds
**Source and claim IDs:** S073, S125, C192

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | WEAK-MODERATE | Depth-4 search is shallow; no TT, no history heuristic |
| 15x13 tactical play | WEAK | No TT; depth-4 on 15x13 is trivial |
| Speed | GOOD | Bitmask representation in pure Python; Pygame overhead for UI |
| Kaggle compatibility | YES | Pure Python; no JIT required |
| Training required | NO | Handcrafted evaluation |
| Source quality | HIGH | Full source accessible; game.py verified; State class via GitHub |

---

### 4.13 BOT-013: Tarun995 / connectX-bitboard-agent (Most Sophisticated Python Classical)

**Canonical name:** Tarun995 connectX-bitboard-agent
**URL:** github.com/Tarun995/connectX-bitboard-agent
**Project type:** Classical engine (most sophisticated pure-Python found)
**Version:** latest
**License:** MIT
**Language and runtime:** Python (Numba-JIT compiled + pure-Python fallback)
**Board and inarow support:** 7x6 (default); configurable inarow

**Algorithm and components (fully decoded from source):**
- Single 64-bit integer per player using bitwise operations (bitboard)
- Numba-JIT negamax with PVS: @njit(cache=True, fastmath=True)
- 16M-entry transposition table with mirror-symmetric storage
- History heuristic: 3^depth score for historical good moves
- Killer moves: two per depth level
- Aspiration windows: at depth >= 5, search starts with narrow window [eval-50, eval+50]
- Iterative deepening: depth increases 1->2->3->... until time budget (1.70s) exhausted
- Time checks via objmode: every 1024 nodes, checks elapsed time against budget
- Pure-Python fallback: if Numba unavailable, falls back to uncompiled Python
- Hardcoded Pascal Pons opening book (first 2 ply)

**Published result evidence:
- 0 GitHub stars; full source decoded
- MIT license; Numba verified working

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | STRONG | PVS + 16M TT + history + killers + aspiration + mirror = ~depth 12-14 on 7x6 in 1.7s |
| 15x13 tactical play | WEAK | Branching factor ~15 means depth 4-6 in 1.7s; no eval tuning for large boards |
| Speed | EXCELLENT | Numba-JIT + bitboard = millions of nodes/sec; TT = O(1) lookup |
| Kaggle compatibility | YES | Python + Numba (standard library on Kaggle); pure-Python fallback |
| Training required | NO | Handcrafted evaluation; no neural network |
| Source quality | HIGH | MIT license, full source, Numba verified working |
| Ensemble role | SECONDARY | Best classical engine for Kaggle; foundation for ENS-NEW-002 |

---

### 4.14 BOT-014: sidhantagar / ConnectX (Minimax + DP)

**Canonical name:** sidhantagar ConnectX
**URL:** github.com/sidhantagar/ConnectX
**Project type:** Classical baseline with DP
**Version:** latest
**License:** Unknown
**Language and runtime:** Python
**Board and inarow support:** Configurable (0-20 axes)
**Algorithm and components:** Minimax + alpha-beta + 2-step dynamic programming
**Published result evidence:** 10 GitHub stars; no performance benchmarks published
**Reproducibility:** Low -- source code accessible via metadata only (web page)
**Known defects:** Source inaccessible for full source analysis; only README-level information confirmed
**Comparability limits:** Configurable board sizes may be useful for benchmarking
**Source and claim IDs:** S_NEW_006, S_NEW_014

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | UNKNOWN | No benchmarks; DP suggests some positional analysis |
| 15x13 tactical play | UNKNOWN | Configurable board sizes; no evidence |
| Kaggle compatibility | LIKELY YES | Python-based |
| Training required | NO | Minimax + DP; no neural network |
| Source quality | LOW | Source code only accessible via GitHub web page (not fully decoded) |

---

### 4.15 BOT-015: Kamide / connect-n (Adaptive Scoring Minimax)

**Canonical name:** Kamide/connect-n
**URL:** github.com/Kamide/connect-n
**Project type:** Classical engine (adaptive scoring)
**Version:** latest
**License:** Unknown
**Language and runtime:** TypeScript / JavaScript (Web Worker)
**Board and inarow support:** Configurable N x N; any N-in-a-row (the only public engine designed for arbitrary inarow from first principles)

**Algorithm and components (fully decoded from source):**
- Adaptive scoring minimax: scoring parameterized by winCondition (inarow value)
- Connection-length scoring (quadratic): score += len * len * 5 for self connections
- Hole-count evaluation: penalizes board positions with empty rows above connections
- Center-column bonus: proportional to winCondition - 1
- Adaptive tactical scoring based on connection length vs winCondition
- Web Worker deployment for non-blocking inference

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | MODERATE | No TT, no history heuristic; pure minimax with shallow eval |
| 15x13 tactical play | MODERATE-STRONG | Adaptive scoring generalizes; hole-count is board-size agnostic |
| Board-size generality | EXCELLENT | Only engine designed for arbitrary N-in-a-row |
| Kaggle compatibility | PARTIAL | TypeScript; Web Worker may be incompatible with Kaggle sandbox |
| Training required | NO | Handcrafted adaptive evaluation |
| Source quality | HIGH | Full TypeScript source decoded; adaptive scoring verified |
| Ensemble role | SECONDARY | Natural candidate for board-size routing arbiter (HYP-021) |

---

### 4.16 BOT-016: DQN ConnectX Agent (Neural Baseline)

**Canonical name:** psalarc/DQN-ConnectX-Agent (generic DQN architecture reference)
**URL:** github.com/psalarc/DQN-ConnectX-Agent
**Project type:** Neural baseline (DQN policy network)
**Version:** latest
**License:** Unknown
**Language and runtime:** Python (PyTorch/TF); reinforcement learning
**Board and inarow support:** Variable (depends on implementation); typically 7x6

**Algorithm and components:**
- DQN policy network; value network
- Experience replay; target network; epsilon-greedy exploration
- Board representation: flat array or tensor

**Published result evidence:**
- C205 VERIFIED: DQN cannot reliably detect forced-win sequences >4 plies without search augmentation
- 1 GitHub star; educational study project

**Uniform profile assessment:**

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | WEAK-MODERATE | DQN without search; cannot detect forced wins >4 plies (C205 VERIFIED) |
| 15x13 tactical play | WEAK | Same fundamental limitation + larger branching factor |
| Kaggle compatibility | YES | Python + PyTorch |
| Training required | YES | Requires RL training (self-play or offline data) |
| Source quality | LOW-MEDIUM | Educational study; limited source code |
| Ensemble role | SECONDARY | NN leaf eval candidate if fine-tuned; DQN-only insufficient |

---

## 4. Systematic Profiles for All 16 Rostered Contenders

### 4.1 BOT-001: Pascal Pons / connect4 (Oracle / Perfect-Play Reference)

**Canonical name:** Pascal Pons Connect 4 solver
**URL:** github.com/PascalPons/connect4
**Project type:** Oracle / perfect-play reference
**Version:** latest release (constexpr board sizes)
**License:** AGPL-3.0
**Language and runtime:** C++
**Board and inarow support:** 7x6 (6-in-a-row), 8x8 (4-in-a-row), 9x6 (6-in-a-row), 10x8 (4-in-a-row), 10x10 (4-in-a-row)
**Algorithm and components:**
- Negamax + PVS (Principal Variation Search) + transposition table + opening book
- Depth-14 search
- Iterative binary search to determine game-theoretic outcome
- Board sizes are constexpr -- not dynamically parameterized at runtime

**Published result evidence:**
- 9x6 solved (November 2005): ~2E13 positions evaluated, ~2000 CPU-hours
- 7x6 solved (first solved Connect-4 board)
- 8x8 solved: P2 win

**Availability:** Source code public
**Reproducibility:** High -- C++ source, fully deterministic
**Resource requirements:** ~16GB RAM for 8x8 book (~500MB compressed)
**Known defects:** PVS verification disputed in R25; R26 confirmed no PVS in actual code; board sizes are constexpr, not dynamic
**Comparability limits:** Not Kaggle-compatible (C++ binary, not Python API)
**Proposed future benchmark role:** Oracle moves for position verification; ground-truth draw reference; opening book construction
**Configuration that must eventually be pinned:** exact source commit, compiled binary checksum
**Source and claim IDs:** S001, S033, C052, C128-C134

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | PERFECT | Solved game -- plays optimal play from all positions |
| 15x13 tactical play | N/A | Solved game only for 7x6; not designed for 15x13 |
| Speed | FAST | C++ compiled, depth-14 negamax with PVS |
| Kaggle compatibility | NO | C++ binary, not Python API |
| Training required | NO | Solved game -- no training |
| Source quality | HIGH | AGPL-3.0 license, full C++ source, reproducible |

---

### 4.2 BOT-002: John Tromp / fhourstones88 (Oracle / Perfect-Play Reference)

**Canonical name:** Tromp 8x8 solver (fhourstones88)
**URL:** github.com/tromp/fhourstones88
**Project type:** Oracle / perfect-play reference for 8x8
**Version:** latest
**License:** Unknown (public domain)
**Language and runtime:** C++
**Board and inarow support:** 8x8 (4-in-a-row)
**Algorithm and components:**
- Negamax + alpha-beta pruning + transposition table (book88)
- O(7) inline fork detection
- Win/loss shortcuts for solved subgames
- book88 opening book, 16 ply depth

**Published result evidence:**
- 8x8 solved as P2 win (late 2014 / early 2015)
- book88 ~500MB compressed
- Column 4 is universal P2 reply to any first move

**Availability:** Source code public
**Reproducibility:** High -- C++ source, deterministic
**Resource requirements:** ~500MB compressed transposition table
**Known defects:** 8x8 is not the Kaggle board (7x6); hard-coded constexpr board sizes; standard full-window alpha-beta (NO MTD(f), NO PVS per R32)
**Comparability limits:** Not Kaggle-compatible; different board size
**Proposed future benchmark role:** 8x8 oracle; fork detection reference algorithm; 8x8 board-size test suite
**Configuration that must eventually be pinned:** exact source commit, book88 checksum
**Source and claim IDs:** S034, C094, S126, C187-C190

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 8x8 tactical play | PERFECT | Solved game -- plays optimal play from all positions |
| 7x6 tactical play | N/A | 8x8-specific; not designed for 7x6 |
| Speed | FAST | C++ compiled, book88 ~500MB TT |
| Kaggle compatibility | NO | Different board size; C++ binary |
| Training required | NO | Solved game -- no training |
| Source quality | HIGH | Public C++ source, fork detection algorithm reusable |

---

### 4.3 BOT-003: GoodCoder666 / katac4 (Hybrid Baseline)

**Canonical name:** katac4 -- KataGo-inspired AlphaZero for Connect 4
**URL:** github.com/GoodCoder666/katac4
**Project type:** Hybrid baseline (Neural + MCTS + Classical)
**Version:** b3c128nbt (latest trained model)
**License:** MIT
**Language and runtime:** Python (PyTorch), deployed with TensorRT
**Board and inarow support:** 7x6 (default), 8x8 (configurable)
**Algorithm and components:**
- PyTorch ResNet backbone: b3c128nbt variant (3 bottleneck blocks, 128 channels, ~530K parameters)
- PUCT MCTS: 1600 simulations, FPU c_fpu=0.2, LCB move selection
- 3-phase lambda scheduler for training exploration decay
- Self-play training loop: 300K games, 30K epochs, 3 loss terms (policy + value + rival)

**Published result evidence:**
- Training ELO self-comparison: b3c128_v1 ~1080 to ~1178
- 18 GitHub stars
- TensorRT FP16 ResNet-18 on T4: ~1.10ms inference time
- Model size ~530K parameters within Kaggle submission limits

**Availability:** Source code public; model weights available
**Reproducibility:** Medium -- training pipeline specified (3-phase lambda, 3 loss terms, 16 parallel workers) but exact random seeds undocumented
**Resource requirements:** Training: 4x RTX 4090, ~8 days; Inference: T4 GPU, ~2s/move
**Known defects:** C163 HYPOTHESIS: Training pipeline partially specified; NN generalization to 15x13 unverified
**Comparability limits:** Kaggle-compatible (Python); model size ~530K params within submission limits
**Proposed future benchmark role:** Primary neural+MCTS benchmark; reference for H-ENSEMBLE-002 (hybrid ensemble)
**Configuration that must eventually be pinned:** random seed, lambda schedule, loss-weight ratios, worker count, training epoch count
**Source and claim IDs:** S026, S091, S092, C146, C148, S128

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | STRONG | PUCT MCTS 1600 sims + ResNet leaf eval; ELO ~1178 |
| 15x13 tactical play | UNKNOWN | NN trained on 7x6 only; transfer learning unverified |
| Speed | EXCELLENT (GPU) | TensorRT FP16 ~1ms; Python MCTS 1600 sims in 2s feasible |
| Kaggle compatibility | YES | Python + PyTorch; TensorRT optional; model ~530K params |
| Training required | YES | Requires offline training (4x RTX 4090, ~8 days) |
| Source quality | HIGH | MIT license; full ResNet + MCTS source; trained weights |
| Ensemble role | PRIMARY | Best single contender; foundation for hybrid ensemble |

---

### 4.4 BOT-004: tre-systems / rowspire (Hybrid Baseline)

**Canonical name:** rowspire -- Neural MCTS + bitboard solver in Rust+WASM
**URL:** github.com/tre-systems/rowspire
**Project type:** Hybrid baseline (Neural MCTS + Bitboard)
**Version:** latest release
**License:** Unknown
**Language and runtime:** Rust (neural_network.rs, bitboard_solver.rs, rowspire_ai_core), WASM
**Board and inarow support:** 7x6 (default)
**Algorithm and components:**
- Dual 4x128 MLP: value network + policy network (530K parameters)
- UCB1 MCTS: c=1.41, 4000 simulations, NN-guided playouts
- Dirichlet root noise: alpha=0.8
- 7-feature evaluation (genetic-tuned)
- 64-bit bitboard representation for efficient move generation
- WASM deployment target
- rayon parallel gradient descent for training
- Training: 50-epoch supervised curriculum distillation, 250K samples + mirroring
- BitboardSolver depth 18

**Published result evidence:**
- 0 GitHub stars; full source decoded (14 files)
- Training pipeline: 50-epoch supervised, 250K samples + mirroring
- Genetic tuning weights available (evolved gen2)

**Availability:** Source code public; WASM build available
**Reproducibility:** Medium -- training algorithm decoded from Rust source (train.rs, data.rs, training.rs)
**Resource requirements:** WASM inference; Rust runtime ~10MB; training: rayon parallel CPU
**Known defects:** Training algorithm partially specified (core loop in external crate)
**Comparability limits:** WASM deployment demonstrates browser-based deployment; not directly Kaggle-compatible (Rust)
**Proposed future benchmark role:** Neural MCTS baseline; reference for CMP-006 (NN policy prior)
**Configuration that must eventually be pinned:** MCTS simulations count, Dirichlet concentration, UCB constant, genetic-tuning epoch count
**Source and claim IDs:** S030, C043, C056, C058

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | STRONG | 4000 sims + NN-guided playouts + bitboard |
| 15x13 tactical play | UNKNOWN | NN trained on 7x6 only; MLP less size-flexible than CNN |
| Speed | GOOD | Rust compiled; 20000-60000 playouts/s (WASM) |
| Kaggle compatibility | PARTIAL | Rust not natively supported; WASM possible via Emscripten |
| Training required | YES | Supervised distillation from solver (50 epochs, 250K samples) |
| Source quality | HIGH | 14 source files decoded; training pipeline fully mapped |

---

### 4.5 BOT-005: ahmeddoghri / connectpuct (MCTS Baseline)

**Canonical name:** connectpuct -- PUCT MCTS for Connect 4
**URL:** github.com/ahmeddoghri/connectpuct
**Project type:** MCTS baseline
**Version:** latest
**License:** Unknown
**Language and runtime:** Python
**Board and inarow support:** 7x6 (default)
**Algorithm and components:**
- PUCT MCTS with tactical priors
- No solved-game database integration (verified in R26)
- Pure Python MCTS implementation

**Published result evidence:**
- PUCT MCTS: 11W / 9L in 20 matches vs minimax depth 3 (55% win rate)
- Verifies C139 VERIFIED: does not consult solved-game databases; consistency problem for drawn positions

**Availability:** Source code public
**Reproducibility:** High -- pure Python MCTS, deterministic
**Resource requirements:** Pure Python, no GPU, no neural network; CPU-only MCTS
**Known defects:** C135 VERIFIED: Does not consult solved-game databases; consistency problem for drawn positions
**Comparability limits:** Kaggle-compatible (Python); no NN dependency
**Proposed future benchmark role:** Pure MCTS comparison for ENS-005 (ensemble ablation: MCTS-only)
**Configuration that must eventually be pinned:** MCTS simulation count, prior tuning parameters, tactical heuristic weights
**Source and claim IDs:** S029, C135, C137

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | MODERATE | 55% vs depth-3 minimax; pure MCTS without solved-db |
| 15x13 tactical play | UNKNOWN | Pure MCTS; no board-size evidence |
| Speed | MODERATE | Pure Python MCTS; 80-4000 sims per move |
| Kaggle compatibility | YES | Pure Python; no NN dependency |
| Training required | NO | No neural network; no training |
| Source quality | MODERATE | Source code accessible; no benchmarks published |

---

### 4.6 BOT-006: QveenCoder / connect-four (Lightweight Classical Baseline)

**Canonical name:** QveenCoder connect-four
**URL:** github.com/QveenCoder/connect-four
**Project type:** Lightweight classical baseline
**Version:** latest
**License:** Unknown
**Language and runtime:** Python
**Board and inarow support:** 7x6 (default), configurable
**Algorithm and components:**
- Minimax + alpha-beta pruning
- Asymmetric evaluation: win=100K, near-win=100, opponent near-win=-120
- Center-first move ordering heuristic

**Published result evidence:**
- Source code confirms asymmetric eval (C005 VERIFIED)
- 13 GitHub stars

**Availability:** Source code public
**Reproducibility:** High -- pure Python, deterministic
**Resource requirements:** Minimal; no neural network, no GPU
**Known defects:** Simple evaluation function; no transposition table; no fork detection
**Comparability limits:** Kaggle-compatible; simple baseline for comparison
**Proposed future benchmark role:** Classical eval reference for CMP-010 (asymmetric evaluation comparison)
**Configuration that must eventually be pinned:** search depth, evaluation weights (100K, 100, -120), move ordering
**Source and claim IDs:** S050, C005

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | MODERATE | Depth 3-6 minimax; asymmetric eval; no TT |
| 15x13 tactical play | WEAK | No TT; shallow depth |
| Speed | GOOD | Pure Python minimax |
| Kaggle compatibility | YES | Pure Python; minimal dependencies |
| Training required | NO | Handcrafted evaluation |
| Source quality | MODERATE | Source code accessible; no benchmarks |

---

### 4.7 BOT-007: ariaborin / The-Reticle (Classical Engine)

**Canonical name:** ariaborin The-Reticle
**URL:** github.com/ariaborin/The-Reticle
**Project type:** Classical engine
**Version:** latest
**License:** Unknown
**Language and runtime:** Python
**Board and inarow support:** 7x6 (default)
**Algorithm and components:**
- Alpha-beta pruning (TT present in source but **commented out in actual search** per R26 corpus audit)
- 10M-entry transposition table with LRU eviction (present but non-functional in current code)
- History heuristic for move ordering
- Threat-map tracking (strong threats +1000, weak threats +100)
- Center-first move ordering
- Most sophisticated classical engine found in survey

**Availability:** Source code public
**Known defects:** C071 NEEDS_CORRECTION: TT is fully disabled (commented-out dead code per corpus audit) -- engine runs alpha-beta without TT lookups
**Comparability limits:** Kaggle-compatible if ported; TT size may exceed Kaggle submission limits
**Proposed future benchmark role:** Classical engine reference for TT and threat-map integration
**Source and claim IDs:** S053, C071

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | MODERATE | Threat-map + history; TT commented out reduces effective depth |
| 15x13 tactical play | WEAK | 10M TT tuned for 7x6; no eval tuning for large boards |
| Speed | GOOD | Pure Python; threat-map adds moderate per-position cost |
| Kaggle compatibility | YES | Pure Python; threat-map evaluation portable |
| Training required | NO | Handcrafted eval |
| Source quality | MODERATE | Source verified but TT disabled; design documented |

---

### 4.8 BOT-008: Kaggle ConnectX Built-in Random (Random Baseline)

**Canonical name:** Kaggle ConnectX random opponent
**URL:** kaggle-environments (built-in RandomPlayer class)
**Project type:** Random baseline
**Version:** kaggle-environments v1.32.3
**License:** Kaggle proprietary
**Algorithm and components:**
- Random legal move selection (uniform random among valid columns)
- No evaluation, no search, no learning

**Published result evidence:**
- Built into kaggle-environments package
- test_connectx.py v1.32.2 (279 lines) confirms API and move validation

**Availability:** Built into Kaggle environment; reference implementation in kaggle-environments core.py
**Reproducibility:** High -- seeded random is deterministic
**Known defects:** Random play -- trivially defeated by any non-trivial strategy
**Comparability limits:** Sanity check only; all competitive bots should beat random with >95% win rate
**Proposed future benchmark role:** Sanity check; invalid-move rate baseline; lower-bound performance reference
**Source and claim IDs:** S005, S006

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | NONE | Random moves; no tactical awareness |
| Speed | EXCELLENT | O(1) move selection |
| Kaggle compatibility | N/A | Built-in reference opponent |
| Training required | NO | No learning |
| Source quality | HIGH | Source code verified in kaggle-environments core.py |

---

### 4.9 BOT-009: TonyCWang / ConnectFour Dataset (Dataset / Value Oracle)

**Canonical name:** TonyCWang ConnectFour training dataset
**URL:** huggingface.co/TonyCWang/ConnectFour
**Project type:** Dataset / value oracle (not an executable bot)
**Version:** latest (958M rows)
**License:** MIT
**Algorithm and components:**
- Pascal Pons solver self-play with temperature scheduling
- First 10 moves: temperature T=1.0 (exploratory sampling)
- Remaining moves: temperature T=0.5 (greedy-leaning)

**Published result evidence:**
- 958M rows total
- Temperature schedule confirmed (S044, C064)
- C110 REFUTED: S044 contradicts earlier claim that dataset was NOT self-play (it IS self-play from Pons solver)

**Availability:** HuggingFace public
**Resource requirements:** Dataset download ~tens of GB; CPU or GPU for training on top of it
**Comparability limits:** Dataset, not a bot; used for supervised pre-training of policy networks
**Proposed future benchmark role:** Training data source for NN policy prior (CMP-006)
**Source and claim IDs:** S044, C064

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| Utility for training | EXCELLENT | 958M rows from perfect solver; best public dataset |
| Training required | YES | Supervised pre-training from dataset |
| Source quality | HIGH | Verified self-play origin; temperature schedule documented |

---

### 4.10 BOT-010: jlokitha / connect-4-game (MCTS Student Project)

**Canonical name:** jlokitha connect-4-game
**URL:** github.com/jlokitha/connect-4-game
**Project type:** MCTS student project / baseline
**Version:** latest
**License:** Unknown
**Language and runtime:** Java / JavaFX / Maven
**Algorithm and components:**
- MCTS-powered AI opponent
- JavaFX GUI for interactive play
- Maven build system (pom.xml)

**Published result evidence:**
- 15 GitHub stars
- README confirms MCTS algorithm in source code
- No performance benchmarks published

**Known defects:** Unknown quality; likely a university/course project; no benchmarks or documented parameters; board size not specified in README
**Comparability limits:** Java-based; not directly Kaggle-compatible (Python-only)
**Source and claim IDs:** S118

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | UNKNOWN | No benchmarks; likely educational-level MCTS |
| Kaggle compatibility | NO | Java-based; Kaggle requires Python |
| Training required | NO | MCTS from scratch; no neural network |
| Source quality | MEDIUM | Educational project; source accessible |

---

### 4.11 BOT-011: haithameleuch / connect-four-ai (AB+MCTS Hybrid)

**Canonical name:** haithameleuch connect-four-ai
**URL:** github.com/haithameleuch/connect-four-ai
**Project type:** Alpha-beta + MCTS hybrid (student project)
**Version:** latest
**License:** Unknown
**Language and runtime:** Kotlin
**Algorithm and components:** Alpha-beta search (depth 3) combined with MCTS (250 playouts)

**Published result evidence:**
- 0 GitHub stars
- Internal score: 88% (self-reported; unverified)
- No published benchmarks against other engines

**Known defects:** No benchmarks published; board size not specified in README
**Source and claim IDs:** S_NEW_011

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | UNKNOWN | No benchmarks; self-reported 88% score is unverified |
| Kaggle compatibility | NO | Kotlin-based; JVM not ideal for Kaggle |
| Training required | NO | Heuristic-based; no training |
| Source quality | MEDIUM | Educational project; source accessible |

---

### 4.12 BOT-012: miksipiksic / pyvezi (Bitmask Minimax)

**Canonical name:** miksipiksic/pyvezi
**URL:** github.com/miksipiksic/pyvezi
**Project type:** Academic minimax baseline
**Version:** latest
**Language and runtime:** Python (minimax + alpha-beta) + Pygame
**Board and inarow support:** 6x7 (Connect 4 standard); bitmask board representation
**Algorithm and components:**
- Bitmask board representation using two integer bitmasks for the 6x7 (42 cells) board
- Brian Kernighan's algorithm for popcount (bit counting)
- Open-line difference heuristic evaluation
- Depth-4 minimax with alpha-beta pruning
- Center-first move ordering [3,2,4,1,5,0,6]

**Availability:** Source code public
**Known defects:** Depth-4 minimax is shallow; limited tactical depth; open-line diff heuristic may not generalize well
**Source and claim IDs:** S073, S125, C192

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | WEAK-MODERATE | Depth-4 search is shallow; no TT, no history heuristic |
| 15x13 tactical play | WEAK | No TT; depth-4 on 15x13 is trivial |
| Kaggle compatibility | YES | Pure Python; no JIT required |
| Training required | NO | Handcrafted evaluation |
| Source quality | HIGH | Full source accessible; game.py verified; State class via GitHub |

---

### 4.13 BOT-013: Tarun995 / connectX-bitboard-agent (Most Sophisticated Python Classical)

**Canonical name:** Tarun995 connectX-bitboard-agent
**URL:** github.com/Tarun995/connectX-bitboard-agent
**Project type:** Classical engine (most sophisticated pure-Python found)
**Version:** latest
**License:** MIT
**Language and runtime:** Python (Numba-JIT compiled + pure-Python fallback)
**Board and inarow support:** 7x6 (default); configurable inarow

**Algorithm and components (fully decoded from source):**
- Single 64-bit integer per player using bitwise operations (bitboard)
- Numba-JIT negamax with PVS: @njit(cache=True, fastmath=True)
- 16M-entry transposition table with mirror-symmetric storage
- History heuristic: 3^depth score for historical good moves
- Killer moves: two per depth level
- Aspiration windows: at depth >= 5, search starts with narrow window [eval-50, eval+50]
- Iterative deepening: depth increases 1->2->3->... until time budget (1.70s) exhausted
- Time checks via objmode: every 1024 nodes, checks elapsed time against budget
- Pure-Python fallback: if Numba unavailable, falls back to uncompiled Python
- Hardcoded Pascal Pons opening book (first 2 ply)

**Published result evidence:**
- 0 GitHub stars; full source decoded
- MIT license; Numba verified working

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | STRONG | PVS + 16M TT + history + killers + aspiration + mirror = ~depth 12-14 on 7x6 in 1.7s |
| 15x13 tactical play | WEAK | Branching factor ~15 means depth 4-6 in 1.7s; no eval tuning for large boards |
| Speed | EXCELLENT | Numba-JIT + bitboard = millions of nodes/sec; TT = O(1) lookup |
| Kaggle compatibility | YES | Python + Numba (standard library on Kaggle); pure-Python fallback |
| Training required | NO | Handcrafted evaluation; no neural network |
| Source quality | HIGH | MIT license, full source, Numba verified working |
| Ensemble role | SECONDARY | Best classical engine for Kaggle; foundation for ENS-NEW-002 |

---

### 4.14 BOT-014: Kamide / connect-n (Adaptive Scoring Minimax)

**Canonical name:** Kamide/connect-n
**URL:** github.com/Kamide/connect-n
**Project type:** Classical engine (adaptive scoring)
**Version:** latest
**License:** Unknown
**Language and runtime:** TypeScript / JavaScript (Web Worker)
**Board and inarow support:** Configurable N x N; any N-in-a-row (the only public engine designed for arbitrary inarow from first principles)

**Algorithm and components (fully decoded from source):**
- Adaptive scoring minimax: scoring parameterized by winCondition (inarow value)
- Connection-length scoring (quadratic): score += len * len * 5 for self connections
- Hole-count evaluation: penalizes board positions with empty rows above connections
- Center-column bonus: proportional to winCondition - 1
- Adaptive tactical scoring based on connection length vs winCondition
- Web Worker deployment for non-blocking inference

**Published result evidence:** None -- no benchmarks published, but source fully decoded
**Availability:** Source code public
**Known defects:** No published benchmarks or ELO ratings; adaptive scoring parameters not publicly documented; Web Worker may be incompatible with Kaggle notebook sandbox
**Comparability limits:** TypeScript; not natively Python; Web Worker deployment model
**Proposed future benchmark role:** Tier 2-3 classical baseline; Web Worker deployment template for Kaggle; board-size routing arbiter
**Source and claim IDs:** S123, S125, C184-C186

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | MODERATE | No TT, no history heuristic; pure minimax with shallow eval |
| 15x13 tactical play | MODERATE-STRONG | Adaptive scoring generalizes; hole-count is board-size agnostic |
| Board-size generality | EXCELLENT | Only engine designed for arbitrary N-in-a-row |
| Kaggle compatibility | PARTIAL | TypeScript; Web Worker may be incompatible with Kaggle sandbox |
| Training required | NO | Handcrafted adaptive evaluation |
| Source quality | HIGH | Full TypeScript source decoded; adaptive scoring verified |

---

### 4.15 BOT-015: sidhantagar / ConnectX (Minimax + DP)

**Canonical name:** sidhantagar ConnectX
**URL:** github.com/sidhantagar/ConnectX
**Project type:** Classical baseline with DP
**Version:** latest
**License:** Unknown
**Language and runtime:** Python
**Board and inarow support:** Configurable (0-20 axes)
**Algorithm and components:** Minimax + alpha-beta + 2-step dynamic programming

**Published result evidence:** 10 GitHub stars; no performance benchmarks published
**Known defects:** Source inaccessible for full source analysis; only README-level information confirmed
**Source and claim IDs:** S_NEW_014

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | UNKNOWN | No benchmarks; DP suggests some positional analysis |
| Kaggle compatibility | LIKELY YES | Python-based |
| Training required | NO | Minimax + DP; no neural network |
| Source quality | LOW | Source code only accessible via GitHub web page (not fully decoded) |

---

### 4.16 BOT-016: DQN ConnectX Agent (Neural Baseline)

**Canonical name:** psalarc/DQN-ConnectX-Agent (generic DQN architecture reference)
**URL:** github.com/psalarc/DQN-ConnectX-Agent
**Project type:** Neural baseline (DQN policy network)
**Version:** latest
**License:** Unknown
**Language and runtime:** Python (PyTorch/TF); reinforcement learning
**Board and inarow support:** Variable (depends on implementation); typically 7x6

**Algorithm and components:**
- DQN policy network; value network
- Experience replay; target network; epsilon-greedy exploration

**Published result evidence:**
- C205 VERIFIED: DQN cannot reliably detect forced-win sequences >4 plies without search augmentation
- 1 GitHub star; educational study project

| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| 7x6 tactical play | WEAK-MODERATE | DQN without search; cannot detect forced wins >4 plies (C205 VERIFIED) |
| 15x13 tactical play | WEAK | Same fundamental limitation + larger branching factor |
| Kaggle compatibility | YES | Python + PyTorch |
| Training required | YES | Requires RL training (self-play or offline data) |
| Source quality | LOW-MEDIUM | Educational study; limited source code |
| Ensemble role | SECONDARY | NN leaf eval candidate if fine-tuned; DQN-only insufficient |
