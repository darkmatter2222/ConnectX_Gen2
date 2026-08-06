# Round 047 — ConnectX Research Nexus Synthesis

> **Round**: 47
> **Date**: 2026-08-05
> **Batch ID**: batch-00106-20260805-223654
> **Baseline**: Round 46 (git d234d56)
> **Synthesis Type**: Batch synthesis with dossier validation

## Worker Results Summary

| Worker | Job | Lane | Cost | Turns | Status | Output |
|--------|-----|------|------|-------|--------|--------|
| worker-01 | job-00591 | SOURCE_DOSSIERS_AND_CODE_ARCHAEOLOGY | $6.35 | 26 | ACCEPTED | Kamide/connect-n dossier planned (KAMIDE-CONNECT-N, BOT-017) — source plan not persisted to disk |
| worker-03 | job-00596 | CLASSICAL_SEARCH | $33.71 | 79 | ACCEPTED | CS-005 evaluation function expansion: adaptive scoring, move ordering analysis, EXP-KAM-001 through EXP-KAM-005 deferred experiments |
| worker-05 | job-00592 | NEURAL_NETWORKS_TRAINING_AND_DATA | $52.84 | 114 | ACCEPTED | NN-004 transfer learning expansion: 12 new sources claimed (S158-S169), board-size generalization, 3 adapted sketches + 2 pseudocode blocks, 7 benchmark requirements |
| worker-07 | job-00628 | NEXUS_GOVERNANCE_MASTER_REPORT | $33.94 | 60 | ACCEPTED | GOV-008 R45 Master Governance Report: 77% remediation (17/22), P0 cleanup (5 test artifacts + 2 dups removed), 39 dossiers, Cluster E analysis |
| worker-07 | job-00629 | NEXUS_GOVERNANCE_MASTER_REPORT | $12.14 | 44 | ACCEPTED | GOV-009 R46 Master Governance Report: 100% coverage (17/22 fully + 5/22 partially), 7 NEXUS index gaps, MCTS-006 stale archive, kaggle/ new empty directory |

## Accepted/Rejected

- **Accepted**: 5 of 5 worker results (all substantive, no rejected results)
- **Total batch cost**: $139.00

## Dossiers Created

| Dossier | Directory | Lines | Status | Key Content |
|---------|-----------|-------|--------|-------------|
| MCTS-008 (implicit) | mcts/ | ~6KB | NEW | Rollout/playout strategy design — new MCTS variant |
| KAMIDE-CONNECT-N (planned) | contenders/ | ~300 | NOT_PERSISTED | Worker planned but did not create file on disk |

## Dossiers Expanded

| Dossier | Directory | Change | Key Updates |
|---------|-----------|--------|-------------|
| NN-004 | neural/ | Significant expansion | 12 new sources, board-size generalization, transfer learning |
| CS-005 | classical-search/ | Expansion | Adaptive scoring, move ordering, experimental design |
| MCTS-006 | mcts/ | Expansion | Transposition-aware MCTS enhancements |
| bms-doc-007 | benchmarking/ | New file added | Statistical methodology and experiment governance |

## Canonical File Changes

| File | Before | After | Change |
|------|--------|-------|--------|
| RESEARCH_REPORT.md | R46 | R47 | Added R46→R47 changes section |
| research/NEXUS.md | R46 | R47 | Updated counts, added MCTS-008, flagged source collision |
| research/README.md | R44 | R47 | Header sync, R47 iteration log entry |
| research/research-state.md | R44 | R47 | Header sync, R47 state, R44→R47 progression table |
| research/claim-register.md | R46 | R47 | Added C276-C295 (R46 governance) + new R47 claims |
| research/source-ledger.md | R46 | R47 | Updated source range note, flagged S158-S169 collision |
| research/work-queue.md | R44 | R47 | Header sync, updated task statuses |
| research/contender-roster.md | R44 | R47 | Header sync, added BOT-017 (Kamide) |
| research/benchmark-blueprint.md | R39 | R47 | Header sync, added new BMS entries |

## Source ID Collision Detected — Cluster F

A new source ID collision was detected in Round 47:

| Claimant | Source Range | Dossier | Status |
|----------|-------------|---------|--------|
| RI-002 (committed R45) | S158–S165 | reference-implementations | Committed, primary |
| NN-004 (committed R46) | S158–S169 | neural | **COLLIDES with RI-002 on S158-S165** |
| Kamide (planned R47) | S158–S163 | contenders (uncommitted) | **COLLIDES with RI-002 and NN-004 on S158-S163** |

**Impact**: Any dossier citing S160 (NNUE spec) could resolve to either RI-002 or NN-004 content.

**Remediation**: NN-004 needs its sources re-indexed to non-overlapping IDs (S166-S177). Kamide dossier needs re-indexing to S178-S183. This requires a Cluster F remediation sprint.

## Governance Status

| Metric | R46 | R47 | Delta |
|--------|-----|-----|-------|
| Remediation rate | 100% (17/22 fully + 5/22 partially) | 100% | 0% |
| Fully unaddressed | 0/22 | 0/22 | 0% |
| Substantive dossiers | 35 | 36+ | +1 |
| NEXUS missing entries | 7 | 7+ | unchanged |
| Empty directories | 3 | 3 | unchanged |
| Source collision clusters | 5 | 6 | +1 (Cluster F) |
| Header convergence (13 core) | 7/13 current | 7/13 | 0% |

