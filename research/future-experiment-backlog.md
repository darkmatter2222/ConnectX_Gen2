# Future Experiment Backlog — ConnectX Bot v9

> **Created**: 2026-08-03 (Round 27)
> **Last Updated**: 2026-08-06 (Round 53)
> **Total experiments**: 59+ (EXP-001 through EXP-037, EXP-CS-001 through EXP-CS-002, EXP-NEW-001 through EXP-NEW-010, EXP-BMS-001 through EXP-BMS-008, EXP-NN-001 through EXP-NN-005, BMS-016 through BMS-021, BMS-036 through BMS-039)
> **R35**: 5 new governance experiments planned (EXP-033 through EXP-037); not yet added to backlog body due to research-only phase; deferred to next batch
> **R44**: 8 new experiments added from BMS-DOC-005 (EXP-BMS-001 through EXP-BMS-008): Kaggle competitive benchmark, resource profiling pilot, pipeline gate calibration, board-size stress test, overtime profiling, statistical power analysis, resource comparison, pipeline gate precision/recall.
> **All statuses**: DEFERRED or SPECIFIED — no experiment may be marked completed in research-only phase.
> **R34**: No new experiments added (batch-00019 focused on hypothesis/component/ensemble generation, not empirical experiment specification)

---

## Status Legend

| Status | Meaning |
|--------|---------|
| **DEFERRED** | Requires research-only work before empirical execution can begin |
| **SPECIFIED** | Experimental design is complete; ready for implementation when phase transitions |
| **BLOCKED** | Waiting on prerequisite research to complete |
| **READY_FOR_IMPLEMENTATION** | All prerequisites met; awaiting implementation phase |
| **RETIRED** | Experimental goal no longer relevant or superseded |

---

## Experiment Summary

| # | ID | Hypothesis | Ensemble | Purpose | Status | Priority |
|---|----|------------|----------|---------|--------|----------|
| 1 | EXP-001 | HYP-001, HYP-004 | ENS-001, ENS-004 | Conservative vs warm-start MCTS | SPECIFIED | P0 |
| 2 | EXP-002 | HYP-003 | ENS-003 | Adjacent-opening draw detection | SPECIFIED | P0 |
| 3 | EXP-003 | HYP-004 | ENS-004 | Warm-start MCTS vs pure MCTS | SPECIFIED | P1 |
| 4 | EXP-004 | HYP-002 | ENS-002 | MCTS visit variance threshold | BLOCKED | P2 |
| 5 | EXP-005 | HYP-002 | ENS-002 | Three-way hybrid training | BLOCKED | P2 |
| 6 | EXP-006 | HYP-005 | — | MCP theorem verification | SPECIFIED | P0 |
| 7 | EXP-007 | — | — | Automated claim reconciliation | SPECIFIED | P1 |
| 8 | EXP-008 | — | — | Source ID namespace isolation | SPECIFIED | P1 |
| 9 | EXP-009 | HYP-009 | ENS-002 | Three-loss vs two-loss objective ablation | SPECIFIED | P1 |
| 10 | EXP-010 | HYP-010 | — | Temperature schedule comparison | SPECIFIED | P1 |
| 11 | EXP-011 | HYP-009 | ENS-002 | AZAL auxiliary loss training | SPECIFIED | P2 |
| 12 | EXP-012 | HYP-007 | ENS-002 | 80/20 policy prior mixing ratio | SPECIFIED | P2 |
| 13 | EXP-013 | HYP-009 | — | NeuralConnect4 vs katac4 training comparison | SPECIFIED | P2 |
| 14 | EXP-014 | — | — | Gemu03 Search+RL hybrid validation | SPECIFIED | P2 |
| 15 | EXP-015 | HYP-005, HYP-003 | — | MCTS consistency budget analysis | SPECIFIED | P1 |
| 16 | EXP-016 | HYP-003 | — | Adjacent-opening MCTS consistency measurement | SPECIFIED | P1 |
| 17 | EXP-017 | HYP-003 | ENS-003 | Adjacent-opening draw detection ensemble validation | SPECIFIED | P1 |
| 18 | EXP-018 | HYP-005 | — | NN-guided vs random-playout MCTS on adjacent openings | SPECIFIED | P1 |
| 19 | EXP-019 | — | — | Kamide/connect-n adaptive scoring minimax benchmark | SPECIFIED | P2 |
| 20 | EXP-020 | — | — | Tromp fhourstones88 search system validation (8.3M TT, dual-lock, history heuristic) | SPECIFIED | P2 |
| 21 | EXP-021 | — | — | MTD(f) and PVS gap investigation across Connect 4 engines | SPECIFIED | P1 |
| 22 | EXP-022 | — | — | Board representation comparison across Kaggle implementations | SPECIFIED | P2 |
| 23 | EXP-023 | — | ENS-013 | Board-size-adaptive ensemble routing protocol validation | SPECIFIED | P1 |
| 24 | EXP-024 | — | — | Kamide Web Worker deployment constraints study | SPECIFIED | P2 |
| 25 | EXP-025 | — | — | Corpus governance audit automation (round fragmentation, claim-count reconciliation) | SPECIFIED | P1 |
| 26 | EXP-026 | HYP-020 | — | Fabricated data detection benchmark (S117, S120) | SPECIFIED | P1 |
| 27 | EXP-027 | — | — | Benchmark suite coverage audit (BMS-001 through BMS-012 cross-reference) | SPECIFIED | P1 |
| 28 | EXP-028 | HYP-018 | — | TonyCWang temperature schedule replication audit | SPECIFIED | P1 |
| 29 | EXP-029 | HYP-018 | — | TonyCWang dataset claim verification | SPECIFIED | P1 |
| 30 | EXP-030 | HYP-019 | — | MCP theorem citation verification (arXiv:1203.2285) | SPECIFIED | P1 |
| 31 | EXP-031 | HYP-019 | — | Source ID collision detection automation (4 clusters) | SPECIFIED | P1 |
| 32 | EXP-032 | HYP-018, HYP-019, HYP-020 | — | Adversarial hypothesis stress test | SPECIFIED | P1 |

---

## Experiment Details

### EXP-001: Conservative vs Warm-Start MCTS

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-001 (Conservative Ensemble), HYP-004 (Warm-Start MCTS) |
| **Ensemble** | ENS-001 (Solved-Game + Alpha-Beta), ENS-004 (Warm-Start MCTS) |
| **Purpose** | Test whether solved-game ensemble beats warm-start MCTS on 7x6 center-opening positions |
| **Independent variable** | Ensemble type (ENS-001 vs ENS-004) |
| **Dependent variables** | Win rate, draw rate, average game length, per-move latency |
| **Fixed controls** | 7x6 board, center opening, 2s/move, T4 hardware, 1000 center-opening positions |
| **Contenders** | ENS-001 (pure classical: solved-game + alpha-beta + fork detection), ENS-004 (warm-start MCTS: alpha-beta depth-4 + MCTS) |
| **Benchmark suites** | BMS-004 (fixed-opponent paired), BMS-005 (round robin) |
| **Board configs** | 7x6 only |
| **Sample size** | 1000 center-opening positions |
| **Metrics** | Win rate, draw rate, latency per move, simulation efficiency |
| **Expected outcome** | ENS-001 wins >80% (solved-game eliminates consistency problem) |
| **Falsification** | If ENS-001 wins <50% vs ENS-004, solved-game ensemble provides no advantage |
| **Compute** | T4 GPU (Kaggle), 2s/move, pure Python |
| **Reproducibility** | Seed all random operations; log all positions and moves |
| **Prerequisite research** | Optimal phase boundary for solved-game → search transition (DG-004) |
| **Status** | SPECIFIED |

---

