# ConnectX Research Nexus — Corpus Index

> **Current Round**: 47 (2026-08-05)
> **Last Updated**: 2026-08-05 22:00 ET (Round 47)
> **Purpose**: Single entry point for navigating the entire ConnectX research corpus

---

## Corpus Statistics (Round 47)

| Category | Count | Range |
|----------|-------|-------|
| Claims | 280+ | C001-C295 (C226-C240 gov R43, C241-C260 gov R44-R45, C256-C295 gov R45-R46) |
| Verified | 135+ | 48% (includes C233-C236 MCTS-007 R45, C226-C260 gov R43-R45, C256-C295 gov R45-R46, C276-C295 GOV-009 VERIFIED) |
| Needs Correction | 24 | 9% (same as R46) |
| Hypothesis | 24 | 9% (unchanged) |
| Other | 97+ | 35% (unchanged minus C276-C295 promotion) |
| Hypotheses | 24 | HYP-001 through HYP-024 (unchanged) |
| Ensembles | 24 | E-001 through E-012, ENS-013 through ENS-024 (unchanged) |
| Contenders | 24+ | BOT-001 through BOT-017, DOS-006, DOS-007, CBL-002, KAGGLE-CONNX-SPEC, CON-001 |
| Benchmark Suites | 54+ | BMS-001-BMS-012, BMS-016-BMS-021, BMS-029-BMS-039, EXP-BMS-001-008, BMS-NN-001-007, BMS-KAM-001-006, BMS-CON-001-006 |
| Experiments | 96+ | EXP-001-046, EXP-NEW-001-010, EXP-NN-001-006, EXP-TS-001-004, EXP-BMS-001-008 |
| Sources | 165+ | S001-S165 (NN-004 claimed S158-S169 — **COLLISION** with RI-002 S158-S165; Kamide claimed S158-S163 — **COLLISION** with RI-002) |
| Dossiers | 46+ | 39 substantive + 7 test/artifact across 12 directories (3 empty: ensembles, kaggle, training-data) |
| Governance Findings | 110+ | F-001-F-022 (GOV-001) + C216-C220 (GOV-004) + C226-C240 (GOV-006 R43) + C241-C260 (GOV-007 R44-R45) + C276-C295 (GOV-009 R46) + FU-001-FU-186 |
| Remediation Rate | 100% | 17/22 fully + 5/22 partially repaired (GOV-009 R46). **100% coverage plateau** — 0 fully unaddressed for 2 rounds |

---

## Source of Truth Hierarchy

| Tier | Files | Purpose |
|------|-------|---------|
| Tier 1: Master Report | `RESEARCH_REPORT.md` | Primary user entry point; living research summary |
| Tier 2: Canonical Index | `research/README.md` | Canonical file registry; round report table |
| Tier 3: Corpus Index | `research/NEXUS.md` | THIS FILE — cross-link map, collision ledger, dossier index |
| Tier 4: State Registers | `research/research-state.md`, `research/claim-register.md`, `research/source-ledger.md`, etc. | Working state; updated each round |
| Tier 5: Dossiers | 45+ | | See Dossier Index below — GOV-001 through GOV-008, CS-001 through CS-005, MCTS-001 through MCTS-008, BMS-DOC-002 through BMS-DOC-007, NN-001 through NN-004, DOS-006, DOS-007, CBL-002, KAGGLE-CONNX-SPEC, RI-001, RI-002, CON-001, KAMIDE-CONNECT-N (uncommitted), benchmark-science-and-tournament-design (38 substantive + 7 test/artifact) |
| Tier 6: Iteration Reports | `research/iterations/round-NNN.md` | Per-round worker result summaries |

---

## Source ID Collision Map

7 collision clusters identified across rounds R16–R48. **41+ source IDs affected.**

### Cluster F — RI-002 / NN-004 / Kamade source overlap (R45, R46, R47) **NEW**

| Source ID | RI-002 usage (R45) | NN-004 usage (R46) | Kamade usage (R47 planned) | Resolution |
|-----------|-------------------|-------------------|--------------------------|------------|
| S158-S163 | RI-002 reference implementation sources | NN-004 transfer learning sources | Kamade source sources | **CRITICAL** — all three dossiers claim same IDs for different content. Must re-index NN-004 to S166-S177 and Kamade to S178-S183. |
| S164-S165 | RI-002 sources | NN-004 claims | — | Overlap with NN-004 |

