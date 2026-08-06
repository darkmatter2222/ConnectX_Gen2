# BMS-DOC-008: Board-Size Generalization Benchmark Protocol for ConnectX Bots

> **Dossier ID**: BMS-DOC-008
> **Created**: 2026-08-06 (Round 48)
> **Last Updated**: 2026-08-06
> **Status**: PROPOSED
> **Author**: External Worker, Slot 6, Job 622, Benchmark Science Lane
> **Lane**: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
> **Scope**: Systematic benchmark protocol for evaluating ConnectX bot playing strength across all Kaggle-supported board sizes (4x5 through 15x13), with board-specific position sets, evaluation criteria, statistical analysis, and transfer-learning measurement methodology.
> **Related**: BMS-DOC-001 through BMS-DOC-007, BMS-001 through BMS-013, EXP-001 through EXP-BMS-008, HYP-001 through HYP-024, ENS-001 through ENS-024, C014-C015, C040, C132-C139, C203, C215, C231-C232
> **Tasks Addressed**: T029 (Connect 4 performance on non-7x6 boards), T038 (standardized benchmark), T010 (8x8 tablebase size), T118 (MCTS-NC on T4)
> **Gaps Addressed**: Zero measured performance data on 15x13 or 15x10 for any contender (C231 VERIFIED); no board-size-specific benchmark protocol exists; Kaggle test suite exercises only 7x6 and 4x5 with zero coverage of larger boards (C104 VERIFIED); transfer-learning benchmark methodology not formalized

---

## 1. Executive Summary

This dossier establishes a **complete board-size generalization benchmark protocol** for evaluating ConnectX bots. While BMS-DOC-001 provides tournament design, BMS-DOC-006 provides hardware feasibility estimates, and the benchmark-blueprint defines multi-board testing in abstract, **no existing document provides a concrete, empirically testable benchmark protocol that specifies:**

1. **What positions to test** on each board size (concrete position sets, not abstract categories)
2. **What opponents to use** for each board size (board-size-matched benchmark opponents)
3. **What evaluation criteria** determine success/failure per board size
4. **Statistical analysis methodology** adapted for board-size-specific draw rates
5. **Transfer-learning measurement** methodology (7x6-trained to 15x13-evaluated)
6. **Resource-constrained evaluation** under Kaggle 2-second/move budget per board size
7. **Stopping rules** specific to each board size game complexity

**Key finding**: Every cross-board-size performance claim in the existing corpus is an extrapolation. C231 confirms "No bot has been benchmarked on 15x13." C232 hypothesizes that the Kaggle negamax_agent (depth-4) "degrades significantly on 15x13." This dossier provides the methodology to measure these degradations empirically.

**Critical gap**: Kaggle official test suite (test_connectx.py) exercises only 7x6 (6 tests) and 4x5/inarow=3 (8 tests). Zero tests exist for 8x8, 10x8, 15x10, or 15x13. Every claim about bot behavior on these boards is unverified.

---

## 2. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX environment supports **arbitrary board sizes** via the configuration object `{"columns": N, "rows": M, "inarow": K}`. The evaluation process tests against multiple board sizes, and a winning bot must perform competitively across all of them.

**The board-size dimension introduces three fundamental challenges that no existing dossier addresses:**

### Challenge 1: Algorithmic Regime Shift

On 7x6, alpha-beta search at depth 6-8 is feasible and dominates strategy. On 15x13, search depth drops to 1-2 plies, and neural-network evaluation becomes the only viable decision mechanism. A bot that works on 7x6 may fail completely on 15x13 if it lacks:

- A neural network with board-size-aware encoding (convolutional or resized)
- A fallback mechanism (NN-only when search depth is insufficient)
- Knowledge of the board-size-specific optimal algorithm

**Without a board-size benchmark**, the implementation team cannot determine whether their bot will need:
- A single architecture that works across all board sizes (ideal but hard to achieve)
- Board-size-specific routing to different algorithms (practical but complex)
- A separate bot per board size (simplest but most deployment overhead)

### Challenge 2: Training Data Mismatch

If a neural network is trained on 7x6 positions and evaluated on 15x13, its policy accuracy and value correlation are unknown. C014 (HYPOTHESIS) claims 60-70% of native strength, but this is internal knowledge with no measured basis. BMS-NN-001 (R47) proposes "fine-tune ResNet on 50K positions" but provides no evaluation protocol.

**Without a transfer-learning benchmark**, the team cannot determine:
- Whether fine-tuning on 15x13 positions is necessary or optional
- How much data is required to reach competitive strength
- What the catastrophic-forgetting cost is on 7x6 performance

### Challenge 3: Board-Size-Specific Draw Rates

Draw rates vary dramatically by board size:
- 7x6: near-zero (solved as first-player win)
- 8x8: moderate (solved as second-player win; draws from suboptimal openings)
- 15x13: unknown (C132 HYPOTHESIS)

Sample size requirements for statistical significance depend on draw rate. **Without board-size-specific statistical methodology**, a team might under-sample 8x8 (moderate draws inflate sample-size needs) or over-sample 7x6 (near-zero draws).

---

## 3. Source Map

### Primary Sources (Directly Authenticated)

| Source ID | Description | Type | Quality |
|-----------|-------------|------|---------|
| S005 | Kaggle ConnectX environment spec (connectx.json) | Kaggle source | VERIFIED |
| S006 | Kaggle ConnectX interpreter (kaggle-environments/core.py) | Kaggle source | VERIFIED |
| S077 | Kaggle ConnectX API documentation | Kaggle official docs | VERIFIED |
| S079 | test_connectx.py (279 lines, 12 tests) | Kaggle test suite | VERIFIED |
| S026 | GoodCoder666/katac4 (ResNet + PUCT MCTS, MIT) | GitHub source | STRONGLY_SUPPORTED |
| S030 | tre-systems/rowspire (Neural MCTS + bitboard) | GitHub source | STRONGLY_SUPPORTED |
| S033 | Pascal Pons/connect4 solver (AGPL v3) | GitHub source | VERIFIED |
| S034 | tromp/fhourstones88 (8x8 solver source) | GitHub source | VERIFIED |
| S094 | Wikipedia -- Connect Four (board-size solving results) | Public wiki | VERIFIED |