### EXP-002: Adjacent-Opening Draw Detection

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-003 (Adjacent-Opening Draw Detection) |
| **Ensemble** | ENS-003 (Draw Detection Ensemble) |
| **Purpose** | Test whether draw-detection ensemble beats pure MCTS on adjacent-opening positions |
| **Independent variable** | Ensemble type (ENS-003 vs pure MCTS baseline) |
| **Dependent variables** | Draw rate, win rate, average game length, MCTS visit variance |
| **Fixed controls** | 7x6 board, adjacent opening (Col 3 or 5 for P1), 2s/move, 500 positions |
| **Contenders** | ENS-003 (draw detection: classical search for draw positions), connectpuct (pure MCTS baseline) |
| **Benchmark suites** | BMS-004 (fixed-opponent paired) |
| **Board configs** | 7x6 only |
| **Sample size** | 500 adjacent-opening positions |
| **Metrics** | Draw rate, win rate, MCTS visit variance |
| **Expected outcome** | ENS-003 achieves >60% draw rate; pure MCTS achieves <20% draw rate |
| **Falsification** | If ENS-003 draw rate <30%, draw-detection ensemble provides no advantage |
| **Compute** | T4 GPU (Kaggle), 2s/move |
| **Reproducibility** | Seed all random operations; log all positions |
| **Prerequisite research** | C139 validation (adjacent opening = draw) — DG-003 |
| **Status** | SPECIFIED |

---

### EXP-003: Warm-Start MCTS vs Pure MCTS

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-004 (MCTS Warm-Start) |
| **Ensemble** | ENS-004 (Warm-Start MCTS) |
| **Purpose** | Benchmark warm-start MCTS (alpha-beta depth-4 + MCTS) vs pure MCTS (1600 simulations) |
| **Independent variable** | Warm-start depth (0, 2, 4, 6 — alpha-beta depth) |
| **Dependent variables** | Win rate vs baseline MCTS, per-move latency, MCTS simulation efficiency |
| **Fixed controls** | Same total time budget, same random seed, same board positions, 1000 positions |
| **Contenders** | ENS-004 (warm-start MCTS variants), connectpuct (pure MCTS baseline) |
| **Benchmark suites** | BMS-004 (fixed-opponent paired), BMS-010 (ablation) |
| **Board configs** | 7x6 |
| **Sample size** | 1000 positions |
| **Metrics** | Win rate, latency, simulation count, simulation efficiency |
| **Expected outcome** | Warm-start MCTS wins >55% of games |
| **Falsification** | If warm-start wins <55%, warm-start provides no measurable advantage |
| **Compute** | T4 GPU (Kaggle), 2s/move, pure Python |
| **Reproducibility** | Seed all random operations; log warm-start depth used per position |
| **Prerequisite research** | Alpha-beta implementation with depth control |
| **Status** | SPECIFIED |

---

### EXP-004: MCTS Visit Variance Threshold

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-002 (High-Ceiling Ensemble) |
| **Ensemble** | ENS-002 (NN + MCTS + Classical) |
| **Purpose** | Measure MCTS visit variance threshold for confidence gating — at what variance does MCTS best move disagree with classical best? |
| **Independent variable** | MCTS visit variance threshold (0.1, 0.2, 0.3, 0.4, 0.5) |
| **Dependent variables** | Agreement rate between MCTS best and classical best, win rate |
| **Fixed controls** | Same positions, same simulation count, same board, 500 positions at varying game phases |
| **Contenders** | katac4 (MCTS with visit-count logging), ariaborin (classical engine) |
| **Benchmark suites** | BMS-010 (ablation) |
| **Board configs** | 7x6 |
| **Sample size** | 500 positions at varying game phases |
| **Metrics** | Visit variance, move agreement rate, win rate |
| **Expected outcome** | Threshold identified at visit variance > 0.3 where MCTS and classical disagree |
| **Falsification** | If no clear variance threshold exists, confidence gating is not useful for ENS-002 |
| **Compute** | T4 GPU (Kaggle), 2s/move |
| **Reproducibility** | Log all visit counts per move per position |
| **Prerequisite research** | MCTS implementation with visit-count logging; classical engine baseline |
| **Status** | BLOCKED — requires MCTS implementation with visit-count logging |

---

### EXP-005: Three-Way Hybrid Training and Benchmarking

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-002 (High-Ceiling Ensemble) |
| **Ensemble** | ENS-002 (NN + MCTS + Classical) |
| **Purpose** | Train and benchmark H-ENSEMBLE-002 (three-way hybrid) vs ENS-001 baseline |
| **Independent variables** | Training data (self-play vs TonyCWang dataset), NN architecture (ResNet vs MLP), board size (7x6, 8x8) |
| **Dependent variables** | Win rate vs ENS-001, NN minimax agreement rate, inference latency |
| **Fixed controls** | Same test set, same hardware (T4), 2s/move, ENS-001 baseline |
| **Contenders** | ENS-002 (three-way hybrid: solved-game + NN + MCTS + classical), ENS-001 (pure classical) |
| **Benchmark suites** | BMS-005 (round robin), BMS-010 (ablation) |
| **Board configs** | 7x6 primary; 8x8 secondary |
| **Sample size** | 1000-position test set |
| **Metrics** | Win rate, NN agreement rate, latency per layer, training time, loss curves |
| **Expected outcome** | Three-way hybrid wins >60% vs classical baseline |
| **Falsification** | If hybrid wins <55%, NN guidance + MCTS provides no advantage over classical search |
| **Compute** | T4 GPU (Kaggle); training: ~24 hours on T4; Inference: 2s/move |
| **Reproducibility** | Log training seed, loss curves, evaluation checkpoints, NN architecture |
| **Prerequisite research** | NN training pipeline specification (C163); TensorRT deployment; optimal phase boundaries |
| **Status** | BLOCKED — requires NN training pipeline and deployment infrastructure |

---

### EXP-006: MCP Theorem Verification

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-005 (Monte Carlo Perfectness Theorem) |
| **Ensemble** | — |
| **Purpose** | Verify Althöfer's Monte Carlo Perfectness theorem applies to Connect 4 — is Connect 4 a Monte Carlo Perfect game? |
| **Independent variable** | Theorem statement vs Connect 4 game properties |
| **Dependent variables** | Theorem applicability (yes/no); MCTS convergence bounds |
| **Fixed controls** | N/A (theoretical analysis) |
| **Contenders** | N/A (theoretical) |
| **Benchmark suites** | Informs BMS-003 (solver-oracle agreement) design |
| **Board configs** | All (theoretical result universal) |
| **Sample size** | N/A (theoretical) |
| **Metrics** | N/A (theoretical) |
| **Expected outcome** | Connect 4 is NOT a Monte Carlo Perfect game |
| **Falsification** | If Connect 4 is proven to be MCP, the MCTS consistency problem disappears |
| **Compute** | None (literature review) |
| **Reproducibility** | Document all sources and reasoning |
| **Prerequisite research** | Full-text of Althöfer 2012 MCP paper (S101); Asimov et al. 2014 (S102) |
| **Status** | SPECIFIED — research-only (literature review) |

---

### EXP-007: Automated Claim-Count Reconciliation

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Build automated claim-count reconciliation that reads all canonical files and flags discrepancies between research-state.md, claim-register.md header, and detail rows |
| **Independent variable** | File parser implementation, reconciliation algorithm |
| **Dependent variables** | Number of discrepancies found, false positive rate |
| **Fixed controls** | Same canonical files (claim-register.md, research-state.md, source-ledger.md) |
| **Contenders** | N/A |
| **Benchmark suites** | N/A |
| **Board configs** | N/A |
| **Sample size** | All claims in corpus (C001-C166) |
| **Metrics** | Discrepancy count, reconciliation accuracy |
| **Expected outcome** | Automated reconciliation matches manual audit from Worker 7 (SF-1 through SF-12) |
| **Falsification** | If automated reconciliation disagrees with manual audit on >5% of claims, algorithm needs revision |
| **Compute** | None (research-only — Markdown analysis script) |
| **Reproducibility** | Log all parsing decisions and flag reasons |
| **Prerequisite research** | Complete claim register from C001-C166 |
| **Status** | SPECIFIED |

