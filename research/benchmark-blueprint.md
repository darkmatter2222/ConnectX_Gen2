# Benchmark Blueprint - ConnectX Bot

> **Last Updated**: 2026-08-04 (Round 33)
> **Created**: 2026-08-03 (Round 26)
> **Status**: BMS-001 through BMS-012 fully designed; R33 added BMS-007 through BMS-012 specifications
> **Last Updated**: 2026-08-04 (Round 33)
> **Purpose**: Rigorous benchmark methodology and tournament design for ConnectX bot evaluation
> **Status**: DRAFT - design only, no execution required
> **Suite count**: 12 benchmark suites (BMS-001 through BMS-012), all designed

---

## Executive Summary

This document defines the benchmark science framework for evaluating ConnectX bots. It covers:

1. **Benchmark opponents**: A ladder of reference opponents from trivial to expert
2. **Evaluation tiers**: Progressive testing from tactical correctness to strategic strength
3. **Position suites**: Curated test positions for tactical verification
4. **Statistical methodology**: Elo estimation, confidence intervals, stopping rules
5. **Ablation design**: Isolating component contributions
6. **Board-size generalization**: Multi-board evaluation protocol
7. **Kaggle emulation**: Testing under Kaggle competition constraints

---

## 1. Benchmark Opponent Ladder

### Tier 1: Trivial Baselines

| ID | Name | Description | Purpose |
|----|------|-------------|---------|
| B-01 | Random | Uniform random valid move | Sanity check: bot must not lose |
| B-02 | Win-Seek-Block | Always attempt win, then block opponent win, then random | Tests basic tactical awareness |
| B-03 | Depth-1 Minimax | Minimax depth 1 with no eval function | Tests forced-move recognition |

### Tier 2: Classical Weak

| ID | Name | Description | Purpose |
|----|------|-------------|---------|
| B-04 | Depth-2 Minimax | Minimax depth 2, no eval function | Tests multi-move lookahead without position evaluation |
| B-05 | Depth-3 Minimax | Minimax depth 3, window-scoring eval | Tests shallow search with basic eval (per connectpuct benchmark) |
| B-06 | Depth-3 Minimax + Random | Mix of depth-3 and random moves | Tests robustness against unpredictable opponents |

### Tier 3: Classical Strong

| ID | Name | Description | Purpose |
|----|------|-------------|---------|
| B-07 | Full Classical | Alpha-beta + PVS + TT (10M entries) + history heuristic + killer moves + center-first ordering + full move ordering | Reference point: best possible classical play per Chess Programming Wiki hierarchy (C079-C097) |
| B-08 | Perfect 7x6 | Tablebook from solved game (Bock W-D-L) for first ~20 moves, then full classical | Tests bot midgame/endgame play independent of opening book |
| B-09 | Tromp-style Solver | Tromp-style negamax with book88 methodology on 7x6 | Tests against highly optimized classical engine (per tromp/fhourstones88) |

### Tier 4: Neural/MCTS

| ID | Name | Description | Purpose |
|----|------|-------------|---------|
| B-10 | MCTS Random Playouts | MCTS with random playouts, no NN guidance | Tests pure MCTS without neural guidance (baseline for neural guidance benefit) |
| B-11 | PUCT MCTS | PUCT MCTS with c_puct=1.4, 80 simulations (per connectpuct) | Tests MCTS strength against classical (connectpuct achieves 50-66% vs minimax d3) |
| B-12 | MCTS + Policy Prior | MCTS guided by policy network prior, no value network | Tests policy-only guidance for move ordering |
| B-13 | NN Value Leaf Eval | Alpha-beta with NN value network at leaf nodes | Tests value-network guidance in classical search |
| B-14 | Full NN-MCTS | AlphaZero-style MCTS with policy+value NN (per katac4: 1600 sims, FPU c_fpu=0.2, LCB) | Tests highest-ceiling approach (per katac4 architecture) |

### Tier 5: Expert