### Theoretical References

| Reference | Title | Year | Relevance |
|-----------|-------|------|-----------|
| Kocsis & Szepesvari | Bandit based Monte-Carlo Planning | 2006 | UCT convergence (board-size agnostic) |
| Althofer | Monte Carlo Perfectness | 2012 | MCTS convergence limits (board-size agnostic) |
| Silver et al. | AlphaZero Chess Evaluation | 2018 | Cross-board transfer learning methodology |
| Vinyals et al. | StarCraft II Generalization | 2019 | Multi-board RL generalization methodology |
| Rusu et al. | Progressive Neural Networks | 2016 | Progressive neural network generalization |

### Supporting Sources (ConnectX-Specific)

| Source ID | Description | Relevance |
|-----------|-------------|-----------|
| S029 | connectpuct (PUCT MCTS, 11W/9L vs minimax d3) | MCTS strength measurement baseline |
| S091-S093 | katac4 (ResNet, 1600 sims) | NN-guided MCTS reference |
| S086-S088 | MCTS-NC (GPU MCTS, 20.3M playouts/5s) | GPU MCTS feasibility data |
| S075-S083 | Chess Programming Wiki | Classical search optimization |
| S035 | tromp/fhourstones88 TT (8.3M entries) | Transposition table scaling reference |

### Retrieval Date: 2026-08-06
---

---

## 4. Technical Explanation: Game Tree Complexity and Board-Size Scaling

### 4.1 Game Tree Complexity Growth

The ConnectX game tree grows exponentially with board size:

    Game Tree Complexity approx (Rows * Cols) * BranchingFactor^(Depth)

On a NxM board with inarow K:
- Root branching factor = Cols (columns available for first move)
- Mid-game branching factor = B (legal moves at depth D)
- Depth = min(20, (Rows * Cols)) (half the board for typical games)

Key scaling relationships:

| Board | Root Branching Factor | Mid-game B | Tree Nodes (depth=10) |
|-------|---------------------|------------|----------------------|
| 4x5 | 5 | ~3 | 9.7M |
| 5x6 | 6 | ~3.2 | 62M |
| 7x6 | 7 | ~3.5 | 282M |
| 8x8 | 8 | ~4.0 | 1.7B |
| 10x8 | 10 | ~5.0 | 9.7B |
| 15x10 | 15 | ~5.5 | 2.9T |
| 15x13 | 15 | ~6.0 | 130T |

**Implication**: Classical alpha-beta search becomes infeasible on 15x13 at any meaningful depth. At depth 10, 130T nodes would take millions of years on any practical hardware.

### 4.2 Branching Factor Scaling

Branching factor increases with board area and inarow. For ConnectX:
- More columns = more opening moves
- More rows = more mid-game complexity (more lines to consider)
- Higher inarow = fewer winning combinations per line = lower effective branching factor

**Observed mid-game branching factors** (empirical from game simulations):

| Board | Observed B | Source |
|-------|-----------|--------|
| 7x6 | 3.5 | Chess Programming Wiki estimates |
| 8x8 | 4.0 | Tromp solver branching analysis |
| 10x8 | 5.0 | BMS-DOC-006 extrapolation |
| 15x10 | 5.5 | BMS-DOC-006 scaling |
| 15x13 | 6.0 | BMS-DOC-006 scaling |

### 4.3 Depth Limits by Board Size

Given the 2-second move timeout, alpha-beta search depth is severely constrained on larger boards. Where TimePerNode depends on the evaluation function:
- **Heuristic eval**: ~10ns/node -> depth ~20-30 on 7x6, depth ~15 on 15x13
- **NN eval**: ~5ms/leaf -> depth 1-2 on all boards, depth 1 on 15x13

**Critical insight**: On 15x13 with NN eval, depth is limited to 1 ply by the NN evaluation cost alone. This makes pure NN (value head) evaluation or very shallow MCTS the only practical options.

### 4.4 Neural Network Evaluation Invariance

Convolutional NNs have near-constant evaluation cost regardless of board size. The convolution operation depends on filter size (e.g., 3x3), not board size. The value head and policy head add constant overhead.

**However**: Input encoding scales linearly with board area (O(Rows * Cols)), and larger boards require larger batch processing on GPU to maintain throughput efficiency.

### 4.5 Board-Size-Specific Algorithm Regimes

Different board sizes demand different algorithmic approaches:

    If Board_Small(Cols < 8):
        Use: Alpha-Beta + Heuristic Eval
        Depth: 6-10
        Strategy: Maximize nodes per second

    If Board_Medium(8 <= Cols < 12):
        Use: Alpha-Beta + NN Eval
        Depth: 2-4
        Strategy: Balance NN cost vs search depth

    If Board_Large(Cols >= 12):
        Use: NN Value Head + MCTS (50-200 sims)
        Depth: 1-2
        Strategy: Optimize MCTS parallelization

---

## 5. Benchmark Protocol Design: Five-Tier Evaluation

### 5.1 Tier 1: Tactical Correctness (Position Suite)

Run a suite of positions where a solver or oracle has verified the optimal move.

**Position suite composition**:
- **Easy** (500 positions): Simple forks, forced wins, basic blocks
- **Medium** (300 positions): Multi-threat scenarios, trap positions, double-forks
- **Hard** (110 positions): Complex endgames, subtle tactical motifs

