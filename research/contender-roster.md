# ConnectX Contender Roster

> **Current Round**: 47
> **Last Updated**: 2026-08-05 22:00 ET

## Roster Summary

| ID    | Name                              | Type                     | Board        | Language | Algorithm                        | GitHub  |
|-------|------------------------------------|--------------------------|--------------|----------|----------------------------------|---------|
| BOT-001 | Pascal Pons Connect 4 solver     | Oracle / Perfect-Play    | Multi        | C++      | Negamax + PVS + TT + book        | —       |
| BOT-002 | Tromp 8x8 solver (fhourstones88)  | Oracle / Perfect-Play    | 8x8          | C++      | Negamax + AB + TT + forks        | —       |
| BOT-003 | katac4 (GoodCoder666)            | Hybrid baseline          | 7x6, 8x8     | Python   | ResNet + PUCT MCTS + self-play    | 18*     |
| BOT-004 | rowspire (tre-systems)           | Hybrid baseline          | 7x6          | Rust     | Dual MLP + UCB1 MCTS + bitboard   | 0*      |
| BOT-005 | connectpuct (ahmeddoghri)        | MCTS baseline            | 7x6          | Python   | PUCT MCTS + tactical priors       | —       |
| BOT-006 | connect-four (QveenCoder)        | Lightweight classical    | 7x6          | Python   | Minimax + AB + asymmetric eval    | 13*     |
| BOT-007 | The-Reticle (ariaborin)          | Classical engine         | 7x6          | Python   | AB + 10M TT + threat-map          | —       |
| BOT-008 | Kaggle built-in random            | Random baseline          | 7x6          | Python   | Random legal move                 | —       |
| BOT-009 | TonyCWang ConnectFour dataset     | Dataset / value oracle   | 7x6          | N/A      | Pons solver self-play (temp)      | 958M rows |

**Total contenders: 10** - 2 oracle, 1 hybrid (Neural+MCTS, PyTorch), 1 hybrid (Neural MCTS, Rust+WASM), 2 MCTS baselines, 1 lightweight classical, 1 sophisticated classical, 1 random sanity baseline, 1 training dataset.

---

## Detailed Entries

### BOT-001: Pascal Pons / connect4 (Oracle / Perfect-Play Reference)

- **Canonical name:** Pascal Pons Connect 4 solver
- **URL:** github.com/PascalPons/connect4
- **Project type:** Oracle / perfect-play reference
- **Version:** latest release
- **License:** Unknown
- **Language and runtime:** C++
- **Board and inarow support:** 7x6 (6-in-a-row), 8x8 (4-in-a-row), 9x6 (6-in-a-row), 10x8 (4-in-a-row), 10x10 (4-in-a-row), 10x7 (5-in-a-row)
- **Algorithm and components:**
  - Negamax + PVS (Probabilistic Verification Search) + transposition table + opening book
  - Depth-14 search
  - Iterative binary search to determine game-theoretic outcome
  - Board sizes are constexpr -- not dynamically parameterized at runtime
- **Published result evidence:**
  - 9x6 solved (November 2005): ~2E13 positions evaluated, ~2000 CPU-hours
  - 7x6 solved (first solved Connect-4 board)
  - 8x8 solved: P2 win
- **Availability:** Source code public
- **Reproducibility:** High -- C++ source, fully deterministic
- **Resource requirements:** ~16GB RAM for 8x8 book (~500MB compressed)
- **Known defects:**
  - PVS verification disputed in R25; R26 confirmed no PVS in actual code
  - Board sizes are constexpr, not dynamic
- **Comparability limits:** Not Kaggle-compatible (C++ binary, not Python API)
- **Proposed future benchmark role:** Oracle moves for position verification; ground-truth draw reference
- **Configuration that must eventually be pinned:** exact source commit, compiled binary checksum
- **Source and claim IDs:** S033, C052, C128-C134

---

### BOT-002: John Tromp / fhourstones88 (Oracle / Perfect-Play Reference)

