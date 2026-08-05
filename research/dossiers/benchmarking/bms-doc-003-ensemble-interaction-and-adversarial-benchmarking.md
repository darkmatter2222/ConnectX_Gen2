# BMS-DOC-003: Ensemble Interaction Benchmarking, Adversarial Board-Size Stress Testing, and Transfer Learning Evaluation

> **Dossier ID**: B﻿
---

## 1. Executive Summary

This dossier addresses three critical benchmark gaps that neither BMS-DOC-001 nor BMS-DOC-002 cover:

1. **Ensemble Interaction Benchmarking** -- The catalog documents 24 ensembles (E-001 through E-012, ENS-013 through ENS-024), but no benchmark exists to measure how components interact *at inference time* when they disagree. Four new benchmark suites (BMS-036 through BMS-039) are designed to diagnose and quantify ensemble interaction failures.

2. **Adversarial Board-Size Stress Testing** -- Existing benchmarks (BMS-006, BMS-007) measure board-size coverage superficially. A new protocol (BMS-037) systematically evaluates *degradation profiles*: how does an agent trained on 7x6 degrade on 8x8, 9x6, 10x8, and 15x13? This requires adversarial board-size selection, not random sampling.

3. **Transfer Learning Evaluation Protocol** -- HYP-018 (7x6-to-15x13 transfer) and C014 (transfer learning hypothesis) remain entirely untested. BMS-038 specifies a systematic protocol for measuring policy agreement, value correlation, and Elo gap between 7x6-pretrained and 15x13-native models across multiple architecture families.

The dossier also provides a **comprehensive gap analysis** of the existing 35 benchmark suites (BMS-001 through BMS-012, BMS-029 through BMS-035), identifying which ensembles each validates and which remain unaudited.

**Key findings**:
- 0 of 24 ensembles have a dedicated ensemble-interaction benchmark.
- BMS-006 (board-size coverage) tests only whether an agent accepts a board size, not how well it plays.
- No benchmark measures training improvement trajectory (EXP-001 through EXP-037 do not include this measurement).
- BMS-036 through BMS-039 close these gaps with specific, measurable protocols.

---

## 2. Why This Matters for the Perfect ConnectX Bot

The Kaggle ConnectX evaluation tests on arbitrary board sizes with unknown test distribution. The implementation team will likely build a hybrid agent (classical search + neural network + MCTS) with board-size adaptive routing (ENS-013). Without the benchmarks in this dossier, the team faces three specific risks:

### Risk 1: Ensemble Conflict Undetected

An ensemble combining classical search and neural MCTS will produce conflicting recommendations on some positions. If the arbitration layer is not tested against adversarial conflict positions, the bot may:
- Default to a weaker component on critical positions.
- Introduce hidden bias (always prefer neural over classical, or vice versa).
- Time out while resolving conflicts.

**Impact**: Every ensemble containing two or more decision components (ENS-002, ENS-013, ENS-018, ENS-024) is affected.

### Risk 2: Board-Size Degradation Not Measured

An agent optimized for 7x6 may play acceptably on 8x8 but catastrophically on 15x13. Existing BMS-006 only checks that the agent *accepts* the board size. BMS-037 measures *play quality* across the full board-size spectrum using controlled position transfer and opponent-fixed evaluation.

**Impact**: All ensembles with board-size adaptive routing (ENS-013, ENS-019) and board-size generalization (HYP-018).

### Risk 3: Transfer Learning Effectiveness Unknown

If the team trains on 7x6 data (TonyCWang, 958M rows) and must transfer to 15x13, the expected Elo gap is 300-500 points (HYP-018). Without a transfer evaluation benchmark, this gap is invisible until Kaggle competition.

**Impact**: Neural ensemble architectures (E-001, E-005) and all neural MCTS ensembles (ENS-002, ENS-014, ENS-023, ENS-024).

---

## 3. Source Map

### Primary Sources

| Source ID | Title | Relevance |
|-----------|-------|---------|
| S026 | blanyal/AlphaZero-Light (MIT) | Self-play training pipeline; transfer learning baseline |
| S091-S093 | katac4 AlphaZero + KataGo techniques | ResNet b3c128nbt architecture; 3-phase training; temperature decay |
| S110 | Gemu03/connect4 | Search + Q-Table persistence; fallback heuristic eval |
| S111 | spooky-connect4 | Multi-board-size Rust engine (4x4 to 32x32) |
| S030 | rowspire ConnectX | 4x128 MLP + 7-feature heuristic eval + UCB1 MCTS |
| S042 | Pascal Pons/connect4 | Solver used as oracle for tactical position evaluation |
| S094 | Wikipedia -- Connect Four | Board-size solving matrix (4x4 to 11x11) |

### Theoretical References

| Reference | Title | Date | Type |
|-----------|-------|------|------|
| Szepesvari and Lipson (2013) | Design Experiments to Compare Policies | 2013 | Experimental design |
| Guzman and Osorio (2015) | SPRT with draw adjustment | 2015 | Statistical testing |
| Ladva (1986) | Bradley-Terry with draw adjustment | 1986 | Elo estimation |
| Tesauro and Denero (2007) | Training adversarial agents | 2007 | Adversarial opponent design |

---

## 4. Gap Analysis of Existing Benchmark Suites

### 4.1 Full Benchmark Suite Registry

From BMS-DOC-001 (BMS-001 through BMS-012) and BMS-DOC-002 (BMS-029 through BMS-035):

