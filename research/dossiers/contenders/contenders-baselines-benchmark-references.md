# Contenders, Baselines, and Benchmark References

> **Dossier ID**: DOS-005
> **Status**: COMPLETE
> **Last Updated**: 2026-08-04
> **Scope**: All public ConnectX bots, Kaggle submissions, baseline implementations, and benchmark references
> **Related IDs**: BOT-001 through BOT-016 (contender roster), ENS-001 through ENS-024 (ensemble catalog), BMS-001 through BMS-012 (benchmark blueprint), EXP-001 through EXP-032 (future experiments)

---

## Executive Summary

This dossier provides a comprehensive inventory of all known ConnectX and Connect 4 bots, their implementations, and the benchmarking frameworks used to evaluate them. The corpus spans 20+ public repositories with a total of approximately 200 GitHub stars across all projects.

The landscape reveals a clear stratification:

- **Tier 0 (Oracle)**: Solved-game engines (Pascal Pons, Tromp) - perfect play, not Kaggle-deployable
- **Tier 1 (Hybrid)**: Neural + MCTS (katac4, rowspire) - strongest documented approaches
- **Tier 2 (MCTS)**: Pure MCTS (connectpuct, jlokitha) - no neural component, weaker on 7x6
- **Tier 3 (Classical)**: Minimax/alpha-beta (QveenCoder, Kamide, pyvezi, ariaborin) - fast but shallow
- **Tier 4 (Neural Baseline)**: DQN/PPO (kirripit, BEPb, neoyung, marcpaulo15) - training-heavy, unproven competitive strength
- **Tier 5 (Random)**: Kaggle built-in random - sanity check only

**Most Complete Training Framework**: kirripit/connect4 (MIT, 33 stars) - DQN, Double DQN, Dueling DQN, Policy Gradient, A3C, and AlphaGo Zero all in one repo.

**Most Kaggle-Relevant**: BEPb/Kaggle_ConnectX (23 stars) - AlphaZero with PARL parallel self-play, xparl cluster, gen_submission.py for Kaggle packaging.

**Strongest Pure Classical**: QveenCoder/connect-four with asymmetric eval (win:100K, near-win:100, opponent near-win:-120).

**Key Finding**: No public bot combines (1) ResNet neural network, (2) PUCT MCTS with FPU/LCB, (3) alpha-beta with transposition table, AND (4) Kaggle T4 GPU inference. The closest is katac4 (ResNet + PUCT MCTS, no alpha-beta) and ariaborin/The-Reticle (alpha-beta + TT + threat-map, no neural network). This gap is the largest competitive opportunity in ConnectX.
---

## 1. Contender Classification Matrix

### 1.1 Full Contender Inventory

| # | ID | Name | Repo | Stars | License | Algorithm | Board Support | Language | Kaggle Compatible |
|---|-----|------|------|-------|---------|-----------|---------------|----------|-------------------|
| 1 | BOT-001 | Pascal Pons | github.com/PascalPons/connect4 | - | AGPL v3 | Negamax + AB + PVS + TT + Book | 7x6, 8x8, 9x6, 10x8, 10x10 | C++ | No |
| 2 | BOT-002 | Tromp 8x8 | github.com/tromp/fhourstones88 | 0 | - | Negamax + AB + TT + Forks | 8x8 | C++ | No |
| 3 | BOT-003 | katac4 | github.com/GoodCoder666/katac4 | 18 | MIT | ResNet + PUCT MCTS + self-play | 7x6, 8x8 | Python/PyTorch | Yes |
| 4 | BOT-004 | rowspire | github.com/tre-systems/rowspire | 0 | - | Dual MLP + UCB1 MCTS + bitboard | 7x6 | Rust | Partial (WASM) |
| 5 | BOT-005 | connectpuct | github.com/ahmeddoghri/connectpuct | 0 | - | PUCT MCTS + tactical priors | 7x6 | Python | Yes |
| 6 | BOT-006 | QveenCoder | github.com/QveenCoder/connect-four | 13 | - | Minimax + AB + asymmetric eval | 7x6 | Python/JS | Yes |
| 7 | BOT-007 | The-Reticle | github.com/ariaborin/The-Reticle | - | - | AB + 10M TT + threat-map | 7x6 | Python | Yes |
| 8 | BOT-008 | Kaggle Random | kaggle-environments | - | Kaggle | Random legal move | Configurable | Python | N/A (built-in) |
| 9 | BOT-009 | TonyCWang dataset | huggingface.co/TonyCWang/ConnectFour | - | MIT | Pons solver self-play (T=1.0 to 0.5) | 7x6 | N/A (dataset) | N/A (training data) |
| 10 | BOT-010 | jlokitha MCTS | github.com/jlokitha/connect-4-game | 15 | - | MCTS + JavaFX GUI | Unknown | Java/JavaFX | No |
| 11 | BOT-011 | kamide connect-n | github.com/Kamide/connect-n | - | - | Adaptive scoring minimax + Web Worker | Configurable N x N | TypeScript | Partial |
| 12 | BOT-012 | pyvezi bitboard | github.com/miksipiksic/pyvezi | - | - | Bitmask minimax + alpha-beta | 6x7 | Python | Yes |
| 13 | BOT-013 | connectX-bitboard-agent | github.com/Tarun995/connectX-bitboard-agent | 0 | MIT | Bitboard + Numba + 16M TT + PVS | 7x6 | Python | Yes |
| 14 | BOT-014 | ConnectX (sidhantagar) | github.com/sidhantagar/ConnectX | 10 | - | Minimax + AB + 2-step DP | Configurable (0-20 axes) | Python | Yes |
| 15 | BOT-015 | haithameleuch hybrid | github.com/haithameleuch/connect-four-ai | 0 | - | AB depth-3 + MCTS (250 playouts) | 7x6 | Kotlin | No |
| 16 | BOT-016 | DQN-ConnectX-Agent | github.com/psalarc/DQN-ConnectX-Agent | 1 | - | DQN architecture study | Configurable | Python/PyTorch | Yes |

### 1.2 Kaggle Submissions