- **Canonical name:** Tromp 8x8 solver (fhourstones88)
- **URL:** github.com/tromp/fhourstones88
- **Project type:** Oracle / perfect-play reference
- **Version:** latest
- **License:** Unknown
- **Language and runtime:** C++
- **Board and inarow support:** 8x8 (4-in-a-row)
- **Algorithm and components:**
  - Negamax + alpha-beta pruning + transposition table (book88)
  - O(7) inline fork detection
  - Win/loss shortcuts for solved subgames
  - book88 opening book, 16 ply depth
- **Published result evidence:**
  - 8x8 solved as P2 win (late 2014 / early 2015)
  - book88 ~500MB compressed
- **Availability:** Source code public
- **Reproducibility:** High -- C++ source, deterministic
- **Resource requirements:** ~500MB compressed transposition table; significant memory footprint for classical solver
- **Known defects:**
  - 8x8 is not the Kaggle board (7x6)
  - Hard-coded constexpr board sizes
- **Comparability limits:** Not Kaggle-compatible; different board size
- **Proposed future benchmark role:** 8x8 oracle; fork detection reference algorithm
- **Configuration that must eventually be pinned:** exact source commit, book88 checksum
- **Source and claim IDs:** S034, C094

---

### BOT-003: GoodCoder666 / katac4 (Hybrid Baseline -- Neural + MCTS + Classical)

- **Canonical name:** katac4 -- KataGo-inspired AlphaZero for Connect 4
- **URL:** github.com/GoodCoder666/katac4
- **Project type:** Hybrid baseline
- **Version:** b3c128nbt (latest trained model)
- **License:** MIT
- **Language and runtime:** Python (PyTorch), deployed with TensorRT
- **Board and inarow support:** 7x6 (default), 8x8 (configurable)
- **Algorithm and components:**
  - PyTorch ResNet backbone: b3c128nbt variant (3 bottleneck blocks, 128 channels, ~530K parameters)
  - PUCT MCTS: 1600 simulations, FPU c_fpu=0.2, LCB move selection
  - 3-phase lambda scheduler for training exploration decay
  - Self-play training loop: 300K games, 30K epochs, 3 loss terms (policy + value + rival)
- **Published result evidence:**
  - Training ELO self-comparison: b3c128_v1 ~1080 to ~1178
  - 18* GitHub stars
  - TensorRT FP16 ResNet-18 on T4: ~1.10ms inference time
  - Model size ~530K parameters within Kaggle submission limits
- **Availability:** Source code public; model weights available
- **Reproducibility:** Medium -- training pipeline specified (3-phase lambda, 3 loss terms, 16 parallel workers) but exact random seeds undocumented
- **Resource requirements:**
  - Training: 4x RTX 4090, ~8 days
  - Inference: T4 GPU, ~2s/move
- **Known defects:**
  - C163 HYPOTHESIS: Training pipeline partially specified
  - NN generalization to 15x13 unverified
- **Comparability limits:** Kaggle-compatible (Python); model size ~530K params within submission limits
- **Proposed future benchmark role:** Primary neural+MCTS benchmark; reference for H-ENSEMBLE-002 (hybrid ensemble)
- **Configuration that must eventually be pinned:** random seed, lambda schedule, loss-weight ratios, worker count, training epoch count
- **Source and claim IDs:** S026, S091, S092, C146, C148

---

### BOT-004: tre-systems / rowspire (Hybrid Baseline -- Neural MCTS + Bitboard)

- **Canonical name:** rowspire -- Neural MCTS + bitboard solver in Rust+WASM
- **URL:** github.com/tre-systems/rowspire
- **Project type:** Hybrid baseline
- **Version:** latest release
- **License:** Unknown
- **Language and runtime:** Rust (neural network in neural_network.rs, MCTS in bitboard_solver.rs, WASM deployment in rowspire_ai_core)
- **Board and inarow support:** 7x6 (default)
- **Algorithm and components:**
  - Dual 4x128 MLP: value network + policy network (530K parameters)
  - UCB1 MCTS: c=1.41, 4000 simulations, NN-guided playouts
  - Dirichlet root noise: 0.8
  - 7-feature evaluation (genetic-tuned)
  - Bitboard representation for efficient move generation
  - WASM deployment target
  - rayon parallel gradient descent for training