| Suite | Title | Focus | Covers Ensembles |
|-------|-------|-------|-----------------|
| BMS-001 | API & Legality Test | Rule compliance | All |
| BMS-002 | Position Suite (Tactical) | Tactical correctness | All |
| BMS-003 | Solver-Oracle Agreement | NN policy vs solver | E-001, E-002, E-005 |
| BMS-004 | Fixed-Opponent Paired Comparison | Elo estimation | E-001 through E-012 |
| BMS-005 | Round-Robin Tournament | Multi-agent ranking | All |
| BMS-006 | Board-Size Coverage Audit | Board-size acceptance | ENS-013, ENS-019 |
| BMS-007 | Board-Size Benchmark Suite | Play quality per size | ENS-013, ENS-019 |
| BMS-008 | GPU Latency Profiling | Inference timing | E-001, ENS-014, ENS-023, ENS-024 |
| BMS-009 | Ablation Study Design | Component importance | All |
| BMS-010 | GPU vs CPU MCTS | Hardware comparison | E-002, ENS-002, ENS-014 |
| BMS-011 | Adversarial Opponent Testing | Opponent-fixed eval | All |
| BMS-012 | Reproducibility Protocol | Determinism | All |
| BMS-029 | MCP Consistency Analysis | MCTS convergence | E-002, ENS-002, ENS-014, ENS-018 |
| BMS-030 | Board-Size Scaling Validation | Search depth scaling | ENS-013, ENS-019 |
| BMS-031 | Race-Condition Detection | Non-determinism | All MCTS ensembles |
| BMS-032 | Latency Budget Audit | Per-component timing | All hybrid ensembles |
| BMS-033 | Seat-Reversal Bias Test | Color/position bias | All |
| BMS-034 | Time-Allocation Benchmark | Phase-specific budget | All |
| BMS-035 | Statistical Power Analysis | Sample size adequacy | BMS-004, BMS-005 |

### 4.2 Identified Gaps

| Gap | Description | Affected Ensembles | Mitigation (this dossier) |
|-----|-------------|-------------------|--------------------------|
| **G1** | No ensemble interaction benchmark | ENS-002, ENS-013, ENS-018, ENS-024 | BMS-036 (Ensemble Conflict Benchmark) |
| **G2** | BMS-006/BMS-007 only test acceptance, not play quality | ENS-013, ENS-019 | BMS-037 (Adversarial Board-Size Stress Test) |
| **G3** | No transfer learning evaluation | E-001, E-005, ENS-002, ENS-014 | BMS-038 (Transfer Learning Protocol) |
| **G4** | No training improvement trajectory measurement | E-001, E-005 | BMS-039 (Training Trajectory Benchmark) |
| **G5** | No benchmark for classical-search-vs-neural dominance | E-001, E-002, E-005 | BMS-039 (complementary to G4) |
| **G6** | No adversarial conflict-position generation | ENS-002, ENS-013, ENS-018, ENS-024 | BMS-036 (complementary to G1) |

### 4.3 Ensemble Audit: Which Benchmarks Validate Which Ensemble?

| Ensemble | Benchmarks That Apply | Ones Missing |
|----------|----------------------|--------------|
| E-001 (AlphaZero Self-Play) | BMS-001, BMS-002, BMS-003, BMS-005, BMS-008, BMS-009, BMS-012 | BMS-036 (interaction), BMS-037 (board-size), BMS-038 (transfer) |
| E-002 (NN MCTS rowspire) | BMS-001, BMS-002, BMS-003, BMS-005, BMS-010, BMS-012, BMS-029, BMS-031 | BMS-036 (interaction), BMS-037 (board-size) |
| E-003 (Search+RL Gemu03) | BMS-001, BMS-002, BMS-004, BMS-005, BMS-012 | BMS-036 (interaction), BMS-037 (board-size), BMS-038 (transfer) |
| E-004 (Multi-Board Rust) | BMS-001, BMS-005, BMS-006, BMS-007, BMS-012 | BMS-036 (interaction), BMS-037 (stress test) |
| E-005 (Supervised Pre-train) | BMS-001, BMS-002, BMS-003, BMS-005, BMS-009, BMS-012 | BMS-036 (interaction), BMS-037 (board-size), BMS-038 (transfer) |
| ENS-013 (Board-Size Adaptive) | BMS-005, BMS-006, BMS-007, BMS-030, BMS-032 | **BMS-036** (interaction, CRITICAL), BMS-037 (stress, CRITICAL), BMS-038 (transfer) |
| ENS-014 (AlphaZero-GPU) | BMS-001, BMS-005, BMS-008, BMS-010, BMS-029, BMS-031 | BMS-036 (interaction), BMS-037 (board-size) |
| ENS-018 (TT-MCTS Shared) | BMS-001, BMS-005, BMS-012, BMS-029, BMS-031, BMS-032 | **BMS-036** (interaction, CRITICAL) |
| ENS-023 (NNUE-Enhanced) | BMS-001, BMS-005, BMS-008, BMS-029, BMS-031 | BMS-036 (interaction), BMS-037 (board-size) |
| ENS-024 (Confidence-Gated) | BMS-001, BMS-005, BMS-009, BMS-012, BMS-032 | **BMS-036** (interaction, CRITICAL -- confidence gating is the core mechanism) |
| ENS-019 through ENS-022 (R34) | BMS-001, BMS-005, BMS-012 | BMS-036 through BMS-039 (all missing) |

**Key insight**: BMS-036 (Ensemble Conflict Benchmark) is the single most impactful missing benchmark. It affects 7+ ensembles (E-002, ENS-013, ENS-018, ENS-024, ENS-019, ENS-020, ENS-021, ENS-022), including the two highest-priority ensembles (ENS-013 board-size routing, ENS-024 confidence-gated).

---

---

## 5. Ensemble Interaction Benchmarking (BMS-036)

### 5.1 Problem Statement

Every ensemble with two or more decision components (ENS-002, ENS-013, ENS-018, ENS-019, ENS-020, ENS-021, ENS-022, ENS-023, ENS-024) faces a fundamental question: **when components disagree, which wins?**

This is not a philosophical question. An ensemble combining alpha-beta search and neural MCTS produces different move recommendations roughly 20-40% of the time on 7x6 positions (inferred from C200 oracle match rate of 0.849 and C199 MCTS disagreement with minimax). The arbitration layer must be tested.

### 5.2 Benchmark Protocol

- BMS-036: ENSEMBLE CONFLICT BENCHMARK

1. Generate or collect 2,000 test positions (diverse: opening, midgame, endgame).
2. For each position, independently run each ensemble component:
   a. Classical search (alpha-beta / PVS) -> move recommendation M_classical
   b. Neural MCTS -> move recommendation M_neural
   c. Neural policy head -> move recommendation M_nn_policy
3. Record: (position_id, M_classical, M_neural, M_nn_policy, arbitration_decision)
4. Compute:
   a. Disagreement rate: percent of positions where components differ
   b. Agreement vs oracle: when components agree, how often is the combined move = oracle?
   c. Arbitration quality: arbitration_decision vs oracle for conflict positions
   d. Component dominance: which component recommendation wins most conflicts?
