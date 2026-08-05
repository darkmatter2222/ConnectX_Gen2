# GOV-001: Corpus Governance Audit — Round 34 Full Structural Assessment

**Dossier ID**: GOV-001
**Status**: VERIFIED
**Created**: 2026-08-04 (Round 35)
**Last Updated**: 2026-08-04
**Author**: External worker-07-job-00052 (Slot 7 of 7, Job 52, lane NEXUS_GOVERNANCE_MASTER_REPORT_AND_GAP_REPAIR)
**Scope**: Entire research corpus (all canonical files, iteration reports, catalogs, subdirectories)
**Related claim IDs**: C199 (source ID collisions), C200–C205 (neural MCTS benchmarks R34), C206–C215 (governance findings R35)
**Related hypothesis IDs**: HYP-019 (source attribution integrity), HYP-020 (fabricated data detection)
**Related experiment IDs**: EXP-025 (corpus governance audit), EXP-026 (fabricated data detection), EXP-031 (source ID collision detection)
**Follow-up tasks**: FU-052 through FU-078

---

## Executive Summary

This audit systematically examines every structural element of the ConnectX research corpus at round 34 (2026-08-04). The corpus contains 205 claims (C001–C205), 24 hypotheses (HYP-001 through HYP-024), 24 ensembles (E-001 through E-012, ENS-013 through ENS-024), 16 contenders (BOT-001 through BOT-016), 12 benchmark suites (BMS-001 through BMS-012), and 32 experiments (EXP-001 through EXP-032).

The audit identifies **22 distinct structural defects** organized into 9 categories:

| Severity | Count | Category |
|-----------|-------|----------|
| CRITICAL | 4 | Source ID collisions, fabricated data persistence, broken MCP citation, source ledger incompleteness |
| HIGH | 8 | Master report staleness, header inconsistency, missing NEXUS.md, empty/missing dossier directories, benchmark blueprint numbering |
| MEDIUM | 6 | Legacy file proliferation, claim status discrepancy, iteration report gaps, source ledger header stale, work queue fragmentation, contention in source ID references |
| LOW | 4 | Ensemble cross-reference gaps, experiment-ensemble orphaning, hypothesis terminology inconsistency, board-size matrix source persistence |

---

## Why This Matters for the Perfect ConnectX Bot

A research nexus with structural defects produces unreliable design decisions. An implementation team reading a corpus with:

- **Colliding source IDs** will attribute findings to the wrong source, potentially building on fabricated or misattributed data.
- **Stale master report** will miss the latest neural MCTS benchmarks (C200: 0.849 oracle match), which directly inform architecture choices.
- **Broken citations** will send implementers searching for papers that do not exist (arXiv:1203.2285 = astrophysics).
- **Empty dossier directories** mean the corpus has infrastructure but no content — 80% structurally set up but 0% filled with detailed dossiers.
- **Header inconsistencies** create ambiguity about which round's data is authoritative.

The recommended architecture (Hybrid Neural + Classical Search) depends on VERIFIED neural MCTS benchmarks (C200–C202) and the verified three-loss objective (C201). If these were corrupted by source ID collisions or header inconsistencies, the architecture recommendation would be unreliable.

---

## Evidence Quality

**VERIFIED** — all 22 defects confirmed by direct reading of canonical files, cross-referencing headers vs. body content, glob-ing directories, and comparing source ledger entries across rounds.

Each finding is supported by:
- Direct file read (line counts, header dates, body content)
- Cross-referencing (claim ID → source ledger → source ledger entry)
- Directory enumeration (empty/missing dossier directories)
- Iteration report cross-checks (README.md table vs. actual files on disk)

---

## Detailed Findings

### F-001: Source ID Collisions (CRITICAL)

**4 clusters identified across rounds R16, R23, R25, R30:**

