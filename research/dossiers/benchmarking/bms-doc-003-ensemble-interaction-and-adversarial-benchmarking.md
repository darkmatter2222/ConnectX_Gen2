# BMS-DOC-003: Ensemble Interaction Benchmarking, Adversarial Board-Size Stress Testing, and Transfer Learning Evaluation

> **Dossier ID**: BMS-DOC-003
> **Created**: 2026-08-05 (Round 41)
> **Last Updated**: 2026-08-05
> **Status**: PROPOSED
> **Lane**: BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
> **Task**: Slot 6, Job 612, Lane BENCHMARK_SCIENCE_AND_FUTURE_EXPERIMENTS
> **Related**: BMS-DOC-001, BMS-DOC-002, BMS-001 through BMS-035, ENS-001 through ENS-024, EXP-001 through EXP-037, EXP-NEW-001 through EXP-NEW-006, HYP-003, HYP-005, HYP-014, HYP-018, C136-C142, C151-C222, MCTS-001, MCTS-002, MCTS-003, CS-003, CS-004, NN-001, DOS-006

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
