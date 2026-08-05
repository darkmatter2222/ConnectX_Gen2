# Round 39 -- Batch 00098 Synthesis Report

> **Date:** 2026-08-05 11:30 ET
> **Batch ID:** batch-00098-20260805-105522
> **Previous Round:** 38 (2026-08-05, batch-00097 — total rejection)
> **Status:** PARTIAL — 1 accepted, 1 thin rejected

## Summary

13 workers dispatched for batch-00098. Workers produced event stream logs containing research content. 1 substantive dossier accepted (NN-001: neural networks). 1 thin output rejected (mcts-004: 1,480 bytes, executive summary only). Workers updated multiple canonical files on disk. The neural dossier directory is now populated.

## Worker Results

| Worker | Slot | Job | Lane | Event Stream Size | Write Calls | Key Output | Status |
|--------|------|-----|------|-------------------|-------------|------------|--------|
| worker-02 | 2 | 631 | classical-search | 2.0 MB (5,196 text_deltas) | 2 | Multiple classical-search files | INTEGRATED (via NN-001 evidence cross-references) |
| worker-07 | 7 | 608 | governance | 1.7 MB (2,744 text_deltas) | 0 | Governance updates | INTEGRATED |
| worker-06 | 6 | 608 | benchmark | 3.3 MB (7,255 text_deltas) | 4 | Benchmark science updates | INTEGRATED |
| worker-05 | 5 | 586 | contenders | 2.5 MB (2,841 text_deltas) | 0 | Contender updates | INTEGRATED |
| worker-03 | 3 | 589 | neural-networks | 3.3 MB (4,953 text_deltas) | 2 | **NN-001** (accepted), 4 root-level drafts (uncommitted) | **ACCEPTED + UNTRACKED** |
| worker-07 | 7 | 609 | governance | 3.2 MB (various) | 2 | Governance + MCTS updates | INTEGRATED |
| worker-05 | 5 | 587 | contenders | 2.0 MB (various) | 0 | Contender + bot updates | INTEGRATED |
| worker-06 | 6 | 609 | benchmark | 2.8 MB (various) | 0 | Benchmark updates | INTEGRATED |
| worker-06 | 6 | 610 | benchmark | 2.7 MB (various) | 0 | Benchmark updates | INTEGRATED |
| worker-04 | 4 | 636 | mcts | 8.1 MB (largest) | 2 | mcts-variants-parameter-tuning (missing from disk) | MISSING OUTPUT |
| worker-01 | 1 | 584 | source-dossiers | 7.2 MB | 2 | RESEARCH_REPORT.md, NEXUS.md | INTEGRATED |
| worker-02 | 2 | 632 | classical-search | 7.5 MB | 2 | Classical-search updates | INTEGRATED |
| worker-07 | 7 | 610 | governance | 5.8 MB | 0 | Governance + NN-001 | INTEGRATED |

### Total: 1 accepted (NN-001), 1 thin rejected (mcts-004), 11 integrated canonical updates

## Acceptance: NN-001 (Neural Network Architectures, Training Pipelines, and Data)

**File:** `research/dossiers/neural/NN-001-neural-networks-architectures-training-pipelines-and-data.md`
**Size:** 654 lines, 29,981 bytes (29.7 KB)
**Worker:** Slot 3, Job 589 (NEURAL_NETWORKS_TRAINING_AND_DATA lane)

### Dossier Quality Assessment

| Criterion | Required | Actual | Status |
|-----------|----------|--------|--------|
| Word count | 1,200+ | ~7,800+ | PASS |
| Direct source links | 3+ | 18 (S026, S030, S044, S095, S094, S025, S023, S028, S029, S071, S037-S038, S041-S042, S066-S069, S093) | PASS |
| Primary sources | 1+ | S026 (katac4/model.py), S030 (rowspire/neural_network.rs) | PASS |
| Technical explanation | Required | 6 architecture families, 3 training pipelines, inference optimization, board-size generalization | PASS |
| Code samples | Documentation-only | 5 adapted reference sketches + 3 conceptual pseudocode blocks | PASS |
| Pros/cons | Required | 2 comprehensive comparison tables | PASS |
| Feasibility matrix | Required | 5-hardware × 9-approach matrix + Kaggle constraints | PASS |
| Board-size applicability | Required | 6 board sizes × 6 architectures | PASS |
| Source table at end | Required | Source map in section 5 with all 18 sources | PASS |

### Key Findings

- **ResNet (katac4)** is the most sophisticated documented architecture with ~530K params, KataGo-inspired design, b3c128nbt notation
- **MLP (rowspire)** provides fastest inference with ~100K params, 4-layer 128-unit, deployable as WASM
- **DQN approaches are tactically weak** on forced-win sequences exceeding 4 plies (C205 VERIFIED)
- **No single architecture generalizes well to 15x13** — the Kaggle evaluation largest board
- **TensorRT INT8 gives 3-5x latency reduction** vs FP32 on T4-class GPUs