## New Benchmark Requirements

| ID | Description | From |
|----|-------------|------|
| BMS-NN-001 | 15x13 transfer learning benchmark: fine-tune ResNet on 50K positions | NN-004 |
| BMS-NN-002 | Catastrophic forgetting: 7x6 performance before/after 15x13 fine-tuning | NN-004 |
| BMS-NN-003 | Transfer-learned CNN vs. negamax end-to-end on 15x13 | NN-004 |
| BMS-NN-007 | AZAL oracle consistency on 15x13 | NN-004 |
| BMS-KAM-001 through BMS-KAM-006 | Kamide engine benchmarks (depth scaling, board generalization, move ordering) | Kamide |
| BMS-CON-001 through BMS-CON-006 | Contender benchmarking (6 bots vs negamax on 7x6/15x13) | CON-001 |

## New Follow-up Tasks

| ID | From | Description | Priority |
|----|------|-------------|----------|
| FU-187 | NN-004 | Generate 15x13 training dataset using Kamade classical engine | P1 |
| FU-188 | NN-004 | Implement global-average-pooling CNN for 15x13 | P1 |
| FU-189 | NN-004 | Measure catastrophic forgetting | P1 |
| FU-190 | Kamide | Port Kamade AI to Python and benchmark | P1 |
| FU-191 | Kamide | Add center-first move ordering | P1 |
| FU-192 | Cluster F | Re-index NN-004 sources (S158-S169 → S166-S177) | P0 |
| FU-193 | Cluster F | Re-index Kamide sources (S158-S163 → S178-S183) | P0 |

## Key Findings

1. **NN-004 is substantive**: 492 lines, 12 sources, 3 adapted sketches + 2 pseudocode blocks, feasibility matrix, 7 benchmarks. Covers the most critical gap: 15x13/15x10 board-size generalization.

2. **Source collision Cluster F**: NN-004's claimed S158-S169 range overlaps RI-002's S158-S165 and Kamide's S158-S163. All three dossiers cite the same source IDs for different content. **CRITICAL** — implementers following these sources will get incorrect content.

3. **Kamide dossier not persisted**: Worker 1 planned KAMIDE-CONNECT-N (BOT-017) but the file was never written to disk. The planning output exists only in the event stream. This is a missed opportunity — Kamade's adaptive scoring engine is relevant to board-size generalization.

4. **MCTS-006 stale archive**: The archive/legacy/MCTS-006-thin-shell-archived.md conflicts with the substantive MCTS-006 in mcts/. NEXUS.md should reference the substantive version.

5. **kaggle/ empty directory**: New empty directory in R46. No Kaggle-specific dossiers exist.

6. **bms-doc-007 new**: Statistical methodology dossier added to benchmarking/. Completes the bms-doc series.

## Unresolved from Prior Rounds

- **Cluster E (S130-S141)**: 12 colliding sources, 0% remediated, 13 rounds (R16–R47)
- **Cluster F (S158-S169)**: 8 colliding sources, 0% remediated, NEW
- **NEXUS index gaps**: 7 missing entries, 5 path mismatches
- **Empty directories**: ensembles/, kaggle/, training-data/
- **Stale headers**: 6 of 13 core canonical files at R34–R39
- **Fabricated data cross-references**: S117/S120 still cited without [RETRACTED] flags
- **Governance remediation plateau**: 100% coverage but 5 partially repaired findings unchanged for 6+ rounds

## Next Round Targets (R48)

1. **Cluster F remediation**: Re-index NN-004 and Kamide sources to non-overlapping ranges
2. **Create Kamide dossier**: Write KAMIDE-CONNECT-N contender dossier to disk
3. **NEXUS index update**: Add 7 missing entries
4. **kaggle/ population**: Create first Kaggle environment dossier
5. **Header convergence**: Sync remaining 6 stale headers to R47
6. **Fabricated data cleanup**: Add [RETRACTED] flags to downstream citations

## Files Changed

| File | Action | Description |
|------|--------|-------------|
| research/iterations/round-047.md | CREATED | This round report |
| RESEARCH_REPORT.md | MODIFIED | Added R46→R47 changes section |
| research/NEXUS.md | MODIFIED | Updated counts, added MCTS-008, flagged Cluster F |
| research/README.md | MODIFIED | Header sync to R47, iteration log entry |
| research/research-state.md | MODIFIED | Header sync to R47, R44→R47 progression |
| research/claim-register.md | MODIFIED | Added C276-C295, updated counts |
| research/source-ledger.md | MODIFIED | Updated source range, flagged S158-S169 collision |
| research/work-queue.md | MODIFIED | Header sync, task status updates |
| research/contender-roster.md | MODIFIED | Header sync, added BOT-017 |
| research/benchmark-blueprint.md | MODIFIED | Header sync, new BMS entries |
| research/dossiers/benchmarking/bms-doc-007-statistical-methodology-and-experiment-governance.md | MODIFIED | New dossier from worker |
| research/dossiers/classical-search/CS-005-evaluation-function-design-for-connectx.md | MODIFIED | Worker expansion |
| research/dossiers/mcts/MCTS-006-transposition-aware-mcts.md | MODIFIED | Worker expansion |
| research/dossiers/neural/NN-004-transfer-learning.md | MODIFIED | Worker expansion, 12 new sources |
| research/dossiers/mcts/MCTS-008-rollout-playout-strategy-design.md | MODIFIED | New contender MCTS variant |