---

### EXP-008: Source ID Namespace Isolation

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Implement source ID namespace isolation to prevent cross-round ID conflicts (S094-S098, S101-S102 overwritten by R23/R24, making R25 claims unreliable) |
| **Independent variable** | Namespace scheme (R27-S001 prefix vs. unique UUIDs vs. per-round section) |
| **Dependent variables** | Number of source ID conflicts eliminated, citation reliability |
| **Fixed controls** | Same source ledger (source-ledger.md) |
| **Contenders** | N/A |
| **Benchmark suites** | N/A |
| **Board configs** | N/A |
| **Sample size** | All sources in ledger (S001-S108+) |
| **Metrics** | Source ID conflict count before/after, citation error rate |
| **Expected outcome** | Zero source ID conflicts after namespace isolation |
| **Falsification** | If any source ID conflict persists after namespace isolation, scheme needs revision |
| **Compute** | None (research-only — Markdown restructuring) |
| **Reproducibility** | Log all source ID changes and migration decisions |
| **Prerequisite research** | Complete audit of all source IDs (S093-S098, S101-S102) and their round origins |
| **Status** | SPECIFIED |

### EXP-009: Three-Loss vs Two-Loss Ablation

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-009 (Three-Loss Objective Superiority) |
| **Ensemble** | ENS-002 (High-Ceiling NN+MCTS) |
| **Purpose** | Measure the contribution of the rival CE term (0.15× weight) in katac4's three-loss training objective |
| **Independent variable** | Loss function: two-loss (policy CE + 1.5× value CE) vs three-loss (policy CE + 1.5× value CE + 0.15× rival CE) |
| **Dependent variables** | MCTS win rate, policy accuracy on test set, value head correlation with MCTS results |
| **Fixed controls** | ResNet b3c128nbt architecture, training data, hyperparameters, 30K epochs, T4 hardware |
| **Contenders** | Two-loss model, three-loss model |
| **Benchmark suites** | BMS-010 (ablation), BMS-005 (round robin) |
| **Board configs** | 7x6 (default), 8x8 (generalization) |
| **Sample size** | 1,000 diverse positions against 5 different opponents |
| **Metrics** | Win rate, draw rate, loss rate, policy accuracy, value MAE |
| **Expected outcomes** | Three-loss model achieves ≥97% of two-loss model (small advantage) or ≥105% (meaningful advantage) |
| **Falsification criteria** | Two-loss model achieves ≥95% of three-loss model's win rate |
| **Compute** | RTX 5090 or equivalent; ~4 days per model |
| **Reproducibility** | Fixed random seed, identical architecture, pinned dependencies |
| **Prerequisite research** | Complete katac4 source analysis (S111, S115, S116) |
| **Status** | SPECIFIED |

### EXP-010: Temperature Schedule Comparison

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-010 (Temperature Schedule Threshold) |
| **Ensemble** | — |
| **Purpose** | Determine optimal temperature schedule boundary for Connect 4 self-play data generation |
| **Independent variable** | Temperature schedule: T=1.0 for first 10 moves vs T=1.0 for first 5 vs T=1.0 for all moves |
| **Dependent variables** | Policy accuracy on test set, training data diversity, downstream MCTS performance |
| **Fixed controls** | ResNet b3c128nbt architecture, Pascal Pons solver targets, 50 epochs |
| **Contenders** | Three temperature schedule variants |
| **Benchmark suites** | BMS-010 (ablation) |
| **Board configs** | 7x6 (default) |
| **Sample size** | 1,000-position test suite spanning early/mid/late game |
| **Metrics** | Policy accuracy, MCTS win rate, data diversity metric (entropy of move distribution) |
| **Expected outcomes** | T=1.0 for 10 moves is near-optimal; T=1.0 for 5 moves loses ≤3%; T=1.0 for all loses ≥10% |
| **Falsification criteria** | Any alternative schedule achieves ≥95% of T=1.0-for-10 model's policy accuracy |
| **Compute** | RTX 5090 or equivalent; ~1 day per model |
| **Reproducibility** | Fixed random seed, identical solver targets, pinned dependencies |
| **Prerequisite research** | TonyCWang dataset card analysis (S117), C151 verification |
| **Status** | SPECIFIED |

### EXP-011: AZAL Auxiliary Loss Training

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-009 (Three-Loss objective) + AZAL research |
| **Ensemble** | ENS-002 (High-Ceiling NN+MCTS) |
| **Purpose** | Test whether AZAL (AlphaZero Auxiliary Loss) improves oracle match rate over vanilla three-loss self-play training |
| **Independent variable** | Training: vanilla three-loss vs three-loss + AZAL auxiliary CE |
| **Dependent variables** | Oracle match rate (policy vs depth-18 solver), MCTS win rate, convergence speed |
| **Fixed controls** | ResNet b3c128nbt, 30K epochs, same replay buffer, same training data |
| **Contenders** | Vanilla three-loss, three-loss + AZAL |
| **Benchmark suites** | BMS-010 (ablation), BMS-012 (regression) |
| **Board configs** | 7x6 (default) |
| **Sample size** | Oracle match rate measured on 10,000 positions |
| **Metrics** | Oracle match rate, policy accuracy, convergence epochs |
| **Expected outcomes** | AZAL improves oracle match rate from ~0.785 to ≥0.85; vanilla three-loss at 0.785 |
| **Falsification criteria** | AZAL does not improve oracle match rate by ≥3 percentage points |
| **Compute** | 4×RTX 4090 or equivalent; ~8 days per model |
| **Reproducibility** | Fixed random seed, identical architecture, AZAL implementation from arXiv 2607.08984 |
| **Prerequisite research** | Read full AZAL paper (S114), implement auxiliary loss mechanism |
| **Status** | SPECIFIED |

### EXP-012: 80/20 Policy Prior Mixing Ratio

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-007 (NN Policy Prior replaces Dirichlet) + katac4 root expansion |
| **Ensemble** | ENS-002 (High-Ceiling NN+MCTS) |
| **Purpose** | Verify the optimal mixing ratio between NN policy prior and uniform exploration at MCTS root |
| **Independent variable** | Mixing ratio: 80/20 (katac4 standard) vs 90/10 vs 70/30 vs 100/0 |
| **Dependent variables** | MCTS convergence speed, win rate, move diversity, policy accuracy |
| **Fixed controls** | MCTS PUCT c_puct=1.0, same ResNet, same board positions |
| **Contenders** | Four mixing ratios |
| **Benchmark suites** | BMS-010 (ablation) |
| **Board configs** | 7x6 (default) |
| **Sample size** | 500 center-opening positions |
| **Metrics** | MCTS win rate, simulation-to-decision ratio, move diversity entropy |
| **Expected outcomes** | 80/20 is near-optimal; 100/0 (pure NN) may degrade diversity; 70/30 may add too much noise |
| **Falsification criteria** | Any alternative ratio achieves ≥95% of 80/20 model's win rate |
| **Compute** | T4 GPU; ~4 hours per model |
| **Reproducibility** | Fixed random seed, same MCTS implementation, pinned parameters |
| **Prerequisite research** | katac4 MCTS source analysis (S115) |
| **Status** | SPECIFIED |

