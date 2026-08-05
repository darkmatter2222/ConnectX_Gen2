# ConnectX Research Nexus — Corpus Index

> **Current Round**: 36 (2026-08-04)
> **Last Updated**: 2026-08-04
> **Purpose**: Single entry point for navigating the entire ConnectX research corpus

---

## Corpus Statistics (Round 36)

| Category | Count | Range |
|----------|-------|-------|
| Claims | 215 | C001–C215 |
| Verified | 96 | 45% |
| Needs Correction | 22 | 10% |
| Hypothesis | 24 | 11% |
| Other | 73 | 34% |
| Hypotheses | 24 | HYP-001 through HYP-024 |
| Ensembles | 24 | E-001 through E-012, ENS-013 through ENS-024 |
| Contenders | 16 | BOT-001 through BOT-016 |
| Benchmark Suites | 12 | BMS-001 through BMS-012 |
| Experiments | 32 | EXP-001 through EXP-032 |
| Sources | 126+ | S001 through S126 (with 4 collision clusters) |
| Dossiers | 3 | GOV-001, MCTS-001, BMS-DOC-001 |
| Governance Findings | 22 | F-001 through F-022 (4 CRITICAL, 8 HIGH, 6 MEDIUM, 4 LOW) |

---

## Source of Truth Hierarchy

| Tier | Files | Purpose |
|------|-------|---------|
| Tier 1: Master Report | `RESEARCH_REPORT.md` | Primary user entry point; living research summary |
| Tier 2: Canonical Index | `research/README.md` | Canonical file registry; round report table |
| Tier 3: Corpus Index | `research/NEXUS.md` | THIS FILE — cross-link map, collision ledger, dossier index |
| Tier 4: State Registers | `research/research-state.md`, `research/claim-register.md`, `research/source-ledger.md`, etc. | Working state; updated each round |
| Tier 5: Dossiers | `research/dossiers/**` | Substantive deep-dive research |
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

| Source | Fabrication | Detected | Referenced By |
|--------|-------------|----------|---------------|
| S117 | "40-40-20 phase distribution" (no such stat in TonyCWang dataset) | R33 | C151, EXP-028 |
| S120 | "Uniform random" methodology (actual = self-play with temp schedule) | R30 | EXP-029 |
| arXiv:1203.2285 | MCP theorem citation (actual = astrophysics paper, not game theory) | R33 | C136, HYP-019, HYP-020 |

**Remediation**: R35 adds [RETRACTED] flags to S117 and S120 in source-ledger.md. arXiv:1203.2285 requires replacement with verified game theory source (FU-072).

---

## Dossier Index

### Governance (1 dossier)

| ID | Title | Status | Path |
|----|-------|--------|------|
| GOV-001 | Corpus Governance Audit — Round 34 Full Structural Assessment | VERIFIED | `dossiers/governance/GOV-001-corpus-governance-audit-round-34.md` |

### MCTS (1 dossier)

| ID | Title | Status | Path |
|----|-------|--------|------|
| MCTS-001 | MCTS Consistency Problem for Solved Games in Connect 4 | VERIFIED | `dossiers/mcts/mcts-consistency-solved-games.md` |

### Benchmarking (1 dossier)

| ID | Title | Status | Path |
|----|-------|--------|------|
| BMS-DOC-001 | Benchmark Science and Tournament Design for ConnectX Bot Evaluation | VERIFIED | `dossiers/benchmarking/benchmark-science-and-tournament-design.md` |

### Planned Dossiers (not yet created)

| Target | Content | Priority |
|--------|---------|----------|
| Foundations | Board representation, win/fork detection, game theory | HIGH |
| Kaggle | Competition spec, environment analysis, evaluation methodology | HIGH |
| Contenders | 16 contender dossiers (BOT-001 through BOT-016) | HIGH |
| Classical Search | Alpha-beta, MTD(f), PVS, move ordering, killer moves | HIGH |
| Neural | NN architectures, ResNet, DQN, NNUE, policy/value networks | HIGH |
| Training Data | Self-play, solver-distilled, temperature schedules | MEDIUM |
| Ensembles | Ensemble design dossiers (ENS-013 through ENS-024) | MEDIUM |
| Reference Implementations | AlphaZero (katac4), rowspire, Tromp, Pascal Pons | MEDIUM |