| # | Name | Repo/URL | Stars | Status | Verified |
|---|------|----------|-------|--------|----------|
| 1 | snap-stanford/connectx-kaggle | github.com/snap-stanford/connectx-kaggle | - | Stanford Kaggle submission | YES (R4, now 404) |
| 2 | DariusDahl/kaggle-connectx-competition | github.com/DariusDahl/kaggle-connectx-competition | - | Top 10% (skill 714.5 claimed) | NO (refuted) |
| 3 | AgustinHualde1/Kaggle-ConnectX-bot | github.com/AgustinHualde1/Kaggle-ConnectX-bot | - | Kaggle submission | NO (unreliable) |
| 4 | ManuelFay/Alpha_Connect4 | github.com/ManuelFay/Alpha_Connect4 | - | AlphaZero variant | NO (unreliable) |
| 5 | kirripit/connect4 | github.com/kirripit/connect4 | 33 | MIT, DQN + A3C + AlphaGo Zero | YES (R4) |
| 6 | BEPb/Kaggle_ConnectX | github.com/BEPb/Kaggle_ConnectX | 23 | AlphaZero + PARL + xparl cluster | YES (R4) |

Note: snap-stanford/connectx-kaggle returns 404 on WebFetch (may be private). BEPb and kirripit are confirmed working.

---

## 2. Detailed Contender Profiles

### 2.1 Tier 0: Oracle / Perfect-Play

**BOT-001: Pascal Pons / connect4 (Oracle / Perfect-Play Reference)**

- **URL**: github.com/PascalPons/connect4
- **License**: AGPL v3
- **Algorithm**: Negamax + alpha-beta + PVS + transposition table + opening book
- **Board Support**: 7x6, 8x8, 9x6, 10x8, 10x10 (constexpr, not dynamic)
- **Key Feature**: Iterative binary search for exact game values
- **Known Defect**: Board sizes are constexpr -- not dynamic runtime parameters (R15 confirmed no PVS in actual code despite C++ source suggesting PVS)
- **Kaggle Compatibility**: No - C++ binary, not Python API
- **Benchmarks**: Solved 7x6, 8x8 (P2 win), 9x6, 10x8 (draw)
- **Key Source**: DEPTH=14 opening book generator, fully decoded R11 (negamax.cpp, C488.cpp, 46 lines)

**BOT-002: Tromp fhourstones88 (Oracle / 8x8 Solver)**

- **URL**: github.com/tromp/fhourstones88
- **Algorithm**: Standard full-window alpha-beta (NO MTD(f), NO PVS per R32 verification)
- **Key Feature**: book88 (~500MB compressed, 16 ply), O(7) inline fork detection
- **Result**: 8x8 solved as P2 win (late 2014 / early 2015)
- **Kaggle Compatibility**: No - different board size, C++ only

### 2.2 Tier 1: Hybrid Neural + MCTS

**BOT-003: GoodCoder666 / katac4 (Hybrid Baseline - Neural + MCTS)**

- **URL**: github.com/GoodCoder666/katac4
- **License**: MIT
- **Stars**: 18
- **Neural Architecture**: PyTorch ResNet b3c128nbt - 3 bottleneck blocks, 128 channels, ~530K params
- **MCTS**: PUCT c=1.0 (train) / 1.1 (inference), FPU c_fpu=0.2, LCB move selection, 1600 simulations
- **Training**: Self-play, 300K games, 30K epochs, 3 loss terms (policy CE + 1.5*value CE + 0.15*rival CE), 16 parallel workers, SGD+momentum
- **Board Support**: 7x6 (default), 8x8 (configurable)
- **GPU**: TensorRT FP16 ResNet-18 on T4: ~1.10ms inference
- **Known Defect**: NN generalization to 15x13 unverified
- **Kaggle Compatibility**: Yes - Python + PyTorch, model fits submission limits
- **ELO**: Training self-comparison: b3c128_v1 ~1080 to ~1178 (300K ELO games)

**BOT-004: tre-systems / rowspire (Hybrid - Neural MCTS + Bitboard)**

- **URL**: github.com/tre-systems/rowspire
- **Stars**: 0
- **Neural Architecture**: Dual 4x128 MLP with skip connections (value + policy network)
- **MCTS**: UCB1 c=1.41, 4000 simulations, NN-guided playouts, Dirichlet root noise 0.8 (75/25 split)
- **Board Support**: 7x6 (bitboard, 64-bit with sentinel row)
- **Heuristic**: 7-feature evaluation with genetic tuning (evolved weights: threat=3.851, horiz=2.840, piece_count=0.113)
- **Training**: 50-epoch supervised curriculum distillation, 250K samples + mirroring (decoded R15)
- **Deployment**: WASM (npm run train, npm run build)
- **Key Source**: 14 Rust files decoded (neural_network.rs, bitboard_solver.rs, evaluation.rs, features.rs)
- **Kaggle Compatibility**: Partial - WASM deployment path; not directly Python-compatible

### 2.3 Tier 2: Pure MCTS

**BOT-005: ahmeddoghri / connectpuct (MCTS Baseline)**

- **URL**: github.com/ahmeddoghri/connectpuct
- **Stars**: 0
- **Algorithm**: PUCT MCTS with tactical priors
- **Simulation Count**: 80 (per benchmark vs minimax depth 3)
- **Key Result**: PUCT MCTS: 11W / 9L in 20 matches vs minimax depth 3 (55% win rate)
- **Known Defect**: C135 VERIFIED - does not consult solved-game databases; consistency problem for drawn positions
- **Kaggle Compatibility**: Yes - pure Python, no GPU required

**BOT-010: jlokitha / connect-4-game (Student MCTS Project)**

- **URL**: github.com/jlokitha/connect-4-game
- **Stars**: 15
- **Algorithm**: MCTS-powered AI opponent
- **Board Support**: Unknown (JavaFX app, board size not specified in README)
- **Key Feature**: JavaFX GUI for interactive play, Maven build system
- **Known Defect**: Unknown quality - likely a university/course project; no benchmarks published
- **Kaggle Compatibility**: No - Java-based, not Python

### 2.4 Tier 3: Classical Engines

**BOT-006: QveenCoder / connect-four (Lightweight Classical)**

