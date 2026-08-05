# ConnectX Research Nexus — Corpus Index

> **Current Round**: 42 (2026-08-05)
> **Last Updated**: 2026-08-05 15:00 ET (Round 42)
> **Purpose**: Single entry point for navigating the entire ConnectX research corpus

---

## Corpus Statistics (Round 42)

| Category | Count | Range |
|----------|-------|-------|
| Claims | 222+ | C001-C222+ (unchanged from R41) |
| Verified | 100+ | 45% (unchanged) |
| Needs Correction | 22+ | 10% (unchanged) |
| Hypothesis | 24 | 11% (unchanged) |
| Other | 79+ | 34% (unchanged) |
| Hypotheses | 24 | HYP-001 through HYP-024 (unchanged) |
| Ensembles | 24 | E-001 through E-012, ENS-013 through ENS-024 (unchanged) |
| Contenders | 16 | BOT-001 through BOT-016 (unchanged) |
| Benchmark Suites | 19+ | BMS-001 through BMS-012, BMS-029 through BMS-035 (+ BMS-016 through BMS-021 from R42) |
| Experiments | 43+ | EXP-001 through EXP-043, EXP-NEW-001 through EXP-NEW-006 (+ EXP-NN-001 through EXP-NN-005, EXP-TS-001 through EXP-TS-004 from R42) |
| Sources | 131+ | S001 through S141+ (with 5 collision clusters — new S132-S139 collision from R42) |
| Dossiers | 25 | F-001, CS-001, CS-002, CS-003, CS-004, MCTS-001, MCTS-002, MCTS-003, MCTS-004, MCTS-005, BMS-DOC-001, BMS-DOC-002, BMS-DOC-003, GOV-001, GOV-002, GOV-003, GOV-004, D-034, RI-001, NN-001, NN-002, mcts-004, bms-doc-002, DOS-006, board-representation-and-move-generation (CS-002), opening-book-engineering (CS-001), search-algorithm-comparison (CS-004) |
| Governance Findings | 29+ | F-001 through F-022 (GOV-001) + C216-C220 (GOV-004) + FU-001 through FU-088 (R42 governance workers) |

---

## Source of Truth Hierarchy

| Tier | Files | Purpose |
|------|-------|---------|
| Tier 1: Master Report | `RESEARCH_REPORT.md` | Primary user entry point; living research summary |
| Tier 2: Canonical Index | `research/README.md` | Canonical file registry; round report table |
| Tier 3: Corpus Index | `research/NEXUS.md` | THIS FILE — cross-link map, collision ledger, dossier index |
| Tier 4: State Registers | `research/research-state.md`, `research/claim-register.md`, `research/source-ledger.md`, etc. | Working state; updated each round |
| Dossiers | 24 | F-001, CS-001, CS-002, CS-003, CS-004, MCTS-001, MCTS-002, MCTS-003, MCTS-004, BMS-DOC-001, BMS-DOC-002, GOV-001, GOV-002, GOV-003, GOV-004, D-034, RI-001, NN-001, NN-002, mcts-004, bms-doc-002, DOS-006, board-representation-and-move-generation (CS-002), opening-book-engineering (CS-001), search-algorithm-comparison (CS-004) |
| Tier 6: Iteration Reports | `research/iterations/round-NNN.md` | Per-round worker result summaries |

---

## Source ID Collision Map

5 collision clusters identified across rounds R16–R42. **30+ source IDs affected.**

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

### Cluster E — S132-S139 Cross-Batch Collision (R38 + R40 + R42)

| Colliding ID | Assigned In | Worker Description | Ledger Description |
|--------------|-------------|-------------------|-------------------|
| S130 | R38 + R40 + R42 | MCTS-NC README | haoxiang-xu/connectX web platform |
| S131 | R38 + R40 + R42 | rowspire README | katac4 README |
| S132 | R38 + R40 + R42 | TonyCWang dataset card | MCTS-NC README |
| S133 | R38 + R40 + R42 | NeuralConnect4 model card | rowspire README |
| S134 | R38 + R40 + R42 | ecc521 NNUE header | TonyCWang dataset card |
| S135 | R38 + R40 + R42 | ecc521 7x6 weights | NeuralConnect4 model card |
| S136 | R38 + R40 + R42 | ecc521 8x8 weights | ecc521 NNUE header |
| S137 | R38 + R40 + R42 | Chess Programming Wiki | ecc521 8x8 weights (NN-002) |
| S138 | R38 + R40 + R42 | Marcpaulo15 RL-connect4 | Chess Programming Wiki (MCTS tuning) |
| S139 | R38 + R40 + R42 | Waidchen XAI paper | connectpuct adversarial.py |

**Risk**: HIGH — 10 source IDs have been re-assigned with completely different descriptions across R38, R40, and R42. Worker-03 (NN-002, R42) used S132-S141 but S132-S139 already have different descriptions. Worker-06 (BMS-DOC-002, R42) reused S130-S137 with NN/mCTS descriptions that conflict with R38/R40 entries. Worker-02 (CS-005 proposal, R42) reused S138-S139 with classical search descriptions that conflict.