- **Published result evidence:**
  - 0* GitHub stars; full source decoded (14 files)
  - Training pipeline: 50-epoch supervised curriculum distillation, 250K samples + mirroring
  - BitboardSolver depth 18
  - Genetic tuning weights available (evolved gen2)
- **Availability:** Source code public; WASM build available
- **Reproducibility:** Medium -- training details partially decoded; genetic tuning completeness unknown
- **Resource requirements:** WASM inference; Rust runtime ~10MB
- **Known defects:**
  - Training algorithm partially specified
  - Genetic tuning completeness unknown
- **Comparability limits:** WASM deployment demonstrates browser-based deployment; not directly Kaggle-compatible (Rust)
- **Proposed future benchmark role:** Neural MCTS baseline; reference for CMP-006 (NN policy prior)
- **Configuration that must eventually be pinned:** MCTS simulations count, Dirichlet concentration, UCB constant, genetic-tuning epoch count
- **Source and claim IDs:** S030, C043, C056

---

### BOT-005: ahmeddoghri / connectpuct (MCTS Baseline)

- **Canonical name:** connectpuct -- PUCT MCTS for Connect 4
- **URL:** github.com/ahmeddoghri/connectpuct
- **Project type:** MCTS baseline
- **Version:** latest
- **License:** Unknown
- **Language and runtime:** Python
- **Board and inarow support:** 7x6 (default)
- **Algorithm and components:**
  - PUCT MCTS with tactical priors
  - No solved-game database integration (verified in R26)
- **Published result evidence:**
  - PUCT MCTS: 11W / 9L in 20 matches vs minimax depth 3 (55% win rate)
- **Availability:** Source code public
- **Reproducibility:** High -- pure Python MCTS, deterministic
- **Resource requirements:** Pure Python, no GPU, no neural network
- **Known defects:**
  - C135 VERIFIED: Does not consult solved-game databases; consistency problem for drawn positions
- **Comparability limits:** Kaggle-compatible (Python); no NN dependency
- **Proposed future benchmark role:** Pure MCTS comparison for ENS-005 (ensemble ablation: MCTS-only)
- **Configuration that must eventually be pinned:** MCTS simulation count, prior tuning parameters, tactical heuristic weights
- **Source and claim IDs:** S029, C135, C137

---

### BOT-006: QveenCoder / connect-four (Lightweight Classical Baseline)

- **Canonical name:** QveenCoder connect-four
- **URL:** github.com/QveenCoder/connect-four
- **Project type:** Lightweight classical baseline
- **Version:** latest
- **License:** Unknown
- **Language and runtime:** Python
- **Board and inarow support:** 7x6 (default), configurable
- **Algorithm and components:**
  - Minimax + alpha-beta pruning
  - Asymmetric evaluation: win=100K, near-win=100, opponent near-win=-120
  - Center-first move ordering heuristic
- **Published result evidence:**
  - Source code confirms asymmetric eval (C005 VERIFIED)
  - 13* GitHub stars
- **Availability:** Source code public
- **Reproducibility:** High -- pure Python, deterministic
- **Resource requirements:** Minimal; no neural network, no GPU
- **Known defects:**
  - Simple evaluation function
  - No transposition table
  - No fork detection
- **Comparability limits:** Kaggle-compatible; simple baseline for comparison
- **Proposed future benchmark role:** Classical eval reference for CMP-010 (asymmetric evaluation comparison)
- **Configuration that must eventually be pinned:** search depth, evaluation weights (100K, 100, -120), move ordering
- **Source and claim IDs:** S050, C005

---

### BOT-007: ariaborin / The-Reticle (Classical Engine -- Sophisticated)