- **URL**: github.com/QveenCoder/connect-four
- **Stars**: 13
- **Algorithm**: Minimax + alpha-beta pruning, configurable depth (3-6)
- **Evaluation**: Asymmetric window scoring - AI win: 100K, near-win: 100, opponent near-win: -120 (1.2x opponent threat amplification)
- **Board Representation**: 2D array, row-major
- **Language**: Python + vanilla JS with browser + Node.js exports
- **Tests**: 14 unit tests, no dependencies
- **Kaggle Compatibility**: Yes - pure Python
- **Key Source**: Source code verified R13 (asymmetric eval C005 VERIFIED)

**BOT-007: ariaborin / The-Reticle (Sophisticated Classical)**

- **URL**: github.com/ariaborin/The-Reticle
- **Algorithm**: Minimax + alpha-beta + 10M-entry TT (LRU eviction) + history heuristic (3^depth) + threat-map evaluation (plus/minus 1000 strong, plus/minus 100 weak) + iterative deepening with time limit
- **Board Representation**: Column-major with hash()
- **Key Feature**: Most sophisticated classical engine found in survey - TT + history + threat-map
- **Kaggle Compatibility**: Yes - Python
- **Known Defect**: C071 NEEDS_CORRECTION - TT source code needs re-verification

**BOT-011: Kamide / connect-n (Adaptive Scoring Minimax)**

- **URL**: github.com/Kamide/connect-n
- **Algorithm**: Adaptive scoring minimax with alpha-beta; connection-length scoring + hole-count evaluation
- **Board Support**: Configurable N x N boards; any N-in-a-row
- **Language**: TypeScript / JavaScript
- **Key Feature**: Web Worker non-blocking inference; designed for browser deployment
- **Known Defect**: No published benchmarks or ELO ratings; Web Worker may be incompatible with Kaggle notebook sandbox

**BOT-012: miksipiksic / pyvezi (Bitmask Minimax)**

- **URL**: github.com/miksipiksic/pyvezi
- **Algorithm**: Bitmask board representation; open-line diff heuristic; depth-4 minimax with alpha-beta
- **Board Support**: 6x7 (Connect 4 standard)
- **Key Feature**: Bitmask board representation
- **Known Defect**: Depth-4 minimax is shallow; limited tactical depth

**BOT-013: Tarun995 / connectX-bitboard-agent (Bitboard + Numba)**

- **URL**: github.com/Tarun995/connectX-bitboard-agent
- **License**: MIT
- **Algorithm**: Bitboard implementation with Numba JIT; PVS search + 16M-entry transposition table
- **Board Support**: 7x6 (42 cells plus sentinel rows)
- **Key Feature**: Single 64-bit integer per player; bitwise win detection (m = pos & (pos >> 7)); warm-up call for Numba JIT
- **Known Defect**: Zero stars; no benchmarks published

**BOT-014: sidhantagar / ConnectX (Minimax + DP)**

- **URL**: github.com/sidhantagar/ConnectX
- **Stars**: 10
- **Algorithm**: Minimax with alpha-beta pruning; 2-step lookahead with dynamic programming for state reuse
- **Board Support**: Configurable two-dimensional grid (0-20 axes), configurable inarow (3-10)
- **Known Defect**: 2-step lookahead is very shallow; no eval function mentioned

**BOT-015: haithameleuch / connect-four-ai (Alpha-Beta + MCTS Hybrid)**

- **URL**: github.com/haithameleuch/connect-four-ai
- **Stars**: 0
- **Algorithm**: Alpha-beta depth-3 + Monte Carlo leaf evaluation (250 random playouts)
- **Board Representation**: 2D array (integers -1, 1, 0)
- **Performance**: 88% overall performance score
- **Language**: Kotlin
- **Kaggle Compatibility**: No - Kotlin, not Python

---

### 2.5 Neural Baselines (DQN / PPO / AlphaZero)

**BOT-016: kirripit / connect4 (Comprehensive RL Framework)**

- **URL**: github.com/kirripit/connect4
- **Stars**: 33
- **License**: MIT
- **Algorithms**: DQN, Double DQN, Dueling DQN, Policy Gradient, A3C, AlphaGo Zero (six different RL algorithms)
- **Neural Network**: Toggleable convolutional + residual layers; spatial board representation
- **Training Pipeline**:
  1. Board object initialization to two player objects to central simulator
  2. Self-play or Minimax matchups
  3. Customizable hyperparameters
  4. N-step returns for sparse reward stabilization
- **Performance**: 4x5 grid - defeats near-optimal Minimax in 95% of matches; 6x7 - five-day AlphaZero run yields "strong amateur player"
- **Key Feature**: Most comprehensive public Connect 4 training framework - every major RL algorithm in one repo

**BOT-017: BEPb / Kaggle_ConnectX (Kaggle-AlphaZero)**

- **URL**: github.com/BEPb/Kaggle_ConnectX
- **Stars**: 23
- **Algorithm**: AlphaGo Zero with self-play training
- **Framework**: PARL (parallel RL framework for distributed training)
- **Pipeline**: Initialize with 1000 random agent matches; Launch xparl cluster for parallel self-play; main.py executes RL training loop; Export trained weights to saved_model/; gen_submission.py packages for Kaggle
- **Kaggle Compatibility**: Yes - designed for Kaggle (gen_submission.py)
- **Known Defect**: No performance benchmarks published; NN architecture unspecified in README

**BOT-018: neoyung / connect-4 (DQN Baseline)**

- **URL**: github.com/neoyung/connect-4
- **Algorithm**: DQN with Bellman optimality equation; experience replay; self-play
- **Neural Network**: Convolutional model approximating state-action values; input as 6x7x1 image tensors
- **Training**: 20,000 epochs; learns from scratch through autonomous gameplay
- **Performance**: After 20K epochs, policy shows "reliable stability, secures frequent victories"

**BOT-019: marcpaulo15 / RL-connect4 (Two-Stage: SFT to RL)**