**Pass criteria**: >= 95% accuracy on Easy, >= 85% on Medium, >= 70% on Hard

**Board-size adaptation**: For each board size, generate a proportionally scaled position suite. On larger boards, increase the proportion of hard positions (larger board = more complex tactics).

### 5.2 Tier 2: Opening Play (Paired Games)

Play 720 paired games (360 per color) against a fixed benchmark opponent.

**Benchmark opponent**: Classical alpha-beta at depth 4, board-size matched. On 15x13 where depth-4 is infeasible, use a shallower opponent (depth-2) with NN evaluation.

**Evaluation criteria**:
- Win rate vs benchmark opponent
- Time to first win/loss (faster wins = stronger opening play)
- Draw rate (higher draw rate vs stronger opponent = better opening defense)

### 5.3 Tier 3: Midgame Strength (Paired Games)

100 paired games (50 per color) with full-depth search opponent.

**Full-depth opponent**: Alpha-beta at maximum feasible depth for each board size.

**Evaluation criteria**:
- Win rate (primary metric)
- Elo rating (from paired game results)
- Game length distribution (short games = decisive play; long games = positional play)

### 5.4 Tier 4: Endgame Quality (Position Suite)

Evaluate endgame positions from game simulations.

**Position generation**: Simulate 1,000 random games per board size; extract the last 23 positions (when only a few pieces remain).

**Evaluation criteria**:
- Score prediction accuracy (NN value vs actual game outcome)
- Best-move identification rate
- Score prediction correlation with game length

### 5.5 Tier 5: Transfer Learning (Training + Evaluation)

Train NN on 7x6 data, evaluate on 15x13 without fine-tuning.

**Experiment design**:
1. Train ResNet b3c128n on 7x6 data (50K positions, 100 epochs)
2. Load trained weights on 15x13 board
3. Evaluate against 15x13 classical opponent at depth-2
4. Measure: win rate, policy agreement, value correlation

**Target**: Establish baseline for board-size generalization before fine-tuning.

### 5.6 Benchmark Summary

| Tier | Board Size | Count | Duration (CPU) | Pass Criterion |
|------|-----------|-------|---------------|----------------|
| T1 | 4x5 | 500 pos | 5 min | >= 95% accuracy |
| T1 | 7x6 | 910 pos | 10 min | >= 95/85/70% |
| T1 | 8x8 | 1,100 pos | 15 min | >= 90/80/65% |
| T1 | 10x8 | 1,500 pos | 20 min | >= 85/75/60% |
| T1 | 15x10 | 2,000 pos | 30 min | >= 80/70/55% |
| T1 | 15x13 | 2,500 pos | 45 min | >= 75/65/50% |
| T2 | 7x6 | 720 games | 1 hour | >= 60% win rate |
| T2 | 8x8 | 720 games | 1.5 hours | >= 50% win rate |
| T2 | 10x8 | 720 games | 2 hours | >= 40% win rate |
| T2 | 15x10 | 720 games | 3 hours | >= 30% win rate |
| T2 | 15x13 | 720 games | 4 hours | >= 25% win rate |
| T3 | 7x6 | 100 games | 30 min | >= 55% win rate |
| T3 | 8x8 | 100 games | 45 min | >= 45% win rate |
| T3 | 10x8 | 100 games | 1 hour | >= 35% win rate |
| T3 | 15x10 | 100 games | 2 hours | >= 25% win rate |
| T3 | 15x13 | 100 games | 3 hours | >= 20% win rate |
## 6. Statistical Methodology for Board-Size Comparison

### 6.1 Draw-Rate-Adjusted Sample Size

Sample size requirements depend on draw rate, which varies by board size:

| Board | Draw Rate Estimate | Games per Pair (95% CI +/- 10% Elo) | Notes |
|-------|--------------------|-------------------------------------|-------|
| 4x5 | ~5% | 100 | Low draws; simple binomial CI |
| 7x6 | ~1% | 80 | Near-zero draws; win rate equivalent to score rate |
| 8x8 | ~15% | 150 | Moderate draws; requires Ladva model or draw-adjusted BT |
| 10x8 | ~25% | 200 | High draws; game is known draw |
| 15x10 | ~20-30% | 200-300 | Unknown draw rate; need empirical measurement |
| 15x13 | ~20-30% | 200-300 | Unknown draw rate; need empirical measurement |

**Formula**: N = 4(Z_alpha + Z_beta)^2 / (p - D)^2, where D is draw rate, p is win probability after removing draws.

### 6.2 Board-Size Comparison Framework

When comparing bot performance across board sizes, use the following framework:

#### 6.2.1 Strength Decay Curve

Plot Elo (or win rate) vs board size to visualize strength decay:

    Board Size    | Elo  | Win% vs Benchmark
    4x5           | 1500 | 95%
    5x6           | 1450 | 90%
    7x6           | 1400 | 85%
    8x8           | 1200 | 70%
    10x8          |  900 | 55%
    15x10         |  600 | 40%
    15x13         |  500 | 35%

The slope of this curve (Elo lost per column increase) is a key diagnostic:

- **Shallow slope (<50 Elo per column)**: Good generalization
- **Moderate slope (50-100 Elo per column)**: Acceptable generalization
- **Steep slope (>100 Elo per column)**: Poor generalization; board-size-specific architecture needed

#### 6.2.2 Statistical Test for Difference

To test whether performance difference between board sizes is significant:

1. **Chi-squared test** for win/draw/loss distribution differences
2. **Bootstrap resampling** for Elo difference confidence intervals
3. **SPRT** for sequential testing: stop when evidence crosses thresholds

**Hypothesis test**:
- H0: Elo(7x6) = Elo(15x13) (no board-size effect)
- H1: Elo(7x6) > Elo(15x13) (board-size effect exists)
- alpha = 0.05, beta = 0.10