### EXP-013: NeuralConnect4 vs katac4 Training Comparison

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-009 (Training objective comparison) |
| **Ensemble** | ENS-002 (High-Ceiling NN+MCTS) |
| **Purpose** | Compare NeuralConnect4 (ha22yx) self-play pipeline against katac4 pipeline on Connect 4 |
| **Independent variable** | Training pipeline: ha22yx NeuralConnect4 vs katac4 (ResNet b3c128nbt) |
| **Dependent variables** | MCTS win rate, oracle match rate, training convergence speed |
| **Fixed controls** | Same board (7x6), same MCTS engine, same test positions |
| **Contenders** | NeuralConnect4 (ha22yx), katac4 (GoodCoder666) |
| **Benchmark suites** | BMS-005 (round robin), BMS-010 (ablation) |
| **Board configs** | 7x6 (default), 8x8 (generalization) |
| **Sample size** | 500 paired games per board size |
| **Metrics** | Win/draw/loss rates, oracle match rate, training epochs to convergence |
| **Expected outcomes** | katac4 pipeline outperforms NeuralConnect4 by ≥5% due to three-loss objective and larger model |
| **Falsification criteria** | NeuralConnect4 achieves ≥95% of katac4 pipeline win rate |
| **Compute** | RTX 5090 or equivalent; ~5 days per pipeline |
| **Reproducibility** | Both sources available on GitHub (S109, S111) |
| **Prerequisite research** | Source code analysis of both pipelines |
| **Status** | SPECIFIED |

### EXP-014: Gemu03 Search+RL Hybrid Validation

| Field | Value |
|-------|-------|
| **Hypothesis** | Classical search + RL hybrid for ConnectX |
| **Ensemble** | — |
| **Purpose** | Validate whether Gemu03's Search+RL hybrid approach achieves better results than pure classical or pure NN on 7x6 |
| **Independent variable** | Strategy: Gemu03 hybrid vs classical alpha-beta vs NN-only (ResNet) |
| **Dependent variables** | Win rate, tactical error rate, endgame accuracy |
| **Fixed controls** | Same board (7x6), same time budget (2s/move), same opponents |
| **Contenders** | Gemu03 hybrid, classical alpha-beta, ResNet-only |
| **Benchmark suites** | BMS-004 (fixed-opponent paired), BMS-005 (round robin) |
| **Board configs** | 7x6 (default) |
| **Sample size** | 300 paired games per strategy pair |
| **Metrics** | Win/draw/loss rates, per-move latency, tactical error count |
| **Expected outcomes** | Gemu03 hybrid achieves ≥100% of classical (equal) and ≥110% of NN-only |
| **Falsification criteria** | Pure classical alpha-beta achieves ≥95% of Gemu03 hybrid win rate |
| **Compute** | Kaggle T4; source code available (S110) |
| **Reproducibility** | Gemu03 source available on GitHub |
| **Prerequisite research** | Source code analysis of Gemu03 |
| **Status** | SPECIFIED |

### EXP-015: MCTS Consistency Budget Analysis

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-005 (MCP Theorem), HYP-003 (Adjacent-Opening Draw) |
| **Ensemble** | — |
| **Purpose** | Measure how many MCTS simulations are needed for reasonable accuracy on solved-game positions |
| **Independent variable** | Simulation count: 100, 400, 800, 1600, 4000 |
| **Dependent variables** | Accuracy vs solved-game oracle, consistency rate, computational cost |
| **Fixed controls** | connectpuct MCTS engine, 7x6 center-opening positions |
| **Contenders** | Five simulation budgets |
| **Benchmark suites** | BMS-004 (fixed-opponent paired) |
| **Board configs** | 7x6 (default) |
| **Sample size** | 500 center-opening positions |
| **Metrics** | Oracle agreement rate, win/draw/loss accuracy, per-simulation cost |
| **Expected outcomes** | 800 simulations achieves ≥80% oracle agreement; 1600 achieves ≥90% |
| **Falsification criteria** | 4000 simulations achieves <90% oracle agreement on 7x6 |
| **Compute** | T4 GPU or equivalent; ~2 hours per budget |
| **Reproducibility** | connectpuct source (S094, S105) |
| **Prerequisite research** | C135-C142 (MCTS consistency problem), connectpuct analysis |
| **Status** | SPECIFIED |

---