### Empty Directories (awaiting content)

| Directory | Purpose |
|-----------|---------|
| `dossiers/foundations/` | Mathematical and game theory foundations |
| `dossiers/kaggle/` | Kaggle competition analysis |
| `dossiers/classical-search/` | Classical search algorithm dossiers |
| `dossiers/neural/` | Neural network architecture dossiers |
| `dossiers/training-data/` | Training data analysis dossiers |
| `dossiers/contenders/` | Contender dossiers (16 planned) |
| `dossiers/ensembles/` | Ensemble design dossiers |
| `dossiers/reference-implementations/` | Reference code analysis dossiers |

---

## Cross-Link Map

### Claims → Experiments

| Claim | Experiment(s) | Type |
|-------|--------------|------|
| C200 (Neural MCTS 0.849 oracle match) | EXP-016 | VERIFIED |
| C201 (AZAL three-loss objective) | EXP-017 | VERIFIED |
| C202 (TensorRT INT8 latency) | EXP-018 | VERIFIED |
| C205 (DQN tactical weakness) | EXP-019 | VERIFIED |
| C199 (Source ID collisions) | EXP-031 | VERIFIED |
| C151 (Fabricated data S117) | EXP-028 | NEEDS_CORRECTION |

### Hypotheses → Ensembles

| Hypothesis | Ensemble(s) |
|------------|-------------|
| HYP-021 (Board-size adaptive routing) | ENS-019, ENS-020 |
| HYP-022 (Phase-boundary calibration) | ENS-021 |
| HYP-023 (TensorRT INT8 advantage) | ENS-022 |
| HYP-024 (NNUE vs DQN) | ENS-023, ENS-024 |

### Governance Findings → Experiments

| Finding | Related Experiment |
|---------|-------------------|
| F-001 (Source ID collisions) | EXP-031, EXP-034 |
| F-002 (Fabricated data) | EXP-025, EXP-026, EXP-035 |
| F-003 (Master report staleness) | EXP-036 |
| F-004 (Source ledger incompleteness) | EXP-034 |
| F-006 (Missing NEXUS.md) | — (resolved by this file) |
| F-007 (Empty dossier directories) | EXP-037 |

---

## Key Unknowns and Future Experiments

| Unknown | Experiment | Expected Timeline |
|---------|-----------|-------------------|
| Board-size routing threshold | HYP-021, BMS-005 | Deferred empirical |
| Phase-boundary calibration | HYP-022, BMS-006 | Deferred empirical |
| TensorRT INT8 on Kaggle T4 | HYP-023, EXP-018 | Deferred empirical |
| NNUE feature engineering | HYP-024, EXP-019 | Deferred empirical |
| Confidence-gated routing | HYP-024, ENS-024 | Deferred empirical |
| Source ID collision remediation | EXP-034 | Round 36 |
| Automated fabrication detection | EXP-035 | Round 37+ |
| Master report staleness impact | EXP-036 | Round 35–36 |

---

## Obsolete Directories

| Path | Status | Reason |
|------|--------|--------|
| `research/dossiers/classical-search/` | Empty | Awaiting classical search dossiers |

---

## Legend

- **VERIFIED**: Confirmed by direct reading of primary source or independent corroboration
- **STRONGLY SUPPORTED**: Multiple independent sources, no direct primary read
- **SUPPORTED**: Single source, plausible but not independently verified
- **HYPOTHESIS**: Proposed but not yet verified
- **NEEDS_CORRECTION**: Claim has factual issues that need correction
- **FABRICATED**: Data that was confirmed to not exist in the cited source
- **RETRACTED**: Source entry that was found to contain fabricated data

---

*This file was created in Round 35 as part of the first V10 dossier synthesis. R36 added 2 dossiers (MCTS-001, BMS-DOC-001). It serves as the canonical index for the entire ConnectX research corpus.*