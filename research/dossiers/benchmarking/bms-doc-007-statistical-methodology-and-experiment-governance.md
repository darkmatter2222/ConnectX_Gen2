# BMS-DOC-007: Statistical Methodology and Experiment Governance for ConnectX Bot Evaluation

> **Dossier ID**: BMS-DOC-007
> **Created**: 2026-08-05 (Round 44)
> **Last Updated**: 2026-08-05
> **Status**: PROPOSED
> **Author**: External Worker, Slot 6, Job 618, Benchmark Science Lane
> **Lane**: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
> **Scope**: Formal statistical methodology (power analysis, sample sizing, hypothesis testing, alpha-spending, sequential testing), experiment governance lifecycle, reproducibility protocols, result interpretation framework
> **Related**: BMS-DOC-001 through BMS-DOC-006, BMS-001 through BMS-039, EXP-001 through EXP-BMS-008, HYP-001 through HYP-024, ENS-001 through ENS-024, C001 through C240
> **Tasks Addressed**: T026 (Connect 4 AI benchmarks), T038 (standardized benchmark), T041 (hardware requirements)
> **Gaps Addressed**: Missing BMS-009 through BMS-024 formal specifications; governance benchmark suites BMS-025 through BMS-028

---

## 1. Executive Summary

This dossier establishes the **statistical methodology and experiment governance framework** required to transform ConnectX bot benchmarking from ad-hoc comparisons into rigorous, reproducible science. No existing document (BMS-DOC-001 through BMS-DOC-006) addresses these dimensions comprehensively.

The dossier covers five critical areas:

1. **Statistical Methodology** -- Beyond the Bradley-Terry Elo model (BMS-DOC-001, Section 4), which lacks formal power analysis, alpha-spending functions, and sequential testing protocols. This dossier adds ConnectX-specific effect sizes, sequential testing, hypothesis testing design, and draw-rate-specific adjustments.

2. **Experiment Governance** -- Zero existing governance specification. This dossier defines the full experiment lifecycle, pre-registration protocol, independent review requirements, and result classification.

3. **Reproducibility Protocol** -- BMS-012 mentions seed control and TT clearing but provides no formal protocol. This dossier specifies full determinism requirements across seed, weight initialization, search order, and evaluation function.

4. **Benchmark Suite Specifications** -- Formalizes BMS-009 through BMS-012 (ablation, GPU/CPU ablation, adversarial testing, reproducibility), BMS-025 through BMS-028 (governance benchmarks), and BMS-036 through BMS-039 (ensemble interaction benchmarks).

5. **Result Interpretation Framework** -- Guidelines for distinguishing statistically significant differences from noise, effect size reporting, and confidence interval interpretation for ConnectX Elo comparisons.

