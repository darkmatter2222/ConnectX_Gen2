# ConnectX Research Nexus — Corpus Index

> **Current Round**: 41 (2026-08-05)
> **Last Updated**: 2026-08-05 14:00 ET (Round 41)
> **Purpose**: Single entry point for navigating the entire ConnectX research corpus

---

## Corpus Statistics (Round 40)

| Category | Count | Range |
|----------|-------|-------|
| Claims | 222 | C001-C222 |
| Verified | 100 | 44% |
| Needs Correction | 22 | 10% |
| Hypothesis | 24 | 11% |
| Other | 79 | 35% |
| Hypotheses | 24 | HYP-001 through HYP-024 |
| Ensembles | 24 | E-001 through E-012, ENS-013 through ENS-024 |
| Contenders | 16 | BOT-001 through BOT-016 |
| Benchmark Suites | 19 | BMS-001 through BMS-019 |
| Experiments | 43 | EXP-001 through EXP-037, EXP-NEW-001 through EXP-NEW-006 |
| Sources | 131 | S001 through S131 (with 4 collision clusters) |
| Dossiers | 18 | F-001, CS-001, CS-002, CS-003, CS-004, MCTS-001, MCTS-002, MCTS-003, BMS-DOC-001, GOV-001, GOV-002, GOV-003, GOV-004, D-034, RI-001, NN-001, plus MCTS-004 (PROPOSED, thin), BMS-DOC-002 (MCTS consistency and board-size scaling, PROPOSED) |
| Governance Findings | 29 | F-001 through F-022 (GOV-001) + C216-C220 (GOV-004) |

---

## Source of Truth Hierarchy

| Tier | Files | Purpose |
|------|-------|---------|
| Tier 1: Master Report | `RESEARCH_REPORT.md` | Primary user entry point; living research summary |
| Tier 2: Canonical Index | `research/README.md` | Canonical file registry; round report table |
| Tier 3: Corpus Index | `research/NEXUS.md` | THIS FILE — cross-link map, collision ledger, dossier index |
| Tier 4: State Registers | `research/research-state.md`, `research/claim-register.md`, `research/source-ledger.md`, etc. | Working state; updated each round |
| Dossiers | 18 | F-001, CS-001, CS-002, CS-003, CS-004, MCTS-001, MCTS-002, MCTS-003, BMS-DOC-001, GOV-001, GOV-002, GOV-003, GOV-004, D-034, RI-001, NN-001, plus MCTS-004 (PROPOSED, thin), BMS-DOC-002 (MCTS consistency and board-size scaling, PROPOSED) |
| Tier 6: Iteration Reports | `research/iterations/round-NNN.md` | Per-round worker result summaries |

---

## Source ID Collision Map

4 collision clusters identified across rounds R16–R34. **27+ source IDs affected.**

### Cluster A — katac4 / TensorRT Inference (R16, R25, R30)

| Colliding ID | Assigned In | Description |
|--------------|-------------|-------------|
| S091–S093 | R16 + R25 + R30 | katac4 PyTorch/TT support, TensorRT inference |

**Risk**: Any claim citing S091–S093 may reference a different source depending on which round's entry is read.

### Cluster B — Tromp fhourstones Methodology (R23, R25, R30)

| Colliding ID | Assigned In | Description |
|--------------|-------------|-------------|
| S094–S097 | R23 + R25 + R30 | Tromp fhourstones methodology |

### Cluster C — NeuralConnect4 / AZAL / Fabricated Data (R25, R30)

| Colliding ID | Assigned In | Description |
|--------------|-------------|-------------|
| S109–S117 | R25 + R30 | NeuralConnect4, Gemu03, katac4 MCTS, AZAL paper |

**Note**: S117 is FABRICATED (40-40-20 phase distribution, detected R33).

### Cluster D — MCTS Benchmark / Fabricated Data (R30 self-duplicate)

| Colliding ID | Assigned In | Description |
|--------------|-------------|-------------|
| S118–S120 | R30 self-duplicate | connectpuct MCTS benchmark, Althöfer MCP citation |

**Note**: S120 ("uniform random") is FABRICATED (detected R30).

---

## Fabricated Data Ledger

| Source | Fabrication | Detected | Referenced By | Status |
|--------|-------------|----------|---------------|--------|
| S117 | "40-40-20 phase distribution" (no such stat in TonyCWang dataset) | R33 | C151, EXP-028 | **[RETRACTED]** |
| S120 | "Uniform random" methodology (actual = self-play with temp schedule) | R30 | EXP-029 | **[RETRACTED]** |
| arXiv:1203.2285 | MCP theorem citation (actual = astrophysics paper, not game theory) | R33 | C136, HYP-019, HYP-020 | Broken — replace with verified source |