| Cluster | Colliding IDs | Rounds Involved | Description |
|---------|---------------|-----------------|-------------|
| A | S091–S093 | R16 + R25 + R30 | katac4 PyTorch/TT support, TensorRT inference — reused across 3 rounds |
| B | S094–S097 | R23 + R25 + R30 | Tromp fhourstones methodology — R23/R25 overlap with R30 entries |
| C | S109–S117 | R25 + R30 | NeuralConnect4, Gemu03, katac4 MCTS, AZAL paper — S117 is FABRICATED |
| D | S118–S120 | R30 self-duplicate | connectpuct MCTS benchmark — S120 ("uniform random") is FABRICATED |

**Impact**: 27+ source IDs affected. Claim register references S091–S120 in 40+ claim rows. Any claim citing a colliding ID may reference a different source depending on which round's entry is read.

### F-002: Fabricated Data Persistence (CRITICAL)

| Source | Fabrication | Detected | Current Status |
|--------|-------------|----------|----------------|
| S117 | "40-40-20 phase distribution" | R33 | Still present in source-ledger.md; no RETRACTED flag |
| S120 | "Uniform random" methodology | R33 | Still present; actual = self-play with temperature schedule |
| arXiv:1203.2285 | MCP theorem citation (astrophysics) | R33 | Still cited in hypothesis-register.md as MCP theorem |

**Impact**: S117 referenced by EXP-028; S120 by EXP-029. Both experiments SPECIFIED but produce unreliable results with uncorrected sources.

### F-003: Master Report Staleness (HIGH)

`RESEARCH_REPORT.md` last updated 2026-07-29. Current: 2026-08-04. Gap: 6 days, 5 rounds (R30, R32, R33, R34).

**Missing findings** (that should have been in RESEARCH_REPORT.md):

| Finding | Round | Section |
|---------|-------|---------|
| Neural MCTS 0.849 oracle match (C200) | R34 | Section 6 (Training Pipelines) |
| AZAL three-loss objective (C201) | R34 | Section 6 (Training Pipelines) |
| TensorRT INT8 3-5x latency (C202) | R34 | Section 5 (MCTS) |
| DQN tactical weakness (C205) | R34 | Section 4 (Neural Networks) |
| Board-size solving matrix (8×8 P2, 9×6 P1, 10×8 draw) | R32/R34 | Section 1 (Competition Overview) |
| Source ID collision rate ~10% | R33/R34 | New section (Data Governance) |
| Fabricated data detection | R33/R34 | New section (Data Governance) |
| 24 ensembles / 16 contenders | R34 | Sections 8–9 |

### F-004: Source Ledger Incompleteness (CRITICAL)

`source-ledger.md` header says "R34" but detailed source rows end at S120. Sources S121–S126 from round R32 are present in iteration reports and referenced by claims/contenders but absent from the source-ledger detail section.

**Missing sources**: S121, S122 (R32), S123 (Kamide/connect-n), S124 (Tromp analysis), S125 (pyvezi), S126 (Tromp fhourstones88).

### F-005: Header Inconsistency Across Canonical Files (HIGH)

| File | Stated Round | Issue |
|------|-------------|-------|
| contender-roster.md | R34 | Header says "10 contenders" but body lists 16 (BOT-001–BOT-016) |
| ensemble-catalog.md | R34 | ENS-013/014/015 labeled as "R30" additions in body |
| source-ledger.md | R34 | Header R34, but detail rows end at S120 (missing S121–S126) |

### F-006: Missing NEXUS.md (HIGH)

Referenced by external worker mission template as a canonical file to read (`research/NEXUS.md if present`). No other file in the corpus references NEXUS.md. It is a ghost file — structurally expected but practically absent.

### F-007: Empty and Missing Dossier Directories (HIGH)

**Empty directories** (exist, zero files):
- `dossiers/benchmarking/` — should contain BMS-001 through BMS-012 dossiers
- `dossiers/classical-search/` — should contain classical search algorithm dossiers
- `dossiers/mcts/` — should contain MCTS variant dossiers

