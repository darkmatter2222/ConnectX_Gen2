# ConnectX Research Nexus — Corpus Index

> **Current Round**: 37 (2026-08-05)
> **Last Updated**: 2026-08-05
> **Purpose**: Single entry point for navigating the entire ConnectX research corpus

---

## Corpus Statistics (Round 37)

| Category | Count | Range |
|----------|-------|-------|
| Claims | 225 | C001–C225 |
| Verified | 100 | 44% |
| Needs Correction | 22 | 10% |
| Hypothesis | 24 | 11% |
| Other | 79 | 35% |
| Hypotheses | 24 | HYP-001 through HYP-024 |
| Ensembles | 24 | E-001 through E-012, ENS-013 through ENS-024 |
| Contenders | 16 | BOT-001 through BOT-016 |
| Benchmark Suites | 12 | BMS-001 through BMS-012 |
| Experiments | 37 | EXP-001 through EXP-037 |
| Sources | 131 | S001 through S131 (with 4 collision clusters) |
| Dossiers | 9 | GOV-001, GOV-002, GOV-003, GOV-004, MCTS-001, MCTS-002, BMS-DOC-001, CS-003, D-034 |
| Governance Findings | 29 | F-001 through F-022 (GOV-001) + C216-C220 (GOV-004) |

---

## Source of Truth Hierarchy

| Tier | Files | Purpose |
|------|-------|---------|
| Tier 1: Master Report | `RESEARCH_REPORT.md` | Primary user entry point; living research summary |
| Tier 2: Canonical Index | `research/README.md` | Canonical file registry; round report table |
| Tier 3: Corpus Index | `research/NEXUS.md` | THIS FILE — cross-link map, collision ledger, dossier index |
| Tier 4: State Registers | `research/research-state.md`, `research/claim-register.md`, `research/source-ledger.md`, etc. | Working state; updated each round |
| Tier 5: Dossiers | 9 | GOV-001, GOV-002, GOV-003, GOV-004, MCTS-001, MCTS-002, BMS-DOC-001, CS-003, D-034 |
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

### MCTS (2 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| MCTS-001 | MCTS Consistency Problem for Solved Games | VERIFIED | `dossiers/mcts/mcts-consistency-solved-games.md` |
| MCTS-002 | Neural MCTS Integration Patterns | VERIFIED | `dossiers/mcts/mcts-002-neural-integration-patterns.md` |

### Classical Search (2 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| CS-001 | Opening Book Engineering | VERIFIED | `dossiers/classical-search/opening-book-engineering.md` |
| CS-003 | Classical Search and Solver Engineering | READY | `dossiers/classical-search/CS-003-classical-search-and-solver-engineering.md` |

### Foundational (2 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| F-001 | Board Representation and Win Detection | VERIFIED | `dossiers/foundations/board-representation-and-win-detection.md` |
| CS-002 | Board Representation and Move Generation | VERIFIED | `dossiers/classical-search/board-representation-and-move-generation.md` |

### Benchmarking (1 dossier)

| ID | Title | Status | Path |
|----|-------|--------|------|
| BMS-DOC-001 | Benchmark Science and Tournament Design | VERIFIED | `dossiers/benchmarking/benchmark-science-and-tournament-design.md` |

### Reference Implementations (1 dossier)

| ID | Title | Status | Path |
|----|-------|--------|------|
| D-034 | New Source Repositories Discovered in GitHub Topic Scan | VERIFIED | `dossiers/reference-implementations/new-repo-sources-r34.md` |

### Contenders (1 dossier — shallow)

| ID | Title | Status | Path |
|----|-------|--------|------|
| D-CBL-001 | Baseline Contender Comparison | PROPOSED | `dossiers/contenders/contenders-baselines-benchmark-references.md` |

### Empty Directories (3)

| Directory | Status |
|-----------|--------|
| `dossiers/ensembles/` | EMPTY — needs ensemble dossiers |
| `dossiers/neural/` | EMPTY — needs neural approach dossiers |
| `dossiers/training-data/` | EMPTY — needs training pipeline dossiers |

---

## Cross-Link Map

### Governance Chain
GOV-001 (22 findings R34) → GOV-002 (remediation tracking R36) → GOV-003 (post-merger assessment R36) → GOV-004 (comprehensive audit R37, 55% remediation)

### MCTS Chain
MCTS-001 (consistency problem) → MCTS-002 (integration patterns) → BMS-DOC-001 (benchmark requirements)

### Classical Search Chain
CS-001 (opening books) → CS-003 (classical search and solver engineering) → F-001 (board representation)

### Reference Chain
D-034 (new repos) → D-CBL-001 (baseline contenders) → BMS-DOC-001 (benchmarking)

---

## Recent Changes (Round 37)

- **Added:** MCTS-002 (neural MCTS integration patterns, 6 sources, 5 patterns, feasibility matrix)
- **Added:** D-034 (3 new GitHub repos from topic scan)
- **Added:** CS-003 (classical search and solver engineering, 8 sources)
- **Added:** GOV-004 (comprehensive audit, 55% remediation rate)
- **Rejected:** 3 thin worker outputs (worker-01-job-00534, worker-02-job-00070, worker-07-job-00556)
- **Updated:** Source count from 127 to 131 (S128–S131)
- **Updated:** Claim count from 215 to 225 (C216–C225)
- **Updated:** Dossier count from 6 to 9