**Remediation**: R35 adds [RETRACTED] flags to S117 and S120 in source-ledger.md. arXiv:1203.2285 requires replacement with verified game theory source (FU-072).

---

## Dossier Index

### Governance (4 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| GOV-001 | Corpus Governance Audit — Round 34 Full Structural Assessment | VERIFIED | `dossiers/governance/GOV-001-corpus-governance-audit-round-34.md` |
| GOV-002 | R36 Gap Repair — Remediation Tracking | VERIFIED | `dossiers/governance/GOV-002-R36-gap-repair-remediation-tracking.md` |
| GOV-003 | R36 Governance Gap Repair — Post-Merger Assessment | VERIFIED | `dossiers/governance/GOV-003-R36-gap-repair-executive-report.md` |
| GOV-004 | R37 Comprehensive Corpus Audit | VERIFIED | `dossiers/governance/GOV-004-R37-comprehensive-audit.md` |

### MCTS (5 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| MCTS-001 | MCTS Consistency Problem for Solved Games | VERIFIED |  |
| MCTS-002 | Neural MCTS Integration Patterns | VERIFIED |  |
| MCTS-003 | MCTS Variant Taxonomy (UCT, PUCT, LCB, FPU, PCR) | PROPOSED |  |
| MCTS-004 | MCTS Deployment Architecture (Board-Size Templates, Timing Governance, Ensemble Integration) | PROPOSED |  |



### Classical Search (3 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| CS-001 | Opening Book Engineering | VERIFIED | `dossiers/classical-search/opening-book-engineering.md` |
| CS-003 | Classical Search and Solver Engineering | READY | `dossiers/classical-search/CS-003-classical-search-and-solver-engineering.md` |
| CS-004 | Search Algorithm Comparison | PROPOSED | `dossiers/classical-search/search-algorithm-comparison.md` |

### Foundational (2 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| F-001 | Board Representation and Win Detection | VERIFIED | `dossiers/foundations/board-representation-and-win-detection.md` |
| CS-002 | Board Representation and Move Generation | VERIFIED | `dossiers/classical-search/board-representation-and-move-generation.md` |

### Benchmarking (2 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| BMS-DOC-001 | Benchmark Science and Tournament Design | VERIFIED | `dossiers/benchmarking/benchmark-science-and-tournament-design.md` |
| BMS-DOC-002 | MCTS Consistency Theory and Board-Size Scaling | PROPOSED | `dossiers/benchmarking/bms-doc-002-mcts-consistency-theory-and-board-size-scaling.md` |

### Reference Implementations (2 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| D-034 | New Source Repositories Discovered in GitHub Topic Scan | VERIFIED | `dossiers/reference-implementations/new-repo-sources-r34.md` |
| RI-001 | katac4 Reference Implementation (AlphaZero + KataGo) | VERIFIED | dossiers/reference-implementations/katac4-reference-implementation.md |

### Contenders (2 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| D-CBL-001 | Baseline Contender Comparison | PROPOSED | `dossiers/contenders/contenders-baselines-benchmark-references.md` |
| DOS-006 | Contender Deep Profiles and Board-Size Analysis | VERIFIED | `dossiers/contenders/contenders-deep-profiles-and-board-size-analysis.md` |

### Neural (1 dossier)

| ID | Title | Status | Path |
|----|-------|--------|------|
| NN-001 | Neural Network Architectures, Training Pipelines, and Data | READY | `dossiers/neural/NN-001-neural-networks-architectures-training-pipelines-and-data.md` |

**Scope:** 5 architecture families (ResNet, MLP, CNN, DQN, NNUE), 3 training pipelines, 18 sources, inference optimization (TensorRT INT8), board-size generalization.

### Empty Directories (2)

| Directory | Status | Action Needed |
|-----------|--------|---------------|
| ensembles/ | EMPTY | Needs ensemble design dossiers |
| training-data/ | EMPTY | Needs training pipeline data dossiers |
---

## Cross-Link Map

### Governance Chain
GOV-001 (22 findings R34) -> GOV-002 (remediation tracking R36) -> GOV-003 (post-merger assessment R36) -> GOV-004 (comprehensive audit R37, 55% remediation)


CS-001 (opening books) -> CS-002 (board rep) -> CS-003 (solver engineering) -> CS-004 (algorithm comparison) -> F-001 (foundations)