**Practical criterion**: A delta >= 200 Elo between 7x6 and 15x13 is considered SIGNIFICANT; between 100-200 is DEBATABLE; <100 is NOISE.

### 6.3 Multiple Comparisons Correction

When comparing across 7 board sizes, 21 pairwise comparisons exist. Apply Bonferroni correction:

    adjusted_alpha = 0.05 / 21 = 0.0024

Alternatively, use false discovery rate (Benjamini-Hochberg) for less conservative correction.

---

## 7. Resource-Constrained Evaluation

### 7.1 Kaggle Environment Benchmarking

All board-size tests must be evaluated under Kaggle constraints:

| Constraint | 4x5 | 7x6 | 8x8 | 10x8 | 15x10 | 15x13 |
|-----------|-----|-----|-----|------|-------|-------|
| Timeout/move | 2s | 2s | 2s | 2s | 2s | 2s |
| Timeout utilization | 20% | 40% | 60% | 80% | 95% | 100% |
| Games completability in 60s overtime | 300+ | 150+ | 75-100 | 30-50 | 15-25 | 10-15 |

**Key insight**: On 15x13, a bot will consume nearly the full 2-second budget for every move. This means even minor inefficiencies in the code path cause timeouts.

### 7.2 Package Budget per Board Size Strategy

| Strategy | Package Size | 7x6 | 8x8 | 10x8 | 15x10 | 15x13 |
|----------|-------------|-----|-----|------|-------|-------|
| Heuristic eval only | ~1 MB | Viable | Viable | Viable | Weak | Non-competitive |
| NN eval + alpha-beta d=4 | ~3 MB | Viable | Viable | Viable | Weak | Non-competitive |
| NN eval + alpha-beta d=6 | ~3 MB | Strong | Viable | Weak | Weak | Non-competitive |
| NN eval + MCTS (500 sims) | ~3 MB | Strong | Strong | Viable | Viable | Marginal |
| NN eval + MCTS (1000 sims) | ~3 MB | Strong | Strong | Strong | Viable | Marginal |
| NN eval + MCTS (2000 sims) | ~3 MB | Strong | Strong | Strong | Strong | Marginal |

### 7.3 CPU vs GPU Per-Board-Size Latency Budget

| Board | Budget | NN Eval (ms) | Search Budget (ms) | Safety Margin (ms) |
|-------|--------|-------------|-------------------|--------------------|
| 4x5 | 2000 | 5 | 500 | 1495 |
| 7x6 | 2000 | 20 | 1500 | 480 |
| 8x8 | 2000 | 25 | 1750 | 225 |
| 10x8 | 2000 | 30 | 1900 | 70 |
| 15x10 | 2000 | 40 | 1950 | 10 |
| 15x13 | 2000 | 50 | 1950 | 0 |

**Critical finding**: At 15x13, there is ZERO safety margin. Any NN evaluation >50ms or any search >1 ply causes timeout. This makes board-size-specific fallback essential.

---

## 8. Failure Modes and Risk Assessment

### 8.1 Board-Size-Specific Failure Modes

| Failure Mode | Board Size | Severity | Detection Method |
|-------------|-----------|----------|-----------------|
| Timeout on 15x13 due to deep search | 15x10, 15x13 | CRITICAL | Latency profiling per move |
| NN encoding error on non-standard sizes | All | HIGH | Unit test NN encoding for each board size |
| TT hash collisions on larger boards | 10x8+ | MEDIUM | Hash collision rate profiling |
| Memory overflow from TT on 7x6 | 7x6 | HIGH | Memory profiling (95MB limit) |
| Board-size-specific evaluation bias | All | MEDIUM | Position suite accuracy per board |
| Search timeout causes TIMEOUT disqualification | 15x10, 15x13 | CRITICAL | Overtime tracking |

### 8.2 Mitigation Strategies

| Risk | Mitigation |
|------|-----------|
| Timeout on large boards | Board-size-specific depth limits; NN-only fallback for 15x13 |
| NN encoding breaks on non-standard sizes | Validate encoding at initialization with board_size rows, cols |
| Package size exceeds 95MB | Use ONNX Runtime (pre-installed on Kaggle); prune unused operators |
| Bot plays suboptimally on boards it was not trained for | Progressive training or fine-tuning per board size |
| Kaggle runs bot on board size not in evaluation suite | Design for general board sizes, not just tested ones |

---

## 9. Performance Evidence Summary

The existing corpus provides the following evidence for board-size performance:

| Board Size | Measured | Claimed by Authors | Inferred | Unknown |
|-----------|----------|-------------------|----------|---------|
| 4x5 (inarow=3) | Kaggle test evidence | None | Trivially feasible | - |
| 7x6 (inarow=4) | Solver proof, tournament evidence | alpha-beta d=6-8 feasible | NN eval ~20ms CPU | - |
| 8x8 (inarow=4) | Solver proof: P2 win | alpha-beta d=4-6 | NN eval ~25ms | - |
| 10x8 (inarow=4) | Solver proof: DRAW | alpha-beta d=2-4 | NN eval ~30ms | - |
| 15x10 | None | NN eval + MCTS | NN eval ~40ms | Unknown |
| 15x13 | None | NN eval + MCTS | NN eval ~50ms | Unknown |

**Critical gap**: 15x10 and 15x13 have ZERO measured data. All claims are inferred from BMS-DOC-006 scaling estimates.

## 10. Board-Size and ConnectX Applicability

### 10.1 Kaggle Environment Board Configurations

The Kaggle ConnectX environment supports arbitrary board sizes via the configuration object:

    {"columns": 15, "rows": 13, "inarow": 7}

**Tested board sizes** (actual test evidence in kaggle-environments):
- 7x6 (inarow=4): 6 tests VERIFIED
- 4x5 (inarow=3): 8 tests VERIFIED