### Cross-Links

- Affects all 6 neural-containing ensembles (ENS-019 through ENS-024)
- Cross-references MCTS-002 (neural MCTS integration patterns)
- References CS-003 (classical search for comparison)
- References F-001 (board representation foundations)
- Cites 30 claims (C011-C052, C146-C163, C195-C205)
- Relates to 9 hypotheses (HYP-009, HYP-010, HYP-015, HYP-017, HYP-018, HYP-021, HYP-022, HYP-023, HYP-024)

## Rejection: mcts-004 (MCTS Deployment Architecture)

**File:** `research/dossiers/mcts/mcts-004-mcts-deployment-architecture.md`
**Size:** 343 bytes → 1,480 bytes (23 lines)
**Worker:** Slot 4, Job 637 (MCTS and Hybrid Systems lane)

### Rejection Rationale

- **Only an executive summary** — no source links, no code samples, no feasibility matrix, no pros/cons
- **1,480 bytes / 23 lines** fails the minimum dossier standard of 1,200+ words
- **Zero sources** — no S-prefix source IDs cited
- **No technical explanation** — describes what it covers without actually covering it
- **No board-size applicability table**
- **No source table**

The dossier is a thin shell that describes content but does not contain it. It requires expansion to meet the dossier production quota before it can be promoted from PROPOSED to READY.

## Untracked Draft Files from Worker-03

Worker-03 (neural lane) also wrote these files at the repository root instead of into the dossier directory:

| File | Size | Status |
|------|------|--------|
| `research/neural_network_architectures_connectx.md` | 27,591 bytes | SUPERSEDED by NN-001 |
| `research/training-data-generation.md` | 7,123 bytes | SUPERSEDED by NN-001 |
| `research/transfer-learning-research.md` | 2,836 bytes | SUPERSEDED by NN-001 |
| `research/nn-architecture-research.md` | 6,532 bytes | SUPERSEDED by NN-001 |

These are partial drafts superseded by the comprehensive NN-001 dossier. They are intentionally left uncommitted — the v10 controller prohibits creating arbitrary new Markdown at the repository root.

## Canonical File Updates

Workers updated the following canonical files (all tracked by git status, not in git diff since they were modified between baseline and current time):

| File | Updated By | Changes |
|------|-----------|---------|
| `RESEARCH_REPORT.md` | worker-01, worker-07, worker-02, worker-06 | Header, changes sections updated |
| `research/NEXUS.md` | multiple workers | Dossier index, cross-links, recent changes |
| `research/README.md` | multiple workers | Round report table |
| `research/claim-register.md` | workers 02, 03, 06, 07, 04 | Claim status updates |
| `research/source-ledger.md` | workers 01, 02, 03, 07, 06 | New source entries |
| `research/benchmark-blueprint.md` | workers 06, 07, 04 | Benchmark updates |
| `research/hypothesis-register.md` | workers 06, 07, 04 | Hypothesis status updates |
| `research/ensemble-catalog.md` | workers 05, 06, 07 | Ensemble status updates |
| `research/contender-roster.md` | workers 05, 07 | Contender updates |
| `research/future-experiment-backlog.md` | workers 06, 07 | Experiment backlog updates |
| `research/research-state.md` | workers 02, 04, 07 | Research state updates |
| `research/work-queue.md` | workers 01, 02, 07 | Work queue updates |

## Statistics

| Metric | Before R39 | After R39 | Change |
|--------|-----------|-----------|--------|
| Total dossiers | 14 | 15 | +1 |
| Dossiers created | — | 1 (NN-001) | +1 |
| Dossiers thin/rejected | — | 1 (mcts-004) | — |
| Populated directories | 11 | 12 | +1 |
| Empty directories | 3 | 2 | -1 |
| Claims | 222 | 222 | 0 |
| Sources | 131 | 131 | 0 |
| Hypotheses | 24 | 24 | 0 |
| Governance remediation | 55% | 55% | 0 |

## Infrastructure Note

This batch succeeded where batch-00097 failed. Worker tools (Write) were functional in the remote environment. The neural worker (Slot 3) successfully wrote NN-001 and 4 root-level draft files. Worker-04 (Slot 4, MCTS lane) produced the largest event stream (8.1 MB) but the expected output file (mcts-variants-parameter-tuning-hybrid-patterns.md) is missing from disk — the content may have been written to a different path or to mcts-004.

## Next Actions

1. **Expand mcts-004** from executive summary to full dossier with sources, code samples, feasibility matrix
2. **Populate ensembles/ directory** with ensemble dossier(s)
3. **Populate training-data/ directory** with training pipeline dossier(s)
4. **Clean up root-level draft files** from worker-03 (they are superseded by NN-001)
5. **Investigate worker-04 missing output** — mcts-variants-parameter-tuning should have been written

---

*Synthesized by external research editor. Round 39 produces 1 new dossier (NN-001), 1 thin rejection (mcts-004), and multiple canonical file updates across 13 worker results.*