RI-001 (katac4 reference) -> D-034 (new repos) -> D-CBL-001 (baseline contenders) -> DOS-006 (deep profiles) -> BMS-DOC-001 (benchmarking)
DOS-006 (deep profiles) -> CS-003 (classical search) -> F-001 (foundations)
DOS-006 (board-size routing) -> ENS-NEW-001/002/003 (ensemble designs)
DOS-006 (contender deep profiles) -> ensemble-catalog.md (ensemble designs)
DOS-006 (benchmark mapping) -> benchmark-blueprint.md (BMS-001 through BMS-012)

NN-001 (neural architectures) -> MCTS-002 (neural MCTS) -> MCTS-001 (consistency)
NN-001 (TensorRT) -> MCTS-002 (inference patterns) -> BMS-DOC-001 (benchmarking)
BMS-DOC-002 (MCTS consistency theory) -> MCTS-001 (consistency problem) -> MCTS-002 (neural MCTS)
BMS-DOC-002 (board-size scaling) -> DOS-006 (board-size routing) -> benchmark-blueprint.md (BMS-001 through BMS-019)
BMS-DOC-002 (race detection) -> BMS-DOC-001 (reproducibility) -> BMS-012 (reproducibility protocol)
BMS-DOC-002 (seat-reversal bias) -> DOS-006 (contender deep profiles) -> ensemble-catalog.md
BMS-DOC-002 (latency budgeting) -> NN-001 (TensorRT latency) -> MCTS-002 (GPU patterns) -> BMS-DOC-001 (benchmarking)
NN-001 (neural eval) -> CS-003 (classical search) -> F-001 (foundations)

---

## Recent Changes (Round 37 through 40)

- **Added:** MCTS-003 (MCTS variant taxonomy, PROPOSED), RI-001 (katac4 reference), CS-003 (classical search/solver engineering), GOV-004 (corpus audit R37)
- **Added:** NN-001 (Neural Network Architectures, Training Pipelines, and Data — 654 lines, 18 sources, feasibility matrix, board-size applicability)
- **Added:** MCTS-004 (MCTS Deployment Architecture — PROPOSED, 632 lines, 8 sources, 6 board-size architecture templates)
- **Added:** DOS-006 (Contender Deep Profiles and Board-Size Analysis — 1,006 lines, ~50KB, 9 primary + 5 reference sources, board-size routing strategy, 3 new ensemble designs)
- **Added:** CS-004 (Search Algorithm Comparison — 761 lines, 31.7KB, 8+ sources, 7 algorithm specs, self-corrections C006/C007)
- **Added:** RI-001 (katac4 Reference Implementation — 771 lines, 51.2KB, 13 sources via WebFetch, VERIFIED)
- **Expanded:** MCTS-003 (variant taxonomy expanded to 8 variants, 6 hybrid patterns)
- **Rejected:** mcts-004 (thin), batch-00097 total failure (8/8 workers), batch-00099 9/18 workers failed (Write tool unavailable or no output)
- **Updated:** Dossier count from 9 to 17 across 11 directories (2 empty: ensembles, training-data)
- **Updated:** Dossier count from 14 to 16 (DOS-006); contenders directory now has 2 dossiers
- **Updated:** Classical Search directory: 2→3 dossiers (added CS-004)
- **Updated:** MCTS directory: 4→5 dossiers (added MCTS-003 expansion)
- **Updated:** Reference Implementations directory: 2→3 dossiers (added RI-001)

## Recent Changes (Round 41)

- **Added:** BMS-DOC-002 (MCTS Consistency Theory, Board-Size Scaling Laws, and Benchmark Methodology Gaps — PROPOSED, 791 lines, ~38KB, 13+ sources, 8 code/pseudocode blocks, feasibility matrix, 7 new benchmark suites, 6 new experiments)
- **New benchmarks proposed:** BMS-013 through BMS-019 (MCP consistency analysis, board-size scaling validation, race-condition detection, latency budget audit, seat-reversal bias test, time-allocation benchmark, statistical power analysis)
- **New experiments specified:** EXP-NEW-001 through EXP-NEW-006 (MCTS consistency test, board-size scaling measurement, race detection, latency profiling, seat-reversal bias test, time allocation optimization)
- **Updated:** Benchmark Suites count from 12 to 19 (BMS-001 through BMS-019)
- **Updated:** Dossiers count from 17 to 18 (BMS-DOC-002 added to benchmarking directory)
- **Updated:** Experiments count from 37 to 43 (6 new experiments)
