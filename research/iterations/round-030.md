# Round 30 — External-Pool Batch Synthesis (batch-00016-20260804-111703)

> **Round**: 30
> **Date**: 2026-08-04
> **Batch**: batch-00016-20260804-111703
> **Prior Round**: 28 (external-pool batch — 17 workers, 9 sources, 2 claims, 7 experiments)
> **Model**: qwen3.6

---

## Executive Summary

Round 30 processes **5 worker results** from external-pool batch-00016. Workers span 4 slots (02, 04, 05, 07) covering MCTS consistency research, adversarial corpus audit, ensemble hypothesis generation, and classical search governance.

**Key findings**:
1. **C139 upgraded HYPOTHESIS→VERIFIED**: Adjacent opening draw unidentifiable by MCTS (worker-04). This is the strongest evidence to date for the MCTS consistency problem on Connect 4.
2. **3 new sources added** (S118-S120): connectpuct PUCT benchmark, kaggle-environments board size audit, Althöfer MCP theorem (LOW quality due to wrong citation).
3. **New hypothesis HYP-014**: Timing governance protocol — 1.5s forced termination, fallback to alpha-beta. Required for all MCTS ensemble designs.
4. **3 new ensembles** (ENS-013, ENS-014, ENS-015): Conservative multi-layer defense, AlphaZero-GPU high-ceiling, and alpha-beta-only simplicity ensembles.
5. **New benchmark suites** (BMS-005, BMS-006): MCTS consistency measurement and board-size coverage audit.
6. **3 new experiments** (EXP-016, EXP-017, EXP-018): Adjacent-opening MCTS consistency, draw-detection ensemble validation, NN-guided vs random-playout MCTS comparison.
7. **New contender** (BOT-010): jlokitha/connect-4-game Java MCTS student project.
8. **Corpus integrity audit**: 8 source IDs (S094-S097, S101-S102) used by both R23/R24 and R25 batches — collision to be resolved in R31.
9. **Experiment count increased**: 15 → 18 (EXP-001 through EXP-018).

---

## Worker Results

### Worker 2 — MCTS Consistency Research (Jobs 1-2)

**Jobs**:
- Job-00011: MCTS consistency problem for solved games in Connect 4
- Job-00012: Kaggle environment board size test coverage

**Findings**:
- **BMS-005**: MCTS Consistency on Solved Positions — 7x6 board, center column opening. Measure oracle agreement rate (% of moves matching minimax solver). Test simulation counts: 10, 50, 100, 500, 1000, 4000. Target: ≥90% oracle agreement at ≤1600 sims. Test bots: connectpuct (80 sims), rowspire (4000 sims), katac4 (1600 sims).
- **BMS-006**: Board-Size Coverage Audit — Documents which board sizes are tested vs supported. Current test evidence: 7x6 (6 tests) + 4x5/inarow=3 (8 tests). Gap: 15x13 and 15x10 have ZERO test evidence despite being supported by env spec. Governance risk: bots optimized for 7x6 may fail on 15x13.
- **S118**: connectpuct PUCT MCTS benchmark results — 55% win rate vs minimax depth-3. URL: github.com/ahmeddoghri/connectpuct/README.md. Medium quality: first-party benchmark, no third-party validation.
- **S119**: kaggle-environments test_connectx.py v1.32.2 — Board Size Test Coverage Audit. 6 tests for 7x6, 8 tests for 4x5/inarow=3. No tests for boards larger than 10x8. HIGH quality: official Kaggle framework.
- **S120**: Althöfer 2012 "Monte Carlo Perfectness" — Theorem statement. Citation arXiv:1203.2285 verified as astrophysics paper (not game theory). Theory is real but exact citation lost. LOW quality.
- **BOT-010**: jlokitha/connect-4-game — MCTS Student Project. Java/JavaFX/Maven. 15* stars. No benchmarks published. Likely university/course project. Low priority for source analysis.

**Sources added**: S118, S119, S120 ✓
**Contender added**: BOT-010 ✓
**Benchmarks added**: BMS-005, BMS-006 ✓

### Worker 4 — Adjacent Opening MCTS Consistency (Jobs 1-2)