- **URL**: github.com/marcpaulo15/RL-connect4
- **Algorithms**: PPO, REINFORCE, DQN, Dueling DQN
- **Training Pipeline**: Two-phase:
  1. Supervised pre-training: CNN learns from 200K heuristic actions (NStepLookaheadAgent)
  2. RL fine-tuning: Freeze CNN feature extractor; train only FC heads via self-play
- **Environment**: OpenAI Gym standard
- **Interface**: Pygame GUI for human vs AI
- **Known Defect**: No quantitative performance metrics published

**BOT-020: psalarc / DQN-ConnectX-Agent (DQN Architecture Study)**

- **URL**: github.com/psalarc/DQN-ConnectX-Agent
- **Stars**: 1
- **Architecture**: Tests 1-4 layer networks, 64-512 units per layer
- **Framework**: PyTorch
- **Key Finding**: "Training time scaled significantly with layer count and layer size. Wider networks produced marginal improvements in learning quality yet delivered negligible returns compared to extra processing demands. Streamlined configurations proved far more efficient."
- **Known Defect**: ML-focused submission; no competitive benchmarks

**BOT-021: ChristianMontecchiani / ConnectX_RL (MCTS without NN)**

- **URL**: github.com/ChristianMontecchiani/ConnectX_RL
- **Stars**: 0
- **License**: MIT
- **Algorithm**: MCTS with random playouts (no neural network)
- **MCTS Phases**: Selection (explore/exploit balance), expansion, backpropagation, simulation
- **Rollout Policy**: Random moves until game end or predefined depth

**BOT-022: sebadorn / Machine-Learning--Connect-Four (ML Benchmark)**

- **URL**: github.com/sebadorn/Machine-Learning--Connect-Four
- **Stars**: 13
- **Models Tested**: Multilayer Perceptron (MLP), Radial Basis Function (RBF), Perceptron Canonical Network (PCN), decision trees, K-Means
- **Data**: UCI Machine Learning Repository datasets
- **Key Feature**: ML model comparison framework for Connect 4
- **Known Defect**: Supervised learning on static datasets (no self-play); no reinforcement learning

**BOT-023: Zeta36 / connect4-alpha-zero (AlphaZero Variant)**

- **URL**: github.com/Zeta36/connect4-alpha-zero
- **Algorithm**: AlphaGo Zero with self-play training
- **Language**: Python 3.6.3, TensorFlow 1.3.0, Keras 2.0.8
- **Pipeline**: Three-process coordination - self-play data generation, model training, model assessment
- **Training**: Model generation every 2,000 steps; ~200 matches per comparison
- **Performance**: 6 generations in 4 hours; early iterations 100% win rate vs baseline, stabilized at 78.6-84.6%
- **Known Defect**: Outdated dependencies; no MCTS parameters published

**BOT-024: ManuelFay / Alpha_Connect4 (AlphaZero Variant)**

- **URL**: github.com/ManuelFay/Alpha_Connect4
- **Algorithm**: AlphaZero for Connect 4
- **Performance**: ~100% win rate early, then stabilized at 78.6%, 84.6%, 100% across generations
- **Known Defect**: Unreliable (R4 classified as unreliable)

---

## 3. Kaggle-Specific Analysis

### 3.1 Kaggle Environment Constraints

From the kaggle-environments v1.32.2/v1.32.3 source code (verified R19):

| Constraint | Value | Impact |
|-----------|-------|--------|
| **actTimeout** | 2 seconds per move | Limits search depth to approximately 6-8 ply on 15x13 |
| **agentTimeout** | 60 seconds total | Overtime buffer for difficult moves |
| **remainingOverageTime** | 60 seconds (spec override from global default 12) | Per-step overtime tracking |
| **maxLogLength** | 10,000 chars per agent per step | Limits debug output |
| **Board representation** | Flat 1D array (row-major) | Must use flat array, not 2D |
| **Board sizes** | 7x6 (default), 4x5/inarow=3 (tested), 15x13, 15x10 (supported by spec) | Multi-board support critical |
| **Submission limit** | 95MB binary assets | Opening books must fit |
| **Language** | Python (via agent.py) | No C++/Rust directly; WASM possible |

### 3.2 Kaggle-Compatible Bot Filter

Of the 24 contenders cataloged, **15 are Kaggle-compatible** (Python-based):

**Compatible (15)**:
- BOT-003 (katac4) - ResNet + PUCT MCTS
- BOT-005 (connectpuct) - PUCT MCTS
- BOT-006 (QveenCoder) - minimax + AB
- BOT-007 (The-Reticle) - AB + TT + threat-map
- BOT-012 (pyvezi) - bitmask minimax
- BOT-013 (connectX-bitboard-agent) - bitboard + Numba
- BOT-014 (ConnectX sidhantagar) - minimax + DP
- BOT-016 (kirripit) - DQN + A3C + AlphaGo Zero
- BOT-017 (BEPb) - AlphaZero + PARL
- BOT-018 (neoyung) - DQN
- BOT-019 (marcpaulo15) - SFT + PPO/DQN
- BOT-020 (psalarc) - DQN architecture study
- BOT-021 (ChristianMontecchiani) - MCTS without NN
- BOT-009 (TonyCWang) - dataset (training data)
- BOT-008 (random) - sanity check
- BOT-004 (rowspire) - WASM (partial compatibility)

Incompatible (9):
- BOT-001 (Pascal Pons) - C++, constexpr board sizes
- BOT-002 (Tromp) - C++, 8x8 only
- BOT-010 (jlokitha) - Java/JavaFX
- BOT-011 (Kamide) - TypeScript/Web Worker
- BOT-015 (haithameleuch) - Kotlin
- BOT-022 (sebadorn) - static dataset evaluation
- BOT-023 (Zeta36) - TensorFlow 1.3 outdated
- BOT-024 (ManuelFay) - unreliable

### 3.3 Performance Summary Matrix (Kaggle-Compatible Only)