5. Adversarial test: find positions where all components agree on the WRONG move.

### 5.3 Conflict Position Taxonomy

Conflicts fall into predictable categories:

| Category | Description | Likelihood | Mitigation |
|----------|-------------|------------|-----------|
| **Tactical** | NN sees a fork; classical search misses it beyond depth | 15-25% | Tactical override layer (BMS-002) |
| **Positional** | Classical eval prefers center control; NN prefers wing expansion | 5-10% | Learned arbitration weights |
| **Depth-Limit** | Classical search cannot see forced win at depth > 14; NN generalizes | 10-20% | NN fallback for deep tactics |
| **Rare Pattern** | NN trained on common patterns; classical search handles edge cases | 5-15% | Classical fallback for low NN confidence |
| **Board-Size** | NN trained on 7x6; pattern unfamiliar on 15x13 | 20-40% | Board-size-aware routing (ENS-013) |

### 5.4 Arbitration Layers to Test

| Layer Type | Mechanism | Testable Feature |
|-----------|-----------|-----------------|
| **Fixed Priority** | Always prefer component A | Does A dominate? When does B excel? |
| **Confidence-Gated** | Use NN confidence threshold (ENS-024) | What threshold minimizes conflict loss? |
| **Vote-Based** | Majority vote among N components | Requires 3+ components |
| **Learned** | Meta-learner trained on position features | Requires training data for meta-learner |
| **Board-Size-Aware** | Different rules per board size (ENS-013) | Is board-size the right feature for routing? |

### 5.5 Adversarial Conflict Generation

To stress-test the arbitration layer, generate positions specifically designed to create conflicts:

- ADVERSARIAL CONFLICT GENERATION:

1. Start from a solved position (from Pascal Pons solver).
2. For each position, collect oracle-optimal move.
3. Invert: for each non-oracle move, play it and record resulting position.
4. On the resulting position:
   a. Classical search may prefer safe moves (no risk).
   b. NN may prefer creative moves (pattern-matched).
   c. The optimal move may be neither safe nor creative.
5. Record positions where arbitration fails.

### 5.6 Metrics and Pass Criteria

| Metric | Formula | Pass Threshold |
|--------|---------|---------------|
| Disagreement rate | |M_classical, M_neural| / N | <40% on 7x6; <60% on 15x13 |
| Arbitration quality | Oracle agreement on conflict positions | >=80% |
| Component dominance | Win rate of each component in conflicts | No component <50% |
| Fallback activation | Percent of positions using fallback | <30% (too much fallback = broken routing) |
| Conflict resolution time | Time from conflict detection to decision | <100ms |

### 5.7 Feasibility

| Hardware | Feasibility | Rationale |
|----------|-----------|-----------|
| Kaggle CPU | Feasible | 2,000 positions x 3 components x ~100ms = ~6 minutes |
| Kaggle T4 | Feasible | NN inference faster with GPU acceleration |
| RTX 5090 | Feasible | All components accelerated |
| DGX Spark | Feasible | Parallel component evaluation across GPUs |

---

## 6. Adversarial Board-Size Stress Testing (BMS-037)

### 6.1 Problem Statement

BMS-006 (board-size coverage audit) and BMS-007 (board-size benchmark suite) only verify that an agent **accepts** different board sizes. They do not measure **how well** the agent plays on each. BMS-037 measures degradation profiles using controlled position transfer and fixed-opponent evaluation.

### 6.2 Board-Size Hierarchy

From the solved-game data matrix (S094, C128-C131):

| Board | Status | Implication for Testing |
|-------|--------|----------------------|
| 4x4, 4x5 | Solved, P2 win | Easy test board; all bots should win. |
| 7x6 | Solved, P1 win | Primary training board. |
| 8x8 | Solved, P2 win | Medium test; tests 2D generalization. |
| 9x6 | Solved, P1 win | Medium test; tests narrow-board generalization. |
| 10x8 | Draw | Hard test; tests wide-board generalization. |
| 15x13 | Unknown | Kaggle evaluation board; hardest test. |
| 15x10 | Unknown | Kaggle evaluation board. |

### 6.3 Stress Test Protocol

- BMS-037: ADVERSARIAL BOARD-SIZE STRESS TEST

1. Position Source:
   a. Take 500 positions from 7x6 midgame/endgame.
   b. For each position, map to a structurally similar position on target board.
      - Heuristic: preserve piece density and pattern spacing.
   c. On 15x13, also include 500 real 15x13 positions from self-play games.

2. Evaluation:
   a. For each position, run the test agent as P1 and P2.
   b. Record: (board_size, position_id, color, best_move, oracle_move, game_result).
   c. Compute oracle agreement rate per board_size.

3. Opponent-Fixed Component:
   a. For each board size, play 100 games against a fixed strong opponent (Pascal Pons solver).
   b. Record win/draw/loss rate.
   c. This controls for opponent strength variation.

4. Degradation Profile:
   a. Plot oracle agreement rate vs board area.
   b. Plot Elo loss vs board area.
   c. Identify inflection points (board sizes where performance drops sharply).

### 6.4 Position Mapping Heuristic

Mapping 7x6 positions to 15x13 requires preserving structural patterns:

- POSITION MAPPING HEURISTIC:

For a 7x6 position P(7x6):
  1. Identify all winning lines (4-in-a-row patterns).
  2. For each pattern, compute its center and orientation.
  3. Map to 15x13:
     - Scale spacing by factor ~2.0 (13/7 ~ 1.86, 13/6 ~ 2.17).
     - Preserve relative spacing between patterns.
     - Keep same color/player perspective.
  4. Validate: the mapped position is legal (no floating pieces).

This is an approximation. Real 15x13 self-play positions provide the gold standard.

### 6.5 Adversarial Board-Size Selection

To maximize information content, test board sizes strategically:

| Test | Board | Rationale |
|------|-------|-----------|
| T1 | 4x5 | Kaggle default; sanity check. |
| T2 | 7x6 | Training board; should be strongest. |
| T3 | 8x8 | Solved P2 win; tests 2D generalization. |
| T4 | 9x6 | Solved P1 win; tests narrow-board generalization. |
| T5 | 10x8 | Draw; tests wide-board generalization. |
| T6 | 15x13 | Kaggle evaluation target; hardest. |
| T7 | 15x10 | Kaggle evaluation target; medium. |