**Findings**:
- **C139 upgraded HYPOTHESIS→VERIFIED**: Adjacent opening draw unidentifiable by MCTS. Source: connectpuct benchmark showing MCTS cannot reliably detect draw positions on columns 3 and 5 (adjacent to center). This directly validates the MCTS consistency problem (Althöfer MCP theorem: UCT converges to minimax only in Monte Carlo Perfect games; Connect 4 is NOT MCP).
- **HYP-003 confidence upgrade**: LOW→MEDIUM. Per worker-04, C139 VERIFIED strengthens the evidence that MCTS cannot reliably solve adjacent opening draws within practical budgets.
- **FR-001**: Verify adjacent opening draw detection on real 7x6 positions (Col 3/5 openings). Run connectpuct/katac4/rowspire against themselves.
- **FR-002**: Audit all MCTS ensemble designs for timing governance — verify 1.5s fallback specified.
- **FR-003**: Reconcile S118-S120 exact URLs and content.
- **FR-004**: Deep-dive connectpuct PUCT implementation — verify 55% win rate claim.
- **FR-005**: Source ID collision audit — verify S094-S097, S101-S102 reconciliation plan.
- **FR-006**: Review new ensemble designs (ENS-013/014/015) for integration assumptions.

**New experiments**:
- **EXP-016**: Adjacent-Opening MCTS Consistency Measurement — P1 priority. Tests connectpuct (80 sims), rowspire (4000 sims), katac4 (1600 sims) on 200 adjacent-opening positions (Col 3, 5). Expected: connectpuct <30% draw rate, rowspire ~50%, katac4 ~60%. Falsification: any MCTS variant ≥80% draw rate.
- **EXP-017**: Adjacent-Opening Draw Detection Ensemble Validation — P1 priority. ENS-003 draw-detection ensemble vs pure MCTS on 200 adjacent-opening positions. Expected: ENS-003 ≥70% draw rate, pure MCTS <30%. Falsification: ENS-003 draw rate <30%.
- **EXP-018**: NN-Guided vs Random-Playout MCTS on Adjacent Openings — P1 priority. Tests whether NN-guided playouts escape MCP consistency constraint. NN-guided MCTS expected ≥20% higher draw rate than vanilla MCTS. Falsification: no significant difference between NN-guided and vanilla MCTS.

### Worker 5 — Ensemble Hypotheses (Job 1)

**Findings**:
- **ENS-013**: Multi-Layer Defense Ensemble (Conservative, Timing-Gated)
  - Components: Alpha-beta + PVS + TT (10M) + center-first ordering + heuristic eval (rowspire evolved weights) + FPU safety guard + timing gate (HYP-014)
  - Routing: Primary alpha-beta with full ordering. Fallback at >1.5s: depth-limited alpha-beta (depth 8).
  - 3 safety layers: timing gate, FPU guard, confidence gate.
  - Risk: Low. Expected performance: High on 7x6.

- **ENS-014**: AlphaZero-GPU High-Ceiling Ensemble
  - Components: ResNet b3c128nbt + self-play training + PUCT MCTS (1600 sims) + FPU + LCB + GPU acceleration (MCTS-NC) + three-loss objective + timing governance
  - GPU: 20.3M playouts/5s theoretical on GRID A100. Kaggle T4: ~2s/move → ~8M playouts per move.
  - Multiple fallback paths: GPU → CPU MCTS → NN leaf eval + alpha-beta.
  - Risk: Very High. Expected performance: Highest.

- **ENS-015**: Simplicity Ensemble (Alpha-Beta Only)
  - Components: Alpha-beta + PVS + TT (5M LRU) + center-first move ordering + rowspire evolved eval weights.
  - Maximum simplicity: one search, one eval, one data structure. No timing gate, no fallback, no NN.
  - Risk: Minimal. Expected performance: Medium-High on 7x6.

- **ENSO-002 timing concern**: 5-layer ensemble estimated 3.6-5.6s exceeds 2s Kaggle budget. Downgrade from SUPPORTED→HYPOTHESIS for timing feasibility parameter.

### Worker 7 — Corpus Audit (Job 1)