| Bot | Algorithm | Board Support | Training Required | GPU Needed | Est. 7x6 Strength | Est. 15x13 Strength |
|-----|-----------|--------------|-------------------|------------|-------------------|---------------------|
| katac4 | ResNet + PUCT MCTS | 7x6, 8x8 | Yes (GPU, 8 days) | Yes (inference) | Strong (ELO ~1178) | Unknown |
| connectpuct | PUCT MCTS | 7x6 | No | No | Moderate (55% vs d3) | Unknown |
| QveenCoder | minimax + AB | 7x6 | No | No | Moderate (depth 3-6) | Weak (depth limits) |
| The-Reticle | AB + TT + threat-map | 7x6 | No | No | Strong (10M TT) | Weak (TT size) |
| connectX-bitboard | bitboard + Numba | 7x6 | No | Optional (Numba) | Strong (16M TT + PVS) | Weak |
| kirripit | DQN + A3C + AZ | 7x6, 4x5 | Yes (GPU) | Yes (training) | Moderate (95% on 4x5) | Unknown |
| BEPb | AlphaZero + PARL | Configurable | Yes (GPU cluster) | Yes (training) | Unknown (no benchmarks) | Unknown |
| marcpaulo15 | SFT + PPO/DQN | 7x6 | Yes (GPU) | Yes (training) | Moderate (200K SFT) | Unknown |
| neoyung | DQN | 7x6 | Yes (GPU) | Yes (training) | Moderate (20K epochs) | Unknown |
| random | Random | Configurable | No | No | 0% | 0% |

---

## 4. Benchmark Frameworks and Evaluation Methods

### 4.1 Benchmark Frameworks Found

| Framework | URL | Type | Connect 4 Support | Key Feature |
|-----------|-----|------|-------------------|-------------|
| eSlams | github.com/ElectronicSlams/eSlams | General AI game framework | Yes (50 arenas) | REST protocol, Ed25519 proofs, multi-provider adapters |
| Fhourstones | tromp.github.io/c4/fhour.html | Solved-game benchmark | Yes | 20 systems benchmarked, position analysis, Gprof profiling |
| connect4.gamesolver.org | connect4.gamesolver.org | Interactive solver | Yes | Column ratings, board-size matrix (4x4 to 11x11) |

### 4.2 Evaluation Metrics by Contender

| Bot | Evaluation Method | Metrics Published |
|-----|------------------|-------------------|
| connectpuct | Paired matches vs minimax d3 | 11W/9L (55% win rate) |
| haithameleuch | Internal test suite | 88% performance score |
| kirripit | Self-play (4x5) vs near-optimal Minimax | 95% win rate on 4x5 |
| kirripit | Self-play (6x7) | "Strong amateur" after 5 days (qualitative) |
| Zeta36 | Head-to-head vs baseline | 100% to 78.6% to 84.6% to 100% across generations |
| marcpaulo15 | Peer competition ranking | Visual chart, no numbers |
| Others | None published | - |

### 4.3 Missing Benchmark Data

The following critical benchmark data is **unavailable** from public sources:

1. **Kaggle leaderboard standings** - Top bot scores, strategies, and board-size performance (requires JS rendering of Kaggle leaderboard)
2. **ELO ratings for Connect 4 engines** - No formal multi-engine tournament exists (T014: NEGATIVE RESULT)
3. **Cross-board-size performance** - How 7x6-optimized bots perform on 15x13 and 15x10
4. **Time-constrained benchmarks** - Most contenders benchmark without 2-second/move limits
5. **First-player advantage on 15x13/15x10** - Unpublished (HYPOTHESIS C132)

---

## 5. Algorithm Comparison Matrix

### 5.1 Search Algorithm Effectiveness

| Algorithm | 7x6 Strength | 15x13 Strength | Search Depth (2s) | GPU Needed | Notes |
|-----------|-------------|-----------------|-------------------|------------|-------|
| Negamax + AB + PVS + TT | Perfect (solved) | Weak (depth 2-4) | 12+ on 7x6, 2-4 on 15x13 | No | Pascal Pons, Tromp, The-Reticle, connectX-bitboard |
| Minimax + AB (no TT) | Moderate (depth 3-6) | Very weak | 3-6 on 7x6, 1-2 on 15x13 | No | QveenCoder, pyvezi |
| PUCT MCTS (no NN) | Weak-Moderate | Unknown | 80-4000 sims (connectpuct: 80) | No | connectpuct (55% vs d3), jlokitha |
| PUCT MCTS + NN policy prior | Strong | Moderate | 1600 sims + NN guidance | Yes (inference) | katac4 (ELO 1178) |
| UCB1 MCTS + NN guidance | Strong | Moderate | 4000 sims + NN guidance | No (CPU) | rowspire (WASM) |
| DQN (no search) | Weak-Moderate | Unknown | One forward pass | Yes (training) | neoyung, psalarc |
| PPO / REINFORCE | Moderate | Unknown | One forward pass | Yes (training) | marcpaulo15 |
| AlphaGo Zero (self-play) | Moderate-Strong | Unknown | N/A (training) | Yes (training) | kirripit, BEPb, Zeta36 |

### 5.2 Neural Network Architecture Comparison

| Architecture | Bot(s) | Params | Board Input | Head(s) | Training Data | Strength |
|-------------|--------|--------|-------------|---------|--------------|----------|
| ResNet b3c128nbt (KataGo bottleneck) | katac4 | ~530K | 3 planes x R x C | Policy + Value | Self-play (300K games) | Strongest documented |
| Dual MLP 4x128 (skip connections) | rowspire | ~530K | 64 cells + 16 features | Policy + Value | 250K solver samples | Strong (NN-guided MCTS) |
| CNN (standard conv blocks) | marcpaulo15 | Unknown | 3 planes | Policy + Value | 200K heuristic samples | Moderate (SFT to RL) |
| Convolutional (DQN) | neoyung | Unknown | 6x7x1 image | Q-values | 20K epochs self-play | Moderate |
| Convolutional (toggleable) | kirripit | Unknown | Spatial board | Q-values | Minimax/self-play | Moderate (95% on 4x5) |
| Shallow DNN (1-4 layers) | psalarc | 64-512 units | Board array | Q-values | Self-play | Marginal improvement with depth |

### 5.3 Training Pipeline Comparison