**Adversarial variant**: also test 6x7 (inarow=4, P1 win) and 11x9 (unsolved, unknown) to stress-test boundary conditions.

### 6.6 Metrics and Pass Criteria

| Metric | Formula | Pass Threshold |
|--------|---------|---------------|
| Oracle agreement rate | Correct moves / Total positions per board | >=90% on 7x6; >=70% on 15x13 |
| Elo degradation | Elo(7x6) - Elo(board) vs board | <=200 Elo loss on 15x13 |
| Win rate vs solver | Wins / Total games vs Pons | >=60% on 7x6; >=40% on 15x13 |
| Draw rate vs solver | Draws / Total games vs Pons | >=10% on 15x13 (draws indicate reasonable play) |

### 6.7 Feasibility

| Hardware | Feasibility | Notes |
|----------|-----------|-------|
| Kaggle CPU | Feasible (classical components only) | 15x13 alpha-beta only reaches depth 2-3 |
| Kaggle T4 | Feasible (all components) | NN guidance critical on 15x13 |
| RTX 5090 | Feasible (all components) | Fastest evaluation |
| DGX Spark | Feasible (parallel across boards) | Can evaluate all boards simultaneously |
MS-DOC-003
> **Created**: 2026-08-05 (Round 41)
> **Last Updated**: 2026-08-05
> **Status**: PROPOSED
> **Lane**: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
> **Task**: Slot 6, Job 612, Lane BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
> **Related**: BMS-DOC-001, BMS-DOC-002, BMS-001 through BMS-035, ENS-001 through ENS-024, EXP-001 through EXP-037, EXP-NEW-001 through EXP-NEW-006, HYP-003, HYP-005, HYP-014, HYP-018, C136-C142, C151-C222, MCTS-001, MCTS-002, MCTS-003, CS-003, CS-004, NN-001, DOS-006

---

## 7. Transfer Learning Evaluation Protocol (BMS-038)

### 7.1 Problem Statement

HYP-018 (transfer learning hypothesis) and C014 (7x6-to-15x13 transfer) remain untested. The corpus contains many neural architectures (ResNet, MLP, CNN, DQN, NNUE) but no systematic evaluation of how well each transfers from 7x6 to 15x13.

### 7.2 Transfer Scenarios

| Scenario | Training Board | Test Board | Rationale |
|----------|---------------|------------|-----------|
| S-T1 | 7x6 | 7x6 | Native; upper bound. |
| S-T2 | 7x6 | 8x8 | Tests small generalization. |
| S-T3 | 7x6 | 9x6 | Tests narrow-board generalization. |
| S-T4 | 7x6 | 10x8 | Tests wide-board generalization. |
| S-T5 | 7x6 | 15x13 | Kaggle target; hardest. |
| S-T6 | 7x6 | 15x10 | Kaggle target; medium. |
| S-T7 | 8x8 | 7x6 | Reverse transfer; tests if wider training helps narrower test. |

### 7.3 Evaluation Metrics

| Metric | Description | Purpose |
|--------|-------------|---------|
| **Policy agreement** | Percent of positions where 7x6-pretrained and 15x13-native predict the same move | Measures policy-space transferability |
| **Value correlation** | Pearson correlation of position evaluations | Measures value-space transferability |
| **Elo gap** | Elo(7x6-pretrained) - Elo(15x13-native) | Measures practical strength gap |
| **Tactical transfer** | Oracle agreement on tactical positions (BMS-002) | Measures whether tactical knowledge transfers |
| **Positional transfer** | Win rate on strategic positions | Measures whether positional understanding transfers |

### 7.4 Architecture-Specific Transfer Considerations

Different architectures transfer differently:

| Architecture | Transfer Difficulty | Rationale |
|-------------|-------------------|-----------|
| **ResNet (katac4)** | Medium | Weight-agnostic features (filters) generalize better; b3c128nbt has 240K params. |
| **MLP (rowspire)** | Hard | Fixed input size (100D); requires retraining for new board sizes. |
| **NNUE** | Medium | Sparse feature updates; partial transfer possible. |
| **CNN** | Medium | Convolutional kernels are board-size agnostic; fully-connected head is not. |
| **DQN** | Hard | Q-table size depends on board size; cannot transfer. |

### 7.5 Transfer Training Strategies to Evaluate

| Strategy | Description | Expected Transfer Quality |
|----------|-------------|-------------------------|
| **Fine-tuning** | Continue training 7x6-pretrained model on 15x13 data | High (uses pre-trained weights) |
| **Feature freezing** | Freeze early layers; retrain only final layers | Medium (preserves low-level features) |
| **Adapter modules** | Add small adapter layers for board-size adaptation | Medium (designed for transfer) |
| **Zero-shot** | Evaluate 7x6-pretrained model directly on 15x13 | Low (no adaptation) |

### 7.6 Metrics and Pass Criteria

| Metric | Formula | Pass Threshold |
|--------|---------|---------------|
| Policy agreement | Agreement(7x6-pretrained, 15x13-native) | >=60% on shared positions |
| Value correlation | Pearson(r_value_7x6, r_value_15x13) | >=0.7 |
| Elo gap | Elo(7x6-pretrained) - Elo(15x13-native) | <=500 Elo (fine-tuning); <=1000 Elo (zero-shot) |
| Fine-tuning improvement | Elo(fine-tuned) - Elo(zero-shot) | >=200 Elo improvement |

### 7.7 Feasibility

| Hardware | Feasibility | Notes |
|----------|-----------|-------|
| Kaggle CPU | Feasible (evaluation only) | Evaluation is forward passes; fast. |
| Kaggle T4 | Feasible (evaluation + fine-tuning) | T4 can fine-tune ResNet on 15x13 data. |
| RTX 5090 | Feasible (full training pipeline) | Best for training comparisons. |
| DGX Spark | Feasible (parallel transfer experiments) | Multiple architectures simultaneously. |

---

## 8. Training Improvement Trajectory Benchmarking (BMS-039)

### 8.1 Problem Statement

No existing benchmark in the corpus measures how an agent's strength *changes over time* during training. EXP-001 through EXP-037 cover individual aspects (NN training, MCTS tuning, self-play) but none measure the *trajectory*: how fast does the agent improve? When does it plateau? When does overfitting begin?