**Remediation**: S132-S139 require namespace isolation. Each S### within this range must be verified against the ledger entry and corrected to match a single authoritative description. NN-002's S132-S136 (NNUE-specific) should be reassigned to S142-S146. BMS-DOC-002's S130-S137 references should be corrected to point to the existing ledger entries.

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
| MCTS-003 | MCTS Variant Taxonomy (UCT, PUCT, LCB, FPU, PCR) | PROPOSED | `dossiers/mcts/mcts-003-mcts-variant-taxonomy.md |
| MCTS-004 | MCTS Deployment Architecture (Board-Size Templates, Timing Governance, Ensemble Integration) | PROPOSED | `dossiers/mcts/MCTS-004-MCTS-deployment-architecture.md |
| MCTS-005 | Hybrid Search Systems and Tactical Override Architectures (Tactical Override, Game-Phase Routing, TT Integration, Search Tree Management) | PROPOSED | `dossiers/mcts/MCTS-005-hybrid-search-systems.md` |



### Classical Search (5 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| CS-001 | Opening Book Engineering | READY | `dossiers/classical-search/CS-001-opening-book-engineering.md` |
| CS-002 | Board Representation and Move Generation | VERIFIED | `dossiers/classical-search/CS-002-board-representation-and-move-generation.md` |
| CS-003 | Classical Search and Solver Engineering | VERIFIED | `dossiers/classical-search/CS-003-classical-search-algorithm-engineering.md` |
| CS-004 | Search Algorithm Comparison | PROPOSED | `dossiers/classical-search/search-algorithm-comparison.md` |

### Foundational (1 dossier)

| ID | Title | Status | Path |
|----|-------|--------|------|
| F-001 | Board Representation and Win Detection | VERIFIED | `dossiers/foundations/board-representation-and-win-detection.md` |

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

### Neural (2 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| NN-001 | Neural Network Architectures, Training Pipelines, and Data | READY | `dossiers/neural/NN-001-neural-networks-architectures-training-pipelines-and-data.md` |
| NN-002 | NNUE Architecture Deep Dive — 7x6/8x8 source decode, incremental accumulator, ResNet specification, training data generation, inference optimization taxonomy | PROPOSED | `dossiers/neural/NN-002-train-deep-dive.md` |

**NN-001 scope:** 5 architecture families (ResNet, MLP, CNN, DQN, NNUE), 3 training pipelines, 18 sources, inference optimization (TensorRT INT8), board-size generalization.
**NN-002 scope:** NNUE incremental evaluation (O(changes) cost, QA=127 quantization), 7x6 vs 8x8 board size analysis, ResNet vs NNUE comparison.

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
BMS-DOC-002 (board-size scaling) -> DOS-006 (board-size routing) -> benchmark-blueprint.md (BMS-001 through BMS-012, BMS-029 through BMS-035)
BMS-DOC-002 (race detection) -> BMS-DOC-001 (reproducibility) -> BMS-012 (reproducibility protocol)
BMS-DOC-002 (seat-reversal bias) -> DOS-006 (contender deep profiles) -> ensemble-catalog.md
BMS-DOC-002 (latency budgeting) -> NN-001 (TensorRT latency) -> MCTS-002 (GPU patterns) -> BMS-DOC-001 (benchmarking)
NN-001 (neural eval) -> CS-003 (classical search) -> F-001 (foundations)

MCTS-005 (hybrid search) -> MCTS-001 (consistency) -> MCTS-002 (neural integration) -> MCTS-003 (variant taxonomy) -> MCTS-004 (deployment)
MCTS-005 (tactical override) -> CS-003 (classical search) -> CS-004 (algorithm comparison) -> CS-002 (board representation)
MCTS-005 (transposition table) -> CS-002 (hashing foundations) -> F-001 (win detection)
MCTS-005 (game-phase routing) -> DOS-006 (board-size analysis) -> ENS-002, ENS-004, ENS-008, ENS-011, ENS-013, ENS-014, ENS-018, ENS-023, ENS-024

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