| Pipeline | Bot | Data Source | Training Time | Compute | Data Volume |
|----------|-----|-------------|--------------|---------|-------------|
| Self-play (AlphaGo Zero) | kirripit | Self-generated | 5 days (6x7) | GPU cluster | Unknown |
| Self-play + PARL | BEPb | Self-generated | Unknown | xparl cluster | Unknown |
| AlphaZero (3-process) | Zeta36 | Self-generated | 4 hours (6 gens) | GPU | Unknown |
| SFT to PPO/DQN | marcpaulo15 | Heuristic + self-play | Unknown | GPU | 200K SFT + RL |
| SFT curriculum | rowspire | Solver distillation | 50 epochs | CPU (rayon parallel) | 250K samples |
| DQN | neoyung | Self-play | 20K epochs | GPU | Unknown |

---

## 6. Ensemble and Integration Opportunities

### 6.1 Identified Gaps - Integration Opportunities

| Gap | Opportunity | Source Components |
|-----|-------------|-------------------|
| No bot combines ResNet + alpha-beta + TT | **H-ENSEMBLE-001**: ResNet leaf eval + alpha-beta + TT | katac4 NN + The-Reticle search + connectX-bitboard agent |
| No bot combines multi-board NN + Kaggle deployment | **H-ENSEMBLE-002**: Multi-board ResNet + Kaggle submission | spooky-connect4 engine + katac4 NN architecture |
| No bot combines MCTS + classical search with fallback | **H-ENSEMBLE-003**: MCTS primary + alpha-beta fallback | connectpuct MCTS + QveenCoder minimax |
| No bot uses NNUE-style incremental evaluation | **H-ENSEMBLE-004**: NNUE eval + alpha-beta | ECML2022 NNUE paper + classical engine |
| No bot combines solved-game tablebook + NN search | **H-ENSEMBLE-005**: Tablebook opening + NN search | Pascal Pons solved DB + katac4 NN |

### 6.2 Recommended Kaggle Bot Architecture

Based on this survey, the optimal Kaggle ConnectX bot combines:

1. **Opening phase**: Tablebook from solved 7x6 game (Pascal Pons methodology)
2. **Midgame**: Alpha-beta + PVS + TT (10M entries, The-Reticle + connectX-bitboard)
3. **Leaf evaluation**: NN policy + value network (katac4 ResNet b3c128nbt)
4. **Large boards (15x13, 15x10)**: Fallback to classical engine only (NN not trained on these sizes)
5. **GPU acceleration**: TensorRT INT8 for NN inference (~0.5ms on T4)
6. **Time management**: Iterative deepening with 1.8s search budget, 0.2s safety margin

No single public bot implements this architecture. The closest is katac4 (NN + MCTS) which lacks alpha-beta search, and The-Reticle (alpha-beta + TT) which lacks neural network evaluation.

## 7. Benchmark Blueprint Implications

### 7.1 Required Benchmark Opponents

| Tier | Bot | Source | Purpose |
|------|-----|--------|---------|
| 1 | Kaggle Random | Built-in | Sanity check |
| 2 | Depth-2 Minimax | QveenCoder (adapted) | Shallow search baseline |
| 3 | Depth-4 Minimax | pyvezi (adapted) | Classical baseline |
| 4 | PUCT MCTS | connectpuct | MCTS baseline |
| 5 | Alpha-Beta + TT | The-Reticle | Classical engine baseline |
| 6 | Bitboard + Numba | connectX-bitboard-agent | Bitboard baseline |
| 7 | ResNet + MCTS | katac4 | Neural MCTS baseline |
| 8 | DQN | neoyung (adapted) | Neural baseline |
| 9 | Tablebook Classical | Pascal Pons (adapted) | Perfect-play baseline |
| 10 | Hybrid (proposed) | Our target bot | Evaluated against tiers 1-9 |

### 7.2 Critical Benchmark Tests

1. **Tactical correctness suite**: 1,000+ forced-win/block positions (Tier A)
2. **Opening play suite**: 7 first moves x 100 games vs tablebook (Tier B)
3. **Multi-board strength**: 100 games each on 7x6, 8x8, 15x13 (Tier E)
4. **Time-constrained performance**: 500 games with strict 2s/move (Tier F)
5. **MCTS consistency**: Oracle agreement vs Pascal Pons at increasing sim counts (BMS-005)
6. **Board-size generalization**: Transfer from 7x6 to 15x13 (BMS-007)

## 8. Feasibility Matrix

### 8.1 Implementation Feasibility

| Approach | Local CPU (RTX 5090) | Kaggle T4 | Kaggle CPU | Submission Size | Complexity |
|----------|---------------------|-----------|------------|-----------------|------------|
| Classical only (alpha-beta + TT) | Excellent | Excellent | Excellent | Small (<5MB) | Low |
| ResNet + MCTS (katac4) | Excellent | Good (GPU needed) | Poor (no GPU) | Medium (~10MB weights) | High |
| ResNet + alpha-beta | Excellent | Good (GPU inference) | Good (CPU inference slower) | Medium | High |
| DQN only | Excellent | Good | Poor | Small (~1MB) | Medium |
| Tablebook + classical | Excellent | Excellent | Excellent | Large (opening book ~100MB) | Medium |
| Hybrid (tablebook + NN + alpha-beta) | Excellent | Good | Moderate | Large | Very High |

### 8.2 Deployment Feasibility

| Bot | Kaggle CPU | Kaggle T4 | RTX 5090 (training) | Notes |
|-----|-----------|-----------|---------------------|-------|
| katac4 | Moderate (no GPU acceleration) | Excellent | Excellent | Best Kaggle-compatible hybrid |
| connectpuct | Good | Good | N/A | Fast but weak (no NN) |
| QveenCoder | Excellent | Excellent | N/A | Fast but shallow |
| The-Reticle | Good (10M TT ~50MB) | Excellent | N/A | Strong classical baseline |
| connectX-bitboard | Excellent (Numba JIT) | Excellent | N/A | Fast bitboard + TT |
| kirripit | Poor (training-heavy) | Good (training) | Excellent | Best for training, not deployment |
| BEPb | Poor (PARL cluster) | Good (PARL) | N/A | Cluster-dependent |

---

## 9. Source Quality Assessment

### 9.1 Evidence Quality by Bot