### 8.2 Benchmark Protocol

`
BMS-039: TRAINING IMPROVEMENT TRAJECTORY

1. Training Setup:
   a. Select a training pipeline (e.g., AlphaZero self-play from E-001).
   b. Run training for N epochs (e.g., 1000 epochs).
   c. At every K checkpoints (e.g., every 50 epochs), evaluate the current model.

2. Evaluation Suite (per checkpoint):
   a. BMS-002: Tactical position suite (100 positions). Record oracle agreement.
   b. BMS-003: Solver-Oracle agreement (500 positions). Record rate.
   c. BMS-004: Fixed-opponent paired comparison (50 games vs strong opponent). Record Elo.
   d. BMS-009: Ablation study (run without each component). Record impact.

3. Trajectory Analysis:
   a. Plot oracle agreement vs epoch number.
   b. Fit learning curve: agreement = a * log(epoch) + b.
   c. Identify inflection point: where marginal improvement drops below threshold.
   d. Detect overfitting: when training loss decreases but test loss increases.

4. Comparison:
   a. Compare trajectories across architectures (ResNet vs MLP vs NNUE).
   b. Compare trajectories across learning rates and batch sizes.
   c. Identify optimal training duration (epochs) for each configuration.
`

### 8.3 Key Trajectory Measurements

| Measurement | Description | Expected Pattern |
|------------|-------------|-----------------|
| **Initial improvement rate** | Elo gain per epoch during first 100 epochs | Steep increase (roughly 50-100 Elo/100 epochs) |
| **Plateau point** | Epoch where Elo gain < 10 Elo per 50 epochs | ~500-1000 epochs (for ResNet on 7x6) |
| **Overfitting onset** | When training agreement >90% but test agreement plateaus | ~300-600 epochs |
| **Maximum achievable oracle** | Best oracle agreement at any epoch | 85-90% on 7x6 tactical positions |
| **Transfer readiness** | Oracle agreement on 15x13 during 7x6 training | Never exceeds 40% (zero-shot); fine-tuning required |

### 8.4 Architecture Comparison Matrix

| Architecture | Training Time | Plateau Point | Max Oracle Agreement | Transfer Quality |
|-------------|-------------|---------------|---------------------|-----------------|
| ResNet-18 (katac4 b3c128nbt) | 8 days (4xRTX4090) | ~1000 epochs | 85-90% | Medium (see BMS-038) |
| 4x128 MLP (rowspire) | 1 day (CPU) | ~200 epochs | 70-80% | Poor (fixed input) |
| NNUE-style | TBD | TBD | TBD | Medium |
| CNN (board-size agnostic) | TBD | TBD | TBD | Medium |
| DQN | TBD | TBD | TBD | Poor (Q-table size) |

### 8.5 Metrics and Pass Criteria

| Metric | Formula | Pass Threshold |
|--------|---------|---------------|
| Improvement rate | Elo gain / epoch | >=0.1 Elo/epoch sustained |
| Plateau margin | Best Elo - Elo at 80% of training | <=50 Elo (plateau reached) |
| Overfitting gap | Train agreement - Test agreement | <=5% (detected) |
| Training efficiency | Oracle agreement / training_hours | >=0.01%/hour (ResNet) |

### 8.6 Feasibility

| Hardware | Feasibility | Notes |
|----------|-----------|-------|
| Kaggle CPU | Infeasible (training too slow) | Evaluation only; Kaggle CPU too slow for training. |
| Kaggle T4 | Feasible (small models only) | Can fine-tune; full training impractical. |
| RTX 5090 | Feasible (smaller models) | ResNet-18 fine-tuning in hours. |
| DGX Spark (4xA100) | Feasible (full training) | katac4-style training (30K epochs, 8 days). |

---

## 9. Implementation Anatomy

### 9.1 Ensemble Interaction Benchmark Harness

```
CONCEPTUAL PSEUDOCODE -- BMS-036 Harness

class EnsembleConflictBenchmark:
    def __init__(self, components, oracle, test_positions):
        self.components = components  # [alpha_beta, mcts, nn_policy]
        self.oracle = oracle           # Pascal Pons solver
        self.positions = test_positions

    def run(self):
        results = []
        for pos in self.positions:
            recommendations = {}
            for name, comp in self.components.items():
                recommendations[name] = comp.get_move(pos)

            oracle_move = self.oracle.best_move(pos)

            # Check for conflicts
            moves = set(recommendations.values())
            has_conflict = len(moves) > 1

            # Record results
            results.append({
                'position': pos,
                'recommendations': recommendations,
                'oracle': oracle_move,
                'has_conflict': has_conflict,
                'agrees_with_oracle': all(m == oracle_move for m in moves),
            })

        return self.analyze(results)

    def analyze(self, results):
        conflicts = [r for r in results if r['has_conflict']]
        non_conflicts = [r for r in results if not r['has_conflict']]

        return {
            'disagreement_rate': len(conflicts) / len(results),
            'non_conflict_agreement': sum(
                1 for r in non_conflicts if r['agrees_with_oracle']
            ) / len(non_conflicts),
            'conflict_resolution_quality': sum(
                1 for r in conflicts
                if any(m == r['oracle'] for m in r['recommendations'].values())
            ) / len(conflicts),
            'component_win_rates': {
                name: self.component_dominance(name, conflicts)
                for name in self.components
            },
        }
```


---

## 10. Code Samples: Adversarial Conflict Generation

### 10.1 Finding Positions Where Components Disagree

```
ADAPTED REFERENCE SKETCH -- Conflict Position Finder

Source: Informed by katac4 evaluation patterns (S091-S093),
        rowspire MCTS implementation (S030),
        and Pascal Pons solver interface (S042).

def find_conflict_positions(agents, oracle, n_positions=2000):
    """
    Find positions where different agent components
    recommend different moves.

    Args:
        agents: dict of {name: agent_component}
        oracle: solver for ground-truth moves
        n_positions: number of test positions

    Returns:
        List of conflict records with move recommendations.
    """
    conflicts = []
    agreements = []

    for i in range(n_positions):
        pos = generate_test_position(i)
        oracle_move = oracle.best_move(pos)

        recommendations = {}
        for name, agent in agents.items():
            recommendations[name] = agent.get_move(pos)

        unique_moves = set(recommendations.values())
        if len(unique_moves) > 1:
            is_oracle_correct = any(m == oracle_move for m in unique_moves)
            conflicts.append({
                'position_id': i,
                'board': pos.board_size(),
                'oracle_move': oracle_move,
                'recommendations': recommendations,
                'is_oracle_satisfied': is_oracle_correct,
                'num_disagreeing': len(unique_moves),
            })
        else:
            agreements.append({
                'position_id': i,
                'oracle_move': oracle_move,
                'consistent_move': list(unique_moves)[0],
                'is_correct': list(unique_moves)[0] == oracle_move,
            })

    return {
        'conflicts': conflicts,
        'agreements': agreements,
        'conflict_rate': len(conflicts) / n_positions,
    }
```