**Remediation**: Cluster F re-indexing sprint required in R48. NN-004 sources must be re-indexed to S166-S177. Kamade sources must be re-indexed to S178-S183. **STATUS R48: 0% remediated, 7 rounds.** NN-005 claimed S174-S183 (non-overlapping) but created Cluster G with RI-007.

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

### Cluster E — S132-S146 Cross-Batch Collision (R38 + R40 + R42 + R43)

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
| S140 | R42 (NN-002) | Chess Programming Wiki (MCTS) | Waidchen XAI paper (NN-002) |
| S141 | R42 (NN-002) | Waidchen XAI paper (NN-002) | Chess Programming Wiki (MCTS) |
| S142 | R42 (NN-002) | ecc521 NNUE.hpp | NNUE.hpp (NN-002) |
| S143 | R42 (NN-002) | ecc521 nnue_weights_7x6.hpp | nnue_weights_7x6 (NN-002) |
| S144 | R42 (NN-002) | ecc521 nnue_weights_8x8.hpp | nnue_weights_8x8 (NN-002) |
| S145 | R42 (NN-002) | ecc521 NNUEAccumulator.hpp | NNUEAccumulator (NN-002) |
| S146 | R42 (NN-002) | Waidchen XAI paper | Waidchen XAI (NN-002) |

**Risk**: CRITICAL — 17 source IDs (S130–S146) have been re-assigned with completely different descriptions across R38, R40, R42, and R43 (GOV-006 confirms all 5 collision clusters persist). NN-002's S136–S141 reassigned to S142–S146 (R42). NN-003's S150–S157 verified non-colliding. RI-002's S158–S165 verified non-colliding.

**Remediation**: S130–S141 require namespace isolation (e.g., S130E–S141E). Each S### within this range must be verified against the ledger entry and corrected to match a single authoritative description. NN-002's S136–S141 (NNUE-specific) have been reassigned to S142–S146 (completed, R42). New sources should be assigned IDs above S165. S142–S146 are verified as non-colliding NNUE-specific sources. S150–S157 and S158–S165 verified non-colliding.

**R45 Note**: RI-002 added S158–S165 (connectpuct) — verified non-colliding. NN-004 agent claimed S160–S173; S160–S165 overlap with NN-003/RI-002; unique sources S166–S173 need de-duplication and unique assignment.

### Cluster F — S158–S169 Cross-Dossier Collision (R45–R47)

| Claimant | Source Range | Dossier | Ledger Assigned |
|----------|-------------|---------|-----------------|
| RI-002 (R45) | S158–S165 | connectpuct PUCT MCTS | connectpuct engine, mcts, minimax, adversarial, benchmark, pyproject.toml, README.md |
| NN-004 (R46) | S158–S169 (overlaps S158–S165) | Transfer Learning — 15x13 | **COLLISION** — NN-004's S158–S165 overlap with RI-002's S158–S165. NN-004's S166–S169 are verified non-colliding. |
| Kamade (planned R47) | S158–S163 (overlaps) | Contender dossier (NOT PERSISTED) | **COLLISION** — Kamade planned but never persisted to disk. |

**Impact**: Any dossier citing S160 (NNUE spec) or S163 (adversarial.py) could resolve to RI-002 or NN-004 content. **CRITICAL for implementers.**

**Remediation**: NN-004 sources S158–S169 need re-indexing to S166–S177. Kamade sources need re-indexing to S178–S183. RI-002 sources S158–S165 verified as canonical — no change needed.

### Cluster G — S174–S176 RI-007 / NN-005 Collision (NEW, R48)

| Claimant | Source Range | Dossier | Description |
|----------|-------------|---------|-------------|
| RI-007 (R48) | S166–S176 (includes S174–S176) | 3 new reference impls | S174 = minimax.rs (jesper-olsen), S175 = haithameleuch/connect-four-ai repo, S176 = VierGewinnt.kt |
| NN-005 (R48) | S174–S183 | Model Compression | S174 = Deep Compression (arXiv:1510.00149), S175 = Distillation (arXiv:1503.02531), S176 = Lottery Ticket (arXiv:1803.03635) |

**Impact**: S174–S176 are claimed by both RI-007 (reference source files) and NN-005 (academic papers). **CRITICAL** — these IDs must be disambiguated.

**Remediation**: NN-005's S174–S183 are canonical (academic papers). RI-007's S174–S176 need re-indexing to S184–S186. RI-007's S166–S173 overlap with ledger entries from R45/R46 (jesper-olsen/repos, Woonderpipe, Karthick-dev-cart, sidhantagar, Kaggle official) — these should cross-reference existing ledger entries rather than re-claim.

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