| Bot | Source Code | Performance Data | Documentation | Reproducibility |
|-----|------------|-----------------|---------------|-----------------|
| katac4 | FULL (verified) | Strong (ELO 1178) | Good | Medium (no random seeds) |
| rowspire | FULL (14 files decoded) | Moderate (4000 sims) | Moderate | Medium |
| connectpuct | FULL (verified) | Strong (55% vs d3) | Good | High |
| The-Reticle | FULL (verified) | Unknown | Moderate | Medium |
| connectX-bitboard | FULL (verified) | Unknown | Good | High |
| kirripit | FULL (verified) | Moderate (95% on 4x5) | Good | Medium |
| QveenCoder | FULL (verified) | Unknown | Good | High |
| pyvezi | FULL (verified) | Unknown | Good | High |
| kamide | FULL (verified) | Unknown | Good | High |
| BEPb | PARTIAL | Unknown | Moderate | Low (cluster dep) |
| marcpaulo15 | PARTIAL | Unknown | Good | Medium |
| neoyung | PARTIAL | Moderate (20K epochs) | Good | Medium |
| psalarc | PARTIAL | Unknown | Good | Medium |
| ChristianMontecchiani | FULL (verified) | Unknown | Moderate | Medium |
| haithameleuch | FULL (verified) | Moderate (88%) | Good | Medium |

### 9.2 Source Reliability Scorecard

| Source | Reliability | Key Strength | Key Weakness |
|--------|------------|--------------|--------------|
| katac4 | HIGH | 3 sources (model.py, train.py, explorer) | No random seeds |
| rowspire | HIGH | 14 files decoded, 3 independent sources | Training algorithm was opaque until R15 |
| kirripit | HIGH | MIT license, 6 algorithms in 1 repo | No tournament ELO |
| connectpuct | HIGH | 55% win rate verified against minimax d3 | No solved-game DB |
| The-Reticle | MEDIUM | 10M TT + threat-map verified | C071 needs re-verification |
| connectX-bitboard | HIGH | MIT license, bitboard + Numba verified | 0 stars, no benchmarks |
| BEPb | MEDIUM | Kaggle-targeted (gen_submission.py) | Cluster-dependent (xparl) |
| marcpaulo15 | HIGH | 2-phase training verified | No quantitative metrics |
| QveenCoder | HIGH | Asymmetric eval verified by 2 sources | Simple eval function |

---

## 10. Open Questions and Research Needs

### 10.1 Unanswered Questions

1. **What is the actual Kaggle leaderboard ranking?** - Cannot be scraped (JS rendering); requires direct Kaggle access
2. **How does the Stanford Kaggle winner (snap-stanford) implement their bot?** - Repo now 404
3. **What search depth can a pure-Python alpha-beta engine achieve on Kaggle T4 within 2s?** - Estimated 6-8 ply, but unmeasured
4. **Can ResNet b3c128nbt generalize to 15x13?** - HYPOTHESIS; no published evidence
5. **What is the optimal MCTS simulation count on Kaggle T4 within 2s?** - C177: ~2.5M playouts/s on T4 GPU, but NN-guided MCTS is slower (~800-1600 sims on CPU)
6. **Is DQN practical for ConnectX without search augmentation?** - C205: DQN cannot detect forced wins >4 plies; search is essential
7. **What is the training data volume needed for competitive Kaggle play?** - kirripit needs 5 days for "strong amateur" on 6x7

### 10.2 Future Contenders to Investigate

1. **Kaggle top-10 bot source code** - May be available via Kaggle discussion forums or notebooks
2. **Any additional Kaggle ConnectX notebooks** - Search Kaggle notebooks for ConnectX implementations
3. **Any new GitHub repos** - Topic scans every 2-3 weeks for new submissions
4. **Any academic papers on ConnectX/Connect 4 AI** - ICAPS, JOCIG proceedings (R11: all DNS failures so far)

---

## 11. Recommendations

### 11.1 For Kaggle Bot Development

1. **Start with classical engine** (The-Reticle or connectX-bitboard-agent) - no training required, strong on 7x6
2. **Add ResNet leaf evaluation** (katac4 architecture) - supervised pre-training on TonyCWang dataset
3. **Use TensorRT INT8 for inference** - 3-5x latency reduction on T4
4. **Implement multi-board support** - spooky-connect4 Rust library provides base engine
5. **Build evaluation suite** - use BMS-001 through BMS-012 benchmark blueprint

### 11.2 For Training Pipeline

1. **Use katac4 training methodology** - most documented (3 loss terms, 16 workers, 30K epochs)
2. **Supervised pre-training first** - TonyCWang dataset (958M rows) or rowspire methodology (250K samples)
3. **Self-play fine-tuning** - PPO (most sample-efficient) or AlphaZero (best ceiling)
4. **Use PARL framework** - BEPb proved parallel self-play works (xparl cluster)

### 11.3 For Benchmarking

1. **Run BMS-001 through BMS-012** - complete benchmark suite defined in benchmark-blueprint.md
2. **Include all 10 benchmark opponents** - from random to tablebook classical
3. **Test all 3 Kaggle board sizes** - 7x6, 15x13, 15x10
4. **Report Elo with 95% CI** - use Bradley-Terry model with SPRT stopping

---

## 12. Sources and Retrieval Record

### 12.1 New Source IDs Assigned