- **Canonical name:** ariaborin The-Reticle
- **URL:** github.com/ariaborin/The-Reticle
- **Project type:** Classical engine
- **Version:** latest
- **License:** Unknown
- **Language and runtime:** Python / JS
- **Board and inarow support:** 7x6 (default)
- **Algorithm and components:**
  - Alpha-beta pruning
  - 10M-entry transposition table with LRU eviction
  - History heuristic for move ordering
  - Threat-map tracking
  - Center-first move ordering
  - Most sophisticated classical engine found in survey
- **Published result evidence:**
  - 10M-entry transposition table with LRU eviction verified (pending re-verification)
- **Availability:** Source code public
- **Reproducibility:** Medium -- TT details verified, threat-map implementation partially decoded
- **Resource requirements:** ~10M-entry transposition table ~50MB memory
- **Known defects:**
  - C071 NEEDS_CORRECTION: TT source code needs re-verification
- **Comparability limits:** Kaggle-compatible if ported; TT size may exceed Kaggle submission limits
- **Proposed future benchmark role:** Classical engine reference for TT and threat-map integration
- **Configuration that must eventually be pinned:** TT size (10M), LRU parameters, threat-map scope, history heuristic weights, search depth
- **Source and claim IDs:** S045, C071

---

### BOT-008: ConnectX Built-in Random (Random Baseline)

- **Canonical name:** Kaggle ConnectX random opponent
- **URL:** kaggle-environments (built-in random player)
- **Project type:** Random baseline
- **Version:** kaggle-environments v1.32.3
- **License:** Kaggle proprietary
- **Language and runtime:** Python
- **Board and inarow support:** 7x6 (default), configurable
- **Algorithm and components:**
  - Random legal move selection
- **Published result evidence:**
  - Built into kaggle-environments package
  - test_connectx.py v1.32.2 (279 lines) confirms API
- **Availability:** Built into Kaggle environment
- **Reproducibility:** High -- seeded random is deterministic
- **Resource requirements:** None
- **Known defects:** Random play -- trivially defeated by any non-trivial strategy
- **Comparability limits:** Sanity check only; all competitive bots should beat random with >95% win rate
- **Proposed future benchmark role:** Sanity check; invalid-move rate baseline
- **Configuration that must eventually be pinned:** random seed, board dimensions
- **Source and claim IDs:** S005, S006

---

### BOT-009: TonyCWang / ConnectFour Dataset (Dataset / Value Oracle)

- **Canonical name:** TonyCWang ConnectFour training dataset
- **URL:** huggingface.co/TonyCWang/ConnectFour
- **Project type:** Dataset / value oracle
- **Version:** latest (958M rows)
- **License:** Unknown
- **Language and runtime:** N/A (dataset, not executable)
- **Board and inarow support:** 7x6 (default)
- **Algorithm and components:**
  - Pascal Pons solver self-play with temperature scheduling
  - First 10 moves: temperature T=1.0 (exploratory sampling)
  - Remaining moves: temperature T=0.5 (greedy-leaning)
- **Published result evidence:**
  - 958M rows total
  - 2x6x7 binary matrices (board states) + 7-element target vectors (value/proxy labels)
  - Temperature schedule confirmed from dataset metadata
- **Availability:** HuggingFace public
- **Reproducibility:** Medium -- temperature schedule confirmed but exact agent config undocumented
- **Resource requirements:** Dataset download ~tens of GB
- **Known defects:**
  - C110 REFUTED: S044 contradicts earlier claim that dataset was NOT self-play (it IS self-play from Pons solver)
- **Comparability limits:** Dataset, not a bot; used for supervised pre-training of policy networks
- **Proposed future benchmark role:** Training data source for NN policy prior (CMP-006)
- **Configuration that must eventually be pinned:** temperature schedule, solver version used for generation, data split proportions
- **Source and claim IDs:** S044, C064

---

### BOT-010: jlokitha / connect-4-game (MCTS Student Project)

- **Canonical name:** jlokitha connect-4-game
- **URL:** github.com/jlokitha/connect-4-game
- **Project type:** MCTS student project / baseline
- **Version:** latest
- **License:** Unknown
- **Language and runtime:** Java / JavaFX / Maven
- **Board and inarow support:** Unknown (JavaFX application, board size not specified in README)
- **Algorithm and components:**
  - MCTS-powered AI opponent
  - JavaFX GUI for interactive play
  - Maven build system (pom.xml)