### Governance (9 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| GOV-001 | Corpus Governance Audit — Round 34 Full Structural Assessment | VERIFIED | `dossiers/governance/GOV-001-corpus-governance-audit-round-34.md` |
| GOV-002 | R36 Gap Repair — Remediation Tracking | VERIFIED | `dossiers/governance/GOV-002-R36-gap-repair-remediation-tracking.md` |
| GOV-003 | R36 Governance Gap Repair — Post-Merger Assessment | VERIFIED | `dossiers/governance/GOV-003-R36-gap-repair-executive-report.md` |
| GOV-004 | R37 Comprehensive Corpus Audit | VERIFIED | `dossiers/governance/GOV-004-R37-comprehensive-audit.md` |
| GOV-005 | R42 Comprehensive Corpus Governance Audit | VERIFIED | `dossiers/governance/GOV-005-R42-comprehensive-corpus-governance-audit.md` |
| GOV-006 | R43 Corpus Governance and Index Audit | VERIFIED | `dossiers/governance/GOV-006-R43-corpus-governance-and-index-audit.md` |
| GOV-007 | R43→R44 Post-Commit Governance Audit | VERIFIED | `dossiers/governance/GOV-007-R43-to-R44-post-commit-governance-audit.md` |
| GOV-008 | R45 Master Governance Report — 77% Remediation | PROPOSED | `dossiers/governance/GOV-008-R45-master-governance-report.md` |
| GOV-009 | R46 Master Governance Report — 100% Coverage Plateau | PROPOSED | `dossiers/governance/GOV-009-R46-master-governance-report.md` |

### MCTS (8 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| MCTS-001 | MCTS Consistency Problem for Solved Games | VERIFIED | `dossiers/mcts/MCTS-consistency-solved-games.md` |
| MCTS-002 | Neural MCTS Integration Patterns | VERIFIED | `dossiers/mcts/mcts-002-neural-integration-patterns.md` |
| MCTS-003 | MCTS Variant Taxonomy (UCT, PUCT, LCB, FPU, PCR) | PROPOSED | `dossiers/mcts/mcts-003-mcts-variant-taxonomy.md` |
| MCTS-004 | MCTS Deployment Architecture (Board-Size Templates, Timing Governance, Ensemble Integration) | PROPOSED | `dossiers/mcts/MCTS-004-MCTS-deployment-architecture.md` |
| MCTS-005 | Hybrid Search Systems and Tactical Override Architectures (Tactical Override, Game-Phase Routing, TT Integration, Search Tree Management) | PROPOSED | `dossiers/mcts/MCTS-005-hybrid-search-systems.md` |
| MCTS-006 | Transposition-Aware MCTS (Node Merging, Position Hashing, Move Ordering via Transpositions, GPU Handling) | PROPOSED | `dossiers/mcts/MCTS-006-transposition-aware-mcts.md` |
| MCTS-007 | GPU-Accelerated MCTS | PROPOSED | `dossiers/mcts/MCTS-007-gpu-accelerated-mcts.md` |
| MCTS-008 | Rollout/Playout Strategy Design (Random, Tactical, Policy-Guided, Hybrid Playouts) | PROPOSED | `dossiers/mcts/MCTS-008-rollout-playout-strategy-design.md` |



### Classical Search (5 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| CS-001 | Opening Book Engineering | READY | `dossiers/classical-search/CS-001-opening-book-engineering.md` |
| CS-002 | Board Representation and Move Generation | VERIFIED | `dossiers/classical-search/CS-002-board-representation-and-move-generation.md` |
| CS-003 | Classical Search and Solver Engineering | VERIFIED | `dossiers/classical-search/CS-003-classical-search-algorithm-engineering.md` |
| CS-004 | Search Algorithm Comparison | PROPOSED | `dossiers/classical-search/search-algorithm-comparison.md` |
| CS-005 | Evaluation Function Design for ConnectX | PROPOSED | `dossiers/classical-search/CS-005-evaluation-function-design-for-connectx.md` |

### Foundational (1 dossier)

| ID | Title | Status | Path |
|----|-------|--------|------|
| F-001 | Board Representation and Win Detection | VERIFIED | `dossiers/foundations/board-representation-and-win-detection.md` |