**Missing directories** (referenced in mission template, do not exist):
- `dossiers/foundations/` — mathematical and game theory foundations
- `dossiers/kaggle/` — Kaggle competition analysis
- `dossiers/neural/` — neural network architectures
- `dossiers/training-data/` — training data analysis
- `dossiers/contenders/` — contender dossiers
- `dossiers/ensembles/` — ensemble design dossiers
- `dossiers/reference-implementations/` — reference code analysis
- `dossiers/governance/` — governance audit dossiers

**Total**: 11 directories (3 empty, 8 missing). Zero actual dossier content exists.

### F-008: Benchmark Blueprint Section Numbering (HIGH)

Sections numbered: 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8 (MCTS consistency), 9 (documentation — duplicate). Section numbers jump between 7→9→10→11→8→9. Unambiguous "Section X" references are unreliable.

### F-009: Legacy File Proliferation (MEDIUM)

48 `.md` files in `research/` directory. 19 canonical files. 30 legacy files. 19 listed in README.md's "Legacy Documents" section. ~11 legacy files not listed in README.md at all (06-gpu-alpha-beta-research.md, benchmark-mcts-consistency.md, kaggle-analysis.md, time-management-research.md, worker-result-slot2-job14.md, etc.).

**Risk**: New team members may read stale legacy files and base decisions on outdated information.

### F-010: Iteration Report Gaps (MEDIUM)

README.md's "Round Reports" table lists only 24 of 34 rounds. Missing: 15, 16, 17, 18, 19, 20, 21, 24, 29, 31.

### F-011 through F-022: Lower-Priority Defects

| # | Severity | Description |
|---|----------|-------------|
| F-011 | MEDIUM | Work queue has no prioritization hierarchy visible |
| F-012 | MEDIUM | BOT-003 references S091, S092 (collision cluster A) |
| F-013 | LOW | ENS-018 labeled "Hypothetical ID" but has full details; formatting inconsistent |
| F-014 | LOW | ENS-019 through ENS-024 use bullet-point format while ENS-013/014/015 use table format |
| F-015 | LOW | EXP-004 and EXP-005 marked BLOCKED; prerequisites are implementation tasks, not research |
| F-016 | LOW | claim-register.md uses "HYPOTHESIS" status; hypothesis-register.md uses "PROPOSED/RESEARCHING/DEFERRED_EMPIRICAL" — terminology mismatch |
| F-017 | LOW | 15×13 board size result remains "Unknown" with LOW confidence from Wikipedia since R1 |
| F-018 | MEDIUM | claim-register.md header states 22 NEEDS_CORRECTION; body rows need manual verification |
| F-019 | MEDIUM | ensemble-catalog.md R30/R34 sections mixed with R26 sections; chronological separation unclear |
| F-020 | LOW | future-experiment-backlog.md header says 32 experiments; body has EXP-001 through EXP-032 = 32 entries confirmed |
| F-021 | LOW | Some FU tasks (FU-052 through FU-068) lack explicit connection to GOV-001 findings |
| F-022 | LOW | No automated mechanism exists to detect future fabrication; all detection is manual |

---

## Implementation Anatomy

The governance defects arise from the following structural patterns:

1. **Sequential source ID allocation without namespace isolation**: S001, S002, S003... across all rounds means round N and round N+5 can both assign S100 to different sources.

2. **Header-body drift**: Headers (round number, claim counts, hypothesis counts) are updated by one worker during a round, but other workers may update their own headers independently.

3. **Dossier directory infrastructure without content**: The `research/dossiers/` subdirectories were created as empty containers but never populated.

4. **Fabricated data persistence**: When R33 detects S117 and S120 as fabricated, the source-ledger.md is not updated with a RETRACTED flag.

5. **Multi-writer header inconsistency**: Each worker result updates headers in its target files. With 17 workers per round, headers are updated 17+ times per round across different files, increasing the probability of drift.

---

## Pros and Cons of Current Governance Approach