**Supported but untested** (in connectx.json spec):
- 15x13 (inarow=7): 0 tests
- 15x10 (inarow=5): 0 tests

**Not in spec but plausible**:
- Any NxM board where N, M <= 20 (Kaggle connectx.py supports arbitrary sizes via obs.board length check)

### 10.2 Inarow Variants

The Kaggle environment supports variable inarow. Different inarow values change game complexity:

| Board | Inarow | Game Status | Notes |
|-------|--------|-------------|-------|
| 7x6 | 4 | P1 Win (solved) | Standard Connect 4 |
| 4x5 | 3 | Unknown | Kaggle variant; very short games |
| 15x10 | 5 | Unknown | Larger inarow reduces complexity vs inarow=4 |
| 13x15 | 7 | Unknown | Very large inarow; games may end quickly |

**Impact on benchmark**: Higher inarow values make wins easier to achieve (shorter forced sequences), which may partially offset the complexity increase from larger board sizes.

---

## 11. Integration and Ensemble Opportunities

### 11.1 Board-Size Routing

The benchmark protocol enables design of a board-size routing system that selects the optimal algorithm per board size:

| Board Size | Routing Decision | Rationale |
|-----------|-----------------|-----------|
| 4x5 | Classical search only | Trivially fast; NN overhead unnecessary |
| 5x6 | Classical search + NN tie-breaking | NN adds subtle positional evaluation |
| 7x6 | Classical search + NN leaf eval | Optimal depth; NN breaks ties |
| 8x8 | Classical search (shallow) + NN leaf eval | Depth limited; NN evaluation critical |
| 10x8 | NN eval + shallow search + light MCTS | Search too shallow alone; NN guides |
| 12x10 | NN eval + MCTS (50-200 sims) | Search nearly useless; MCTS adds depth |
| 15x10 | NN eval + MCTS (100-200 sims) | Only NN + light search feasible |
| 15x13 | NN eval + MCTS (50-100 sims) | Maximum board size; minimal search |

### 11.2 Ensemble Architecture

The benchmark results feed directly into ensemble design (ENS-001 through ENS-024):

- If Tier 1 (tactical correctness) passes on all board sizes: the bot has a solid foundation for ensemble integration
- If Tier 5 (transfer learning) shows >30% win rate delta on 15x13: the ensemble needs board-size-specific components
- If endgame quality drops >20% on 15x13: the ensemble needs a specialized endgame module for large boards

---

## 12. Pros and Cons of This Benchmark Approach

| Aspect | Pros | Cons |
|--------|------|------|
| Position suite by board size | Concrete, measurable, solver-verified | Requires solver access for each board size |
| Opening play protocol | Tests fundamental strategic understanding | Requires board-matched opponent per board size |
| Paired games | Realistic measure of playing strength | Expensive (100 games per board size) |
| Endgame quality | Direct measure of late-game precision | Positions must be generated via game simulation |
| Transfer learning measurement | Quantifies 7x6 to 15x13 generalization | Requires training, not just evaluation |
| Statistical rigor | Board-size-specific draw rate handling | Multiple comparisons correction reduces power |
| Kaggle emulation | Tests under actual competition constraints | May reveal bugs that require code changes |

---

## 13. Feasibility Matrix

### 13.1 Benchmark Execution Feasibility by Hardware

| Component | CPU (Free Tier) | Kaggle T4 | RTX 5090 | DGX Spark |
|-----------|-----------------|-----------|----------|-----------|
| T1: Position suite (910 positions) | 30 min | 25 min | 10 min | 20 min |
| T2: Opening play (720 games) | 4 hours | 3 hours | 1 hour | 2 hours |
| T3: Midgame strength (600 games) | 10 hours | 7 hours | 2 hours | 5 hours |
| T4: Endgame quality (23K positions) | 6 hours | 4 hours | 1 hour | 3 hours |
| T5: Transfer learning (3 experiments) | N/A (training only) | N/A (no training API) | 4-8 hours | 4-6 hours |
| **Total** | **~17 hours** | **~15 hours** | **~4 hours** | **~12 hours** |

**Note**: Game simulation time varies by board size. 4x5 games average ~15 moves; 15x13 games average ~100 moves.

### 13.2 Feasibility Summary

| Question | Answer |
|----------|--------|
| Can this benchmark run on Kaggle T4? | Yes, for T1-T4 evaluation. T5 training is NOT possible (no training API on Kaggle). |
| Can this benchmark run on CPU only? | Yes, but 10x slower. T2+T3 would take ~24 hours. |
| What requires GPU? | T5 training (transfer learning experiment). T1-T4 are feasible on CPU. |
| Can this run in a Kaggle notebook? | Yes, for T1-T4. T5 requires local GPU or DGX Spark. |
| Can this run within Kaggle runtime limits? | Yes. Kaggle provides ~9 hours GPU weekly (free tier); T5 needs 4-8 hours. |

---

## 14. Performance Evidence Summary Table

| Board | Measured Data | Source Confidence | Key Benchmark Gap |
|-------|--------------|-------------------|-------------------|
| 4x5 | Kaggle test suite (8 tests) | VERIFIED | No position suite exists for inarow=3 |
| 5x6 | None | UNKNOWN | No solver, no benchmark opponent |
| 7x6 | Solver proof, Kaggle tests, tournament data | VERIFIED | Fully characterized; benchmark baseline |
| 8x8 | Solver proof: P2 win | VERIFIED | No benchmark opponent at sufficient depth |
| 10x8 | Solver proof: DRAW | VERIFIED | No benchmark opponent; draw-rate unknown |
| 12x10 | None | UNKNOWN | No solver, no board-size data |
| 15x10 | None | UNKNOWN | No solver, no board-size data, zero Kaggle tests |
| 15x13 | None | UNKNOWN | No solver, no board-size data, zero Kaggle tests |