| ID | Name | Description | Purpose |
|----|------|-------------|---------|
| B-15 | Tablebook Classical | Opening tablebook (depth ~20) + full classical search + full eval function | Tests against near-perfect classical play |
| B-16 | Tablebook + NN Leaf | Tablebook opening + alpha-beta + NN leaf evaluation | Tests best hybrid classical+NN |

---

## 2. Evaluation Tiers

### Tier A: Tactical Correctness

**Purpose**: Verify bot plays all forced wins and blocks all forced losses.

**Method**: Position suite of 1,000+ tactical positions where optimal play is known.

**Source**: Generated from Pascal Pons solver (S042) and TonyCWang dataset (S044) - positions where solver identifies forced win in <=10 moves.

**Pass Criteria**: Bot achieves >=99% tactical correctness on position suite.

**Position Categories**:
- P1 forced win in 1 move (immediate win)
- P1 forced win in 2 moves (win-in-1 after opponent response)
- P1 forced win in 3-5 moves
- P1 forced win in 6-10 moves
- P1 must block opponent forced win in 1 move
- P1 must block opponent forced win in 2+ moves
- Fork positions (two simultaneous threats)
- Anti-fork positions (one threat blocks two threats)

### Tier B: Opening Play

**Purpose**: Verify bot plays optimally from all possible opening moves.

**Method**: 100 games from each of the 7 first moves. Center column should win in <=41 moves (C001). Adjacent columns should draw. Edge columns should be P2 advantage.

**Pass Criteria**:
- From center: >=95% win rate vs tablebook opponent
- From adjacent: >=90% draw rate vs tablebook opponent
- From edge: >=85% of games should recognize disadvantage

### Tier C: Midgame Strength

**Purpose**: Measure playing strength in positions not covered by opening book.

**Method**: Paired games against benchmark opponents (B-07 through B-15). Each pair: 100 games with color reversal.

**Scoring**: Compute pairwise win/draw/loss rates. Use paired t-test for statistical significance.

### Tier D: Endgame Strength

**Purpose**: Measure playing strength in late-game positions (30+ pieces on board).

**Method**: 500 positions with 30+ pieces, generated by solvers. Evaluate bot move vs solver move.

**Scoring**: Agreement rate vs solver evaluation.

### Tier E: Board-Size Generalization

**Purpose**: Measure how well a bot designed for 7x6 performs on other board sizes.

**Method**: Test against board-size-specific benchmarks:
- 6x5, inarow=3 (standard Kaggle variant): 100 games
- 8x8: 100 games vs classical engine
- 10x8: 100 games vs classical engine
- 12x10: 50 games vs classical engine (limited due to computational cost)

**Scoring**: Win/draw/loss rate vs board-size-specific classical engine.

### Tier F: Resource-Constrained Performance

**Purpose**: Measure performance under Kaggle constraints (2s/move timeout, 60s overtime).

**Method**: Run all evaluations with strict per-move timeout of 2.0 seconds. Track:
- Average depth achieved per move
- Average nodes evaluated per move
- Number of moves exceeding timeout
- Overtime consumption per game

**Scoring**: Win rate under time constraints vs unconstrained baseline.

---

## 3. Position Suites

### Suite A: Forced Win Catalog

**Source**: Generated from solved-game databases (Bock W-D-L, Tromp book88).

**Size**: 5,000 positions minimum.

**Coverage**:
- All 7 first moves x 7 second moves x 5% of remaining positions
- Positions with forced win <=10 moves
- Positions with forced win 11-20 moves

**Format**: JSON array of {board, player, forced_win_moves, solver_move}.

### Suite B: Draw Position Catalog

**Source**: Tromp 8x8 solved positions (book88, S094).

**Size**: 1,000 positions minimum.

**Coverage**: Known draw positions on 8x8 and larger boards.

### Suite C: Fork Positions

**Source**: Chess Programming Wiki fork patterns (C096).

**Size**: 500 positions.

**Coverage**: All 6 canonical fork patterns on 7x6 (H+H, H+V, H+D, V+D, D+D, V+V) plus anti-fork positions.

### Suite D: Edge Cases

**Source**: Generated edge cases.