- **Published result evidence:**
  - 15* GitHub stars
  - README confirms MCTS algorithm in source code
  - No performance benchmarks published
- **Availability:** Source code public
- **Reproducibility:** Unknown — Java project requires source analysis to determine parameters
- **Resource requirements:** Java runtime, Maven build
- **Known defects:**
  - Unknown quality — likely a university/course project
  - No benchmarks or documented parameters
  - Board size not specified in README
- **Comparability limits:** Java-based; not directly Kaggle-compatible (Python-only)
- **Proposed future benchmark role:** MCTS baseline for comparative analysis against connectpuct and rowspire
- **Configuration that must eventually be pinned:** MCTS parameters (c_puct, simulation count, roll-out policy), board size, training data (if any)
- **Source and claim IDs:** S118 (from R30 worker-02)

---

### BOT-013: Kamide/connect-n (Adaptive Scoring Minimax)

- **Canonical name:** Kamide/connect-n
- **Exact URL:** https://github.com/Kamide/connect-n
- **Project type:** Classical engine
- **Version, commit, tag, or release:** Source as of R32
- **License:** GitHub repo license (verify)
- **Language and runtime:** TypeScript / JavaScript (Web Worker)
- **Board and inarow support:** Configurable N×N boards; any N-in-a-row
- **Algorithm and components:** Adaptive scoring minimax with alpha-beta; connection-length scoring + hole-count evaluation; configurable board sizes; Web Worker non-blocking inference
- **Published result evidence:** None — discovered in R32 as new contender
- **Availability:** Source code public
- **Reproducibility:** TypeScript; runs in browser and Node.js; Web Worker deployment model documented
- **Resource requirements:** Minimal — no GPU required; Web Worker compatible
- **Known defects:**
  - No published benchmarks or ELO ratings
  - Adaptive scoring parameters not publicly documented
  - Web Worker may be incompatible with Kaggle notebook sandbox
- **Comparability limits:** TypeScript; not natively Python; Web Worker deployment model
- **Proposed future benchmark role:** Tier 2–3 classical baseline; Web Worker deployment template for Kaggle
- **Configuration that must eventually be pinned:** connection-length scoring parameters, hole-count weights, board size configuration, Web Worker timeout settings
- **Source and claim IDs:** S123 (R32 worker-02), C184-C186 (R32)

---

### BOT-014: miksipiksic/pyvezi (Bitboard Minimax)

- **Canonical name:** miksipiksic/pyvezi
- **Exact URL:** https://github.com/miksipiksic/pyvezi
- **Project type:** Academic minimax baseline
- **Version, commit, tag, or release:** Source as of R32
- **License:** GitHub repo license (verify)
- **Language and runtime:** Python (minimax + alpha-beta)
- **Board and inarow support:** 6×7 (Connect 4 standard); bitmask board representation
- **Algorithm and components:** Bitmask board representation; open-line diff heuristic; depth-4 minimax with alpha-beta pruning
- **Published result evidence:** None — discovered in R32 as new contender
- **Availability:** Source code public
- **Reproducibility:** Pure Python; no external dependencies beyond standard library
- **Resource requirements:** Minimal — CPU only; no GPU required
- **Known defects:**
  - No published benchmarks or ELO ratings
  - Depth-4 minimax is shallow; limited tactical depth
  - Open-line diff heuristic may not generalize well
- **Comparability limits:** Limited to 6×7 board size; shallow search
- **Proposed future benchmark role:** Tier 3 lightweight classical baseline; bitmask representation reference
- **Configuration that must eventually be pinned:** bitmask layout, depth parameter, open-line diff thresholds
- **Source and claim IDs:** S125 (R32), C192 (R32)

---

### BOT-015: Tromp fhourstones88 (8x8 Solved-Game Oracle)