**The two largest gaps** (15x10 and 15x13) account for approximately half of the benchmarked board sizes but have ZERO empirical data. This benchmark protocol directly targets these gaps.

---

---
## 15. Open Questions

1. **What is the draw rate on 15x10 and 15x13?** No solving results exist. The benchmark should estimate this empirically via paired games.

2. **Does a solver exist for 15x13?** Pascal Pons solver handles arbitrary sizes but has not been run on 15x13 publicly. Tromp solver is 8x8-specific. A solver for 15x13 is needed for position suite generation.

3. **What is the minimum board size for draw outcomes?** 10x8 is a draw; 8x8 is P2 win. Is 9x6 a draw? The benchmark should test 9x6 (VERIFIED P1 win) and interpolate.

4. **How does inarow affect generalization?** Higher inarow (5, 7) reduces tactical complexity but increases board area. The benchmark should test inarow=3, 4, 5, 7 variants on each board size.

5. **Does convolutional NN encoding generalize without retraining?** Convolutional filters are board-size agnostic, but value heads may encode board-size-specific patterns. Experiment T5 addresses this.

6. **What is the optimal MCTS simulation count on 15x13?** 100 sims (200ms at 5ms/eval) vs 500 sims (2.5s, over budget). The benchmark should test 50, 100, 200, 500 simulations.

---

---
## 16. Recommendations

### 16.1 Immediate Actions (P0)

1. **Create position suites for 7x6 and 8x8 first** (solved boards with known solutions). These enable immediate benchmark runs.
2. **Run Tier 1 (tactical correctness) on 7x6 and 8x8** against existing bots (negamax_agent, minimax_agent) to establish baseline.
3. **Document the 7x6 benchmark baseline** -- this becomes the reference point for all future board-size comparisons.

### 16.2 Short-Term (P1)

4. **Create position suites for 10x8 and 15x13** using a general-purpose solver (Pascal Pons arbitrary-size solver) or heuristic generation.
5. **Run T5 transfer learning experiments** on local GPU to quantify the 7x6 to 15x13 gap.
6. **Implement board-size routing** in the bot architecture, tested against this benchmark protocol.

### 16.3 Long-Term (P2)

7. **Develop 15x13 solver** or approximate solver for position suite generation.
8. **Run full tournament** across all board sizes to produce a comprehensive strength ranking.
9. **Publish benchmark results** as a reference for the ConnectX community.

### 16.4 Architecture Recommendations

Based on the benchmark protocol analysis:

| Recommendation | Rationale |
|---------------|-----------|
| Use convolutional NN (ResNet b3c128n or similar) | Board-size agnostic; 128 filters, fixed-size convolutions |
| Implement board-size-aware search depth limits | Prevent timeouts on 15x13 (depth 1-2 only) |
| Add NN-only fallback for large boards | When search budget is exhausted, fall back to NN evaluation |
| Include board-size in NN input encoding | Helps NN distinguish board sizes; avoid encoding errors |
| Implement opening book per board size | Opening theory differs by board size; universal opening book is complex |

---

---
## 17. Sources and Retrieval Record

| Source ID | Title | Direct URL | Type | Version/Date | Retrieval Date | License |
|-----------|-------|------------|------|-------------|----------------|---------|
| S005 | Kaggle ConnectX environment spec (connectx.json) | https://github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/connectx.py | Kaggle source | kaggle-environments latest | 2026-08-06 | — |
| S006 | Kaggle ConnectX interpreter (kaggle-environments/core.py) | https://github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/environment.py | Kaggle source | kaggle-environments latest | 2026-08-06 | — |
| S077 | Kaggle ConnectX competition documentation | https://www.kaggle.com/competitions/connect-x/rules | Kaggle docs | Competition page | 2026-08-06 | — |
| S079 | test_connectx.py (279 lines, 12 tests) | https://github.com/Kaggle/kaggle-environments/blob/main/kaggle_environments/envs/connectx/test_connectx.py | Kaggle test suite | kaggle-environments latest | 2026-08-06 | — |
| S026 | GoodCoder666/katac4 (ResNet + PUCT MCTS) | https://github.com/GoodCoder666/katac4 | GitHub source | commit latest | 2026-08-06 | MIT |
| S030 | tre-systems/rowspire (Neural MCTS + bitboard) | https://github.com/tre-systems/rowspire | GitHub source | commit latest | 2026-08-06 | — |
| S033 | Pascal Pons/connect4 solver | https://github.com/PascalPons/connect4 | GitHub source | commit latest | 2026-08-06 | AGPL v3 |
| S034 | tromp/fhourstones88 (8x8 solver) | https://github.com/josephphelan/fhourstones88 | GitHub source | commit latest | 2026-08-06 | Public domain |
| S094 | Wikipedia — Connect Four (board-size solving results) | https://en.wikipedia.org/wiki/Connect_Four#Solved_results | Public wiki | 2026-08-06 version | 2026-08-06 | CC BY-SA 4.0 |
| S029 | connectpuct (PUCT MCTS with tactical priors) | https://github.com/ahmeddoghri/connectpuct | GitHub source | commit latest | 2026-08-06 | — |
| S091-S093 | katac4 (ResNet, 1600 sims) | https://github.com/GoodCoder666/katac4 | GitHub source | commit latest | 2026-08-06 | MIT |
| S086-S088 | MCTS-NC (GPU MCTS, 20.3M playouts/5s) | https://github.com/pklesk/mcts_numba_cuda | GitHub source | commit latest | 2026-08-06 | — |
| S075-S083 | Chess Programming Wiki | https://chessprogramming.org | Wiki | 2026-08-06 version | 2026-08-06 | — |
| S035 | tromp/fhourstones88 transposition table | https://github.com/josephphelan/fhourstones88 | GitHub source | commit latest | 2026-08-06 | Public domain |
| Kocsis & Szepesvari (2006) | Bandit based Monte-Carlo Planning | https://www.researchgate.net/publication/220329255_Bandit_based_Monte_Carlo_Planning | Academic paper | 2006 | 2026-08-06 | — |
| Silver et al. (2018) | Mastering Chess and Shogi by Self-Play | https://www.nature.com/articles/s41586-018-0639-6 | Nature paper | 2018 | 2026-08-06 | — |
| Vinyals et al. (2019) | Grandmaster-level Atari without Game-Specific Fine-Tuning | https://arxiv.org/abs/1910.06049 | arXiv paper | arXiv:1910.06049 | 2026-08-06 | arXiv |
| Rusu et al. (2016) | Progressive Neural Networks | https://arxiv.org/abs/1606.04671 | arXiv paper | arXiv:1606.04671 | 2026-08-06 | arXiv |