**Size**: 500 positions.

**Coverage**:
- All pieces in one column (edge case)
- Nearly full board with unresolved win/loss
- Positions where both players have 3-in-a-row (fork race)

---

## 4. Statistical Methodology

### 4.1 Elo Estimation

**Model**: Bradley-Terry model adapted for draws (Ladva model).

**Formula**: Expected score E[A beats B] = 1 / (1 + 10^(-Delta_Elo / 400))

**Draws**: Adjusted via draw-rate parameter. For Connect 4, expected draw rate depends on board size:
- 7x6: near-zero (solved game, first-player win)
- 8x8: moderate (solved as P2 win, draws possible from suboptimal openings)
- 15x13: unknown (HYPOTHESIS C132)

**Confidence Intervals**: 95% CI computed via bootstrapping (10,000 resamples).

**Stopping Rule**: Stop pairwise comparisons when 95% CI width < 50 Elo or when N >= 200 games per pair, whichever comes first.

### 4.2 SPRT (Sequential Probability Ratio Test)

**Use case**: When comparing two bots and deciding statistically whether one is stronger.

**H0**: Delta_Elo <= delta_small (e.g., 25 Elo)
**H1**: Delta_Elo >= delta_large (e.g., 50 Elo)
**alpha**: Type I error (0.05)
**beta**: Type II error (0.10)

**SPRT stops when**:
- Likelihood ratio exceeds H1 threshold (bot A is stronger)
- Likelihood ratio drops below H0 threshold (no meaningful difference)
- N reaches maximum (200 games per pair)

### 4.3 Sample Size Calculations

For pairwise comparisons with expected draw rate D:
- N = 4 * (Z_alpha + Z_beta)^2 / (p - D)^2 where p is the win probability after removing draws

**Rule of thumb**: 100-200 games per pair for 95% CI within 100 Elo.

### 4.4 Pairwise Comparison Matrix

For N opponents, full pairwise comparison requires N*(N-1)/2 pairs.

With 16 benchmark opponents (B-01 through B-16): 120 unique pairs.

Each pair: 100 games with color reversal (50 games each color).

Total: 12,000 games for full matrix.

For reduced matrix (only compare Tier N opponents within same tier): 40 pairs x 100 = 4,000 games.

---

## 5. Ablation Design

### 5.1 Component Ablation

Ablation study: remove one component at a time from the full Hybrid NN + Search architecture and measure degradation.

**Ablation Matrix**:

| Variant | Description | Expected Delta |
|---------|-------------|----------------|
| Full | Complete hybrid architecture | Baseline |
| -OpeningBook | No opening book (search from root) | -50 to -200 Elo on 7x6 |
| -NN | NN removed, manual eval function used | -100 to -300 Elo on 7x6; larger gap on 15x13 |
| -TT | Transposition table removed | -100 to -300 Elo (TT gives ~18x speedup) |
| -Heuristics | No move ordering heuristics | -200 to -500 Elo (depth drops significantly) |
| -PVS | Principal variation search removed (standard alpha-beta) | -50 to -150 Elo |
| -NNLeaf | NN leaf evaluation removed (return eval function) | -50 to -200 Elo on midgame positions |

### 5.2 Training Ablation

For NN components:

| Variant | Training Data | Expected Performance |
|---------|---------------|---------------------|
| Full | 958M rows from Pascal Pons solver (S044) | Best policy accuracy (~85-90%) |
| -Temperature | No temperature schedule (T=0.5 always) | Lower data diversity, ~5% lower accuracy |
| -Mirroring | No board mirroring in training | ~10% lower accuracy (less data efficiency) |
| 7x6-only | 7x6 data only | Perfect on 7x6, poor on 15x13 (board-size lock-in) |
| Multi-board | Data from 7x6, 8x8, 10x8 combined | Moderate on all boards, better generalization |

### 5.3 Search Ablation