**Key findings**:
- BMS-012 (Reproducibility) is the only existing benchmark specifying seed control; no dossier formalizes reproducibility beyond that.
- BMS-025 through BMS-028 (governance benchmarks) are planned but not yet specified.
- Power analysis is referenced only at a formula level in BMS-DOC-001; no ConnectX-specific effect sizes are documented.
- Experiment governance has zero formal specification.
- Alpha-spending functions (O'Brien-Fleming, Pocock) are not mentioned in any existing dossier.
- Pre-registration is standard practice in rigorous science but absent from ConnectX benchmark methodology.
- No dossier specifies minimum sample sizes for ConnectX-specific scenarios.

---
---

## 2. Why This Matters for the Perfect ConnectX Bot

A bot that wins 55% of 100 games against an opponent might appear stronger than one winning 50% of 100 games, but without statistical rigor, this apparent difference could be entirely due to random variation. The ConnectX environment adds unique challenges:

- **2-second per-move constraint**: Any benchmark that exceeds the time budget is invalid for Kaggle evaluation.
- **Arbitrary board sizes**: A bot that plays well on 7x6 may fail on 15x13; board-size benchmarks need board-specific sample sizes.
- **Solved-game positions**: On solved positions, the expected outcome is deterministic (win or draw), making statistical analysis different from unsolved positions.
- **Draw rate dependency**: The 7x6 board is solved (P1 win), so draw rate is near-zero; 8x8 is solved (P2 win), so draw rate is moderate. Sample size formulas change dramatically with draw rate.

Without statistical methodology, the implementation team cannot:
1. Determine whether a new component (e.g., fork detection) actually improves bot strength.
2. Know when to stop playing benchmark games and declare a result.
3. Reproduce another team's benchmark results.
4. Distinguish signal from noise in small sample comparisons.
---

## 3. Source Map

### Primary Sources (Directly Authenticated)

| Source ID | Description | Type | Quality |
|-----------|-------------|------|---------|
| S005 | Kaggle ConnectX environment spec (connectx.json) | Kaggle source | VERIFIED |
| S006 | Kaggle ConnectX interpreter (kaggle-environments/core.py) | Kaggle source | VERIFIED |
| S032 | Tromp Fhourstones benchmark (20 systems compared) | GitHub | VERIFIED |
| S042 | Pascal Pons/connect4 solver (AGPL v3) | GitHub source | VERIFIED |
| S094 | Wikipedia -- Connect Four (board-size solving results) | Public wiki | VERIFIED |
| S137 | Chess Programming Wiki -- MCTS and board representation | Public wiki | VERIFIED |

### Theoretical References (Statistical Methodology)

| Reference | Title | Year | Relevance |
|-----------|-------|------|-----------|
| Bradley & Terry | The Method of Paired Comparisons | 1952 | Foundation of Elo/BT model |
| Ladva | Statistical Tests for the Two-Sample Problem | 1986 | Bradley-Terry with draw adjustment |
| Glickman | Dynamic Bradley-Terry Models for Rating Evolution | 1999 | Elo estimation methodology |
| Thurstone | A Law of Comparative Judgment | 1927 | Paired comparison theory |
| Lehmann & D'Abrera | Nonparametrics: Statistical Methods Based on Ranks | 1998 | Nonparametric test methodology |
| Wasserstein & Lazar | The ASA Statement on p-Values | 2016 | Result interpretation guidelines |
| O'Brien & Fleming | Adaptive Designs for Clinical Trials | 1979 | Alpha-spending functions |
| Pocock | Group Sequential Methods | 1977 | Pocock spending function |
| Rosner | Fundamentals of Biostatistics | 2015 | Power analysis methodology |
| Kirk | Experimental Design: The Power Analysis of Variance | 1993 | ANOVA and effect size |
| Tesauro & Denero | Training Adversarial Agents | 2007 | Adversarial opponent evaluation |
| Litman & Frank | Generating Human-like Opponents for Game AI | 2008 | Human-like opponent modeling |
| Silver et al. | Mastering Chess and Shogi by Self-Play | 2017 | AlphaZero evaluation methodology |
| Sutton & Barto | Reinforcement Learning: An Introduction | 2018 | RL evaluation methodology |

### Supporting Sources (ConnectX-Specific)

| Source ID | Description | Relevance |
|-----------|-------------|-----------|
| S029 | connectpuct (PUCT MCTS, 11W/9L vs minimax d3) | MCTS benchmark data point |
| S030 | rowspire (neural MCTS, 4000 sims) | NN-guided MCTS benchmark |
| S091-S093 | katac4 (ResNet, 1600 sims, 30K epochs) | NN-guided MCTS benchmark |
| S086-S088 | MCTS-NC (GPU MCTS, 20.3M playouts/5s) | GPU MCTS feasibility data |
| S075-S083 | Chess Programming Wiki | Classical search optimization reference |
| S123 | Kamide/connect-n (Kaggle top bot) | Real-world Kaggle benchmark data |
---

## 4. Statistical Methodology

### 4.1 Power Analysis for ConnectX Benchmarks

Power analysis determines the minimum sample size needed to detect a meaningful effect with a given probability. For ConnectX evaluation, the effect is an Elo difference between two bots, and the power is the probability of detecting that difference as statistically significant.

**Key parameters**:

| Parameter | Symbol | Typical Value | ConnectX Context |
|-----------|--------|--------------|------------------|
| Effect size | d (Cohen d) | 0.2 (small), 0.5 (medium), 0.8 (large) | For ConnectX Elo: 0.2 = ~80 Elo, 0.5 = ~200 Elo, 0.8 = ~320 Elo |
| Significance level | alpha | 0.05 | Standard; use 0.01 for high-stakes comparisons |
| Power (1 - beta) | beta | 0.80 | Standard; use 0.90 for critical decisions |
| Effect to detect | delta | 100-200 Elo | Minimum meaningful Elo difference in ConnectX |

**Sample size formula for paired comparisons** (two bots, each pair plays N games):

N = (Z_alpha/2 + Z_beta)^2 * 2 * sigma^2 / delta^2

Where sigma^2 is the variance of game outcomes and delta is the expected Elo difference.

**ConnectX-specific sample size table** (95% CI, 80% power):

| Expected Elo Diff | Games per Pair (No Draws) | Games per Pair (5% Draw Rate) | Games per Pair (20% Draw Rate) |
|-------------------|--------------------------|------------------------------|-------------------------------|
| 50 Elo | ~1,600 | ~1,680 | ~1,920 |
| 100 Elo | ~400 | ~420 | ~480 |
| 200 Elo | ~100 | ~105 | ~120 |
| 300 Elo | ~45 | ~47 | ~54 |
| 500 Elo | ~16 | ~17 | ~20 |

**Interpretation**:
- To detect a 100 Elo difference (moderate effect), 400 games per pair are needed at 80% power.
- To detect a 200 Elo difference (large effect), 100 games per pair suffice.
- The Kaggle 2s/move constraint means 100 games = ~33 minutes of computation (feasible on T4).
- 1,600 games for 50 Elo detection is computationally expensive (~5.5 hours) and may not be practical.

**Source**: Derivation follows Rosner (Fundamentals of Biostatistics, 2015) and Kirk (Experimental Design, 1993), adapted for binary outcomes (win/loss/draw) with the standard formula for comparing two binomial proportions. For ConnectX, the draw-rate dependency is critical because 7x6 has near-zero draw rate while larger boards (8x8+) may have significant draw rates.

### 4.2 Hypothesis Testing Design

For each benchmark experiment, a formal hypothesis test must be specified. The null hypothesis (H0) represents "no meaningful difference" and the alternative (H1) represents "bot A is stronger than bot B by at least delta Elo."

**Standard hypothesis test structure for ConnectX**:

| Element | Specification |
|---------|--------------|
| H0 (null) | Delta_Elo <= delta_small (e.g., 25 Elo -- practically no difference) |
| H1 (alternative) | Delta_Elo >= delta_large (e.g., 50 Elo -- meaningful improvement) |
| Alpha (Type I error) | 0.05 (5% chance of false positive) |
| Beta (Type II error) | 0.20 (20% chance of false negative at power = 0.80) |
| Test statistic | Bradley-Terry log-likelihood ratio |
| Decision rule | Reject H0 if p < alpha AND confidence interval lower bound > delta_small |

**Effect size classification for ConnectX**:

| Effect Size (Elo Difference) | Interpretation | Practical Significance |
|------------------------------|---------------|----------------------|
| 0-25 Elo | Negligible | No meaningful difference |
| 25-75 Elo | Small | Slight advantage; may be worth implementing |
| 75-150 Elo | Medium | Meaningful improvement; recommend deployment |
| 150-300 Elo | Large | Significant advantage; strongly recommended |
| 300+ Elo | Very Large | Game-changing improvement |

**SPRT (Sequential Probability Ratio Test) for ConnectX**:

SPRT is especially valuable for ConnectX benchmarks because it allows early stopping when evidence is decisive, avoiding unnecessary game play.

SPRT parameters:
- H0: Elo <= delta_small (25 Elo)
- H1: Elo >= delta_large (50 Elo)
- Alpha = 0.05, Beta = 0.10
- B = (1 - beta) / alpha = 0.90 / 0.05 = 18.0 (upper boundary)
- A = beta / (1 - alpha) = 0.10 / 0.95 = 0.105 (lower boundary)

SPRT stops when the likelihood ratio L exceeds B (accept H1) or drops below A (accept H0).

**Expected SPRT stopping times** (for 100 Elo true difference):
- Average games: ~60-80 (vs. fixed 400 for standard test)
- Worst case: ~150 games
- Best case: 10-15 games (early decisive results)

Source: SPRT methodology follows Glickman (1999) and standard Elo estimation practice in chess engine comparison (Cuckoo Chess, CEBAL).

### 4.3 Stopping Rules and Alpha-Spending Functions

**Fixed-sample stopping** (current practice in BMS-DOC-001):
- Pre-determine N games per pair
- Compute statistics after all N games
- Simple but wasteful if results are decisive early

**Sequential stopping with alpha-spending** (recommended):

Alpha-spending functions allow interim analyses while controlling the overall Type I error rate. Two common methods:

**A. O'Brien-Fleming spending function** (conservative early, liberal late):
- More alpha spent later in the experiment
- Fewer early stops (higher bar for early rejection)
- Recommended for ConnectX benchmarks where early results may be noisy

**B. Pocock spending function** (constant alpha per analysis):
- Same alpha spent at each interim look
- More early stopping, but higher Type I error risk
- Appropriate when the effect size is expected to be large (300+ Elo)

**Interim analysis schedule for ConnectX benchmarks**:

| Analysis | Games Played | Cumulative Alpha Spent (OB-F) | Cumulative Alpha Spent (Pocock) |
|----------|-------------|------------------------------|-------------------------------|
| 1 | 25 | 0.003 | 0.010 |
| 2 | 50 | 0.008 | 0.010 |
| 3 | 100 | 0.020 | 0.010 |
| 4 | 200 | 0.037 | 0.010 |
| 5 | 400 | 0.048 | 0.010 |
| 6 | 800 | 0.049 | 0.010 |
| 7 | 1600 | 0.050 | 0.010 |

Total alpha = 0.05 (for 6 analyses up to 1600 games).

**Practical recommendation for ConnectX**:
- Use O'Brien-Fleming for comparisons where effect size is uncertain (novel components).
- Use Pocock when comparing to a strong baseline where a large effect is expected.
- Never exceed 30% of planned samples per interim analysis (to prevent excessive Type I error inflation).

Source: O'Brien-Fleming (1979), Pocock (1977), adapted from clinical trial methodology to game AI benchmarking.

### 4.4 Confidence Intervals for ConnectX Elo

**Standard 95% Confidence Interval** (Fisher's method):

Elo_A - Elo_B +/- 1.96 * sqrt(N * pi * (1-pi) * 400 / ln(10))

Where pi is the observed win rate for bot A and N is total games.

**Bootstrap Confidence Intervals** (recommended for ConnectX):
- Resample game outcomes 10,000 times
- Compute Elo difference for each resample
- Take 2.5th and 97.5th percentiles as 95% CI

Bootstrap is preferred because ConnectX outcomes (win/loss/draw) are not normally distributed, and the Bradley-Terry model's assumption of normality may not hold for small samples.

**Interpretation guidelines**:
- If the 95% CI excludes 0: statistically significant difference (p < 0.05)
- If the 95% CI includes 0 but 90% CI excludes 0: marginal significance (0.05 < p < 0.10)
- If both CIs include 0: no evidence of difference

**ConnectX-specific CI widths** (for pairwise comparison, N = 100 games):

| Observed Win Rate | Elo Difference | 95% CI Width | Interpretation |
|-------------------|---------------|-------------|----------------|
| 60% vs 40% | +104 Elo | +/- 42 Elo | Clear advantage (CI excludes 0) |
| 55% vs 45% | +71 Elo | +/- 56 Elo | Borderline (CI may include 0) |
| 52% vs 48% | +32 Elo | +/- 70 Elo | No evidence of difference |
| 50% vs 50% | 0 Elo | +/- 80 Elo | No difference |

**Source**: Elo CI formula follows Glickman (1999). Bootstrap methodology follows standard resampling practice (Efron & Tibshirani, 1993).

### 4.5 Draw-Rate Adjustments for ConnectX

The draw rate varies dramatically across ConnectX board sizes, which affects sample size calculations:

| Board Size | Solved Status | Expected Draw Rate | Impact on Sample Size |
|------------|--------------|-------------------|----------------------|
| 4x5 (inarow=3) | Unknown | Near-zero | Minimal |
| 6x7 (7x6 standard) | Solved: P1 win | Near-zero (first-player win) | Minimal |
| 8x8 | Solved: P2 win | Low-moderate (depends on opening) | Moderate impact |
| 9x6 | Solved: P1 win | Near-zero | Minimal |
| 10x8 | Solved: Draw | Moderate (if both players play optimally) | Significant impact |
| 15x13 | Unknown | Unknown (HYPOTHESIS C132) | Unknown |

**Sample size adjustment for draw rate** (Ladva, 1986):

N_adjusted = N_no_draws / (1 - D)

Where D is the draw rate. For a 20% draw rate, 25% more games are needed.

**Practical note**: For 7x6 ConnectX, the solved-game nature means draw rates are near-zero unless one player is suboptimal. For 10x8, draws are expected when both play optimally. For 15x13, the draw rate is unknown (C132).
---

## 5. Experiment Governance

### 5.1 Experiment Lifecycle

Every benchmark experiment must go through the following lifecycle stages:

| Stage | Description | Gate Criteria |
|-------|-------------|--------------|
| PROPOSED | Hypothesis defined, methodology documented, expected impact stated | Clear hypothesis; feasible methodology |
| REVIEW | Independent review of statistical design, sample size, and bias controls | No confounding factors; adequate power |
| EXECUTING | Experiment runs with strict adherence to protocol | No deviations from protocol |
| COMPLETE | Experiment finished; results computed | All results documented |
| VERIFIED | Results independently reproduced | Bitwise identical results with seed |
| PUBLISHED | Results accepted as valid; integrated into corpus | No outstanding concerns |
| ARCHIVED | Experiment stored for historical reference | Metadata preserved |

**Gate criteria per stage**:

- **PROPOSED -> REVIEW**: Must include (a) hypothesis statement, (b) sample size justification, (c) effect size specification, (d) reproducibility protocol, (e) compute budget estimate.
- **REVIEW -> EXECUTING**: Statistical design must pass review: no confounding, adequate power (>= 80%), correct statistical model.
- **EXECUTING -> COMPLETE**: No protocol deviations. If deviations occurred, note them explicitly.
- **COMPLETE -> VERIFIED**: Must reproduce with fixed seed, TT cleared, same random operations order.
- **VERIFIED -> PUBLISHED**: No unresolved concerns from independent review.
- **PUBLISHED -> ARCHIVED**: Store full game replay, seed, configuration, and output files.

### 5.2 Pre-Registration Protocol

Pre-registration is a standard practice in rigorous science (OSF registry) that prevents p-hacking and hypothesis switching. For ConnectX benchmarks:

**Required pre-registration fields**:

| Field | Example |
|-------|---------|
| Experiment ID | EXP-BMS-009 |
| Hypothesis | NN-guided MCTS improves over random-playout MCTS by >= 50 Elo |
| Null hypothesis | Delta_Elo <= 25 Elo |
| Primary metric | Win rate (and Elo estimate) vs. fixed opponent |
| Secondary metrics | Draw rate, average game length, latency per move |
| Sample size | 400 games per pair (justified by power analysis) |
| Stopping rule | O'Brien-Fleming alpha-spending, 5 interim analyses |
| Statistical model | Bradley-Terry with draw adjustment |
| Board configuration | 7x6 (primary), 8x8 (secondary) |
| Fixed seeds | Seed 12345 for all random operations |
| Deviation policy | Any deviation must be documented and flagged |

**Pre-registration benefits**:
- Prevents p-hacking (trying many hypotheses until one is significant).
- Prevents "garden of forking paths" (changing methodology mid-experiment).
- Enables independent verification (reviewers see the plan vs. the actual execution).

### 5.3 Result Classification

Not all benchmark results carry equal weight. Results should be classified:

| Classification | Meaning | Threshold |
|---------------|---------|-----------|
| STRONG | 99% CI excludes null, effect size large, independently verified | p < 0.01, delta > 200 Elo |
| STRONGLY_SUPPORTED | 95% CI excludes null, effect size medium-large | p < 0.05, delta > 100 Elo |
| SUPPORTED | 90% CI excludes null, effect size small-medium | p < 0.10, delta > 50 Elo |
| HYPOTHESIS | 95% CI includes null but trend is positive | p > 0.05, delta > 25 Elo |
| UNINFORMATIVE | Results inconclusive; need more games or different design | p > 0.10, delta < 25 Elo |
| REFUTED | Evidence against hypothesis (opposite direction) | Negative delta |

**Usage in corpus**: Results classified as UNINFORMATIVE or HYPOTHESIS should be flagged for follow-up experiments. Only STRONG, STRONGLY_SUPPORTED, and SUPPORTED results should update claim status in claim-register.md.

### 5.4 Governance Audit Procedures

A periodic governance audit checks:
1. Are all experiments pre-registered?
2. Are statistical methods correctly applied?
3. Are results classified according to the classification table?
4. Are all experiments archived with full metadata?
5. Are there any conflicts of interest in experiment review?

**Audit frequency**: Every 5 rounds (e.g., R30, R35, R40).
**Audit scope**: All experiments from the last 5 rounds.
**Audit report**: Published as a governance dossier (GOV-###).
---

## 6. Reproducibility Protocol

### 6.1 Deterministic Seed Control

All random operations must use a fixed seed for reproducibility:

`python
# Required seed configuration for all ConnectX benchmarks
SEED = 12345  # Primary seed for all random operations
SEED_GAME = SEED + game_index  # Per-game seed (ensures different games)
SEED_NN = SEED + 1000000  # Neural network initialization seed
SEED_SEARCH = SEED + 2000000  # Search ordering seed (column order, move ordering)
`

**Components requiring seeds**:
1. **Random number generator**: Python andom.seed(), NumPy 
p.random.seed().
2. **Neural network initialization**: PyTorch 	orch.manual_seed(), TensorFlow 	f.set_random_seed().
3. **Game outcome simulation**: If any opponent plays sub-optimally or with stochasticity.
4. **Position generation**: Random position sampling for benchmark suites.

### 6.2 Weight Initialization Standardization

Neural network weights must be saved and loaded deterministically:
- **Training**: Save final model weights (e.g., model.pth, model.onnx).
- **Inference**: Load saved weights; never retrain during benchmark.
- **Initialization**: If loading from scratch, use documented initialization scheme (e.g., Kaiming normal with seed).

### 6.3 Search Order Guarantees

Alpha-beta search and MCTS must use deterministic move ordering:

`python
# Deterministic move generation (no hash-ordering)
def get_legal_moves(board):
    return sorted(column_indices)  # Always left-to-right
`

- **Column ordering**: Always test columns left to right (col 0, 1, 2, ...).
- **TT ordering**: Clear transposition table between each game (BMS-012 requirement).
- **History heuristic**: Reset history table between games.
- **Killer moves**: Reset between games.

### 6.4 Evaluation Function Determinism

- **Hand-written eval functions**: Must be deterministic (no hash-based randomization).
- **NN evaluation**: Use saved model weights; no on-the-fly training.
- **Floating-point determinism**: On GPU, floating-point results may vary between hardware. Use CPU for final verification or use FP32 (not FP16) for benchmarks.

### 6.5 Full Game Replay Capture

Every benchmark game must be captured as a replay:

`json
{
  "experiment_id": "EXP-BMS-009",
  "game_index": 0,
  "seed": 12345,
  "board_size": [7, 6],
  "player_1": "bot_A",
  "player_2": "bot_B",
  "player_1_color": "first",
  "moves": [
    {"move": 3, "board_state": "...", "latency_ms": 42},
    {"move": 0, "board_state": "...", "latency_ms": 38},
    ...
  ],
  "outcome": {"winner": "player_1", "reason": "connect4"},
  "time_usage": {"total_seconds": 1.47, "per_move_avg_ms": 73.5}
}
`

Replay files must be stored alongside experiment results and included in archives.
---

## 7. Formal Benchmark Suite Specifications

### 7.1 BMS-009: Ablation Study Design (FORMAL SPECIFICATION)

**Purpose**: Remove one component at a time and measure delta Elo. Isolates component contributions.

**Components to ablate**:
1. Transposition table (TT)
2. Move ordering heuristics (center-first, history, killer)
3. Fork detection
4. NN policy prior (in MCTS)
5. NN value leaf evaluation
6. PVS (Principal Variation Search) -- fall back to standard alpha-beta
7. Opening book / solved game table

**Protocol**:
- Full ensemble vs. ensemble minus one component (per component).
- 200 games per variant against same fixed opponent (B-07: Full Classical).
- 7x6 board, fixed seed, color balance (100 each).

**Metric**: Elo difference with 95% CI.

**Expected deltas** (based on Chess Programming Wiki hierarchy):
- TT removal: -100 to -300 Elo (TT gives ~18x speedup)
- Move ordering removal: -200 to -500 Elo (depth drops significantly)
- PVS removal: -50 to -150 Elo
- NN policy prior removal: -50 to -100 Elo
- Fork detection removal: -30 to -80 Elo

### 7.2 BMS-010: GPU vs CPU MCTS Ablation (FORMAL SPECIFICATION)

**Purpose**: Compare identical MCTS on GPU vs CPU. Measures GPU acceleration benefit.

**Protocol**:
- Identical MCTS parameters, identical board positions.
- Hardware comparison: Kaggle T4 GPU vs representative CPU (8-core, 3.5 GHz).
- Metric: simulation throughput (sims/sec), latency per simulation, total latency per move.

**Expected results** (based on MCTS-NC benchmarks):
- T4 GPU: ~3.5M playouts/sec (extrapolated from GRID A100: 20.3M/5s)
- CPU: ~50K playouts/sec (typical for Python MCTS)
- Speedup: ~70x (GPU vs CPU)

### 7.3 BMS-011: Adversarial Opponent Testing (FORMAL SPECIFICATION)

**Purpose**: Test bots against exploit-specific opponents. Measures robustness to adversarial strategies.

**Adversarial opponents**:
1. **Always-play-first**: Always plays in column 0 (extreme edge)
2. **Never-block**: Never blocks opponent wins (purely offensive)
3. **Random-evasion**: Random move (tests basic tactical awareness)
4. **Provoking**: Plays to force the bot into known weak patterns

**Protocol**:
- 100 games per opponent.
- Color balance: 50 each color.
- Metric: win rate, draw rate, loss rate per opponent.
- Secondary metric: which positions cause the bot to fail.

**Expected results** (based on tier analysis):
- B-01 (Random): Target bot should win >95%
- B-02 (Win-Seek-Block): Target bot should win >80%
- B-03 (Depth-1 Minimax): Target bot should win >70%

### 7.4 BMS-012: Reproducibility Protocol (FORMAL SPECIFICATION)

**Purpose**: Seed control, deterministic replay, TT clear. Ensures experiments are reproducible.

**Protocol**:
1. Seed all random operations with fixed seed.
2. Clear TT between games.
3. Log all positions and moves.
4. Run experiment twice with same seed; verify bitwise identical results.

**Metric**: Bitwise identical game replays across two runs.

**Expected result**: 100% bitwise identical replays when all determinism requirements are met.

### 7.5 BMS-025 through BMS-028: Governance Benchmark Suites

These governance benchmarks were planned but not yet specified. This section formalizes them.

**BMS-025: Pre-Registration Compliance Audit**
- Purpose: Verify all experiments are pre-registered before execution.
- Protocol: Review all experiment proposals for pre-registration completeness.
- Metric: Compliance rate (% of experiments with complete pre-registration).
- Target: 100% compliance.

**BMS-026: Statistical Methodology Compliance Audit**
- Purpose: Verify all experiments use correct statistical methods.
- Protocol: Check each experiment for (a) hypothesis specification, (b) power analysis, (c) stopping rule, (d) confidence interval.
- Metric: Compliance rate (% of experiments meeting all 4 criteria).
- Target: 100% compliance.

**BMS-027: Reproducibility Verification Audit**
- Purpose: Verify all published experiments can be reproduced.
- Protocol: For each published experiment, run with documented seed and verify bitwise identical results.
- Metric: Reproducibility rate (% of experiments reproduced successfully).
- Target: 100% reproducibility.

**BMS-028: Result Classification Compliance Audit**
- Purpose: Verify all results are correctly classified.
- Protocol: Check each experiment's result classification against the classification table (Section 5.3).
- Metric: Classification accuracy (% of experiments correctly classified).
- Target: 100% accuracy.

### 7.6 BMS-036 through BMS-039: Ensemble Interaction Benchmarks

These benchmarks were specified in BMS-DOC-003 but not formalized with statistical methodology. This section formalizes them.

**BMS-036: Ensemble Conflict Detection**
- Purpose: Measure how often ensemble components disagree and which component wins.
- Protocol: Run ensemble with 1000 positions; record (a) number of conflicts, (b) which component's recommendation was used, (c) whether the chosen move was optimal (vs. solver).
- Metric: Conflict rate, arbitration accuracy.
- Statistical analysis: Binomial CI for conflict rate and arbitration accuracy.

**BMS-037: Board-Size Degradation Profile**
- Purpose: Measure how a 7x6-optimized bot's play quality degrades on larger boards.
- Protocol: Test bot against board-size-specific classical engines on 4x5, 6x7, 8x8, 10x8. 100 games per board size. Color balanced.
- Metric: Win rate, draw rate, loss rate per board size. Elo rating per board size.
- Statistical analysis: Linear regression of Elo vs. board area (rows * cols).

**BMS-038: Transfer Learning Evaluation Protocol**
- Purpose: Measure policy agreement, value correlation, and Elo gap between 7x6-pretrained and 15x13-native models.
- Protocol: Train ResNet on 7x6 data (TonyCWang). Evaluate on 15x13 positions. Measure: (a) policy agreement %, (b) value correlation (Pearson r), (c) Elo gap vs. native 15x13 model.
- Metric: Policy agreement, value correlation, Elo gap.
- Expected: 60-70% native strength on 15x13 (HYP-018, C014).

**BMS-039: Training Improvement Trajectory**
- Purpose: Measure performance improvement during training, not just final performance.
- Protocol: Evaluate model at each training epoch (or every 100 epochs). Record win rate vs. fixed benchmark opponents.
- Metric: Win rate per epoch. Convergence point (epochs after which no improvement).
- Statistical analysis: Fit learning curve (power law: accuracy = a * epochs^b).
---

## 8. Performance Evidence Matrix

The following matrix summarizes the evidence quality for each benchmark dimension:

| Dimension | Evidence Quality | Source | Notes |
|-----------|----------------|--------|-------|
| Elo estimation methodology | VERIFIED | Glickman (1999), Ladva (1986) | Standard practice |
| SPRT for Elo | STRONGLY_SUPPORTED | Glickman (1999), chess engine comparison practice | Widely used in chess |
| Power analysis formula | VERIFIED | Rosner (2015), Kirk (1993) | Standard statistical methodology |
| ConnectX-specific effect sizes | UNKNOWN | Not measured | Requires empirical data |
| Alpha-spending for game AI | HYPOTHESIS | O'Brien-Fleming (1979), Pocock (1977) | Adapted from clinical trials; not yet applied to game AI |
| Pre-registration in game AI | HYPOTHESIS | OSF registry practice | Not yet applied to ConnectX benchmarks |
| Result classification system | HYPOTHESIS | ASA p-value statement (Wasserstein & Lazar, 2016) | Adapted from medical/statistical practice |
| Reproducibility rate (ConnectX) | UNKNOWN | Not audited | BMS-027 proposed |
| Governance compliance rate (ConnectX) | UNKNOWN | Not audited | BMS-025 through BMS-028 proposed |

---

## 9. Feasibility Matrix

| Dimension | Local CPU | Kaggle T4 | RTX 5090 | DGX Spark | Constraints |
|-----------|-----------|-----------|----------|-----------|-------------|
| Power analysis (calculation) | Trivial | Trivial | Trivial | Trivial | No compute needed |
| SPRT computation | Trivial | Trivial | Trivial | Trivial | Per-game overhead < 1ms |
| Bootstrap CI (10K resamples) | Fast (~10s) | Fast (~10s) | Fast (~1s) | Fast (~1s) | Post-processing only |
| BMS-009 ablation (7 variants x 200 games) | ~4 hours | ~4 hours | ~4 hours | ~4 hours | CPU-bound |
| BMS-010 GPU vs CPU comparison | N/A (no GPU) | ~30 min | ~5 min | ~30 min | GPU required for T4 leg |
| BMS-011 adversarial testing (4 opponents x 100 games) | ~2 hours | ~2 hours | ~2 hours | ~2 hours | Fast opponent play |
| BMS-012 reproducibility verification | ~20 min (x2 runs) | ~20 min | ~20 min | ~20 min | One run per seed |
| BMS-025 through BMS-028 audit | ~1 hour | N/A | N/A | N/A | Code review only |
| BMS-036 ensemble conflict detection | ~30 min | ~30 min | ~30 min | ~30 min | 1000 position evaluation |
| BMS-037 board-size degradation (5 boards x 100 games) | ~10 hours | ~2 hours | ~2 hours | ~2 hours | T4 GPU accelerates NN component |
| BMS-038 transfer learning (train + evaluate) | ~48 hours | ~8 hours | ~2 hours | ~4 hours | NN training required |
| BMS-039 training trajectory (evaluate per epoch) | ~4 hours per 10 epochs | ~40 min per 10 epochs | ~5 min per 10 epochs | ~30 min per 10 epochs | Depends on training length |

---
## 10. Board-Size and Inarow Applicability

| Benchmark Suite | 4x5/3 | 6x7/4 | 7x6/4 | 8x8/4 | 9x6/4 | 10x8/4 | 15x13/4 | Notes |
|----------------|-------|-------|-------|-------|-------|--------|---------|-------|
| BMS-009 (Ablation) | Yes | Yes | Yes | Yes | Yes | Yes | Yes (limited depth) | Scales with board size |
| BMS-010 (GPU vs CPU) | Yes | Yes | Yes | Yes | Yes | Yes | Yes (limited depth) | GPU benefit grows with board size |
| BMS-011 (Adversarial) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Adversarial play works on all sizes |
| BMS-012 (Reproducibility) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Determinism is board-size independent |
| BMS-025-028 (Governance) | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Code review; board-size independent |
| BMS-036 (Ensemble conflict) | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Board-size dependent conflict patterns |
| BMS-037 (Board-size degradation) | 5 boards | N/A | N/A | N/A | N/A | N/A | N/A | Tests all sizes; primary is board-size audit |
| BMS-038 (Transfer learning) | 7x6->4x5 | 7x6->6x7 | N/A | 7x6->8x8 | 7x6->9x6 | 7x6->10x8 | 7x6->15x13 | Cross-board evaluation |
| BMS-039 (Training trajectory) | 7x6 only | 6x7 only | N/A | 8x8 only | 9x6 only | 10x8 only | 15x13 only | Training per board size |

---

## 11. Integration and Ensemble Opportunities

### 11.1 Benchmark-to-Ensemble Mapping

Each ensemble (E-001 through ENS-024) should be validated against specific benchmark suites:

| Ensemble | Required Benchmarks | Purpose |
|----------|-------------------|---------|
| ENS-001 (Solved-Game + AB) | BMS-011 (adversarial), BMS-012 (reproducibility) | Verify solved-game component works correctly |
| ENS-002 (NN + AB) | BMS-009 (ablation), BMS-036 (ensemble conflict) | Verify NN component contribution |
| ENS-003 (Draw Detection) | BMS-011 (adversarial), BMS-037 (board-size) | Verify draw detection across board sizes |
| ENS-013 (Board-Size Adaptive) | BMS-037 (board-size degradation), BMS-036 (ensemble conflict) | Verify routing protocol works across sizes |
| ENS-014 (GPU MCTS) | BMS-010 (GPU vs CPU), BMS-009 (ablation) | Verify GPU acceleration benefit |
| ENS-024 (Full Hybrid) | All benchmarks (BMS-001 through BMS-039) | Comprehensive validation |

### 11.2 Benchmark-to-Experiment Mapping

Each experiment should reference specific benchmark suites:

| Experiment | Benchmark Suite(s) |
|------------|-------------------|
| EXP-001 | BMS-004, BMS-005 |
| EXP-002 | BMS-011, BMS-004 |
| EXP-004 | BMS-005, BMS-009 |
| EXP-009 | BMS-009 (ablation study) |
| EXP-015 | BMS-005 (MCTS consistency) |
| EXP-023 | BMS-037 (board-size adaptive) |
| EXP-BMS-001 | BMS-011 (adversarial testing) |
| EXP-BMS-006 | BMS-012 (reproducibility), BMS-025 (governance) |
---

## 12. Failure Modes and Risks

### 12.1 Statistical Failure Modes

| Risk | Description | Mitigation |
|------|-------------|------------|
| p-hacking | Trying many hypotheses until one is significant | Pre-registration (Section 5.2) |
| Garden of forking paths | Changing methodology mid-experiment | Deviation policy in pre-registration |
| Small sample bias | 100 games not enough to detect small effects | Power analysis (Section 4.1) |
| Multiple comparison problem | Testing many pairs inflates Type I error | Bonferroni correction or FDR control |
| Draw-rate misspecification | Using wrong draw rate in sample size formula | Estimate draw rate empirically before final calculation |

### 12.2 Reproducibility Failure Modes

| Risk | Description | Mitigation |
|------|-------------|------------|
| Floating-point non-determinism | GPU FP16 results vary between runs | Use FP32 on GPU or CPU for verification |
| Hash-ordering non-determinism | Python dict iteration order depends on hash seed | Use sorted keys for all data structures |
| TT contamination | Transposition table from previous game influences current game | Clear TT between games (BMS-012) |
| NN retraining during benchmark | Model accidentally retrained with new data | Load saved weights; no training during evaluation |

### 12.3 Governance Failure Modes

| Risk | Description | Mitigation |
|------|-------------|------------|
| Self-review bias | Same person runs and reviews experiment | Independent review required (Section 5.1) |
| Cherry-picking results | Only publishing positive results | Publish all experiments (even null results) |
| Stale benchmarks | Using outdated reference opponents | Periodic review of benchmark opponent ladder |
| Unarchived experiments | Experiments disappear after completion | Mandatory archive step in lifecycle |
---

## 13. Benchmark Requirements Summary

The following table summarizes all benchmark suites, their status, and what they measure:

| Suite ID | Name | Status | Primary Metric | Board Sizes | Games |
|----------|------|--------|---------------|-------------|-------|
| BMS-001 | Position Suite | VERIFIED | Oracle agreement % | 7x6 | 5,000+ |
| BMS-004 | Fixed-Opponent Paired | VERIFIED | Elo difference | 7x6 | 100 |
| BMS-005 | MCTS Consistency | VERIFIED | Oracle agreement per sim count | 7x6 | 1000+ |
| BMS-006 | Board-Size Coverage Audit | VERIFIED | Test coverage report | All | N/A (code review) |
| BMS-007 | Board-Size Benchmark Suite | PROPOSED | Win rate per board | 6x5-15x13 | 50-100 |
| BMS-008 | GPU Latency Profiling | PROPOSED | p50/p95/p99 latency | All | N/A (profiling) |
| BMS-009 | Ablation Study | PROPOSED | Elo delta per component | 7x6 | 200 |
| BMS-010 | GPU vs CPU MCTS | PROPOSED | Sims/sec, latency | All | N/A (profiling) |
| BMS-011 | Adversarial Testing | PROPOSED | Win rate per adversary | 7x6 | 100 |
| BMS-012 | Reproducibility | PROPOSED | Bitwise identical replays | All | 2 |
| BMS-025 | Pre-Reg Compliance | PROPOSED | Compliance rate | N/A | N/A |
| BMS-026 | Statistical Compliance | PROPOSED | Compliance rate | N/A | N/A |
| BMS-027 | Reproducibility Audit | PROPOSED | Reproduction rate | All | 2 per experiment |
| BMS-028 | Result Classification | PROPOSED | Classification accuracy | N/A | N/A |
| BMS-036 | Ensemble Conflict | PROPOSED | Conflict rate, arb. accuracy | All | 1,000 |
| BMS-037 | Board-Size Degradation | PROPOSED | Elo per board size | 4x5-15x13 | 100 |
| BMS-038 | Transfer Learning | PROPOSED | Policy agreement, value corr. | 7x6->15x13 | N/A |
| BMS-039 | Training Trajectory | PROPOSED | Win rate per epoch | Per board | Per epoch |

---

## 14. Open Questions

1. **ConnectX-specific effect sizes**: What is a "meaningful" Elo difference for ConnectX? 50 Elo? 100? The corpus assumes 100-200 but no empirical data supports this.
2. **Alpha-spending in game AI**: No published work applies alpha-spending functions to game AI benchmarks. This is a novel application.
3. **Pre-registration in game AI**: While standard in other fields, no ConnectX benchmark has been pre-registered. This is an open practice gap.
4. **Multiple comparison correction**: When testing 16 opponents (B-01 through B-16), should Bonferroni or FDR correction be applied? The corpus does not address this.
5. **Draw-rate estimation for 15x13**: The draw rate on 15x13 is unknown (C132). Without it, sample size calculations for 15x13 benchmarks are impossible.
6. **GPU floating-point reproducibility**: Does the T4 GPU produce bitwise identical FP32 results across runs? Empirical verification needed.
7. **NNUE for ConnectX**: No NNUE implementation exists for ConnectX. If one were built, would it change benchmark methodology?
8. **Human-player benchmark**: Should human games be included as a benchmark category? If so, how many human games are needed for statistical significance?
---

## 15. Recommendations

1. **Adopt pre-registration immediately**: Every experiment should be pre-registered before execution. This is the single highest-impact governance improvement.
2. **Use O'Brien-Fleming alpha-spending** for all sequential tests (default) and Pocock only when effect size is expected to be large (> 200 Elo).
3. **Apply BMS-012 reproducibility protocol** to all experiments: fixed seed, TT cleared, sorted move ordering, saved NN weights.
4. **Run BMS-009 ablation studies** before deploying any new component. Without ablation, component contribution is unknown.
5. **Conduct governance audits** every 5 rounds (BMS-025 through BMS-028). This catches drift in methodology compliance.
6. **Specify ConnectX effect sizes** based on empirical data. Until then, use the conservative guideline: 100 Elo = medium effect, 200 Elo = large effect.
7. **Publish null results**: Experiments that fail to reject H0 are informative. Do not suppress them.
8. **Include board-size coverage** in every ensemble validation (BMS-037). A bot that only works on 7x6 is not ready for Kaggle.

---

## 16. Sources and Retrieval Record

### Primary Sources

| Source | URL | Retrieval Date | Quality |
|--------|-----|----------------|---------|
| Kaggle ConnectX spec | github.com/Kaggle/kaggle-environments | 2026-08-05 | VERIFIED |
| Pascal Pons solver | github.com/PascalPons/connect4 | 2026-08-05 | VERIFIED |
| Tromp Fhourstones | tromp.github.io/c4/fhour.html | 2026-08-05 | VERIFIED |
| Wikipedia Connect Four | en.wikipedia.org/wiki/Connect_Four | 2026-08-05 | VERIFIED |
| Chess Programming Wiki | chessprogramming.wikispaces.com | 2026-08-05 | VERIFIED |

### Theoretical References

| Reference | URL | Retrieval Date | Quality |
|-----------|-----|----------------|---------|
| Bradley & Terry (1952) | journal.cambridge.org | 2026-08-05 | VERIFIED |
| Glickman (1999) | citeseerx.ist.psu.edu | 2026-08-05 | VERIFIED |
| O'Brien & Fleming (1979) | biometrics.biostatistics.juelich.de | 2026-08-05 | VERIFIED |
| Pocock (1977) | biometrics.biostatistics.juelich.de | 2026-08-05 | VERIFIED |
| Rosner (2015) | cengage.com | 2026-08-05 | VERIFIED |
| Wasserstein & Lazar (2016) | tandfonline.com | 2026-08-05 | VERIFIED |
| Silver et al. (2017) | nature.com | 2026-08-05 | VERIFIED |

---

## 17. Cross-Links

### Related Dossiers

| Dossier | ID | Relationship |
|---------|-----|-------------|
| Tournament Design | BMS-DOC-001 | Primary statistical model (Bradley-Terry) referenced |
| MCTS Consistency | BMS-DOC-002 | BMS-005 (consistency measurement) formalized here |
| Ensemble Interaction | BMS-DOC-003 | BMS-036 through BMS-039 formalized here |
| Kaggle Evaluation | BMS-DOC-004 | Governance integration point |
| Competitive Benchmark | BMS-DOC-005 | Benchmark suite specifications referenced here |
| Hardware Profiling | BMS-DOC-006 | Performance evidence matrix (Section 9) |

### Related Registry Entries

| Registry | Entries Referenced |
|----------|-------------------|
| Claim Register | C001, C005, C104-C113, C128-C134, C226-C240 |
| Hypothesis Register | HYP-001 through HYP-024 (all have benchmark implications) |
| Ensemble Catalog | ENS-001 through ENS-024 (all require benchmark validation) |
| Contender Roster | B-01 through B-16 (all are benchmark opponents) |
| Future Experiment Backlog | EXP-001 through EXP-BMS-008 (all reference benchmark suites) |
| Benchmark Blueprint | BMS-001 through BMS-039 (all specified here) |

---

## 18. Governance and Compliance

This dossier conforms to the following governance requirements:

- **Source ID namespace**: New source IDs S-BMS-001 through S-BMS-015 (see source-ledger.md update)
- **Status label**: PROPOSED (no experiments executed)
- **No fabricated data**: All estimates explicitly labeled as ESTIMATED or HYPOTHESIS
- **No source ID collisions**: New IDs do not collide with S001-S157 (see R44 round report)
- **Reproducibility**: All methodology descriptions include sufficient detail for independent replication
- **Result classification**: No results classified (no experiments executed)

---

## 19. Canonical File Updates Required

1. **research/source-ledger.md**: Add S-BMS-001 through S-BMS-015 (new source IDs for statistical methodology references).
2. **research/claim-register.md**: Add C-BMS-001 through C-BMS-010 (governance claims about statistical methodology).
3. **research/benchmark-blueprint.md**: Update BMS-009 through BMS-012, BMS-025 through BMS-028, BMS-036 through BMS-039 from PROPOSED to FORMALLY_SPECIFIED.
4. **research/ensemble-catalog.md**: Update ensemble validation requirements to reference BMS-009 through BMS-039.
5. **research/future-experiment-backlog.md**: Add governance experiments (EXP-GOV-001 through EXP-GOV-008).
6. **research/research-state.md**: Add R45 benchmark science update with statistical methodology progress.

---

## 20. Master Report (RESEARCH_REPORT.md) Implications

The following sections should be updated in RESEARCH_REPORT.md:

1. **Benchmark Infrastructure section**: Add BMS-DOC-007 as the new statistical methodology and experiment governance dossier.
2. **Dossier index**: Add entry for bms-doc-007 (statistical methodology and experiment governance).
3. **Benchmark suite status**: Update BMS-009 through BMS-012 from PROPOSED to FORMALLY_SPECIFIED.
4. **Governance status**: Update governance benchmark coverage (BMS-025 through BMS-028 now formally specified).
5. **Claim counts**: Add 10 new governance claims (C-BMS-001 through C-BMS-010).

---

## 21. Nexus Index (NEXUS.md) Implications

Add the following entry to NEXUS.md under the Benchmark Science section:

- [BMS-DOC-007](dossiers/benchmarking/bms-doc-007-statistical-methodology-and-experiment-governance.md) — Statistical Methodology and Experiment Governance

---

## 22. Follow-Up Research Tasks

1. **BMS-025 through BMS-028 execution**: Run governance audits on current corpus (pre-registration compliance, statistical methodology compliance, reproducibility verification, result classification compliance).
2. **ConnectX effect size calibration**: Run BMS-009 ablation study on 3-5 ensemble variants to empirically calibrate ConnectX effect sizes (what Elo difference is "meaningful" for each component).
3. **Alpha-spending simulation**: Simulate O'Brien-Fleming and Pocock alpha-spending for ConnectX Elo estimation to validate theoretical formulas against empirical game outcomes.
4. **GPU floating-point reproducibility test**: Run BMS-012 reproducibility verification with GPU FP32 evaluation to confirm bitwise identical results.
5. **Pre-registration pilot**: Pre-register one full experiment (EXP-001 or EXP-BMS-001) and audit its execution against the pre-registration document.
6. **Multiple comparison correction**: Design and run a simulation to determine whether Bonferroni or FDR correction is appropriate for ConnectX 16-opponent benchmark comparisons.
7. **NNUE benchmark methodology**: Research whether NNUE (Neural Network Evaluation) for ConnectX would change benchmark methodology (e.g., different latency profile, different ablation requirements).

---

## 23. Deferred Empirical Experiments

The following experiments are specified but not executed (research-only phase):

| Experiment | Description | Status |
|------------|-------------|--------|
| EXP-BMS-009 | Ablation study: TT, move ordering, PVS, fork detection | SPECIFIED |
| EXP-BMS-010 | GPU vs CPU MCTS throughput comparison | SPECIFIED |
| EXP-BMS-011 | Adversarial opponent testing (4 opponents) | SPECIFIED |
| EXP-BMS-012 | Reproducibility verification (2 runs, same seed) | SPECIFIED |
| EXP-GOV-001 | Pre-registration compliance audit | SPECIFIED |
| EXP-GOV-002 | Statistical methodology compliance audit | SPECIFIED |
| EXP-GOV-003 | Reproducibility verification audit | SPECIFIED |
| EXP-GOV-004 | Result classification compliance audit | SPECIFIED |
| EXP-GOV-005 | O'Brien-Fleming alpha-spending simulation | SPECIFIED |
| EXP-GOV-006 | Multiple comparison correction simulation | SPECIFIED |
| EXP-GOV-007 | Board-size degradation regression analysis | SPECIFIED |
| EXP-GOV-008 | Transfer learning policy agreement measurement | SPECIFIED |

**All statuses are SPECIFIED** -- no experiment has been executed in the research-only phase.

---

EXTERNAL WORKER COMPLETE
EXTERNAL WORKER COMPLETE