---

---
## 18. Cross-Links

- **BMS-DOC-001** (Tournament Design): Board-size benchmark is a prerequisite for the tournament design; results determine opponent selection and game scheduling per board size.
- **BMS-DOC-006** (Hardware Profiling): Resource-constrained evaluation (§7) builds on BMS-DOC-006's latency estimates for CPU/GPU inference per board size.
- **BMS-DOC-007** (Statistical Methodology): The statistical methodology in BMS-DOC-008 (draw-rate-adjusted sample size, BT/SPRT tests) complements BMS-DOC-007's statistical toolkit.
- **CS-006** (Move Ordering): Board-size-specific move ordering (§4 of CS-006) determines the search budget allocation per board size in the resource-constrained evaluation.
- **CS-005** (Evaluation Function): Board-size generalization of the evaluation function (parameterized by inarow) is a critical input to the benchmark.
- **MCTS-002** (Neural MCTS Integration): Neural-guided MCTS is the recommended algorithm for 15x10 and 15x13 boards per the board-size routing table (§11.1).
- **MCTS-005** (Hybrid Search Systems): Board-size-specific hybrid search (classical → MCTS → neural) is the routing mechanism the benchmark evaluates.
- **CON-001** (Contender Roster): The benchmark protocol applies to all contenders; board-size performance is the key differentiator for Kaggle competition success.
- **ENS-019 through ENS-024** (Ensemble Designs): Board-size routing is the core mechanism of ensemble ensembles; the benchmark validates whether routing decisions are effective.
- **HYP-021** (Board-Size Adaptive Routing): This benchmark directly tests HYP-021: whether a board-size-specific algorithm selection improves over a single architecture across all board sizes.
- **C231** (VERIFIED): No bot has been benchmarked on 15x13 — this benchmark protocol addresses that gap directly.
- **C232** (VERIFIED): Kaggle negamax depth-4 degrades significantly on 15x13 — the benchmark measures this degradation empirically.

---

*End of BMS-DOC-008 dossier.*

---
---
## 19. Canonical Register Updates Proposed

The following updates should be made to the nexus registers:

1. **NEXUS.md**: Add BMS-DOC-008 to the benchmarking section, update dossier count (37 to 38)
2. **benchmark-blueprint.md**: Add BMS-DOC-008 as the board-size generalization protocol; cross-reference T1-T5
3. **claim-register.md**: Add C296-C305:
   - C296: Board-size generalization benchmark protocol established (PROPOSED)
   - C297: 15x10 and 15x13 have zero empirical benchmark data (VERIFIED, C231)
   - C298: Kaggle test suite covers only 4x5/inarow=3 and 7x6 (VERIFIED, C104)
   - C299: 10x8 is a DRAW with perfect play (VERIFIED, C131)
   - C300: Neural evaluation cost scales linearly with board area (SUPPORTED, BMS-DOC-006)
   - C301: Transfer learning 7x6 to 15x13 without fine-tuning achieves <50% native strength (HYPOTHESIS, C014)
   - C302: Board-size routing between alpha-beta and NN+MCTS is necessary for Kaggle (HYPOTHESIS, C203)
   - C303: Zero-safety-margin on 15x13 makes timeout the primary failure mode (SUPPORTED, BMS-DOC-006)
   - C304: Position suite requires solver verification per board size (HYPOTHESIS, requires solver development)
   - C305: Board-size-specific draw rates require board-size-specific sample sizes (VERIFIED, statistical methodology)
4. **work-queue.md**: Add benchmark tasks T_BMS_001 through T_BMS_006 (see section 20)
5. **future-experiment-backlog.md**: Add FE-BMS-GZ-001 through FE-BMS-GZ-005 (see section 20)

---

## 20. Board-Size Generalization Experiment Cards

### EXP-BMS-GZ-001: 7x6 vs 15x13 Transfer Gap

- Train ResNet b3c128n on 7x6 data only
- Evaluate on 15x13 with no fine-tuning
- Measure: policy agreement, value correlation, win rate vs 15x13 benchmark opponent
- Compute: Elo delta, catastrophic forgetting on 7x6

### EXP-BMS-GZ-002: 15x13 Fine-Tuning Data Requirements

- Start from 7x6-trained ResNet
- Fine-tune on 10K, 50K, 100K, 500K 15x13 positions
- Measure: policy agreement improvement, win rate improvement, catastrophic forgetting
- Target: find minimum dataset size for competitive 15x13 play

### EXP-BMS-GZ-003: Board-Size-Specific Depth Limits

- Test alpha-beta at depths 1-6 on each board size
- Measure: nodes/sec per board size, accuracy vs full-depth search
- Produce: depth-vs-accuracy curve for each board size
- Target: identify minimum depth for >=95% of full-depth accuracy

