# Future Experiment Backlog — ConnectX Bot v9

> **Created**: 2026-08-03 (Round 27)
> **Purpose**: Records all future empirical work. No experiments executed during research-only phase.
> **Total experiments**: 15 (8 from R27 + 7 from R28: EXP-009 through EXP-015 from W04/W05 neural MCTS and ensemble research)
> **All statuses**: DEFERRED or SPECIFIED — no experiment may be marked completed in research-only phase.

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

*Backlog created: Round 27. Total experiments: 18 (EXP-001 through EXP-018). SPECIFIED: 16, BLOCKED: 2, DEFERRED: 0, READY_FOR_IMPLEMENTATION: 0, RETIRED: 0. R28 added EXP-009 through EXP-015 (7 new experiments from W04/W05 neural MCTS and ensemble research). R30 added EXP-016 through EXP-018 (3 new adjacent-opening MCTS experiments from W04).*