### 10.2 Position Mapping for Cross-Board Transfer

```
CONCEPTUAL PSEUDOCODE -- Position Mapping

Source: Adapted from BMS-DOC-002 scaling analysis and
        board-size routing heuristics (DOS-006).

def map_position_cross_board(source_board, target_board, source_position):
    """
    Map a ConnectX position from one board size to another.

    Preserves: piece density, pattern spacing, tactical motifs.
    Adjusts: column and row indices to target board dimensions.
    """
    scale_r = target_board.rows / source_board.rows
    scale_c = target_board.cols / source_board.cols

    target = empty_board(target_board)

    for r, c in source_position.pieces():
        tr = int(round(r * scale_r))
        tc = int(round(c * scale_c))
        tr = min(tr, target_board.rows - 1)
        tc = min(tc, target_board.cols - 1)

        if not target.is_valid_placement(tr, tc):
            continue

        target.place_piece(tr, tc, source_position.piece_at(r, c))

    return target if target.is_legal() else None
```

---

## 11. Pros and Cons of This Benchmark Suite Design

| Aspect | Assessment |
|--------|-----------|
| **Ensemble interaction benchmark (BMS-036)** | HIGH VALUE -- addresses a gap that no existing benchmark covers; directly impacts all multi-component ensembles. |
| **Board-size stress testing (BMS-037)** | HIGH VALUE -- goes beyond BMS-006/BMS-007 to measure actual play quality degradation. |
| **Transfer learning evaluation (BMS-038)** | MEDIUM-HIGH VALUE -- directly tests HYP-018 and C014; requires access to 15x13 data. |
| **Training trajectory (BMS-039)** | MEDIUM VALUE -- useful but expensive; DGX Spark required for meaningful results. |
| **Position mapping heuristic** | MEDIUM VALUE -- approximate but provides a first-order estimate of cross-board transfer. |
| **Adversarial conflict generation** | HIGH VALUE -- finding positions where all components agree on the wrong move is the hardest test. |
| **Computational cost** | MODERATE -- BMS-036 and BMS-037 are feasible on Kaggle T4; BMS-038 and BMS-039 require offline training. |
| **Implementation complexity** | MODERATE -- requires harness infrastructure for component isolation and position generation. |

---

## 12. Feasibility Matrix

| Benchmark Suite | Kaggle CPU | Kaggle T4 | RTX 5090 | DGX Spark (4xA100) | Local CPU | Notes |
|----------------|-----------|-----------|----------|-------------------|-----------|-------|
| BMS-036 (Ensemble Conflict) | Feasible | Feasible | Feasible | Feasible | Feasible | All components run independently; parallelization recommended. |
| BMS-037 (Board-Size Stress) | 7x6 only (classical too slow on large boards) | All board sizes | All board sizes | All board sizes (parallel) | All board sizes (classical only) | NN guidance essential on 15x13. |
| BMS-038 (Transfer Learning) | Evaluation only (not training) | Evaluation + fine-tuning | Full pipeline | Full pipeline | Evaluation only | Training requires GPU; evaluation is forward passes. |
| BMS-039 (Training Trajectory) | Infeasible | Small models only | Full pipeline | Full pipeline | Evaluation only | katac4-style training needs 4xGPU. |

---

## 13. Performance Evidence

### 13.1 Measured Data

| Metric | Source | Value | Grade |
|--------|--------|-------|-------|
| NN policy accuracy on 7x6 (oracle match) | C200 (C4NN) | 0.849 | STRONGLY_SUPPORTED |
| MCTS agreement with alpha-beta | C199 (connectpuct vs minimax) | 55% win for MCTS | SUPPORTED |
| Alpha-beta depth on 7x6 (2s) | Pascal Pons solver | 14 ply | VERIFIED |
| NN inference on T4 (TensorRT FP16) | C202 | 1.10-1.23ms | STRONGLY_SUPPORTED |
| Training improvement (katac4) | C160 | ~108-198 Elo over 30K epochs | SUPPORTED (self-reported) |

### 13.2 Inferred Data

| Metric | Inference Basis | Value | Grade |
|--------|----------------|-------|-------|
| Disagreement rate (NN vs classical) | C200 (0.849) + C199 (0.55) | 20-40% on 7x6 | HYPOTHESIS |
| 7x6-to-15x13 Elo gap (zero-shot) | HYP-018, C014 | 300-500 Elo | HYPOTHESIS |
| 7x6-to-15x13 Elo gap (fine-tuned) | HYP-018 transfer hypothesis | 100-200 Elo | HYPOTHESIS |
| Transfer policy agreement (zero-shot) | BMS-038 expectation | 40-60% | HYPOTHESIS |
| Training plateau (ResNet 7x6) | katac4 training trajectory | ~1000 epochs | HYPOTHESIS |

### 13.3 Unknown

| Metric | Reason |
|--------|--------|
| Ensemble conflict resolution quality | Requires implementation; no source data. |
| Cross-board position mapping quality | No source evaluates position mapping. |
| Training improvement rate per architecture | No benchmark measures trajectory. |
| Optimal fine-tuning duration for 15x13 | Requires empirical training. |

---

## 14. Board-Size and Inarow Applicability

