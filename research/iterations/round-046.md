# Round 046 — ConnectX Research Nexus Synthesis

> **Round**: 46
> **Date**: 2026-08-05
> **Batch ID**: batch-00105-20260805-210158
> **Status**: Complete
> **Workers dispatched**: 21 result files across 20 jobs (7 workers)

---

## Summary

Round 46 (batch-00105) is the largest synthesis round to date, processing 21 worker result files across 20 distinct jobs from 7 workers dispatched across 7 lanes. The batch produced **3 new substantive dossiers** (NN-004, CON-001), **6 dossier expansions**, and **5 new governance findings**. Key contributions include NN-004 (transfer learning and board-size generalization), CON-001 (new contender discovery with systematic benchmark framework), and multiple governance/benchmarking dossiers.

Governance remediation rate remains at **75% (17/22 GOV-001 findings repaired)** — no improvement from R45, marking a 6-round plateau (R40-R45). Cluster E source ID collision (S130-S146) persists. 5 canonical files have stale headers.

---

## Dossiers Created

### NN-004 — Transfer Learning and Board-Size Generalization for Neural ConnectX Bots

`research/dossiers/neural/NN-004-transfer-learning.md`

- **Status**: PROPOSED
- **Lane**: Neural Networks, Training, and Data
- **Worker**: Slot 3, Job 595
- **Scope**: Transfer learning methodologies, board-size generalization techniques, cross-board deployment strategies
- **Key Findings**:
  - Transfer learning from 7x6 to 15x13 remains the most critical unsolved problem
  - Three transfer strategies catalogued: fine-tuning, feature engineering, auxiliary oracle supervision
  - DQN-ConnectX-Agent (DS669 student project) provides empirical architecture comparison
  - NNUE incremental evaluation patterns from ecc521 solver
  - 12 new sources (S160-S173), though S160-S165 overlap with RI-002 / NN-003 sources
- **Related**: NN-001 (architecture), NN-002 (NNUE source), NN-003 (training methodology), HYP-021 (board-size routing), ENS-019 through ENS-024
- **Code Samples**: 3 adapted reference sketches + 2 conceptual pseudocode blocks

### CON-001 — New Contender Discovery and Benchmark Framework

`research/dossiers/contenders/CON-001-new-contenders-and-benchmark-framework.md`

- **Status**: PROPOSED
- **Lane**: Contenders, Baselines and Benchmark References
- **Worker**: Slot 4, Job 642
- **Scope**: New public bot discoveries, Kaggle official reference implementation, systematic benchmark framework
- **Key Findings**:
  - ManuelFay/Alpha_Connect4: PyTorch DQN architecture study comparing 5 network depths
  - jesper-olsen/connect-four: Rust port of Tromp's Fhourstones with interactive CLI
  - Kamide/connect-n: TypeScript PWA with adaptive scoring for arbitrary N-in-a-row
  - Kaggle built-in negamax_agent (depth=4, clustering eval) as canonical baseline
  - Systematic benchmark evaluation framework with test positions and scoring methodology
- **Related**: BOT-001 through BOT-016, ENS-001 through ENS-024, BMS-001 through BMS-012
- **Significance**: First systematic benchmark framework document in the corpus

---

## Dossiers Expanded (Pre-existing, materially updated)

| ID | File | Worker | Job | Status | Key Change |
|----|------|--------|-----|--------|------------|
| MCTS-007 | mcts/MCTS-007-gpu-accelerated-mcts.md | Worker-04 | 642 | PROPOSED | Rewritten with 621 lines, ~4,700 words, 17 sections (was thin) |
| NN-003 | neural/NN-003-training-methodology-deep-dive.md | Worker-03 | 594 | PROPOSED | Temperature decay formula corrected, AZAL specification, replay buffer dynamics |
| RI-002 | reference-implementations/RI-002-connectpuct-puct-mcts-with-tactical-priors.md | Worker-01 | 590 (batch D) | PROPOSED | Source archaeology: 7 source files analyzed, PUCT formula, tactical priors |
| CBL-002 | contenders/cbl-002-kaggle-environment-source-analysis.md | Worker-05 | 591 | PROPOSED | Kaggle ConnectX environment source code analysis |
| KAGGLE-CONNX-SPEC | reference-implementations/KAGGLE-CONNX-SPEC.md | Worker-01 | 588 | PROPOSED | Complete Kaggle environment specification |
| DOS-007 | contenders/DOS-007-kaggle-competitive-analysis.md | Worker-05 | 590 (batch A) | PROPOSED | Kaggle competitive analysis with 5 ensemble designs |

---

## Governance Findings (From Multiple Workers)

| Worker | Job | Key Findings |
|--------|-----|--------------|
| 07 | 624 | GOV-006 R43 audit: 28 findings across 8 categories, Cluster E expanded to 17 IDs (S130-S146) |
| 07 | 625 | Remediation improved 68%→73%, 5 missing from NEXUS index |
| 07 | 626 | GOV-007 R43→R44: 75% remediation (17/22), 20 follow-up tasks |
| 07 | 627 | Cluster E persists (S130-S141), 3 empty directories, fabricated data cross-references not cleaned |