| Variant | Search Method | Expected Performance |
|---------|---------------|---------------------|
| Full | Alpha-beta + PVS + TT + full ordering | Best classical baseline |
| Pure alpha-beta | No PVS, no TT | 5-10x slower, same strength if time constant |
| Iterative deepening | Depth-limited iterative deepening | Better time management, same strength |
| MCTS only | Pure MCTS, no alpha-beta | Lower strength on 7x6 (per connectpuct: 50-66% vs minimax d3) |

---

## 6. Kaggle Emulation Protocol

### 6.1 Environment Matching

Replicate Kaggle competition environment as closely as possible:

- **Board representation**: Flat 1D array (C105)
- **Timeout**: 2.0s per move, 60s overtime bank
- **Board size**: 7x6 default (C104: only board with test evidence)
- **Agent signature**: 1-arg or 2-arg function (C113)
- **MaxLogLength**: 10,000 chars per agent per step (C112)
- **Overtime enforcement**: Per-step consumption via max(0, duration - actTimeout) (C106)

### 6.2 Kaggle-Specific Benchmarks

- **Timeout stress**: Run 500 games with strict 2s timeout; measure depth achieved, overtime used
- **Multi-board test**: Run 100 games each on 4x5/inarow=3, 7x6, 8x8
- **Overtime test**: Start games with remainingOverageTime=0 (no overtime budget); measure survival

---

## 7. Future Experiment Cards

FE-001: Run MCTS convergence benchmark: connectpuct/rowspire/katac4 vs minimax depth 5+ with increasing simulation budgets (10, 50, 100, 500, 1000, 4000) - measure win rate improvement and whether MCTS ever identifies draw positions (see work queue FU-025)

FE-002: Benchmark asymmetric eval (opp-threat 1.2x AI-threat) vs symmetric eval (1:1) on 1000 positions from TonyCWang dataset (see work queue FU-025)

FE-003: Train katac4 ResNet on TonyCWang data - verify ~85-90% policy accuracy (see work queue FU-029)

FE-004: Benchmark ConnectX model on Kaggle T4 - measure actual inference latency for ResNet (katac4 ~530K params) (see work queue FU-030)

FE-005: Implement MCTS on Kaggle T4 with NN guidance - estimate 1600 sims in 2s (see work queue FU-031)

FE-006: Transfer learning 7x6 to 15x13 empirically - train ResNet, measure performance gap (see work queue FU-032)

FE-007: Port katac4 3-loss function to Kaggle - test policy CE + value CE + rival CE (see work queue FU-033)

FE-008: AZAL auxiliary loss - verify arXiv 2607.08984 identity, implement auxiliary loss, measure oracle match rate (see work queue FU-034)

FE-009: Board-size matrix source re-verification - find authoritative source for 8x8/9x6/10x8 solved-game results (see work queue FU-037)

FE-010: C071 re-verification against ariaborin source (TT disabled) (see work queue FU-039)

---

## 8. Claim-Status Impact

This benchmark blueprint establishes the following:

- **B-01 through B-16** are proposed benchmark opponent IDs (not yet verified against specific implementations)
- **Tier A correctness criteria** (>=99% forced win) are derived from theoretical guarantees (C001, C005)
- **Board-size matrix** uses verified data from C128-C131 and HYPOTHESIS C132
- **Kaggle emulation constraints** are derived from C104-C113 (verified Kaggle spec)
- **Statistical methodology** follows standard tournament design (Bradley-Terry, SPRT)

No new claims are made about specific bot strength levels - all future experiments are proposed, not executed.

---

## 9. Tournament Design

### 9.1 Round-Robin Tournament

**Format**: All benchmark opponents play each other once per pair (120 pairs for 16 opponents).

**Games per pair**: 100 games (50 each color).

**Scoring**: Win=1, Draw=0.5, Loss=0.

**Rating**: Bradley-Terry model with draw adjustment.

### 9.2 Swiss-style Tournament

**Format**: More efficient for larger opponent pools (32+ opponents).

**Rounds**: Log2(N) rounds, where N = number of opponents.

**Advantage**: Fewer total games needed while still identifying top performers.

### 9.3 Ladder Tournament (Recommended)

**Format**: Progressive ladder - bots advance by defeating their assigned opponent.