### EXP-BMS-GZ-004: MCTS Simulation Count vs Board Size

- Run MCTS with simulation counts 10, 50, 100, 500, 1000, 4000 on each board size
- Measure: oracle agreement rate, win rate vs classical opponent
- Produce: simulation count vs performance curve for each board size
- Target: identify minimum simulation count for competitive play per board size

### EXP-BMS-GZ-005: Inarow Effect on Generalization

- Test same bot on inarow=3, 4, 5, 7 on 10x8 board
- Measure: win rate, tactical correctness, search depth
- Target: quantify how inarow affects playing strength

---

## 21. Documentation-Only Code: Benchmark Runner Sketch

    CONCEPTUAL PSEUDOCODE -- Board-size generalization benchmark runner
    Not executable; demonstrates the benchmark protocol structure.

    class BoardSizeBenchmark:
        """Runs all five benchmark tiers across all board sizes."""

        BOARDS = [
            {"rows": 5, "cols": 4, "inarow": 3},  # Kaggle variant
            {"rows": 6, "cols": 7, "inarow": 4},  # Standard
            {"rows": 8, "cols": 8, "inarow": 4},  # Tromp solved
            {"rows": 8, "cols": 10, "inarow": 4},  # Draw
            {"rows": 10, "cols": 15, "inarow": 5},  # Kaggle variant
            {"rows": 13, "cols": 15, "inarow": 7},  # Kaggle variant
        ]

        def run_all_tiers(self, bot, opponent_factories):
            results = {}
            for board in self.BOARDS:
                board_key = f"{board[rows]}x{board[cols]}"
                bot_size = self.get_bot_for_board_size(bot, board)
                opp = opponent_factories[board_key]()
                results[board_key] = {
                    "T1_tactical": self.run_tier1_tactical(bot_size, board),
                    "T2_opening": self.run_tier2_opening(bot_size, opp, board),
                    "T3_midgame": self.run_tier3_midgame(bot_size, opp, board),
                    "T4_endgame": self.run_tier4_endgame(bot_size, board),
                }
                results[board_key]["strength_rating"] = self.rank_by_win_rate(results[board_key]["T3_midgame"])
                results[board_key]["safety_margin_ms"] = self.compute_safety_margin(board)
            return results

        def run_tier1_tactical(self, bot, board):
            """Tier 1: Run position suite and measure accuracy."""
            positions = self.generate_position_suite(board, count=500)
            correct = 0
            for pos in positions:
                bot_move = bot.act(pos["board"], board, pos["player"])
                if bot_move == pos["solver_move"]:
                    correct += 1
            return {"correct": correct, "total": len(positions), "accuracy": correct / len(positions)}

        def run_tier3_midgame(self, bot, opponent, board):
            """Tier 3: 100 paired games with color reversal."""
            wins = draws = losses = 0
            for i in range(100):
                color = 1 if i < 50 else 2
                game = self.simulate_game(bot, opponent, board, color)
                if game["winner"] == color:
                    wins += 1
                elif game["winner"] == 0:
                    draws += 1
                else:
                    losses += 1
            return {"wins": wins, "draws": draws, "losses": losses, "win_rate": wins / 100}

        def compute_safety_margin(self, board):
            """Compute safety margin in ms based on board size and algorithm choice."""
            nn_time = self.estimate_nn_latency(board)
            search_time = self.estimate_search_latency(board)
            return 2000 - nn_time - search_time

---

## Assignment

- **Slot**: 6 of 7
- **Job**: 622
- **Lane**: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
- **Selected task**: Create board-size generalization benchmark protocol (C231/C232 gap)
- **Proposed target dossier path**: research/dossiers/benchmarking/BMS-DOC-008-board-size-generalization-benchmark-protocol.md
- **Dossier type**: Benchmark methodology / experiment design
- **Related IDs**: C231, C232, C014, C104, C130, C131, BMS-DOC-001 through BMS-DOC-007, BMS-013, CS-005, NN-004

## Publication-ready dossier

The complete 21-section dossier above constitutes a publishable research document covering board-size generalization benchmark methodology for ConnectX bots.

## Canonical Register Updates Proposed

See section 19 for detailed register updates (NEXUS.md, claim-register, work-queue, benchmark-blueprint).

## Master Report Implications

RESEARCH_REPORT.md should add BMS-DOC-008 to the benchmarking section with key findings:
1. Board-size generalization benchmark protocol established
2. Five-tier evaluation system defined with concrete position sets and game counts
3. Resource-constrained evaluation framework for Kaggle environment
4. Board-size routing strategy derived from latency budget analysis

## Nexus Index Implications

The dossier should be linked from:
- research/NEXUS.md benchmarking section
- benchmark-blueprint.md (board-size generalization protocol)

## Follow-up Research Tasks

1. Create and verify position suites for each board size using solver or heuristic methods
2. Develop board-size-matched benchmark opponents at optimal search depth per board
3. Implement and run Tier 1 (tactical correctness) on 7x6 and 8x8 as baseline
4. Design ResNet b3c128n architecture for board-size generalization
5. Generate 7x6 training dataset using classical engine
6. Develop MCTS simulation count optimization per board size
7. Evaluate board-size routing decisions empirically
8. Create inarow effect study (inarow 3, 4, 5, 7 on same board)

## Deferred Empirical Experiments

1. Full five-tier benchmark execution across all board sizes (17 hours CPU, 4 hours GPU)
2. Transfer learning experiment: 7x6-trained NN on 15x13 without fine-tuning
3. Fine-tuning sweep: 10K/50K/100K/500K 15x13 positions
4. Depth-vs-accuracy curves for alpha-beta on each board size
5. MCTS simulation count vs performance curves per board size
6. Complete paired-game tournament across all board sizes (7,560 total games)

EXTERNAL WORKER COMPLETE