### Benchmarking (6 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| BMS-DOC-001 | Benchmark Science and Tournament Design | VERIFIED | `dossiers/benchmarking/benchmark-science-and-tournament-design.md` |
| BMS-DOC-002 | MCTS Consistency Theory and Board-Size Scaling | PROPOSED | `dossiers/benchmarking/bms-doc-002-mcts-consistency-theory-and-board-size-scaling.md` |
| BMS-DOC-003 | Ensemble Interaction and Adversarial Benchmarking | PROPOSED | `dossiers/benchmarking/bms-doc-003-ensemble-interaction-and-adversarial-benchmarking.md` |
| BMS-DOC-004 | Kaggle Evaluation Protocol | PROPOSED | `dossiers/benchmarking/bms-doc-004-kaggle-evaluation-protocol.md` |
| BMS-DOC-005 | Kaggle Competitive Benchmark Design and Evaluation Protocol | PROPOSED | `dossiers/benchmarking/bms-doc-005-kaggle-competitive-benchmark-design-and-evaluation.md` |
| BMS-DOC-006 | Hardware Performance Profiling and Feasibility Boundaries | PROPOSED | `dossiers/benchmarking/bms-doc-006-hardware-performance-profiling-and-feasibility-boundaries.md` |

### Reference Implementations (5 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| D-034 | New Source Repositories Discovered in GitHub Topic Scan | VERIFIED | `dossiers/reference-implementations/new-repo-sources-r34.md` |
| RI-001 | katac4 Reference Implementation (AlphaZero + KataGo) | VERIFIED | `dossiers/reference-implementations/katac4-reference-implementation.md` |
| KAGGLE-CONNX-SPEC | Kaggle ConnectX Environment Spec and Interpreter (JSON Spec, Python Interpreter, Built-in Agents, Game Contract) | PROPOSED | `dossiers/reference-implementations/KAGGLE-CONNX-SPEC.md` |
| RI-002 | connectpuct PUCT MCTS with Tactical Priors | PROPOSED | `dossiers/reference-implementations/RI-002-connectpuct-puct-mcts-with-tactical-priors.md` |
| RI-007 | Three New ConnectX Reference Implementations from 2026 Scan: Tarun995 (Python+Numba bitboard), jesper-olsen (Rust Tromp solver), haithameleuch (Kotlin hybrid) | PROPOSED | `dossiers/reference-implementations/RI-007-three-new-connectx-reference-implementations-from-2026-scan.md` |

### Contenders (6 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| CBL-001 | Contenders, Baselines, and Benchmark References | PROPOSED | `dossiers/contenders/CBL-001-contenders-baselines-benchmark-comprehensive.md` |
| CB-001 | Kaggle Official Built-in Agents — Complete Source Analysis | PROPOSED | `dossiers/contenders/CB-001-kaggle-official-builtin-agents.md` |
| D-CBL-001 | Baseline Contender Comparison | PROPOSED | `dossiers/contenders/contenders-baselines-benchmark-references.md` |
| DOS-006 | Contender Deep Profiles and Board-Size Analysis | VERIFIED | `dossiers/contenders/contenders-deep-profiles-and-board-size-analysis.md` |
| DOS-007 | Kaggle Competitive Analysis — Algorithmic Trade-offs, Board-Size Scaling, Ensemble Strategy | READY | `dossiers/contenders/DOS-007-kaggle-competitive-analysis.md` |
| CON-001 | New Contenders and Benchmark Framework | READY | `dossiers/contenders/CON-001-new-contenders-and-benchmark-framework.md` |

### Neural (4 dossiers)

| ID | Title | Status | Path |
|----|-------|--------|------|
| NN-001 | Neural Network Architectures, Training Pipelines, and Data | READY | `dossiers/neural/NN-001-neural-networks-architectures-training-pipelines-and-data.md` |
| NN-002 | NNUE Architecture Deep Dive — 7x6/8x8 source decode, incremental accumulator, ResNet specification | PROPOSED | `dossiers/neural/NN-002-train-deep-dive.md` |
| NN-003 | Training Methodology Deep Dive — Temperature Schedules, Replay Buffer Dynamics, AZAL, Board-Size Training | PROPOSED | `dossiers/neural/NN-003-training-methodology-deep-dive.md` |
| NN-004 | Transfer Learning — 7x6→15x13 Fine-Tuning, Board-Size Invariant CNN, AZAL Multi-Frame Adaptation | PROPOSED | `dossiers/neural/NN-004-transfer-learning.md` |
| NN-005 | Model Compression: Pruning, Quantization, and Distillation — Global Magnitude Pruning, INT8 PTQ/QAT, Hinton Distillation, 100K-Param Students for 2000-5000 MCTS Eval/Move | PROPOSED | `dossiers/neural/NN-005-model-compression-pruning-quantization-and-distillation.md` |