**Structure**:
- Tier 1 bots (B-01 to B-03) play each other
- Winners of Tier 1 play Tier 2 (B-04 to B-06)
- Winners of Tier 2 play Tier 3 (B-07 to B-09)
- ...and so on up to Tier 5 (B-15, B-16)

**Advantage**: Efficient - tests whether each bot can beat its tier.

**Limitation**: Does not measure exact Elo differences within a tier.

### 9.4 Position-Suite Benchmark (Recommended for Validation)

**Format**: All bots receive the same position suite. Each bot must play the optimal move (as identified by solver).

**Scoring**: Agreement rate with solver (0-100%).

**Advantage**: Direct, unambiguous measure of tactical correctness.

**Cost**: Low (no game play needed, just position evaluation).

---

## 10. Multi-Board Protocol

### 10.1 Board-Size Testing Matrix

| Board | Rows x Cols | Inarow | Known Status | Games per Pair | Source |
|-------|-------------|--------|-------------|----------------|--------|
| 4x5 | 5x4 | 3 | Standard Kaggle variant | 100 | C104 (tested in framework) |
| 6x7 | 7x6 | 4 | Solved: P1 win | 100 | C001 (VERIFIED) |
| 7x8 | 8x7 | 4 | No known result | 50 | HYPOTHESIS |
| 8x8 | 8x8 | 4 | Solved: P2 win | 100 | C129 (VERIFIED, Tromp) |
| 9x6 | 6x9 | 4 | Solved: P1 win | 50 | C130 (VERIFIED) |
| 10x8 | 8x10 | 4 | Draw | 50 | C131 (VERIFIED) |
| 11x11 | 11x11 | 4 | Unknown | 25 | C132 (HYPOTHESIS) |
| 12x12 | 12x12 | 4 | Unknown | 25 | C132 (HYPOTHESIS) |
| 15x13 | 13x15 | 4 | Unknown | 25 | C132 (HYPOTHESIS) |
| 15x10 | 10x15 | 4 | Unknown | 25 | C132 (HYPOTHESIS) |

### 10.2 Board-Size Scaling Analysis

Per gridline-four-android (S096):
- Disc placement: O(R + C)
- Decision: O(C * (R + C))

**Growth rate**: Board size scales quadratically in search nodes.

**Implication**: A bot that achieves depth 10 on 7x6 may only achieve depth 4-5 on 8x8 and depth 2-3 on 15x13 with same time budget.

### 10.3 Transfer Learning Test

If training on 7x6 and evaluating on 15x13:
- Measure policy agreement (same move) vs NN trained on 15x13
- Measure value correlation (position evaluation agreement)
- Expected gap: HYPOTHESIS (C014: 60-70% native strength)

---

## 11. Governance and Constraints

### 11.1 Kaggle Constraints

All experiments must respect:
- 2s/move timeout (actTimeout)
- 60s overtime bank (remainingOverageTime)
- No C++ dependency (Python-only)
- No external network calls during game play
- Board state as flat 1D array (not 2D)

### 11.2 Reproducibility Constraints

- All random seeds must be fixed per experiment
- NN weights must be saved and loaded deterministically
- Search order must be deterministic (sorted columns, not hash-order)
- TT must be cleared between experiments

### 11.3 Hardware Neutrality

Experiments should be runnable on:
- CPU-only (baseline)
- Kaggle T4 GPU (target)
- RTX 5090 (training, if available)

Results should be reported per hardware tier.

---

## 8. MCTS Consistency Benchmarks

### BMS-005: MCTS Consistency on Solved Positions

**Purpose**: Measure whether MCTS-based bots can achieve optimal play on solved-game positions within practical simulation budgets. This is a governance-relevant benchmark because it determines whether MCTS-based bots can be trusted to play optimally on solved boards.