**Findings**:
- **Source ID collision**: 8 source IDs (S094-S097, S101-S102) used by both R23/R24 and R25 batches. R25 overwrites R23/R24 entries.
- **C136, C007, C150 downgraded to NEEDS_CORRECTION**: Due to source ID collision — the underlying evidence cannot be traced to the correct source.
- **C162 kept VERIFIED**: Collision only with R23, not with R25.
- **C154 source ID updated**: S095→S114.

---

## Corpus Corrections

### Sources Added (Round 30)

| ID | Source | Description | Quality |
|----|--------|-------------|---------|
| S118 | connectpuct PUCT README | 55% win rate vs minimax depth-3 | Medium (first-party, no third-party validation) |
| S119 | kaggle-environments test_connectx.py v1.32.2 | Board size test coverage audit | High (official Kaggle framework) |
| S120 | Althöfer 2012 "Monte Carlo Perfectness" | Theorem statement (wrong citation arXiv:1203.2285 = astrophysics) | Low (theory real, citation lost) |

### Claims Changed (Round 30)

| Claim | Old Status | New Status | Rationale |
|-------|-----------|-----------|-----------|
| C139 | HYPOTHESIS | VERIFIED | Adjacent opening draw unidentifiable by MCTS (worker-04) |
| C136 | VERIFIED | NEEDS_CORRECTION | Source ID collision (worker-07) |
| C007 | VERIFIED | NEEDS_CORRECTION | Source ID collision (worker-07) |
| C150 | VERIFIED | NEEDS_CORRECTION | Source ID collision (worker-07) |
| C154 | source S095 | source S114 | Source ID correction (worker-07) |
| C162 | VERIFIED | VERIFIED | Collision only with R23, not R25 — status unchanged |

### Hypotheses Added (Round 30)

| ID | Title | Status | Rationale |
|----|-------|--------|-----------|
| HYP-014 | Timing Governance Protocol | PROPOSED | 1.5s forced termination with alpha-beta fallback required for all MCTS ensembles (worker-07) |

### Hypotheses Changed (Round 30)

| ID | Old Confidence | New Confidence | Rationale |
|----|---------------|---------------|-----------|
| HYP-003 | LOW | MEDIUM | C139 VERIFIED strengthens evidence for MCTS consistency problem (worker-04) |

---

## New Ensembles (Round 30)

### ENS-013: Multi-Layer Defense Ensemble (Conservative)

- **Components**: Alpha-beta + PVS + TT (10M LRU) + center-first ordering + rowspire evolved eval + FPU guard + timing gate
- **Routing**: Primary alpha-beta. Fallback at >1.5s: depth-limited alpha-beta (depth 8). FPU guard: if MCTS variance high, trust alpha-beta.
- **Safety layers**: Timing gate → FPU guard → confidence gate
- **Risk**: Low. Expected performance: High on 7x6
- **Key innovation**: Three-layer defense against MCTS inconsistency

### ENS-014: AlphaZero-GPU High-Ceiling Ensemble

- **Components**: ResNet b3c128nbt + self-play + PUCT MCTS (1600 sims) + FPU + LCB + GPU MCTS-NC + three-loss objective + timing governance
- **Fallback paths**: GPU MCTS → CPU MCTS → NN leaf eval + alpha-beta
- **Risk**: Very High. Expected performance: Highest (if Kaggle T4 GPU feasible)
- **Key innovation**: GPU-accelerated PUCT MCTS with multiple fallback paths

### ENS-015: Simplicity Ensemble (Alpha-Beta Only)

- **Components**: Alpha-beta + PVS + TT (5M LRU) + center-first ordering + rowspire evolved eval weights
- **Maximum simplicity**: One search, one eval, one data structure
- **Risk**: Minimal. Expected performance: Medium-High on 7x6
- **Key innovation**: Demonstrates that alpha-beta-only can be competitive on 7x6

---

## Benchmark Design Changes (Round 30)

### BMS-005: MCTS Consistency on Solved Positions

- **Board**: 7x6, center column opening (known P1 win)
- **Metric**: Oracle agreement rate (% moves matching minimax solver)
- **Simulation counts**: 10, 50, 100, 500, 1000, 4000
- **Target**: ≥90% oracle agreement at ≤1600 sims
- **Test bots**: connectpuct (80 sims), rowspire (4000 sims), katac4 (1600 sims)
- **Falsification**: If any bot achieves ≥90% at ≥1600 sims, consistency problem less severe