**NN-001 scope:** 5 architecture families (ResNet, MLP, CNN, DQN, NNUE), 3 training pipelines, 18 sources, inference optimization (TensorRT INT8), board-size generalization.
**NN-002 scope:** NNUE incremental evaluation (O(changes) cost, QA=127 quantization), 7x6 vs 8x8 board size analysis, ResNet vs NNUE comparison.
**NN-003 scope:** Temperature decay formulas (corrected katac4: max(1.03, 1.35*pow(0.66, step/bs))), replay buffer dynamics (alpha=0.75, beta=0.4, 250K capacity), AZAL auxiliary loss (0.785 oracle match), board-size training strategy (9x9 through 12x12 randomization), Kaggle T4/CPU training feasibility, 8 sources (S150-S157).
**NN-004 scope:** Transfer learning for 15x13 board-size generalization. 12 sources (S158-S169, collision with RI-002). Fine-tuning strategies, NNUE weight switching, AZAL multi-frame adaptation, DQN architecture comparison. 3 adapted sketches + 2 pseudocode blocks. 7 benchmark requirements (BMS-NN-001 through BMS-NN-007).
**NN-005 scope:** Model compression for ConnectX neural nets. Global magnitude pruning, structured channel pruning, PTQ/QAT to INT8, Hinton knowledge distillation, feature-based matching, deployment optimization. 10 sources (S174-S183). Key claim: distilled student (~100K-200K params) enables 2,000-5,000 MCTS evals/move vs 200-400 with large ResNet. 4 adapted sketches + 3 pseudocode blocks.

### Empty Directories (3)

### Empty Directories (3)

| Directory | Status | Action Needed |
|-----------|--------|---------------|
| ensembles/ | EMPTY | Needs ensemble design dossiers |
| training-data/ | EMPTY | Needs training pipeline data dossiers |
| kaggle/ | EMPTY | Needs Kaggle environment/agent dossiers |

---

## Cross-Link Map

### Governance Chain
GOV-001 (22 findings R34) -> GOV-002 (remediation tracking R36) -> GOV-003 (post-merger assessment R36) -> GOV-004 (comprehensive audit R37, 55%) -> GOV-005 (comprehensive audit R42, 68%) -> GOV-006 (index audit R43, 73%) -> GOV-007 (post-commit audit R44, 75%) -> GOV-008 (master governance report R45, 77%) -> GOV-009 (master governance report R46, 100% coverage plateau)


CS-001 (opening books) -> CS-002 (board rep) -> CS-003 (solver engineering) -> CS-004 (algorithm comparison) -> F-001 (foundations)
CS-005 (evaluation function design) -> CMP-003, CMP-012, CMP-014, CMP-017 (component dependencies)

RI-001 (katac4 reference) -> D-034 (new repos) -> D-CBL-001 (baseline contenders) -> DOS-006 (deep profiles) -> BMS-DOC-001 (benchmarking)
DOS-006 (deep profiles) -> CS-003 (classical search) -> F-001 (foundations)
DOS-006 (board-size routing) -> ENS-NEW-001/002/003 (ensemble designs)
DOS-006 (contender deep profiles) -> ensemble-catalog.md (ensemble designs)
DOS-006 (benchmark mapping) -> benchmark-blueprint.md (BMS-001 through BMS-012)
DOS-007 (algorithmic trade-offs) -> DOS-005, DOS-006, CBL-001 (contender survey, deep profiles, systematic roster)
DOS-007 (board-size scaling) -> BMS-DOC-002 (board-size scaling), CS-003 (classical search)
DOS-007 (Kaggle strategy) -> ENS-001 through ENS-024 (ensemble catalog), BMS-DOC-001 (benchmarking)
DOS-007 (new contenders) -> RI-001 (reference implementations), D-034 (new repos)

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
- **Added:** DOS-007 (Kaggle Competitive Analysis — Algorithmic Trade-offs, Board-Size Scaling, Ensemble Strategy — 522 lines, ~38KB, 6 new + 6 previously assigned sources, READY). Covers algorithmic trade-off analysis, board-size scaling laws (branching factor, TT degradation, NN generalization gap), 3 new contender discoveries (puissance4, CogitoNTNU/AlphaZero, spooky-connect4), 5 Kaggle-optimized ensemble designs (K-ENSEMBLE-001 through K-005), competitive strategy playbook.
- **Added:** CS-004 (Search Algorithm Comparison — 761 lines, 31.7KB, 8+ sources, 7 algorithm specs, self-corrections C006/C007)
- **Added:** RI-001 (katac4 Reference Implementation — 771 lines, 51.2KB, 13 sources via WebFetch, VERIFIED)
- **Expanded:** MCTS-003 (variant taxonomy expanded to 8 variants, 6 hybrid patterns)
- **Rejected:** mcts-004 (thin), batch-00097 total failure (8/8 workers), batch-00099 9/18 workers failed (Write tool unavailable or no output)
- **Updated:** Dossier count from 9 to 17 across 11 directories (2 empty: ensembles, training-data)
- **Updated:** Dossier count from 14 to 17 (DOS-006); contenders directory now has 2 dossiers
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