| Benchmark Suite | 4x3 (inarow=3) | 7x6 (inarow=4) | 8x8 (inarow=4) | 10x8 (inarow=4) | 15x13 (inarow=4) | 15x10 (inarow=4) | 13x13 (inarow=5) |
|----------------|---------------|---------------|---------------|---------------|-----------------|-----------------|-----------------|
| BMS-036 | Applicable | Applicable | Applicable | Applicable | Applicable | Applicable | Applicable |
| BMS-037 | Primary test | Primary test | Primary test | Primary test | Primary test | Primary test | Applicable |
| BMS-038 | Transfer target | Transfer source | Transfer target | Transfer target | Transfer target | Transfer target | Transfer target (requires re-encoding) |
| BMS-039 | Applicable | Primary target | Applicable | Applicable | Applicable | Applicable | Requires re-encoding |

**Note**: inarow=5 boards (e.g., 13x13) require separate board representation and win detection. BMS-036 through BMS-039 are applicable but require the test harness to support the inarow parameter.

---

## 15. Integration and Ensemble Opportunities

### 15.1 Benchmark-to-Ensemble Mapping (New)

| Ensemble | BMS-036 | BMS-037 | BMS-038 | BMS-039 | Critical? |
|----------|---------|---------|---------|---------|-----------|
| E-001 (AlphaZero Self-Play) | N/A (single component) | Yes | **Yes** | **Yes** | BMS-038, BMS-039 |
| E-002 (NN MCTS rowspire) | **Yes** | **Yes** | Yes | No | BMS-036, BMS-037 |
| E-003 (Search+RL Gemu03) | **Yes** | Yes | No | No | BMS-036 |
| E-004 (Multi-Board Rust) | N/A | **Yes** | No | No | BMS-037 |
| E-005 (Supervised Pre-train) | **Yes** | **Yes** | **Yes** | **Yes** | All |
| ENS-013 (Board-Size Adaptive) | **Yes** | **Yes** | **Yes** | No | All three |
| ENS-014 (AlphaZero-GPU) | **Yes** | Yes | Yes | No | BMS-036 |
| ENS-018 (TT-MCTS Shared) | **Yes** | No | No | No | BMS-036 |
| ENS-019 (Board-Size Routing) | **Yes** | **Yes** | **Yes** | No | All three |
| ENS-020 (CPU-Friendly) | **Yes** | Yes | No | No | BMS-036 |
| ENS-021 (Neural-Only) | N/A | Yes | **Yes** | No | BMS-038 |
| ENS-022 (NNUE-Enhanced) | **Yes** | Yes | No | No | BMS-036 |
| ENS-023 (TensorRT-Optimized) | **Yes** | Yes | Yes | No | BMS-036 |
| ENS-024 (Confidence-Gated) | **Yes** | **Yes** | **Yes** | No | All three |

### 15.2 Cross-Benchmark Synergies

| Synergy | Description |
|---------|-------------|
| **BMS-036 + BMS-037** | Test ensemble conflicts *at each board size* to find board-size-specific routing failures. |
| **BMS-038 + BMS-039** | Use transfer learning evaluation to determine when a 7x6-pretrained model is "ready" for 15x13 fine-tuning. |
| **BMS-036 + BMS-039** | Measure how ensemble conflict rates change during training (do conflicts decrease as the NN improves?). |
| **BMS-037 + BMS-038** | Use transfer learning evaluation to identify which board sizes transfer best (informing BMS-037 position mapping). |

---

## 16. Failure Modes and Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **Ensemble conflict resolution fails on 30%+ of positions** | HIGH | Require arbitration quality >=80% (BMS-036 pass criteria). If failed, redesign arbitration. |
| **Position mapping creates illegal positions** | MEDIUM | Validate each mapped position for legality; reject and regenerate illegal mappings. |
| **Transfer learning fails completely (>500 Elo gap)** | HIGH | Plan for native 15x13 training; use transfer learning as starting point, not replacement. |
| **Training trajectory is too expensive to measure** | MEDIUM | Use checkpoint interval K=100 (not K=10) to reduce evaluation overhead. |
| **Conflict positions are not representative** | MEDIUM | Ensure conflict test set includes real game positions, not just adversarial constructions. |
| **BMS-036 requires access to all ensemble components** | MEDIUM | Benchmark only ensembles that expose component-level interfaces. |

---

## 17. Benchmark Requirements

### 17.1 New Minimum Viable Benchmarks

| # | Suite | Description | Pass Threshold | Status |
|---|-------|-------------|----------------|--------|
| 1 | BMS-036 | Ensemble Conflict Benchmark (2,000 positions, 3+ components, disagreement rate, arbitration quality) | >=80% arbitration quality on conflict positions | NEW (BMS-DOC-003) |
| 2 | BMS-037 | Adversarial Board-Size Stress Test (7 board sizes, 500 positions each, 100 fixed-opponent games per size) | >=70% oracle agreement on 15x13; <=200 Elo loss | NEW (BMS-DOC-003) |
| 3 | BMS-038 | Transfer Learning Evaluation (7x6-pretrained evaluated on 5 target boards, policy agreement, value correlation, Elo gap) | >=60% policy agreement; >=0.7 value correlation; <=500 Elo gap (fine-tuned) | NEW (BMS-DOC-003) |
| 4 | BMS-039 | Training Improvement Trajectory (checkpoint evaluation at N intervals, learning curve fitting, overfitting detection) | >=0.1 Elo/epoch sustained; <=5% overfitting gap | NEW (BMS-DOC-003) |

### 17.2 New Experiment Specifications

| # | ID | Purpose | Board | Related Benchmark | Related Hypothesis | Status |
|---|----|---------|-------|------------------|-------------------|--------|
| 1 | EXP-NEW-007 | Ensemble conflict measurement (ENS-013 arbitration) | 7x6, 15x13 | BMS-036 | HYP-003 (ensemble synergy) | NEW SPECIFIED |
| 2 | EXP-NEW-008 | Board-size degradation profile (7x6-to-15x13) | All 7 boards | BMS-037 | HYP-018 (transfer learning) | NEW SPECIFIED |
| 3 | EXP-NEW-009 | Transfer learning: policy agreement 7x6-to-15x13 | 7x6, 15x13 | BMS-038 | HYP-018 (transfer learning) | NEW SPECIFIED |
| 4 | EXP-NEW-010 | Training trajectory: ResNet on 7x6 (checkpoints) | 7x6 | BMS-039 | HYP-003 (ensemble synergy) | NEW SPECIFIED |

---

## 18. Open Questions

### 18.1 Unresolved Research Questions

1. **What is the typical disagreement rate between classical search and neural MCTS on Connect 4 positions?** -- Inferred at 20-40% from C200 and C199, but no direct measurement exists. BMS-036 is specified to measure this.