- **Canonical name:** Tromp fhourstones88
- **Exact URL:** https://github.com/joschacht/fhourstones88 (referenced via R32)
- **Project type:** Oracle / perfect-play reference for 8x8
- **Version, commit, tag, or release:** Source as of R32
- **License:** GitHub repo license (verify)
- **Language and runtime:** C++ (standard alpha-beta, NO MTD(f), NO PVS per R32 analysis)
- **Board and inarow support:** 8×8 (inarow=4); 8x8 Connect 4 solved as P2 win
- **Algorithm and components:** Standard full-window alpha-beta; iterative deepening; TT; book-based opening (book88 ~500MB)
- **Published result evidence:** 8x8 Connect 4 solved as P2 win (Tromp, late 2014/2015); book88 ~500MB; column 4 universal P2 reply
- **Availability:** Source code public
- **Reproducibility:** C++; requires compilation; ~500MB book database
- **Resource requirements:** Moderate — C++ compilation; book storage
- **Known defects:**
  - No Kaggle submission target (8x8 not default Kaggle board)
  - Standard alpha-beta only; no MTD(f), no PVS (R32 verification)
  - Book-based opening: not generalizable to arbitrary board sizes
- **Comparability limits:** 8x8 only; not Kaggle ConnectX default (7x6)
- **Proposed future benchmark role:** Oracle/reference for 8x8 solving; 8x8 board-size test suite
- **Configuration that must eventually be pinned:** book88 content (opening positions), alpha-beta depth limits, TT size
- **Source and claim IDs:** S126 (R32), C187-C190 (R32)

---

### BOT-016: DQN ConnectX Baseline

- **Canonical name:** DQN ConnectX Bot (generic reference)
- **Exact URL:** N/A — generic DQN architecture reference
- **Project type:** Neural baseline
- **Version, commit, tag, or release:** N/A
- **License:** N/A
- **Language and runtime:** Python (PyTorch/TF); reinforcement learning
- **Board and inarow support:** Variable (depends on implementation); typically 7x6
- **Algorithm and components:** DQN policy network; value network; experience replay; target network; epsilon-greedy exploration
- **Published result evidence:** C205 (DQN cannot reliably detect forced-win sequences > 4 plies without search augmentation); C144-C145 (DQN training: 3-phase lambda scheduler, 30K epochs)
- **Availability:** DQN architecture well-known; specific ConnectX implementation varies
- **Reproducibility:** Python + PyTorch/TF; requires training data or self-play
- **Resource requirements:** High — training requires GPU and significant compute; inference lightweight
- **Known defects:**
  - C205: DQN tactical weakness; cannot detect forced wins > 4 plies without search augmentation
  - Training data quality critical; self-play data may suffer from solver-distillation problem
  - No published Kaggle ConnectX DQN bot with documented ELO
- **Comparability limits:** Performance highly dependent on training data quality and architecture choices
- **Proposed future benchmark role:** Neural baseline for comparison vs classical and hybrid approaches
- **Configuration that must eventually be pinned:** network architecture, training method, board representation, epsilon schedule
- **Source and claim IDs:** C205 (R34), C144-C145 (R30)

---

## Candidate Classification

### Candidates to Benchmark Against (top-strength tier)

| Candidate          | Strength Rationale                              | Tier       |
|--------------------|--------------------------------------------------|------------|
| BOT-001            | Solved game (7x6); perfect-play reference        | Oracle     |
| BOT-003            | Neural+MCTS hybrid; trained via self-play; ELO 1178 | Hybrid  |
| BOT-004            | Neural MCTS with bitboard; WASM-deployable       | Hybrid     |
| BOT-007            | Most sophisticated classical engine (10M TT, threat-map) | Classical |

No contender enters a top-strength tier based solely on popularity or source-code sophistication. All above candidates have published evidence of non-trivial strength (solved game, trained ELO, or sophisticated classical architecture).

### Candidates as Components to Reuse

| Component          | Reuse Target                                    | Rationale                          |
|--------------------|--------------------------------------------------|-------------------------------------|
| BOT-005            | ENS-005 (MCTS-only ablation)                    | Pure PUCT MCTS baseline             |
| BOT-006            | CMP-010 (asymmetric eval comparison)            | Simple asymmetric evaluation       |
| BOT-008            | Sanity check; invalid-move baseline             | Trivial random opponent             |
| BOT-009            | CMP-006 (NN policy prior pre-training)          | Solver-generated self-play dataset |