**Test specification**:
- Board: 7x6
- Starting position: center column (col 4) — known P1 win
- Opponent: Pascal Pons solver (optimal play)
- Metric: oracle agreement rate (% of moves matching solver's optimal move)
- Simulation counts: 10, 50, 100, 500, 1000, 4000
- Target: ≥90% oracle agreement at ≤1600 sims (Kaggle-feasible)
- Test bots: connectpuct (80 sims), rowspire (4000 sims, NN-guided), katac4 (1600 sims, NN-guided)

**Falsification**: If any bot achieves ≥90% oracle agreement at ≥1600 simulations, the MCTS consistency problem is less severe than hypothesized.

### BMS-006: Board-Size Coverage Audit

**Purpose**: Document which board sizes are tested vs. which are supported by the Kaggle environment specification.

**Test specification**:
- Inspect kaggle-environments test_connectx.py for all board sizes tested
- Cross-reference with connectx.json environment spec for supported board sizes
- Document the coverage gap: current test suite exercises 7x6 (6 tests) and 4x5/inarow=3 (8 tests); 15x13 and 15x10 have ZERO test evidence despite being supported by the environment spec

**Governance risk**: Bots optimized for 7x6 will pass Kaggle evaluation but may fail on 15x13 if the competition ever expands to include those boards.

---

### BMS-007: Board-Size Benchmark Suite

**Purpose**: Measure how a 7×6-optimized bot performs on larger board sizes. Fills the gap identified by BMS-006 (board-size coverage audit).

**Test specification**:
- Board sizes: 6×5 (inarow=3), 8×8, 10×8, 12×10
- Opponent: classical engine at each board size (depth-limited alpha-beta)
- Metric: win rate, draw rate, loss rate, average game length, per-move latency

### BMS-008: GPU Latency Profiling

**Purpose**: Profile NN inference + MCTS latency on T4 GPU. Measures actual compute budget utilization.

**Test specification**:
- Hardware: Kaggle T4 GPU
- Profile points: NN inference, TT lookup, MCTS node expansion, leaf evaluation
- Metric: p50/p95/p99 latency per operation, total latency per move

### BMS-009: Ablation Study Design

**Purpose**: Remove one component at a time and measure delta. Isolates component contributions.

**Test specification**:
- Components to ablate: TT, move ordering, fork detection, NN policy prior, MCTS
- Metric: win rate delta, search speedup, node throughput delta
- Method: run full ensemble vs. ensemble minus each component

### BMS-010: GPU vs CPU MCTS Ablation

**Purpose**: Compare identical MCTS on GPU vs CPU. Measures GPU acceleration benefit.

**Test specification**:
- Identical MCTS parameters, hardware comparison (T4 GPU vs CPU)
- Metric: simulation throughput (sims/sec), latency per simulation
- Control: same MCTS algorithm, same board positions

### BMS-011: Adversarial Opponent Testing

**Purpose**: Test bots against exploit-specific opponents. Measures robustness to adversarial strategies.

**Test specification**:
- Adversarial opponents: always-play-first-move, never-block, random-evasion
- Metric: win rate against each adversary, pattern exploitation detection rate

### BMS-012: Reproducibility Protocol

**Purpose**: Seed control, deterministic replay, TT clear. Ensures experiments are reproducible.

**Test specification**:
- Seed all random operations
- Clear TT between games
- Log all positions and moves
- Metric: bitwise identical results across runs

---

## 9. Documentation and Experiment Tracking

### 12.1 Experiment Metadata

Each experiment tracked with:
- Experiment ID (EXP-###)
- Date started/completed
- Hypothesis being tested
- Experimental setup (board size, opponents, time limits)
- Results (win rates, Elo, statistical significance)
- Source attribution (which claim(s) does this verify or refute)

### 12.2 Reproducibility

- Seed control: Use fixed random seed for all non-deterministic components
- Configuration file: Store all hyperparameters (board size, depth, sim count, NN architecture)
- Output format: JSON with position, bot move, solver move, game outcome
- Artifact: Save full game PGN/replay for every match

### 12.3 Report Format

Each experiment report should include:
- Objective
- Methodology
- Results with confidence intervals
- Conclusion (supported/refuted/neutral)
- Impact on architecture rankings
- Follow-up experiments recommended

---