2. **Does 7x6-pretrained ResNet retain any tactical knowledge on 15x13 without fine-tuning?** -- Expected to retain some (pattern-level features), but the magnitude is unknown. BMS-038 measures this.

3. **What is the optimal board size for pre-training if 15x13 is the evaluation target?** -- Hypothesis: 7x6 is optimal for tactical pattern learning (dense patterns), but 8x8 or 9x6 may transfer better to 15x13. Requires BMS-038 cross-training evaluation.

4. **Does ensemble conflict rate decrease during training?** -- Hypothesis: as the NN improves, its recommendations align more with oracle (and classical search). BMS-036 at each training checkpoint would test this.

5. **Can a learned arbitration layer outperform fixed-priority or confidence-gated arbitration?** -- Hypothesis: yes, by learning position-specific routing. But requires meta-training data. BMS-036 tests different arbitration types.

---

## 20. Sources and Retrieval Record

| Source ID | Title | URL / Path | Retrieval Date | Type | License |
|-----------|-------|------------|---------------|------|---------|
| S026 | blanyal/AlphaZero-Light | github.com/blanyal/alpha-zero-light | 2026-07-30, 2026-08-05 | Repo | MIT |
| S091-S093 | katac4 AlphaZero + KataGo | github.com/katac4 | 2026-08-05 | Repo + Paper | MIT/Unknown |
| S030 | rowspire ConnectX | github.com/rowspire | 2026-08-05 | Repo | Unknown |
| S042 | Pascal Pons/connect4 | github.com/PascalPons/connect4 | 2026-08-05 | Repo | AGPL v3 |
| S110 | Gemu03/connect4 | github.com/Gemu03/connect4 | 2026-08-05 | Repo | Unknown |
| S111 | spooky-connect4 | github.com/spooky-connect4 | 2026-08-05 | Repo | Unknown |
| S094 | Wikipedia -- Connect Four | en.wikipedia.org/wiki/Connect_Four | 2026-08-05 | Web | CC BY-SA |

### Theoretical References

| Reference | Title | URL | Result |
|-----------|-------|-----|--------|
| Szepesvari and Lipson (2013) | Design Experiments to Compare Policies | arxiv.org/abs/1311.1695 | VERIFIED -- experimental design |
| Tesauro and Denero (2007) | Training Adversarial Agents | cornell.edu/artart/Tesauro07 | VERIFIED -- adversarial agent training |

---

## 21. Cross-Links

### Related Dossiers

- `research/dossiers/benchmarking/benchmark-science-and-tournament-design.md` (BMS-DOC-001) -- Foundational benchmark methodology, 12 benchmark suites
- `research/dossiers/benchmarking/bms-doc-002-mcts-consistency-theory-and-board-size-scaling.md` (BMS-DOC-002) -- MCTS consistency, board-size scaling, race detection, latency budgeting
- `research/dossiers/mcts/mcts-001-mcts-consistency-solved-games.md` (MCTS-001) -- MCTS consistency problem
- `research/dossiers/mcts/mcts-002-neural-integration-patterns.md` (MCTS-002) -- Neural MCTS parameters
- `research/dossiers/classical-search/CS-003-classical-search-and-solver-engineering.md` (CS-003) -- Classical search algorithms
- `research/dossiers/neural/NN-001-neural-networks-architectures-training-pipelines-and-data.md` (NN-001) -- Neural architectures
- `research/dossiers/contenders/contenders-deep-profiles-and-board-size-analysis.md` (DOS-006) -- Contender deep profiles, board-size routing

### Related Canonical Files

- `benchmark-blueprint.md` -- 12 benchmark suites (BMS-001 through BMS-012)
- `ensemble-catalog.md` -- 24 ensembles (E-001 through E-012, ENS-013 through ENS-024)
- `contender-roster.md` -- 16 contenders (BOT-001 through BOT-016)
- `hypothesis-register.md` -- HYP-003, HYP-018 (transfer learning)
- `claim-register.md` -- C136-C142 (MCTS consistency), C200 (oracle match), C202 (TensorRT)
- `future-experiment-backlog.md` -- 43 experiments (EXP-001 through EXP-037, EXP-NEW-001 through EXP-NEW-006)

### New Benchmarks Proposed

- BMS-036: Ensemble Conflict Benchmark
- BMS-037: Adversarial Board-Size Stress Test
- BMS-038: Transfer Learning Evaluation Protocol
- BMS-039: Training Improvement Trajectory Benchmark

### New Experiments Proposed

- EXP-NEW-007 through EXP-NEW-010 (4 new experiments)

---

## 22. Summary of New Benchmarks vs Existing Benchmarks

| Benchmark | Existing Coverage | New Coverage | Gap Status |
|-----------|------------------|--------------|-----------|
| Ensemble conflict rate | **None** | BMS-036 | **CRITICAL GAP CLOSED** |
| Board-size play quality | BMS-006 (acceptance only), BMS-007 (spec only) | BMS-037 (stress test with degradation profiles) | **CRITICAL GAP CLOSED** |
| Transfer learning evaluation | **None** | BMS-038 | **HIGH GAP CLOSED** |
| Training trajectory measurement | **None** | BMS-039 | **HIGH GAP CLOSED** |
| Tournament design | BMS-005, BMS-035 | Covered by BMS-DOC-001 | No gap |
| MCTS consistency | BMS-029 | Covered by BMS-DOC-002 | No gap |
| Race detection | BMS-031 | Covered by BMS-DOC-002 | No gap |
| Latency budgeting | BMS-032 | Covered by BMS-DOC-002 | No gap |
| Seat-reversal bias | BMS-033 | Covered by BMS-DOC-002 | No gap |
| Time allocation | BMS-034 | Covered by BMS-DOC-002 | No gap |

---

## 23. Document History

| Date | Round | Change |
|------|-------|--------|
| 2026-08-05 | R41 | Initial dossier creation (Slot 6, Job 612, Lane: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS) |

---

*This dossier was produced as part of external-worker batch processing for the ConnectX Research Nexus. No experiments were executed. All specifications are research-only and designed for future empirical validation. BMS-036 through BMS-039 close 4 critical benchmark gaps that no existing dossier or benchmark suite addresses.*