---

## Future Contenders to Add

### FC-001: H-ENSEMBLE-001 (Pure Classical Ensemble)

- **Status:** Pending implementation
- **Description:** Ensemble of classical engines (minimax + MCTS + Thompson sampling) without neural components
- **Purpose:** Establish pure classical ensemble baseline; compare against BOT-003 hybrid
- **Source components:** BOT-006 (minimax eval), BOT-005 (MCTS), BOT-007 (TT/threat-map)
- **Configuration to pin:** ensemble size, voting strategy, individual engine depths, Thompson sampling priors
- **Planned in round:** TBD

### FC-002: H-ENSEMBLE-004 (Warm-Start MCTS)

- **Status:** Pending implementation
- **Description:** MCTS seeded with policy network priors from BOT-009 dataset (warm-start before search)
- **Purpose:** Test whether dataset priors improve MCTS convergence speed vs BOT-005 cold-start MCTS
- **Source components:** BOT-005 (MCTS engine), BOT-009 (policy prior data)
- **Configuration to pin:** number of warm-start moves, prior smoothing parameter, MCTS simulation budget post-warm-start
- **Planned in round:** TBD

### FC-003: H-ENSEMBLE-003 (Draw Detection)

- **Status:** Pending implementation
- **Description:** Classical engine augmented with solved-position database lookup (draw detection) before search
- **Purpose:** Compare draw-aware vs draw-unaware engines; measure accuracy gain from database lookup
- **Source components:** BOT-001 (solved-game reference for database construction), BOT-007 (TT infrastructure for lookup)
- **Configuration to pin:** database coverage (which board sizes/positions), fallback strategy when position not in database, TT update policy
- **Planned in round:** TBD

### BOT-NEW-001: ManuelFay/Alpha_Connect4 (DQN Architecture Study)

- **URL:** github.com/ManuelFay/Alpha_Connect4
- **Stars:** 0
- **License:** Not specified
- **Language:** Python (PyTorch)
- **Board support:** 7x6 (configurable)
- **Algorithm:** DQN family (DQN, Double DQN, Dueling DQN, Policy Gradient, A3C)
- **Evaluation:** CNN with 3-channel board encoding; predicts win probability per column
- **Strength:** HYPOTHESIS — no published benchmarks
- **Kaggle compatible:** YES (Python + PyTorch, Jupyter notebook)
- **Source IDs:** S166
- **Dossier:** CON-001
- **Key finding:** Lighter architectures converge faster with comparable accuracy
- **Purpose in nexus:** Neural architecture comparison reference for NN-001 ensemble

### BOT-NEW-002: jesper-olsen/connect-four (Rust Fhourstones Port)

- **URL:** github.com/jesper-olsen/connect-four
- **Stars:** 0
- **License:** Unknown
- **Language:** Rust
- **Board support:** 7x6
- **Algorithm:** Alpha-beta negamax with Fhourstones heuristics, bitboard representation
- **Evaluation:** Bitboard-based win detection (O(1)), TT, interactive CLI testing
- **Strength:** HYPOTHESIS — no published benchmarks
- **Kaggle compatible:** NO (Rust)
- **Source IDs:** S167
- **Dossier:** CON-001
- **Key insight:** Fhourstones methodology replicated in modern memory-safe language
- **Purpose in nexus:** Inspiration for Numba-JIT Python bitboard implementation

### BOT-NEW-003: Hemakumargokul/ai-game-agents (Java Minimax Collection)

- **URL:** github.com/Hemakumargokul/ai-game-agents
- **Stars:** 0
- **License:** Unknown
- **Language:** Java
- **Board support:** 7x6
- **Algorithm:** Minimax with alpha-beta pruning
- **Evaluation:** Basic — count connected pieces, fork opportunities
- **Strength:** HYPOTHESIS — educational project quality
- **Kaggle compatible:** NO (Java)
- **Source IDs:** S168
- **Dossier:** CON-001
- **Purpose in nexus:** Educational reference for classic AI patterns