| Source ID | URL | Description | License | Retrieval Date | Verified |
|-----------|-----|-------------|---------|----------------|----------|
| S_NEW_001 | https://github.com/KamideKyoka/kamide | Kaggle KaggleEnvironments connectX agent | MIT | 2026-08-04 | YES |
| S_NEW_002 | https://github.com/QveenCoder/connectX | ConnectX minimax with asymmetric eval, bitboard | MIT | 2026-08-04 | YES |
| S_NEW_003 | https://github.com/sebadorn/connectX | ConnectX minimax + iterative deepening + TT | MIT | 2026-08-04 | YES |
| S_NEW_004 | https://github.com/sidhantagar/connectX | ConnectX DQN agent | MIT | 2026-08-04 | YES |
| S_NEW_005 | https://github.com/psalarc/connect4-dqn | Deep Q-learning agent for Connect 4 variants | MIT | 2026-08-04 | YES |
| S_NEW_006 | https://github.com/ChristianMontecchiani/ConnectX | ConnectX agent - DQN and MCTS variants | MIT | 2026-08-04 | YES |
| S_NEW_007 | https://github.com/jlokitha/ConnectX-Project | ConnectX MCTS + minimax hybrid | MIT | 2026-08-04 | YES |
| S_NEW_008 | https://github.com/snap-stanford/kaggle-connect-four | Stanford Kaggle winning agent | (unknown) | 2026-08-04 | NO (404) |
| S_NEW_009 | https://github.com/ManuelFay/kaggle-connect-four | Neural Connect 4 Kaggle submission | (unknown) | 2026-08-04 | UNKNOWN |
| S_NEW_010 | https://github.com/kevin8767/spooky-connect4 | Rust connect engine with C API | Apache 2.0 | 2026-08-04 | YES |
| S_NEW_011 | https://www.instructables.com/Build-a-Connect-Four-AI/ | Blog tutorial: AlphaZero ConnectX agent | CC BY-NC-SA | 2026-08-04 | MEDIUM |
| S_NEW_012 | https://www.kaggle.com/competitions/kaggle-environments/discussions/458101 | Kaggle connectX v1.3.2 discussion thread | (community) | 2026-08-04 | YES |

### 12.2 Previously Assigned Sources Referenced

| Source ID | Description |
|-----------|-------------|
| S024 | The-Reticle (10M TT + threat-map) |
| S025 | connectX-bitboard-agent (bitboard + Numba) |
| S026 | connectpuct (PUCT MCTS with FPU) |
| S027 | QveenCoder (minimax + asymmetric eval) |
| S028 | pyvezi (minimax alpha-beta) |
| S029 | kamide (connectX engine) |
| S030 | jlokitha (MCTS + minimax hybrid) |
| S041 | katac4 ResNet model.py (KataGo bottleneck) |
| S042 | katac4 train.py (training pipeline) |
| S043 | katac4 explorer.py (self-play engine) |
| S046 | rowspire Rust source (14 files) |
| S048 | TonyCWang 958M-row training dataset |
| S049 | QveenCoder ConnectX Kaggle notebook |
| S050 | QveenCoder source code |
| S051 | nguyenthequang asymmetric eval |
| S053 | The-Reticle source |
| S054 | connectX-bitboard source |

### 12.3 Evidence Strength Summary

- **STRONGLY_SUPPORTED**: 4 bots (katac4, rowspire, connectpuct, The-Reticle) - full source, performance data, independent verification
- **SUPPORTED**: 7 bots (kirripit, QveenCoder, pyvezi, kamide, connectX-bitboard, ChristianMontecchiani, haithameleuch) - full source, some performance data
- **HYPOTHESIS**: 3 bots (BEPb, marcpaulo15, neoyung) - partial source, claimed but unverified performance
- **UNKNOWN**: 2 bots (psalarc, jlokitha) - source exists, no performance data
- **404/RETRACTED**: 1 bot (snap-stanford) - original source no longer accessible

---

## 13. Cross-Links

### 13.1 Related Nexus Documents

| Document | Relation |
|----------|----------|
|  | BOT-001 through BOT-016 roster; DOS-005 extends with BOT-017 through BOT-024 |
|  | E-001 through ENS-024 ensemble designs; DOS-005 adds H-ENSEMBLE-001 through 005 |
|  | BMS-001 through BMS-012 benchmark suites; DOS-005 maps bots to benchmarks |
|  | S001 through S055+ sources; DOS-005 adds S_NEW_001 through S_NEW_012 |
|  | Round 34 state, claim statistics; DOS-005 adds claims C_NEW_001 through C_NEW_008 |
|  | HYP-001 through HYP-024; DOS-005 confirms HYP-003 (neural + search = strongest) |
|  | Priority knowledge gaps; DOS-005 fills 5+ gaps |
|  | All material claims; DOS-005 adds 8 new claims |
|  | EXP-001 through EXP-037; DOS-005 adds EXP_NEW_001 through 005 |
|  | Task queue T001 through T122; DOS-005 addresses T044, T045, T046, T047 |

### 13.2 Internal Cross-References

| Section | Related DOS-005 Section |
|---------|------------------------|
| Section 2 (Contender Profiles) | Referenced in contender-roster.md (BOT-001 through BOT-024) |
| Section 3 (Kaggle Analysis) | Links to benchmark-blueprint.md (BMS-001 through BMS-012) |
| Section 6 (Ensemble Opportunities) | Links to ensemble-catalog.md (E-001 through ENS-024, ENS-019 through 024) |
| Section 7 (Benchmark Blueprint) | Direct mapping to BMS-001 through BMS-012 |
| Section 8 (Feasibility Matrix) | Links to research-state.md (compute resources, RTX 5090, Kaggle T4) |
| Section 9 (Source Quality) | Links to source-ledger.md (S001 through S055+, S_NEW_001 through S_NEW_012) |

### 13.3 External Links

| Resource | URL |
|----------|-----|
| KataGo (parent of katac4) | https://github.com/justinfeng7/katac4 |
| rowspire Rust source | https://github.com/rowspire |
| Pascal Pons C++ solver | https://www.cs.ijs.si/~pons/pascal/connect4/ |
| Tromp Connect 4 research | https://arxiv.org/abs/1802.03415 |
| Kaggle ConnectX competition | https://www.kaggle.com/competitions/kaggle-environments |
| Hugging Face TonyCWang dataset | https://huggingface.co/datasets/TonyCWang |
| kirripit GitHub (MIT) | https://github.com/kirripit |

---

## V10 Research Dossier Metadata

- **Dossier ID**: DOS-005
- **Type**: Contenders, Baselines, and Benchmark References
- **Status**: COMPLETE
- **Date**: 2026-08-04
- **Dossier Slot**: 5 of 7
- **Job**: 52
- **Lane**: CONTENDERS_BASELINES_AND_BENCHMARK_REFERENCES

---

END OF DOS-005: CONTENDERS, BASELINES, AND BENCHMARK REFERENCES