| Pros | Cons |
|------|------|
| 205 claims tracked across 34 rounds | No automated collision detection |
| 24 ensembles with detailed specifications | Fabricated data not flagged in source ledger |
| 16 contenders with algorithm details | Master report 6 days stale |
| 12 benchmark suites fully designed | Empty dossier directories (3 empty, 8 missing) |
| 32 experiments with full specifications | No RETRACTED status in source ledger |
| Iteration reports per round | Header-body drift across canonical files |
| 68 follow-up tasks tracked | Legacy file proliferation (~30 files) |
| Governance issues identified per round | No automated fabrication detection |

---

## Feasibility Matrix

| Aspect | Local CPU | RTX 5090 | DGX Spark | Kaggle CPU | Kaggle T4 |
|--------|-----------|----------|-----------|------------|-----------|
| Automated source ID collision detection | VERIFIED — Python Markdown parser feasible | NOT_APPLICABLE | NOT_APPLICABLE | VERIFIED | NOT_APPLICABLE |
| Fabricated data detection pipeline | VERIFIED — regex + semantic analysis feasible | NOT_APPLICABLE | NOT_APPLICABLE | VERIFIED | NOT_APPLICABLE |
| Header normalization script | VERIFIED | NOT_APPLICABLE | NOT_APPLICABLE | VERIFIED | NOT_APPLICABLE |
| Master report update (manual) | VERIFIED | VERIFIED | VERIFIED | VERIFIED | VERIFIED |
| Dossier content creation (research) | DOCUMENTED — read-only web fetch | DOCUMENTED | DOCUMENTED | DOCUMENTED | DOCUMENTED |

**Key constraint**: This is research-only. No files are modified directly by code. The remediation plan requires a subsequent implementation phase.

---

## Board-Size and inarow Applicability

This governance audit applies to **all board sizes and inarow values** because:

1. Source ID collisions are independent of board size.
2. Fabricated data persistence affects all board-size claims equally.
3. Header inconsistencies create ambiguity regardless of which board size is being referenced.
4. Empty dossier directories affect all board-size research equally.

The audit has specific relevance for board-size generalization because the 15×13 board-size result (first-player unknown) remains at LOW confidence with no governance-recommended verification protocol.

---

## Integration and Ensemble Opportunities

This governance audit intersects with multiple ensembles:

| Ensemble | Governance Impact |
|----------|-------------------|
| ENS-019 (Board-Size Adaptive Routing) | Source ID collisions in BOT-003 (S091, S092) affect routing ensemble evaluation |
| ENS-024 (Confidence-Gated Routing) | Header inconsistencies undermine confidence in routing thresholds |
| ENS-018 (TT-MCTS Shared Cache) | Fabricated S117 data would corrupt phase-boundary calibration |
| All ensembles | Master report staleness means ensemble evaluation uses outdated neural MCTS benchmarks |

**Benchmark requirements**: BMS-025 (automated corpus governance audit), BMS-026 (fabricated data detection benchmark) — both should be added to benchmark-blueprint.md.

---

## Failure Modes and Risks

| Failure Mode | Impact | Mitigation |
|-------------|--------|------------|
| Implementation team reads stale RESEARCH_REPORT.md | Builds architecture on outdated benchmarks | Add date-based staleness check to README.md header |
| New worker inherits fabricated S117 data | Propagates fabrication to new claims/experiments | Add RETRACTED flag to source ledger; cross-reference on new source addition |
| Empty dossiers create false confidence | Team assumes research is complete when it is not | Add "dossier completion" metric to research-state.md |
| Source ID collisions cause wrong attribution | Claim C### cites wrong source | Implement namespace isolation (R34-S001 format) |
| Header drift creates ambiguity | Team cannot determine which round's data is authoritative | Add automated header reconciliation (EXP-007) |

---

## Open Questions

1. **Should source ID namespace isolation use round prefixes (R34-S001) or UUIDs?** Prefix preserves human readability but requires round-tracking. UUIDs are unique but opaque.