- **Added 6 substantive dossiers:** NN-001 (Neural Network Architectures, 786 lines, 18 sources, VERIFIED), CS-001 (Opening Book Engineering, 591 lines, 12+ sources, READY), CS-002 (Board Representation and Move Generation, 718 lines, 10+ sources, VERIFIED), CS-003 (Classical Search Algorithm Engineering, 795 lines, 6 sources, VERIFIED), MCTS-004 (MCTS Deployment Architecture, 632 lines, 8 sources, PROPOSED), DOS-006 (Contender Deep Profiles and Board-Size Analysis, substantive, 10+ sources, VERIFIED)
- **Added:** BMS-DOC-002 (MCTS Consistency Theory, Board-Size Scaling Laws, and Benchmark Methodology Gaps — PROPOSED, 791 lines, ~38KB, 13+ sources, 8 code/pseudocode blocks, feasibility matrix)
- **Classical Search directory expanded:** 3→5 dossiers (added CS-001 opening book, CS-002 board representation)
- **Neural directory expanded:** 1→2 dossiers (added NN-002 NNUE deep dive)
- **MCTS directory expanded:** 5→6 dossiers (added MCTS-004 deployment architecture)
- **Contenders directory expanded:** 2→2 dossiers (DOS-006 deep profiles, already listed)
- **Dossiers count:** 18 → 24 across 12 directories (2 empty: ensembles, training-data)
- **New benchmarks proposed:** BMS-029 through BMS-035 (MCP consistency analysis, board-size scaling validation, race-condition detection, latency budget audit, seat-reversal bias test, time-allocation benchmark, statistical power analysis), BMS-046 through BMS-050 (MCTS deployment benchmarks)
- **New experiments specified:** EXP-NEW-001 through EXP-NEW-006 (MCTS consistency test, board-size scaling measurement, race detection, latency profiling, seat-reversal bias test, time allocation optimization), EXP-038 through EXP-043 (benchmark operational execution)
- **New claims:** C001-C010 verified (opening book claims), C022-C024 (board representation claims), C126-C129 (search algorithm claims), C222+ (governance claims)
- **Infrastructure:** Write tool restored in batch-00100 — 22/22 workers exit code 0, no tool failures reported

## Recent Changes (Round 42)

- **New dossier: MCTS-005** (`research/dossiers/mcts/MCTS-005-hybrid-search-systems.md`) — 680 lines, ~35KB. Hybrid search systems for ConnectX: tactical override layer (win/block/fork detection before MCTS), game-phase routing (alpha-beta vs MCTS vs neural-only selection), transposition table integration between classical and MCTS search, search tree management with virtual loss handling. Four core mechanisms verified across katac4, connectpuct, rowspire, and MCTS-NC implementations. 5+ sources (S130-S137). Status: PROPOSED.
- **Expanded dossier: NN-002** (`research/dossiers/neural/NN-002-train-deep-dive.md`) — 41,205 bytes, 19 sections. Full source-level decode of ecc521/connect-4-solver NNUE: 7x6 (84→256→1, 21,761 params, ~87 KB) and 8x8 (128→256→32→1, 45,057 params, ~180 KB) architectures, incremental accumulator with ~84x speedup, int32_t quantization (QA=127), ResNet source specification from katac4 (b3c128nbt architecture), training data generation (self-play with temperature schedule), inference optimization taxonomy (TensorRT INT8, ONNX Runtime, NNUE). 10 new primary/secondary sources (S132-S141). Status: PROPOSED.
- **Expanded dossier: BMS-DOC-002** — Added depth to MCP theorem treatment, board-size scaling laws, and methodology gap analysis. 39,078 bytes, 791 lines.
- **Source ID collision cluster E identified**: S132-S139 used across R38, R40, and R42 with completely different descriptions. 10 source IDs affected. Remediation required: NN-002 sources S132-S136 should be reassigned to S142-S146; BMS-DOC-002 and Worker-02 sources S130-S139 should be verified against ledger.
- **Governance findings**: 3 governance workers produced 233 total findings (FU-001 through FU-088 from worker-07-job-00616, FU-101 through FU-109 from worker-07-job-00617, and ~36 additional findings from worker-07-job-00618). Findings cover corpus gap repair, source ID collision remediation, header consistency, and automated governance tooling.
- **New experiments proposed**: EXP-NN-001 through EXP-NN-005 (NNUE vs classical eval benchmark, ResNet training on TonyCWang data, NNUE Kaggle T4 inference latency, katac4 self-play training reproduction, two-stage SFT→RL benchmark), EXP-TS-001 through EXP-TS-004 (tactical layer fork detection ELO impact, Kaggle profiling, ResNet with threat features, quiescence search effectiveness), BMS-016 through BMS-021 (tactical override accuracy, solved-game book coverage, TT hit rate, GPU MCTS throughput, NN policy temperature sweep, virtual loss tuning).
- **Workers that failed to write**: Worker-02 (Job 637, CLASSICAL_SEARCH) proposed CS-005 (Tactical Safety Layer) but Write tool unavailable — no file written. Worker-01 (Job 587, SOURCE_DOSSIERS) proposed RI-002 (On-Chain and Classical Source Archaeology) but no file written.
- **MCTS directory expanded**: 6→6 dossiers (MCTS-005 new addition).
- **Neural directory expanded**: 2→2 dossiers (NN-001 + NN-002, both substantive).
- **Dossiers count**: 24 → 25 (MCTS-005 new; NN-002 and BMS-DOC-002 are expansions, not new count).
- **Empty directories**: 2 (ensembles, training-data — unchanged).
- **Infrastructure**: Write tool partially restored — 3 of 8 workers successfully wrote dossiers (NN-002, BMS-DOC-002, MCTS-005). 3 governance workers produced findings without writing new dossier files. 2 workers failed to write (Write tool unavailable).