### BOT-NEW-004: Woonderpipe/connect-4 (Next.js/TS Production Game)

- **URL:** github.com/Woonderpipe/connect-4
- **Stars:** 1
- **License:** Apache 2.0
- **Language:** TypeScript/JavaScript (Next.js 16, React 19, Capacitor)
- **Board support:** Configurable (web and mobile)
- **Algorithm:** Minimax with alpha-beta, POSITIONAL_BONUS matrix
- **Evaluation:** Positional bonus matrix, center-first ordering, difficulty-based depth
- **Strength:** HYPOTHESIS — game AI, not research
- **Kaggle compatible:** NO (TypeScript/Next.js)
- **Source IDs:** S169
- **Dossier:** CON-001
- **Key insight:** 8 difficulty modes provide calibration scale for benchmarking
- **Purpose in nexus:** ENS-020 (difficulty scaling) reference

### BOT-NEW-005: Karthick-dev-cart/connectfour (Flutter Minimax)

- **URL:** github.com/Karthick-dev-cart/connectfour
- **Stars:** 0
- **License:** Unknown
- **Language:** Flutter (Dart)
- **Board support:** 7x6, configurable up to 20x20
- **Algorithm:** Minimax with alpha-beta
- **Evaluation:** Tactical position testing (winning drops, blocking threats)
- **Strength:** HYPOTHESIS — mobile game project
- **Kaggle compatible:** NO (Flutter/Dart)
- **Source IDs:** S170
- **Dossier:** CON-001
- **Key insight:** Configurable inarow (3-10), rare among Connect 4 bots
- **Purpose in nexus:** ENS-019 (inarow generalization) reference

### BOT-NEW-006: sidhantagar/ConnectX (Kaggle + Pygame)

- **URL:** github.com/sidhantagar/ConnectX
- **Stars:** 10
- **License:** MIT
- **Language:** Python
- **Board support:** 7x6 (default), configurable up to 20x20, inarow 3-10
- **Algorithm:** Minimax with alpha-beta + dynamic programming (memoization)
- **Evaluation:** DP-based position caching, configurable board sizes
- **Strength:** HYPOTHESIS — Kaggle notebook aims for "high score"
- **Kaggle compatible:** YES (Python, stdlib + pygame optional)
- **Source IDs:** S171
- **Dossier:** CON-001
- **Key insight:** Most Kaggle-compatible new contender discovered
- **Purpose in nexus:** CMP-007 (DP optimization) reference, primary new benchmark target

---

## Source and Claim ID Index

| ID   | Description                              | ID   | Description                              |
|------|------------------------------------------|------|------------------------------------------|
| S005 | Kaggle environments package              | S034 | Tromp 8x8 solver                         |
| S006 | Kaggle ConnectX API                      | S044 | TonyCWang dataset (self-play)             |
| S026 | katac4 hybrid training pipeline          | S045 | The-Reticle classical engine              |
| S029 | connectpuct MCTS results                 | S050 | QveenCoder connect-four                   |
| S030 | rowspire source decoded                  | S091 | katac4 PyTorch/TT support                 |
| S033 | Pascal Pons Connect 4 solver             | S092 | katac4 TensorRT inference                 |
| C005 | Asymmetric eval verified (BOT-006)      | C043 | rowspire source availability              |
| C052 | Pons Connect 4 oracle                    | C056 | rowspire Neural MCTS baseline             |
| C064 | TonyCWang dataset (CMP-006 source)      | C071 | The-Reticle TT needs re-verification     |
| C094 | Tromp 8x8 solver oracle                  | C110 | REFUTED: dataset is self-play             |
| C128 | Pons solver board sizes                  | C135 | VERIFIED: connectpuct no solved-db       |
| C134 | Pons PVS verification dispute            | C137 | connectpuct MCTS vs minimax results      |
| C146 | katac4 model architecture               | C148 | katac4 training ELO                       |