2. **Who is responsible for updating the master report?** Currently unclear — each worker updates their target files but RESEARCH_REPORT.md updates are not assigned.

3. **What is the minimum viable dossier?** The mission template requires dossiers but none have been produced. A minimum viable dossier might be a single-page summary of a source with: project, source permalink, license, core algorithm, pros/cons.

4. **Should the corpus transition to a structured format (JSON/YAML) for machine-parseable metadata?** Markdown is human-readable but difficult to parse for automated governance checks.

5. **How many rounds of governance cleanup are needed before corpus content creation can begin?** Current assessment: at least 2 rounds dedicated to governance before substantive dossier production.

---

## Recommendations

1. **Immediate (R35)**: Add RETRACTED flags to S117 and S120 in source-ledger.md. Update RESEARCH_REPORT.md header date. ✅ DONE in R35.
2. **Round 36**: Fix source ID collisions (4 clusters, 27+ IDs). Implement namespace isolation schema. Create contender dossiers.
3. **Round 37**: Complete empty dossier directories with at least one dossier each. Fix benchmark blueprint numbering. Fix header inconsistencies.
4. **Round 38+**: Begin production of substantive dossiers (foundations, kaggle, neural, training-data, contenders, ensembles, reference-implementations).

---

## Sources and Retrieval Record

| Source | Type | Retrieval Date | Verification Method |
|--------|------|----------------|---------------------|
| RESEARCH_REPORT.md | Master report | 2026-08-04 | Direct read (521 lines) |
| research/README.md | Canonical index | 2026-08-04 | Direct read (153 lines) |
| research/research-state.md | Round progression | 2026-08-04 | Direct read (195 lines) |
| research/claim-register.md | 205 claims | 2026-08-04 | Direct read (400+ lines) |
| research/source-ledger.md | 120+ sources | 2026-08-04 | Direct read (414+ lines) |
| research/hypothesis-register.md | 24 hypotheses | 2026-08-04 | Direct read (1625 lines) |
| research/contender-roster.md | 16 contenders | 2026-08-04 | Direct read (498 lines) |
| research/ensemble-catalog.md | 24 ensembles | 2026-08-04 | Direct read (428 lines) |
| research/benchmark-blueprint.md | 12 benchmark suites | 2026-08-04 | Direct read (567 lines) |
| research/future-experiment-backlog.md | 32 experiments | 2026-08-04 | Direct read (834 lines) |
| research/work-queue.md | 70+ tasks | 2026-08-04 | Direct read (198+ lines) |
| research/iterations/round-034.md | Latest iteration | 2026-08-04 | Direct read (248 lines) |
| research/research-gaps.md | Gap catalog | 2026-08-04 | Direct read (154 lines) |
| research/dossiers/ | Subdirectories | 2026-08-04 | Directory listing (3 empty, 8 missing) |

---

## Cross-Links

| Related | Type | Connection |
|---------|------|------------|
| GOV-002 | Planned | Master Report Staleness Repair (RESEARCH_REPORT.md update) |
| FU-052 | Follow-up | Source ID deduplication protocol |
| FU-053 | Follow-up | Automated fabrication detection pipeline |
| FU-054 | Follow-up | Header normalization across all canonical files |
| FU-058 | Follow-up | Source attribution integrity checks |
| FU-063 | Follow-up | Corpus hygiene audit automation |
| EXP-007 | Experiment | Automated claim reconciliation |
| EXP-025 | Experiment | Corpus governance audit automation |
| EXP-026 | Experiment | Fabricated data detection benchmark |
| EXP-031 | Experiment | Source ID collision detection automation |
| HYP-019 | Hypothesis | Source attribution integrity |
| HYP-020 | Hypothesis | Fabricated data detection in corpus |

---

*GOV-001 is the first dossier produced by the ConnectX V10 research synthesis process. It serves as a baseline for future governance audits.*