### EXP-016: Adjacent-Opening MCTS Consistency Measurement

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-003 (Adjacent-Opening Draw Detection), HYP-014 (MCTS Simulation Budget Threshold) |
| **Ensemble** | — |
| **Purpose** | Measure MCTS performance on adjacent-opening positions (Col 3, 5) where optimal play is a draw. Test whether different MCTS implementations can identify draw positions. |
| **Independent variable** | MCTS implementation (connectpuct 80 sims, rowspire 4000 sims + NN, katac4 1600 sims + NN), simulation count |
| **Dependent variables** | Win rate vs optimal play, draw rate, oracle agreement rate, MCTS visit distribution |
| **Fixed controls** | 7x6 board, adjacent opening positions (Col 3 or 5 for P1's first move), Pascal Pons solver as oracle, 200 positions |
| **Contenders** | connectpuct (pure MCTS, 80 sims), rowspire (NN-guided MCTS, 4000 sims), katac4 (NN-guided MCTS, 1600 sims) |
| **Benchmark suites** | BMS-003 (solver-oracle agreement), BMS-005 (MCTS consistency on solved positions) |
| **Board configs** | 7x6 (default) |
| **Sample size** | 200 adjacent-opening positions |
| **Metrics** | Win rate, draw rate, loss rate, oracle agreement rate, visit distribution on optimal move |
| **Expected outcomes** | connectpuct <30% draw rate, rowspire ~50%, katac4 ~60%. Pure MCTS significantly underperforms NN-guided MCTS. |
| **Falsification criteria** | Any MCTS variant achieves ≥80% draw rate on adjacent openings (would contradict MCP theorem implications) |
| **Compute** | T4 GPU or equivalent; ~1 hour per MCTS variant |
| **Reproducibility** | connectpuct source (S118), rowspire source (S030), katac4 source (S091-S092) |
| **Prerequisite research** | C139 VERIFIED (adjacent opening = draw), C136-C142 (MCTS consistency problem), S118 (connectpuct benchmark) |
| **Status** | SPECIFIED |

---

### EXP-017: Adjacent-Opening Draw Detection Ensemble Validation

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-003 (Adjacent-Opening Draw Detection) |
| **Ensemble** | ENS-003 (Draw Detection Ensemble) |
| **Purpose** | Compare draw-detection ensemble (classify adjacent opening → enter draw-preserving alpha-beta) vs pure MCTS on adjacent-opening positions. |
| **Independent variable** | Strategy: ENS-003 draw-detection ensemble vs pure MCTS baseline |
| **Dependent variables** | Draw rate, win rate, game length, per-move latency |
| **Fixed controls** | 7x6 board, adjacent opening positions, 200 positions, 2s/move budget |
| **Contenders** | ENS-003 (draw detection: alpha-beta in draw-preserving mode), connectpuct (pure MCTS baseline) |
| **Benchmark suites** | BMS-004 (fixed-opponent paired) |
| **Board configs** | 7x6 (default) |
| **Sample size** | 200 adjacent-opening positions |
| **Metrics** | Draw rate, win rate, average game length, per-move latency |
| **Expected outcomes** | ENS-003 achieves ≥70% draw rate; pure MCTS <30% draw rate |
| **Falsification criteria** | ENS-003 draw rate <30% (would indicate draw-detection ensemble provides no advantage over pure MCTS) |
| **Compute** | T4 GPU or equivalent; ~1 hour |
| **Reproducibility** | ENS-003 design documented in ensemble-catalog.md; connectpuct source available |
| **Prerequisite research** | C139 VERIFIED (adjacent opening = draw), HYP-003 (Adjacent-Opening Draw Detection) |
| **Status** | SPECIFIED |

---

### EXP-018: NN-Guided vs Random-Playout MCTS on Adjacent Openings

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-005 (MCP Theorem), HYP-014 (MCTS Simulation Budget Threshold) |
| **Ensemble** | — |
| **Purpose** | Controlled comparison to test whether NN-guided playouts (rowspire, katac4) escape the MCP consistency constraint compared to vanilla MCTS (connectpuct). |
| **Independent variable** | MCTS playout quality: random (connectpuct), NN-guided (rowspire, katac4) |
| **Dependent variables** | Draw rate on adjacent openings, oracle agreement rate, visit distribution on draw-identifying moves |
| **Fixed controls** | 7x6 board, adjacent opening positions, comparable simulation counts, 200 positions |
| **Contenders** | connectpuct (random playouts, 80 sims), rowspire (NN-guided, 4000 sims), katac4 (NN-guided, 1600 sims) |
| **Benchmark suites** | BMS-003 (solver-oracle agreement), BMS-005 (MCTS consistency) |
| **Board configs** | 7x6 (default) |
| **Sample size** | 200 adjacent-opening positions |
| **Metrics** | Draw rate, oracle agreement rate, MCTS visit distribution, policy accuracy at root |
| **Expected outcomes** | NN-guided MCTS achieves ≥20% higher draw rate than vanilla MCTS on adjacent openings. Supports hypothesis that MCP theorem's assumption of random playouts is key to the consistency problem. |
| **Falsification criteria** | NN-guided MCTS does not significantly outperform vanilla MCTS on adjacent openings (would suggest consistency problem is not driven by playout quality) |
| **Compute** | T4 GPU or equivalent; ~2 hours total |
| **Reproducibility** | All sources available: connectpuct (S118), rowspire (S030), katac4 (S091-S092) |
| **Prerequisite research** | C136 (MCP theorem), C139 (adjacent opening = draw), S118 (connectpuct benchmark) |
| **Status** | SPECIFIED |

---

### EXP-019: Kamide/connect-n Adaptive Scoring Minimax Benchmark

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Benchmark Kamide/connect-n adaptive scoring minimax engine against existing classical baselines on 7x6 and configurable N×N boards |
| **Independent variable** | Board size (7×6, configurable N×N), connection-length scoring parameters, hole-count weights |
| **Dependent variables** | Win rate vs opponent baselines, per-move latency, tactical accuracy |
| **Fixed controls** | Same opponents, same time budget (2s/move Kaggle), same test positions |
| **Contenders** | Kamide/connect-n (adaptive scoring minimax + alpha-beta, TypeScript Web Worker), Kamide/connect-n on 7×6, 8×8, 10×10 |
| **Benchmark suites** | BMS-004 (fixed-opponent paired), BMS-006 (board-size coverage) |
| **Board configs** | 7×6 (default), 8×8, configurable N×N |
| **Sample size** | 300 paired games per board size |
| **Metrics** | Win/draw/loss rates, per-move latency, fork detection accuracy, evaluation function variance |
| **Expected outcomes** | Kamide competitive with classical baselines on 7×6; performance degrades gracefully on larger boards |
| **Falsification criteria** | Kamide achieves <50% win rate vs classical baselines on 7×6 |
| **Compute** | Kaggle T4 (Web Worker deployment); ~1 hour |
| **Reproducibility** | Source available on GitHub (S123) |
| **Prerequisite research** | Kamide source code analysis (S123), adaptive scoring function parameters |
| **Status** | SPECIFIED |

---

### EXP-020: Tromp fhourstones88 Search System Validation

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Validate Tromp fhourstones88 as a reference classical engine: standard full-window alpha-beta, 8.3M-entry dual-lock TT, history-heuristic move ordering, 15-ply book88 opening book |
| **Independent variable** | TT size (8.3M entries), opening book depth (15 ply), history-heuristic parameters |
| **Dependent variables** | Search speed, fork detection rate, book hit rate, oracle agreement |
| **Fixed controls** | 8×8 board (fhourstones88 target), same test positions |
| **Contenders** | Tromp fhourstones88 (C++ search system), Pascal Pons search.cpp (C++ negamax with alpha-beta) |
| **Benchmark suites** | BMS-003 (solver-oracle agreement), BMS-004 (fixed-opponent paired) |
| **Board configs** | 8×8 (default, fhourstones88 target), 7×6 (secondary) |
| **Sample size** | 500 test positions |
| **Metrics** | Oracle agreement rate, TT hit rate, book hit rate, fork detection accuracy, nodes per second |
| **Expected outcomes** | Tromp achieves ≥90% oracle agreement on solved 8×8 positions; dual-lock TT reduces corruption rate below 1% |
| **Falsification criteria** | Tromp achieves <70% oracle agreement without iterative deepening (would suggest dual-lock TT is insufficient) |
| **Compute** | CPU; ~2 hours |
| **Reproducibility** | Source available on GitHub (S124, S126) |
| **Prerequisite research** | Tromp source code analysis (S124), Pascal Pons analysis (S126) |
| **Status** | SPECIFIED |

---

### EXP-021: MTD(f) and PVS Gap Investigation

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Investigate whether MTD(f) and PVS exist in any non-corpus Connect 4 engines; C193-C194 confirmed no MTD(f)/PVS in Tromp, so search externally |
| **Independent variable** | Alpha-beta variant: standard, PVS (null-window), MTD(f) (marginal) |
| **Dependent variables** | Search speedup vs standard AB, node count reduction, depth reached in fixed time |
| **Fixed controls** | Same board, same TT, same move ordering |
| **Contenders** | N/A (implementation investigation) |
| **Benchmark suites** | Informs BMS-008 (optimization comparison) |
| **Board configs** | 7×6 (default) |
| **Sample size** | 100 test positions |
| **Metrics** | Nodes per second, depth reached, speedup ratio vs standard AB |
| **Expected outcomes** | PVS provides 10–30% speedup; MTD(f) provides additional 15–50% speedup |
| **Falsification criteria** | PVS or MTD(f) provides <5% speedup over standard alpha-beta in any Connect 4 engine |
| **Compute** | CPU; ~1 hour |
| **Reproducibility** | Implement all three variants with identical TT and move ordering |
| **Prerequisite research** | C193 (no MTD(f) in Tromp), C194 (no PVS in Tromp), Tromp source analysis (S124) |
| **Status** | SPECIFIED |

---

### EXP-022: Board Representation Comparison Across Kaggle Implementations

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Compare board representations across documented Kaggle implementations: Tromp (64-bit), Kamide (TypeScript 2D array), pyvezi (bitmask), connectpuct (Python list of lists) |
| **Independent variable** | Board representation: 64-bit integer, bitmask, 2D array, list of lists |
| **Dependent variables** | Move generation speed, legal move check latency, fork detection overhead |
| **Fixed controls** | 7×6 board, same move ordering, same evaluation function |
| **Contenders** | Tromp (64-bit, S124), Kamide (TypeScript 2D array, S123), pyvezi (bitmask, S125), connectpuct (Python list of lists, S118) |
| **Benchmark suites** | BMS-006 (board-size coverage) |
| **Board configs** | 7×6 (default), 8×8 (secondary) |
| **Sample size** | 1000 position evaluations per representation |
| **Metrics** | Nodes per second, move generation time, legal move check time |
| **Expected outcomes** | Bitmask/64-bit representations ≥2× faster than array-based on 7×6; TypeScript 2D array competitive with Python list of lists |
| **Falsification criteria** | No representation shows statistically significant speed advantage |
| **Compute** | CPU; ~30 minutes |
| **Reproducibility** | All implementations available on GitHub |
| **Prerequisite research** | Worker-03-job-00016 board representation comparison (R32) |
| **Status** | SPECIFIED |

---

### EXP-023: Board-Size-Adaptive Ensemble Routing Protocol Validation

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-017 (TT-MCTS Cache Sharing) |
| **Ensemble** | ENS-013 (NN-Prior MCTS, board-size-adaptive routing) |
| **Purpose** | Test whether board-size-adaptive ensemble routing (classical on 7×6, NN-guided MCTS on 8×8+) outperforms fixed-strategy ensemble |
| **Independent variable** | Routing protocol: fixed-classical, fixed-NN-MCTS, board-size-adaptive (ENS-013) |
| **Dependent variables** | Win rate, oracle agreement, per-move latency, TT hit rate |
| **Fixed controls** | Same components, same time budget, same opponents |
| **Contenders** | ENS-013 (board-size-adaptive routing), classical baseline (Kamide, pyvezi), NN-MCTS baseline (rowspire, katac4) |
| **Benchmark suites** | BMS-006 (board-size coverage), BMS-007 (hybrid tournament) |
| **Board configs** | 7×6, 8×8, 10×10 |
| **Sample size** | 200 positions per board size |
| **Metrics** | Win rate, draw rate, oracle agreement, routing decision accuracy |
| **Expected outcomes** | ENS-013 achieves ≥5% win rate advantage over fixed-classical on 8×8; ≥95% oracle agreement on 7×6 |
| **Falsification criteria** | Board-size-adaptive routing provides <2% win rate advantage over fixed-classical |
| **Compute** | T4 GPU or equivalent; ~2 hours |
| **Reproducibility** | All components specified in ENS-013 |
| **Prerequisite research** | ENS-013 detailed design (board-size-adaptive routing protocol), C139 (adjacent opening draw), C184-C192 (component specifications) |
| **Status** | SPECIFIED |

---

### EXP-024: Kamide Web Worker Deployment Constraints Study

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Study Kamide/connect-n's Web Worker non-blocking inference pattern and its applicability to Kaggle ConnectX environment |
| **Independent variable** | Web Worker offloading strategy: synchronous, asynchronous with timeout, hybrid |
| **Dependent variables** | Move latency, timeout rate, worker crash rate, Kaggle compatibility |
| **Fixed controls** | Kamide engine, same board positions |
| **Contenders** | Kamide (Web Worker, S123), Kamide (synchronous, non-Worker) |
| **Benchmark suites** | BMS-008 (timeout/latency constraints), BMS-011 (Kaggle-environment emulation) |
| **Board configs** | 7×6 (default) |
| **Sample size** | 300 positions |
| **Metrics** | Move latency, timeout rate, worker crash rate, Kaggle API compatibility |
| **Expected outcomes** | Web Worker offloading reduces perceived latency by ≥50%; no Kaggle API conflicts |
| **Falsification criteria** | Web Worker approach introduces ≥10% timeout rate in Kaggle environment |
| **Compute** | Kaggle notebook environment; ~1 hour |
| **Reproducibility** | Kamide source available on GitHub (S123, S125) |
| **Prerequisite research** | Kamide source code analysis (S123), Web Worker deployment analysis (S125) |
| **Status** | SPECIFIED |

---

### EXP-025: Corpus Governance Audit Automation

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Automate corpus governance audit: detect round number fragmentation, claim-count inconsistencies, source ID collisions, and stale metadata across canonical files |
| **Independent variable** | Audit tool: manual (R27-R32), automated script (Python/PowerShell Markdown parser) |
| **Dependent variables** | Number of structural defects found, false positive rate, audit speed |
| **Fixed controls** | Same canonical files (all under research/) |
| **Contenders** | N/A |
| **Benchmark suites** | N/A (research-only) |
| **Board configs** | N/A |
| **Sample size** | All canonical files in research/ |
| **Metrics** | Defect count, audit time, discrepancy match rate with manual audits |
| **Expected outcomes** | Automated audit matches manual R32 findings on ≥95% of defects |
| **Falsification criteria** | Automated audit disagrees with manual R32 audit on >10% of structural defects |
| **Compute** | CPU; ~10 minutes |
| **Reproducibility** | Audit script reads Markdown files directly; deterministic output |
| **Prerequisite research** | R32 structural defect catalog (SF-001 through SF-005), source ID collision catalog |
| **Status** | SPECIFIED |

---

### EXP-026: Fabricated Data Detection Benchmark

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-020 (Fabricated Data Detection in Corpus) |
| **Ensemble** | — |
| **Purpose** | Validate that automated fabrication detection (phase-distribution analysis, source-methodology cross-referencing, claim-evidence alignment) identifies known-fabricated entries (S117, S120) |
| **Independent variable** | Detection method: phase-distribution analysis, source-methodology cross-ref, claim-evidence alignment, combined |
| **Dependent variables** | True positive rate, false positive rate, detection latency |
| **Fixed controls** | Known corpus with injected fabrication (S117, S120, 3 clean sources) |
| **Contenders** | N/A (research tool evaluation) |
| **Benchmark suites** | BMS-012 (reproducibility) — corpus verification |
| **Board configs** | N/A |
| **Sample size** | 20 known-source audit targets |
| **Metrics** | True positive rate, false positive rate, detection latency |
| **Expected outcomes** | Combined detection achieves ≥95% true positive rate on known fabrications; ≤2% false positive on clean sources |
| **Falsification** | If detection achieves <95% true positive on S117/S120, fabrication detection framework insufficient |
| **Compute** | CPU; ~30 minutes |
| **Reproducibility** | All detection rules and corpus sources deterministic |
| **Prerequisite research** | R33 fabricated data findings (S117, S120), source ID collision catalog (4 clusters) |
| **Status** | SPECIFIED |

---

### EXP-027: Benchmark Suite Coverage Audit

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Audit that all 12 benchmark suites (BMS-001 through BMS-012) are cross-referenced by at least one experiment in the future experiment backlog |
| **Independent variable** | Audit tool: manual, automated |
| **Dependent variables** | Number of BMS-### with ≥1 referencing experiment, audit speed |
| **Fixed controls** | All benchmark-blueprint.md and future-experiment-backlog.md files |
| **Contenders** | N/A |
| **Benchmark suites** | N/A (research-only) |
| **Board configs** | N/A |
| **Sample size** | 12 benchmark suite entries |
| **Metrics** | Cross-reference coverage rate, audit time |
| **Expected outcomes** | All 12 BMS-### have ≥1 experiment reference |
| **Falsification** | If >2 BMS suites lack experiment references, benchmark-experiment coupling is incomplete |
| **Compute** | CPU; ~10 minutes |
| **Reproducibility** | Markdown parser reads both files deterministically |
| **Prerequisite research** | R33 benchmark blueprint completion (BMS-007 through BMS-012) |
| **Status** | SPECIFIED |

---

### EXP-028: TonyCWang Temperature Schedule Replication Audit

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-018 (Phase-Bias in Self-Play Data Generation) |
| **Ensemble** | — |
| **Purpose** | Independently replicate TonyCWang's temperature schedule (T=1.0→T=0.5) and verify claimed phase distribution (40-40-20 opening-midgame-endgame) against actual self-play output |
| **Independent variable** | Temperature schedule: TonyCWang (T=1.0→T=0.5), pure random (T=∞), fixed temperature (T=1.0), fixed temperature (T=0.5) |
| **Dependent variables** | Phase distribution (opening/midgame/endgame move counts), position diversity, game length |
| **Fixed controls** | Same starting position, same board size (7×6), same number of games (1000) |
| **Contenders** | TonyCWang (temperature schedule), random-playout baseline |
| **Benchmark suites** | BMS-002 (tactical position suite) |
| **Board configs** | 7×6 |
| **Sample size** | 1000 games per temperature schedule |
| **Metrics** | Phase distribution percentages, position entropy, average game length |
| **Expected outcomes** | TonyCWang schedule produces non-uniform phase distribution; pure random over-represents endgame positions |
| **Falsification** | If TonyCWang schedule produces uniform phase distribution, temperature schedule does not create phase bias |
| **Compute** | Kaggle notebook; ~4 hours |
| **Reproducibility** | All random seeds fixed; game logs saved |
| **Prerequisite research** | R33 TonyCWang verification (S120, fabricated data, temperature schedule vs uniform random) |
| **Status** | SPECIFIED |

---

### EXP-029: TonyCWang Dataset Claim Verification

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-018 (Phase-Bias in Self-Play Data Generation) |
| **Ensemble** | — |
| **Purpose** | Verify TonyCWang's reported model accuracy improvements across board sizes and temperature schedules against independent re-measurement |
| **Independent variable** | Board size (5×4, 6×5, 7×6), temperature schedule step |
| **Dependent variables** | Model accuracy, phase distribution, self-play agreement rate |
| **Fixed controls** | Same architecture (ResNet-19 equivalent), same dataset split |
| **Contenders** | TonyCWang reported values, re-measured values |
| **Benchmark suites** | BMS-001 (API, legality), BMS-007 (board-size generalization) |
| **Board configs** | 5×4, 6×5, 7×6 |
| **Sample size** | 1000 test positions per board size |
| **Metrics** | Model accuracy, claim agreement rate, phase distribution |
| **Expected outcomes** | Re-measured accuracy within ±5% of TonyCWang reported values on 7×6; larger deviations on smaller boards |
| **Falsification** | If re-measured accuracy deviates >10% from TonyCWang on any board size, claimed accuracy values unreliable |
| **Compute** | Kaggle notebook; ~8 hours |
| **Reproducibility** | TonyCWang dataset available; deterministic evaluation on fixed test set |
| **Prerequisite research** | R33 TonyCWang verification, S120 methodology review |
| **Status** | SPECIFIED |

---

### EXP-030: MCP Theorem Citation Verification

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-019 (Source Attribution Integrity) |
| **Ensemble** | — |
| **Purpose** | Verify arXiv:1203.2285 citation used in MCP theorem claim (C136). Confirm actual paper topic (astrophysics per R33 finding) vs claimed topic (game theory/MCTS convergence) |
| **Independent variable** | Citation source: arXiv:1203.2285, actual game-theory MCP theorem sources |
| **Dependent variables** | Citation accuracy, claim validity, MCP theorem statement correctness |
| **Fixed controls** | arXiv API, MCP theorem literature |
| **Contenders** | N/A |
| **Benchmark suites** | N/A (research-only) |
| **Board configs** | N/A |
| **Sample size** | 1 arXiv paper + 3 verified MCP theorem sources |
| **Metrics** | Citation accuracy (correct/incorrect), topic match rate |
| **Expected outcomes** | arXiv:1203.2285 confirmed as astrophysics; no game-theory MCP theorem in that paper |
| **Falsification** | If arXiv:1203.2285 actually discusses MCP theorem, R33 finding is incorrect |
| **Compute** | CPU; ~5 minutes |
| **Reproducibility** | arXiv API query; deterministic paper metadata extraction |
| **Prerequisite research** | R33 finding (SF-001: arXiv:1203.2285 = astrophysics paper) |
| **Status** | SPECIFIED |

---

### EXP-031: Source ID Collision Detection Automation

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-019 (Source Attribution Integrity) |
| **Ensemble** | — |
| **Purpose** | Build and test automated source ID collision detection: verify all 4 collision clusters (S091-S093, S094-S097, S109-S117, S118-S120) are detected without manual inspection |
| **Independent variable** | Detection scope: intra-round, cross-round, global sequential |
| **Dependent variables** | Collision clusters detected, false positive rate, detection time |
| **Fixed controls** | All source ledger entries, all round reports |
| **Contenders** | N/A |
| **Benchmark suites** | N/A (research-only) |
| **Board configs** | N/A |
| **Sample size** | All source IDs in source-ledger.md |
| **Metrics** | Collision clusters found, detection accuracy, audit speed |
| **Expected outcomes** | Automated detection finds all 4 known collision clusters with 0 false positives |
| **Falsification** | If automated detection misses ≥1 known cluster, detection tool is incomplete |
| **Compute** | CPU; ~5 minutes |
| **Reproducibility** | Source ledger is structured Markdown; deterministic parsing |
| **Prerequisite research** | R33 source ID collision audit (4 clusters, 27+ colliding IDs) |
| **Status** | SPECIFIED |

---

### EXP-032: Adversarial Hypothesis Stress Test

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-018 (Phase-Bias), HYP-019 (Source Attribution), HYP-020 (Fabricated Data) |
| **Ensemble** | — |
| **Purpose** | Design and run adversarial stress tests: attempt to falsify each R33 hypothesis with alternative explanations, verify evidence is sufficient and not merely suggestive |
| **Independent variable** | Hypothesis under test: HYP-018, HYP-019, HYP-020 |
| **Dependent variables** | Alternative explanations proposed, evidence gaps identified, hypothesis status (PROPOSED→RESEARCHING, etc.) |
| **Fixed controls** | Existing evidence catalog, claim register, source ledger |
| **Contenders** | N/A (research-only adversarial review) |
| **Benchmark suites** | N/A (research-only) |
| **Board configs** | N/A |
| **Sample size** | 3 hypotheses × N alternative explanations each |
| **Metrics** | Alternative explanations per hypothesis, evidence confidence changes |
| **Expected outcomes** | Each hypothesis survives ≥1 adversarial pass without status downgrade |
| **Falsification** | If any R33 hypothesis fails adversarial stress test, its evidence is insufficient for current status |
| **Compute** | Research-only (no code execution) |
| **Reproducibility** | Adversarial review protocol documented; deterministic evidence evaluation |
| **Prerequisite research** | R33 hypothesis entries (HYP-018, HYP-019, HYP-020), R33 corpus corrections |
| **Status** | SPECIFIED |

---

### EXP-033: Automated Corpus Governance Audit Tool

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-019 (Source attribution integrity), HYP-020 (Fabricated data detection) |
| **Ensemble** | — |
| **Purpose** | Build Python Markdown parser that reads all canonical files and detects: (a) round number fragmentation, (b) claim count discrepancies, (c) source ID collisions, (d) stale metadata |
| **Independent variable** | Audit tool: automated vs manual GOV-001 findings |
| **Dependent variables** | Detection true positive rate, false positive rate, processing time |
| **Fixed controls** | Corpus state as of R34, all 19 canonical files |
| **Contenders** | GOV-001 manual audit (baseline), automated tool (experimental) |
| **Benchmark suites** | BMS-025 (automated corpus governance audit) |
| **Board configs** | N/A (governance audit, not game play) |
| **Sample size** | 22 known defects from GOV-001 |
| **Metrics** | True positive rate (should be ≥95%), false positive rate (should be ≤2%), processing time |
| **Expected outcomes** | Automated tool detects ≥95% of GOV-001's 22 findings |
| **Falsification criteria** | Automated tool detects <80% of known defects |
| **Compute** | Local CPU; ~30 minutes |
| **Reproducibility** | Deterministic Markdown parsing; same corpus state produces same results |
| **Prerequisite research** | GOV-001 dossier (F-001 through F-022 findings) |
| **Status** | SPECIFIED |

### EXP-034: Source ID Namespace Migration Test

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-019 (Source attribution integrity) |
| **Ensemble** | — |
| **Purpose** | Apply R34-S001 namespace scheme to S091–S120 collision cluster A and verify zero remaining collisions |
| **Independent variable** | ID format: sequential (S091–S120) vs round-scoped (R34-S001–R34-S030) |
| **Dependent variables** | Collision count, cross-reference accuracy |
| **Fixed controls** | Collision cluster A (S091–S093), claim register references |
| **Contenders** | Sequential IDs (baseline), round-scoped IDs (experimental) |
| **Benchmark suites** | BMS-027 (source ID collision detection) |
| **Board configs** | N/A |
| **Sample size** | 27+ colliding IDs across 4 clusters |
| **Metrics** | Collision count (expected: 0 after migration) |
| **Expected outcomes** | 0 collisions after R34-S001 migration |
| **Falsification criteria** | Migration introduces new collisions or breaks existing cross-references |
| **Compute** | Local CPU; ~15 minutes |
| **Reproducibility** | Deterministic ID generation; same source produces same mapped IDs |
| **Prerequisite research** | GOV-001 F-001 (source ID collisions), namespace isolation schema |
| **Status** | SPECIFIED |

### EXP-035: Fabricated Data Detection Benchmark

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-020 (Fabricated data detection) |
| **Ensemble** | — |
| **Purpose** | Validate that automated detection rules identify S117 (40-40-20 phase distribution) and S120 (uniform random) as fabricated when applied to a corpus with 2 injected fabrications and 18 clean sources |
| **Independent variable** | Detection method: regex-based vs semantic analysis |
| **Dependent variables** | True positive rate, false positive rate, processing time |
| **Fixed controls** | 20 known sources (2 fabricated, 18 clean), corpus files |
| **Contenders** | Regex detection (baseline), semantic analysis (experimental) |
| **Benchmark suites** | BMS-026 (fabricated data detection benchmark) |
| **Board configs** | N/A |
| **Sample size** | 20 sources (2 injected fabrications) |
| **Metrics** | True positive rate (≥95%), false positive rate (≤2%) |
| **Expected outcomes** | Both detection methods identify 40-40-20 and "uniform random" as fabricated |
| **Falsification criteria** | Detection method fails to identify ≥1 of 2 injected fabrications |
| **Compute** | Local CPU; ~10 minutes |
| **Reproducibility** | Deterministic detection rules; same corpus produces same results |
| **Prerequisite research** | GOV-001 F-002 (fabricated data), S117/S120 retraction |
| **Status** | SPECIFIED |

### EXP-036: Master Report Staleness Impact Analysis

| Field | Value |
|-------|-------|
| **Hypothesis** | HYP-019 (Source attribution integrity) |
| **Ensemble** | — |
| **Purpose** | Compare RESEARCH_REPORT.md recommendations (based on R29 data) against current R34 findings to identify ≥3 recommendations that should be updated |
| **Independent variable** | Report version: R29 (stale) vs R35 (current) |
| **Dependent variables** | Number of outdated recommendations, accuracy delta |
| **Fixed controls** | Same research domain (ConnectX bot architecture) |
| **Contenders** | R29 report (stale baseline), R35 report (current) |
| **Benchmark suites** | BMS-028 (header consistency validation) |
| **Board configs** | N/A |
| **Sample size** | 14 recommendations across RESEARCH_REPORT.md |
| **Metrics** | Outdated recommendations count (expected: ≥3) |
| **Expected outcomes** | ≥3 recommendations from R29 report should be updated based on R30–R34 findings |
| **Falsification criteria** | R29 report is ≥90% accurate (suggests staleness is less impactful than assessed) |
| **Compute** | Research-only (read and compare); ~1 hour |
| **Reproducibility** | Deterministic comparison; same report versions produce same delta |
| **Prerequisite research** | GOV-001 F-003 (master report staleness), R29 and R35 RESEARCH_REPORT.md |
| **Status** | SPECIFIED |

### EXP-037: Dossier Production Throughput Measurement

| Field | Value |
|-------|-------|
| **Hypothesis** | — |
| **Ensemble** | — |
| **Purpose** | Measure time required to produce a single-entry dossier (source analysis, algorithm extraction, pros/cons, feasibility matrix) from a public GitHub repository |
| **Independent variable** | Source complexity: simple repo (≤10 files) vs complex repo (100+ files) |
| **Dependent variables** | Time per dossier, word count per dossier, citation count |
| **Fixed controls** | Research-only phase, read-only web access, same synthesis protocol |
| **Contenders** | Simple repo, complex repo |
| **Benchmark suites** | — |
| **Board configs** | N/A |
| **Sample size** | 5 repos across complexity spectrum |
| **Metrics** | Minutes per dossier, words per dossier, citations per dossier |
| **Expected outcomes** | 30–90 minutes per dossier with read-only web access |
| **Falsification criteria** | Average dossier production exceeds 4 hours (suggests different approach needed) |
| **Compute** | Research-only; ~5 hours total |
| **Reproducibility** | Same protocol; deterministic output per source |
| **Prerequisite research** | GOV-001 F-007 (empty/missing dossier directories), dossier production plan |
| **Status** | SPECIFIED |

---

## Priority Classification

| Priority | Criteria |
|----------|----------|
| **P0** | Critical for ensemble validation; gates future experiments |
| **P1** | Important for research progress; does not gate other experiments |
| **P2** | Valuable but not urgent; can be deferred if needed |

## Notes

- No experiment is executed during the research-only phase
- EXP-006 and EXP-007/008 are research-only (literature review, corpus hygiene)
- EXP-001/002/003/004/005 require implementation phase to execute
- All experiments reference specific benchmark suites (BMS-###) from benchmark-blueprint.md
- All experiments reference specific hypotheses (HYP-###) from hypothesis-register.md

---

*Backlog created: Round 27. Total experiments: 37 (EXP-001 through EXP-032). SPECIFIED: 30, BLOCKED: 2, DEFERRED: 0, READY_FOR_IMPLEMENTATION: 0, RETIRED: 0. R28 added EXP-009 through EXP-015 (7 new experiments from W04/W05 neural MCTS and ensemble research). R30 added EXP-016 through EXP-018 (3 new adjacent-opening MCTS experiments from W04). R32 added EXP-019 through EXP-025 (7 new experiments: Kamide benchmark, Tromp validation, MTD(f)/PVS gap, board representation comparison, ENS-013 routing, Web Worker constraints, corpus governance automation). R33 added EXP-026 through EXP-032 (7 new experiments: fabrication detection, benchmark coverage audit, TonyCWang replication/verification, MCP theorem citation verification, source ID collision detection, adversarial hypothesis stress test). R35 added EXP-033 through EXP-037 (5 new governance experiments: automated corpus audit, source ID namespace migration, fabricated data detection, master report staleness impact, dossier production throughput). R37 added BMS-011 (Neural MCTS parameter sweep), BMS-012 (NN inference latency profiling), BMS-013 (Neural MCTS vs Classical Search comparison), EXP-CS-001 through EXP-CS-003 (classical search experiments: TT hit rate, LMR reduction tables, fork detection), EXP-NEW-001 (CogitoNTNU self-play reproduction).* R41 added EXP-NEW-001 through EXP-NEW-006 (6 new experiments: MCTS consistency test, board-size scaling measurement, race detection, latency profiling, seat-reversal bias test, time allocation optimization). R41 added BMS-029 through BMS-035 (7 new benchmark suites: MCP consistency analysis, board-size scaling validation, race-condition detection, latency budget audit, seat-reversal bias test, time-allocation benchmark, statistical power analysis). Total experiments: 43 (EXP-001 through EXP-037, EXP-NEW-001 through EXP-NEW-006). Total benchmark suites: 19 (BMS-001 through BMS-012, BMS-029 through BMS-035).