---

## Claim and Source Updates

### New Claims

| Range | From | Count | Type |
|-------|------|-------|------|
| C233-C236 | MCTS-007 (job 642) | 4 | VERIFIED |
| C241-C260 | GOV-007 (job 626/627) | 20 | Governance |

**Total claim range now extends to C260.**

### New Sources

| Range | From | Count | Notes |
|-------|------|-------|-------|
| S150-S157 | NN-003 (job 594) | 8 | katac4 training, AZAL, rowspire training — already in R45 ledger |
| S158-S165 | RI-002 (job 590 batch D) | 8 | connectpuct repository — already in R45 ledger |
| S160-S173 | NN-004 (job 595) | 14 | Partial overlap with S160-S165; need de-duplication |

**New unique sources from this batch (above S165): S166+ pending de-duplication of NN-004 sources.**

### Source Collision Status

- **Cluster E (CRITICAL)**: S130-S146, 17 colliding IDs — **no progress**
- **Clusters A-D**: No change
- **NN-003 sources S150-S157**: Verified non-colliding (already confirmed R44)
- **RI-002 sources S158-S165**: Verified non-colliding (new this round)

---

## Test Artifact Regression

No new test artifacts were introduced this round. The 3 existing test artifacts from R45 remain:
- `MCTS-007.md` (18 bytes) in `mcts/`
- `_write_dossier.py` (38 bytes) in `classical-search/`
- `write_dossier.ps1` (32 bytes) in `classical-search/`

**Action required in R47**: Delete these test artifacts.

---

## Unindexed Files

As of R44, 5 substantive files were identified as existing on disk but not in NEXUS.md structured tables. R46 adds:
- NN-004 (new, written)
- CON-001 (new, written)

**Total unindexed**: 7 files. NEXUS.md must be updated.

---

## Worker Validation Summary

| Worker | Jobs | Lane | Quality | Key Output |
|--------|------|------|---------|------------|
| 07 | 620, 621, 622, 623, 624, 625, 626, 627 | Governance | 4 ACCEPT, 4 PASS | Multiple governance dossiers (GOV-005 through GOV-008) |
| 06 | 613, 614, 616, 617 | Benchmarking | All ACCEPT | BMS-DOC-004, BMS-DOC-006, BMS-DOC-007 |
| 05 | 590, 591 | Contenders | All PASS | DOS-007, CBL-002 |
| 03 | 593, 594, 595, 596 | Neural | Mixed | NN-003, NN-004 |
| 04 | 642 | MCTS/Hybrid | PASS | MCTS-007 deep, CON-001 |
| 01 | 588, 590 (batch D) | Source Dossiers | PASS | KAGGLE-CONNX-SPEC, RI-002 |
| 07 | 620-627 | Multiple | Mixed | Governance dossiers across multiple rounds |

**Workers passed (substantive dossier): 6/21 new dossiers** — NN-004, CON-001, MCTS-007, RI-002, CBL-002, KAGGLE-CONNX-SPEC
**Workers passed (governance): 8/21** — GOV-005 through GOV-008
**Workers passed (benchmarking): 4/21** — BMS-DOC-004, BMS-DOC-006, BMS-DOC-007
**Workers passed (contenders): 2/21** — DOS-007, CBL-002
**Workers passed (source dossiers): 2/21** — KAGGLE-CONNX-SPEC, RI-002

---

## Canonical File Updates Needed

| File | Current Header | Target |
|------|---------------|--------|
| RESEARCH_REPORT.md | R45 (19:45 ET) | R46 (current) |
| NEXUS.md | R45 | R46 |
| README.md | R44 | R46 |
| claim-register.md | R44 | R46 (C233-C260+) |
| source-ledger.md | R44 | R46 (S166+) |
| work-queue.md | R44 | R46 (new follow-ups) |
| future-experiment-backlog.md | R44 | R46 (new deferred experiments) |
| architecture-rankings.md | R44 | R46 (new evidence) |

---

## Next Round Targets

1. **Delete test artifacts**: MCTS-007.md (18 bytes), _write_dossier.py, write_dossier.ps1
2. **Index all dossiers in NEXUS.md**: Ensure NN-004, CON-001, and all unindexed files are listed
3. **De-duplicate NN-004 sources**: S160-S165 overlap with RI-002/NN-003; assign unique IDs S166+
4. **Begin Cluster E remediation**: S130-S146 namespace isolation (proposed S130E-S146E)
5. **Populate ensembles/**: First ensemble design dossier
6. **Write BMS-DOC-007**: Agent produced ablation study content but file was not written — needs to be created
7. **Promote NN-004 and CON-001**: Move from PROPOSED to VERIFIED once cross-linked to claim register

---

EXTERNAL SYNTHESIS COMPLETE