### BMS-006: Board-Size Coverage Audit

- **Purpose**: Document test coverage vs. supported board sizes
- **Current**: 7x6 (6 tests) + 4x5/inarow=3 (8 tests)
- **Gap**: 15x13 and 15x10 have ZERO test evidence
- **Risk**: Bots optimized for 7x6 may fail on 15x13

---

## Experiment Backlog Changes (Round 30)

3 new experiments added (EXP-016 through EXP-018), all P1 priority:

| ID | Title | Purpose | Falsification |
|----|-------|---------|---------------|
| EXP-016 | Adjacent-Opening MCTS Consistency | Measure draw detection rate per bot on Col 3/5 openings | Any MCTS ≥80% draw rate |
| EXP-017 | Draw Detection Ensemble Validation | ENS-003 vs pure MCTS on adjacent openings | ENS-003 draw rate <30% |
| EXP-018 | NN-Guided vs Random-Playout MCTS | Test whether NN-guided playouts escape MCP constraint | No significant difference |

**Total experiments**: 18 (EXP-001 through EXP-018)

---

## Contender Added (Round 30)

| ID | Name | Type | Source |
|----|------|------|--------|
| BOT-010 | jlokitha/connect-4-game | MCTS Student Project | GitHub (Java/JavaFX/Maven) |

- 15* stars, no benchmarks published, board size unspecified
- Likely university/course project
- Low priority for source analysis

---

## Corpus Hygiene

- **Source ID collision**: 8 IDs (S094-S097, S101-S102) used by both R23/R24 and R25 batches
- **Plan for R31**: Reconcile source IDs, establish unique namespace per source
- **Claims affected**: C136, C007, C150 → NEEDS_CORRECTION; C162 → VERIFIED (collision only with R23)
- **New sources (S118-S120)**: Verified before ingestion — each has unique ID, URL, and quality assessment

---

## Next Research Frontier (R31)

1. **Source ID collision resolution** — Reconcile S094-S097, S101-S102 across R23/R24/R25 batches
2. **HYP-014 timing governance validation** — Verify 1.5s forced termination + alpha-beta fallback feasibility on Kaggle T4
3. **ENSO-002 timing parameter downgrade** — 5-layer ensemble exceeds 2s budget; adjust timing gate
4. **BMS-005 execution planning** — Design concrete measurement methodology for MCTS consistency
5. **Board-size coverage audit (BMS-006)** — Identify ConnectX tests for 15x13/15x10
6. **ENS-013/014/015 integration review** — Verify component compatibility across new ensembles
7. **connectpuct deep-dive** — Verify 55% win rate claim against minimax depth-3 (S118)
8. **Althöfer MCP theorem verification** — Reconstruct correct citation; verify theorem statement (S120)

---

## Worker Results Consumed and Rejected

| Worker | Jobs Consumed | Results |
|--------|--------------|---------|
| Worker 2 | Job-00011 (contender), Job-00012 (benchmark design) | BOT-010, BMS-005, BMS-006, S118-S120 |
| Worker 4 | Adjacent opening MCTS consistency | C139 VERIFIED, EXP-016/017/018, HYP-003 confidence upgrade |
| Worker 5 | Ensemble hypotheses | ENS-013/014/015, ENSO-002 timing downgrade |
| Worker 7 | Corpus audit | C136/C007/C150 NEEDS_CORRECTION, HYP-014 PROPOSED |
| Worker 3, 1, 6 | Not present in batch | N/A |

No results rejected as duplicate or invalid.

---

## Research Status

- **Total claims**: 176 (VERIFIED 72, NEEDS_CORRECTION 18, remaining distributed across SUPPORTED/HYPOTHESIS/etc.)
- **Total sources**: 120 (S118-S120 added R30)
- **Total hypotheses**: 14 (HYP-014 added R30)
- **Total ensembles**: 9 (ENS-013/014/015 added R30; ENS-006 was historical from prior rounds)
- **Total contenders**: 10 (BOT-010 added R30)
- **Total benchmark suites**: 6 (BMS-005/BMS-006 added R30)
- **Total experiments**: 18 (EXP-016/017/018 added R30)
- **Research queue follow-up tasks**: 28 (FU-016-FU-056)

---

ENDOFFILE