## Recent Changes (Round 43)

- **Expanded dossier: NN-002** — Added NNUE decode section with 7x6 and 8x8 source-level architecture analysis, incremental accumulator details, QA=127 quantization, ResNet source specification from katac4, training data generation, inference optimization taxonomy. 12 new sources (S142–S146, plus S_NEW_003–S_NEW_014 from CBL-001). Status: PROPOSED.
- **Created dossier: MCTS-005** (`research/dossiers/mcts/MCTS-005-hybrid-search-systems.md`) — 680 lines, ~35KB. Hybrid search systems for ConnectX: tactical override layer (win/block/fork detection before MCTS), game-phase routing (alpha-beta vs MCTS vs neural-only selection), transposition table integration between classical and MCTS search, search tree management with virtual loss handling. Status: PROPOSED.
- **Created dossier: CBL-001** (`research/dossiers/contenders/CBL-001-contenders-baselines-benchmark-comprehensive.md`) — Comprehensive contender baseline analysis with 14 new sources. Status: PROPOSED.
- **Created dossier: DOS-007** (`research/dossiers/contenders/DOS-007-kaggle-competitive-analysis.md`) — Kaggle competitive analysis covering algorithmic trade-offs, board-size scaling, and ensemble strategy. Status: READY.
- **Created dossier: BMS-DOC-003** (`research/dossiers/benchmarking/bms-doc-003-ensemble-interaction-and-adversarial-benchmarking.md`) — Ensemble interaction and adversarial benchmarking dossier. Status: PROPOSED.
- **Source collision**: Cluster E remediation — S136→S142, S137→S143, S138→S144, S139→S145, S140→S146, S141→S146+1. New S142–S146 added to source-ledger.md.
- **Dossiers**: 25→31 (MCTS-005 new, CBL-001 new, DOS-007 new, BMS-DOC-003 new, NN-002 expanded, 3 test files archived).
- **Governance findings**: FU-001–FU-109+ covering corpus governance across R42–R43.


## Changes Since Last Synthesis (Round 41 → 42)

- **New dossier: CS-005** (
esearch/dossiers/classical-search/CS-005-evaluation-function-design-for-connectx.md) — 88,173 bytes, 1430 lines. Comprehensive evaluation function design specification for ConnectX: 6 architectural patterns (window-scoring, feature-aggregation, threat-map, adaptive-formula, exact-solving, neural-dual-head), source-level analysis of 7 implementations (rowspire, Kamide, QveenCoder, ariaborin, Pascal Pons, marcpaulo15, Tromp fhourstones88), genetic tuning deep-dive (16 parameters, threat_weight +142%, piece_count -88%), asymmetric evaluation (1.2x opponent threat from 3 independent sources), fork detection algorithms (Tromp O(WIDTH) pruning), terminal value asymmetry comparison, feature taxonomy (9 categories), board-size adaptability analysis, neural SFT>RL pipeline (marcpaulo15), evaluation design decision framework. 20+ sources. 5 adapted reference sketches + conceptual pseudocode. Status: PROPOSED.
- **Classical Search directory expanded:** 4→5 dossiers (added CS-005).
- **Dossiers count:** 18→19 (1 new CS dossier).
- **Empty directories:** 2 (ensembles, training-data — unchanged).



CS-005 (evaluation function design) -> CMP-003, CMP-012, CMP-014, CMP-017 (component dependencies)







